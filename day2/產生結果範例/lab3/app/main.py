"""FastAPI app: Vector DB management & query UI (Milvus Lite + SentenceTransformers)."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from .vector_store import VectorStoreService

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
DATA_DIR = BASE_DIR.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

app = FastAPI(title="Vector DB Lab")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

service = VectorStoreService(
    db_path=str(DATA_DIR / "milvus_lite.db"),
)


class IndexRequest(BaseModel):
    folder: str = Field(..., description="Path to folder of text files to index")
    collection: str = Field("documents", description="Milvus collection name")
    embedding_model: str = Field(
        "sentence-transformers/all-MiniLM-L6-v2",
        description="HuggingFace sentence-transformers model id",
    )
    chunk_size: int = Field(500, ge=50, le=4000)
    chunk_overlap: int = Field(50, ge=0, le=1000)
    recreate: bool = Field(False, description="Drop collection before indexing")


class QueryRequest(BaseModel):
    query: str
    collection: str = "documents"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    top_k: int = Field(5, ge=1, le=50)


@app.get("/", response_class=HTMLResponse)
def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "default_folder": str(DATA_DIR / "docs"),
            "collections": service.list_collections(),
        },
    )


@app.get("/api/collections")
def list_collections() -> dict[str, Any]:
    return {"collections": service.list_collections()}


@app.delete("/api/collections/{name}")
def drop_collection(name: str) -> dict[str, Any]:
    service.drop_collection(name)
    return {"ok": True, "dropped": name}


@app.post("/api/index")
def index_folder(req: IndexRequest) -> dict[str, Any]:
    folder = Path(req.folder).expanduser()
    if not folder.exists() or not folder.is_dir():
        raise HTTPException(400, f"Folder not found: {folder}")
    try:
        count = service.index_folder(
            folder=folder,
            collection=req.collection,
            embedding_model=req.embedding_model,
            chunk_size=req.chunk_size,
            chunk_overlap=req.chunk_overlap,
            recreate=req.recreate,
        )
    except Exception as exc:  # surface backend error to UI
        raise HTTPException(500, str(exc))
    return {"ok": True, "indexed_chunks": count, "collection": req.collection}


@app.post("/api/query")
def query(req: QueryRequest) -> dict[str, Any]:
    try:
        hits = service.query(
            text=req.query,
            collection=req.collection,
            embedding_model=req.embedding_model,
            top_k=req.top_k,
        )
    except Exception as exc:
        raise HTTPException(500, str(exc))
    return {"ok": True, "results": hits}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=os.environ.get("HOST", "127.0.0.1"),
        port=int(os.environ.get("PORT", "8000")),
        reload=True,
    )
