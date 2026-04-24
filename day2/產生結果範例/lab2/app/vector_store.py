"""Milvus Lite-backed vector store service."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from pymilvus import DataType, MilvusClient
from sentence_transformers import SentenceTransformer

TEXT_EXTENSIONS = {".txt", ".md", ".markdown", ".rst", ".py", ".json", ".csv", ".log"}
PDF_EXTENSIONS = {".pdf"}
SUPPORTED_EXTENSIONS = TEXT_EXTENSIONS | PDF_EXTENSIONS


def _read_pdf(path: Path) -> str:
    from pypdf import PdfReader

    reader = PdfReader(str(path))
    parts: list[str] = []
    for page in reader.pages:
        try:
            parts.append(page.extract_text() or "")
        except Exception:
            continue
    return "\n".join(parts)


def _read_file(path: Path) -> str:
    if path.suffix.lower() in PDF_EXTENSIONS:
        return _read_pdf(path)
    return path.read_text(encoding="utf-8", errors="ignore")


def _simple_chunk(text: str, size: int, overlap: int) -> list[str]:
    if size <= 0:
        return [text]
    chunks: list[str] = []
    start = 0
    n = len(text)
    step = max(1, size - overlap)
    while start < n:
        chunks.append(text[start : start + size])
        start += step
    return [c for c in chunks if c.strip()]


class VectorStoreService:
    def __init__(self, db_path: str) -> None:
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.db_path = db_path
        self.client = MilvusClient(uri=db_path)
        self._models: dict[str, SentenceTransformer] = {}

    def _get_model(self, name: str) -> SentenceTransformer:
        if name not in self._models:
            self._models[name] = SentenceTransformer(name)
        return self._models[name]

    def _embed(self, model_name: str, texts: list[str]) -> list[list[float]]:
        model = self._get_model(model_name)
        vectors = model.encode(texts, normalize_embeddings=True).tolist()
        return vectors

    def _dim(self, model_name: str) -> int:
        return int(self._get_model(model_name).get_sentence_embedding_dimension())

    def list_collections(self) -> list[str]:
        return list(self.client.list_collections())

    def drop_collection(self, name: str) -> None:
        if self.client.has_collection(name):
            self.client.drop_collection(name)

    def _ensure_collection(self, name: str, dim: int, recreate: bool) -> None:
        exists = self.client.has_collection(name)
        if exists and recreate:
            self.client.drop_collection(name)
            exists = False
        if exists:
            return
        schema = self.client.create_schema(auto_id=True, enable_dynamic_field=True)
        schema.add_field("id", DataType.INT64, is_primary=True)
        schema.add_field("vector", DataType.FLOAT_VECTOR, dim=dim)
        schema.add_field("text", DataType.VARCHAR, max_length=65535)
        schema.add_field("source", DataType.VARCHAR, max_length=1024)
        index_params = self.client.prepare_index_params()
        index_params.add_index(
            field_name="vector",
            index_type="AUTOINDEX",
            metric_type="COSINE",
        )
        self.client.create_collection(
            collection_name=name,
            schema=schema,
            index_params=index_params,
        )

    def index_folder(
        self,
        folder: Path,
        collection: str,
        embedding_model: str,
        chunk_size: int,
        chunk_overlap: int,
        recreate: bool,
    ) -> int:
        dim = self._dim(embedding_model)
        self._ensure_collection(collection, dim=dim, recreate=recreate)

        files = [p for p in folder.rglob("*") if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS]
        if not files:
            return 0

        rows: list[dict[str, Any]] = []
        for path in files:
            try:
                text = _read_file(path)
            except Exception:
                continue
            if not text.strip():
                continue
            for chunk in _simple_chunk(text, chunk_size, chunk_overlap):
                rows.append({"text": chunk, "source": str(path)})
        if not rows:
            return 0

        vectors = self._embed(embedding_model, [r["text"] for r in rows])
        for row, vec in zip(rows, vectors):
            row["vector"] = vec

        self.client.insert(collection_name=collection, data=rows)
        return len(rows)

    def query(
        self,
        text: str,
        collection: str,
        embedding_model: str,
        top_k: int,
    ) -> list[dict[str, Any]]:
        if not self.client.has_collection(collection):
            raise ValueError(f"Collection not found: {collection}")
        vector = self._embed(embedding_model, [text])[0]
        res = self.client.search(
            collection_name=collection,
            data=[vector],
            limit=top_k,
            output_fields=["text", "source"],
            search_params={"metric_type": "COSINE"},
        )
        hits = res[0] if res else []
        return [
            {
                "score": float(h.get("distance", 0.0)),
                "text": h.get("entity", {}).get("text", ""),
                "source": h.get("entity", {}).get("source", ""),
            }
            for h in hits
        ]
