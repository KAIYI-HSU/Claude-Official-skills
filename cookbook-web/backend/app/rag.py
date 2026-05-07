"""RAG retrieval + system prompt assembly."""
from __future__ import annotations

import numpy as np

from .config import settings
from .cookbook import read_page
from .embeddings import store


def retrieve(query: str, top_k: int | None = None) -> list[dict]:
    if not store.ready:
        return []
    k = top_k or settings.RAG_TOP_K
    q = store.encode_query(query)
    sims = store.vectors @ q
    idx = np.argsort(-sims)[: k]
    out: list[dict] = []
    for i in idx:
        i = int(i)
        c = store.chunks[i]
        out.append({**c, "score": float(sims[i])})
    return out


def build_system_prompt(query: str, current_page: str | None) -> str:
    parts: list[str] = [
        "你是 Claude Skills cookbook 的學習助教。請使用繁體中文回答。",
        "回答時必須：(1) 根據下方提供的 cookbook 內容回應；(2) 在末尾標註引用來源檔案路徑；(3) 若資料不足，誠實告知並建議使用者翻閱哪個檔案。",
    ]

    if current_page:
        page_text = read_page(current_page) or ""
        if page_text:
            page_text = page_text[: settings.RAG_MAX_PAGE_CHARS]
            parts.append(f"\n=== 使用者目前正在閱讀：{current_page} ===\n{page_text}")

    chunks = retrieve(query)
    if chunks:
        parts.append("\n=== 跨頁面 RAG 檢索結果（依相關度排序）===")
        for c in chunks:
            parts.append(
                f"\n--- 來源：{c['file_path']} | 段落：{c['heading']} | 相關度：{c['score']:.3f} ---\n{c['content'][:1200]}"
            )

    return "\n".join(parts)
