from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .vector_store import SUPPORTED_EXTS, StoreConfig, VectorStore

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"

app = FastAPI(title="Vector DB Lab")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

store = VectorStore(StoreConfig())


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "config": store.config,
            "supported_exts": sorted(SUPPORTED_EXTS),
        },
    )


@app.get("/api/config")
def get_config():
    return {
        "db_path": store.config.db_path,
        "collection": store.config.collection,
        "embedding_model": store.config.embedding_model,
        "chunk_size": store.config.chunk_size,
        "chunk_overlap": store.config.chunk_overlap,
        "supported_exts": sorted(SUPPORTED_EXTS),
    }


@app.post("/api/config")
def update_config(
    db_path: str = Form(""),
    collection: str = Form(""),
    embedding_model: str = Form(""),
    chunk_size: int = Form(0),
    chunk_overlap: int = Form(-1),
):
    updates = {
        "db_path": db_path or None,
        "collection": collection or None,
        "embedding_model": embedding_model or None,
        "chunk_size": chunk_size if chunk_size > 0 else None,
        "chunk_overlap": chunk_overlap if chunk_overlap >= 0 else None,
    }
    store.reconfigure(**{k: v for k, v in updates.items() if v is not None})
    return {"ok": True, "config": get_config()}


@app.post("/api/index")
def index_folder(folder: str = Form(...)):
    try:
        result = store.index_folder(folder)
    except FileNotFoundError as e:
        return JSONResponse({"ok": False, "error": str(e)}, status_code=400)
    return {
        "ok": True,
        "indexed_files": result.indexed_files,
        "skipped_files": result.skipped_files,
        "chunks": result.chunks,
    }


@app.post("/api/query")
def query(q: str = Form(...), top_k: int = Form(5)):
    results = store.query(q, top_k=max(1, top_k))
    return {"ok": True, "results": results}


@app.get("/api/stats")
def stats():
    return store.stats()


@app.post("/api/drop")
def drop():
    store.drop()
    return {"ok": True}
