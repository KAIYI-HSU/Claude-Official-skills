"""FastAPI application — serves cookbook API and the built frontend."""
from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from .config import settings
from .cookbook import build_tree, read_page
from .embeddings import store
from .llm_proxy import proxy
from .rag import build_system_prompt

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
log = logging.getLogger("cookbook-web")


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    log.info("Cookbook root: %s", settings.COOKBOOK_DIR)
    log.info("LLM format=%s endpoint=%s model=%s", settings.LLM_FORMAT, settings.LLM_ENDPOINT, settings.LLM_MODEL)
    try:
        store.load()
        log.info("Embeddings ready: %d chunks", len(store.chunks))
    except Exception:
        log.exception("Embedding load failed; chat will still work but without RAG")
    yield


app = FastAPI(title="Cookbook Web", lifespan=lifespan)


class ChatMessage(BaseModel):
    role: str = Field(..., pattern="^(user|assistant)$")
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMessage]
    current_page: str | None = None


@app.get("/api/health")
async def health() -> dict:
    return {
        "status": "ok",
        "embeddings_loaded": store.ready,
        "chunks": len(store.chunks),
        "llm_format": settings.LLM_FORMAT,
        "llm_model": settings.LLM_MODEL,
    }


@app.get("/api/cookbook/tree")
async def tree() -> dict:
    return build_tree()


@app.get("/api/cookbook/page")
async def page(path: str) -> dict:
    text = read_page(path)
    if text is None:
        raise HTTPException(404, detail="page not found")
    return {"path": path, "content": text}


@app.post("/api/chat")
async def chat(req: ChatRequest):
    if not req.messages:
        raise HTTPException(400, detail="messages required")
    last_user = next((m for m in reversed(req.messages) if m.role == "user"), None)
    if last_user is None:
        raise HTTPException(400, detail="last message must be user")

    system = build_system_prompt(last_user.content, req.current_page)
    messages = [m.model_dump() for m in req.messages]

    async def event_stream() -> AsyncIterator[bytes]:
        # send a meta event with retrieved sources
        try:
            from .rag import retrieve

            sources = [
                {"file_path": c["file_path"], "heading": c["heading"], "score": c["score"]}
                for c in retrieve(last_user.content)
            ]
        except Exception:
            sources = []
        import json as _json
        yield f"event: sources\ndata: {_json.dumps(sources, ensure_ascii=False)}\n\n".encode()

        async for token in proxy.stream(system, messages):
            yield f"data: {_json.dumps(token, ensure_ascii=False)}\n\n".encode()
        yield b"event: done\ndata: {}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")


# ---- static frontend ----

if settings.FRONTEND_DIST.exists():
    app.mount(
        "/assets",
        StaticFiles(directory=settings.FRONTEND_DIST / "assets"),
        name="assets",
    )

    @app.get("/{full_path:path}", include_in_schema=False)
    async def spa_fallback(full_path: str, request: Request):
        if full_path.startswith("api/"):
            return JSONResponse({"detail": "not found"}, status_code=404)
        index = settings.FRONTEND_DIST / "index.html"
        if not index.exists():
            return JSONResponse({"detail": "frontend not built"}, status_code=503)
        return FileResponse(index)
else:
    log.warning("Frontend dist not found at %s — running API-only mode", settings.FRONTEND_DIST)

    @app.get("/")
    async def root_placeholder() -> dict:
        return {"message": "API only — frontend not built", "docs": "/docs"}
