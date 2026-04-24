from __future__ import annotations

import csv
import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from threading import Lock
from typing import Iterable

from pymilvus import MilvusClient, DataType
from sentence_transformers import SentenceTransformer

SUPPORTED_EXTS = {".txt", ".md", ".pdf", ".py", ".json", ".csv", ".log"}


@dataclass
class StoreConfig:
    db_path: str = "./milvus_data/vector.db"
    collection: str = "documents"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    chunk_size: int = 500
    chunk_overlap: int = 50


@dataclass
class IndexResult:
    indexed_files: list[str] = field(default_factory=list)
    skipped_files: list[str] = field(default_factory=list)
    chunks: int = 0


def _read_pdf(path: Path) -> str:
    from pypdf import PdfReader

    reader = PdfReader(str(path))
    return "\n".join((page.extract_text() or "") for page in reader.pages)


def _read_json(path: Path) -> str:
    data = json.loads(path.read_text(encoding="utf-8", errors="ignore"))
    return json.dumps(data, ensure_ascii=False, indent=2)


def _read_csv(path: Path) -> str:
    with path.open("r", encoding="utf-8", errors="ignore", newline="") as f:
        reader = csv.reader(f)
        return "\n".join(", ".join(row) for row in reader)


def read_file(path: Path) -> str:
    ext = path.suffix.lower()
    if ext == ".pdf":
        return _read_pdf(path)
    if ext == ".json":
        return _read_json(path)
    if ext == ".csv":
        return _read_csv(path)
    return path.read_text(encoding="utf-8", errors="ignore")


def chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    if chunk_size <= 0:
        return [text] if text.strip() else []
    overlap = max(0, min(overlap, chunk_size - 1))
    step = chunk_size - overlap
    chunks: list[str] = []
    text = text.strip()
    for start in range(0, len(text), step):
        piece = text[start : start + chunk_size].strip()
        if piece:
            chunks.append(piece)
        if start + chunk_size >= len(text):
            break
    return chunks


def iter_files(folder: Path) -> Iterable[Path]:
    for root, _, files in os.walk(folder):
        for name in files:
            p = Path(root) / name
            if p.suffix.lower() in SUPPORTED_EXTS:
                yield p


class VectorStore:
    def __init__(self, config: StoreConfig) -> None:
        self.config = config
        self._lock = Lock()
        self._model: SentenceTransformer | None = None
        self._client: MilvusClient | None = None
        self._dim: int | None = None

    @property
    def model(self) -> SentenceTransformer:
        if self._model is None:
            self._model = SentenceTransformer(self.config.embedding_model)
            self._dim = self._model.get_sentence_embedding_dimension()
        return self._model

    @property
    def client(self) -> MilvusClient:
        if self._client is None:
            Path(self.config.db_path).parent.mkdir(parents=True, exist_ok=True)
            self._client = MilvusClient(uri=self.config.db_path)
        return self._client

    def reconfigure(self, **kwargs) -> None:
        with self._lock:
            new_model = kwargs.get("embedding_model")
            new_db = kwargs.get("db_path")
            for k, v in kwargs.items():
                if hasattr(self.config, k) and v is not None and v != "":
                    setattr(self.config, k, v)
            if new_model:
                self._model = None
                self._dim = None
            if new_db:
                self._client = None

    def _ensure_collection(self) -> None:
        _ = self.model
        assert self._dim is not None
        if self.client.has_collection(self.config.collection):
            return
        schema = self.client.create_schema(auto_id=True, enable_dynamic_field=True)
        schema.add_field("id", DataType.INT64, is_primary=True)
        schema.add_field("vector", DataType.FLOAT_VECTOR, dim=self._dim)
        schema.add_field("text", DataType.VARCHAR, max_length=8192)
        schema.add_field("source", DataType.VARCHAR, max_length=1024)
        index_params = self.client.prepare_index_params()
        index_params.add_index(field_name="vector", index_type="AUTOINDEX", metric_type="COSINE")
        self.client.create_collection(
            collection_name=self.config.collection,
            schema=schema,
            index_params=index_params,
        )

    def embed(self, texts: list[str]) -> list[list[float]]:
        vecs = self.model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
        return [v.tolist() for v in vecs]

    def index_folder(self, folder: str) -> IndexResult:
        with self._lock:
            result = IndexResult()
            root = Path(folder).expanduser()
            if not root.exists():
                raise FileNotFoundError(f"Folder not found: {root}")
            self._ensure_collection()
            batch_texts: list[str] = []
            batch_meta: list[dict] = []
            for path in iter_files(root):
                try:
                    text = read_file(path)
                except Exception:
                    result.skipped_files.append(str(path))
                    continue
                chunks = chunk_text(text, self.config.chunk_size, self.config.chunk_overlap)
                if not chunks:
                    result.skipped_files.append(str(path))
                    continue
                for c in chunks:
                    batch_texts.append(c)
                    batch_meta.append({"source": str(path)})
                result.indexed_files.append(str(path))
                result.chunks += len(chunks)
                if len(batch_texts) >= 64:
                    self._insert(batch_texts, batch_meta)
                    batch_texts, batch_meta = [], []
            if batch_texts:
                self._insert(batch_texts, batch_meta)
            return result

    def _insert(self, texts: list[str], metas: list[dict]) -> None:
        vectors = self.embed(texts)
        rows = [
            {"vector": v, "text": t[:8000], "source": m["source"]}
            for v, t, m in zip(vectors, texts, metas)
        ]
        self.client.insert(collection_name=self.config.collection, data=rows)

    def query(self, text: str, top_k: int = 5) -> list[dict]:
        with self._lock:
            if not self.client.has_collection(self.config.collection):
                return []
            vector = self.embed([text])[0]
            results = self.client.search(
                collection_name=self.config.collection,
                data=[vector],
                limit=top_k,
                output_fields=["text", "source"],
            )
            hits = results[0] if results else []
            return [
                {
                    "score": float(hit.get("distance", 0.0)),
                    "text": hit.get("entity", {}).get("text", ""),
                    "source": hit.get("entity", {}).get("source", ""),
                }
                for hit in hits
            ]

    def stats(self) -> dict:
        info = {"collection": self.config.collection, "exists": False, "count": 0}
        if self.client.has_collection(self.config.collection):
            info["exists"] = True
            try:
                info["count"] = self.client.get_collection_stats(self.config.collection).get("row_count", 0)
            except Exception:
                pass
        return info

    def drop(self) -> None:
        with self._lock:
            if self.client.has_collection(self.config.collection):
                self.client.drop_collection(self.config.collection)
