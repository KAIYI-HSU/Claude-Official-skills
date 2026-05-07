"""Embed cookbook chunks once at startup; cache to disk."""
from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np

from .config import settings
from .cookbook import collect_all_chunks

if TYPE_CHECKING:
    from sentence_transformers import SentenceTransformer

log = logging.getLogger(__name__)


class EmbeddingStore:
    def __init__(self) -> None:
        self.model: SentenceTransformer | None = None
        self.chunks: list[dict] = []
        self.vectors: np.ndarray | None = None

    @property
    def ready(self) -> bool:
        return self.vectors is not None and len(self.chunks) > 0

    def load(self) -> None:
        from sentence_transformers import SentenceTransformer

        log.info("Loading embedding model: %s", settings.EMBEDDING_MODEL)
        cache_dir = settings.EMBEDDING_CACHE
        cache_dir.mkdir(parents=True, exist_ok=True)
        self.model = SentenceTransformer(
            settings.EMBEDDING_MODEL, cache_folder=str(cache_dir)
        )

        chunks = collect_all_chunks()
        if not chunks:
            log.warning("No cookbook chunks found at %s", settings.COOKBOOK_DIR)
            self.chunks, self.vectors = [], np.zeros((0, 384), dtype="float32")
            return

        cache_path = settings.DATA_DIR / "embeddings.npz"
        manifest_path = settings.DATA_DIR / "manifest.txt"
        manifest = "\n".join(f"{c['file_path']}|{c['heading']}|{len(c['content'])}" for c in chunks)

        if cache_path.exists() and manifest_path.exists():
            try:
                if manifest_path.read_text(encoding="utf-8") == manifest:
                    data = np.load(cache_path)
                    self.vectors = data["vectors"]
                    self.chunks = chunks
                    log.info("Loaded %d cached embeddings", len(self.chunks))
                    return
            except Exception as exc:  # noqa: BLE001
                log.warning("Cache load failed: %s", exc)

        log.info("Embedding %d chunks ...", len(chunks))
        texts = [f"passage: {c['title']} - {c['heading']}\n{c['content']}" for c in chunks]
        vecs = self.model.encode(
            texts,
            batch_size=16,
            normalize_embeddings=True,
            show_progress_bar=False,
        )
        self.vectors = np.asarray(vecs, dtype="float32")
        self.chunks = chunks

        try:
            settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
            np.savez(cache_path, vectors=self.vectors)
            manifest_path.write_text(manifest, encoding="utf-8")
            log.info("Cached embeddings to %s", cache_path)
        except Exception as exc:  # noqa: BLE001
            log.warning("Cache save failed: %s", exc)

    def encode_query(self, query: str) -> np.ndarray:
        assert self.model is not None
        v = self.model.encode(
            [f"query: {query}"], normalize_embeddings=True, show_progress_bar=False
        )
        return np.asarray(v, dtype="float32")[0]


store = EmbeddingStore()
