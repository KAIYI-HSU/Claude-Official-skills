"""Scan cookbooks/ markdown files and expose tree + page content."""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from .config import settings


@dataclass
class TreeFile:
    path: str
    title: str


@dataclass
class TreeCategory:
    slug: str
    title: str
    files: list[TreeFile]


_TITLE_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)


def _read_title(p: Path) -> str:
    try:
        text = p.read_text(encoding="utf-8")
    except Exception:
        return p.stem
    m = _TITLE_RE.search(text)
    return m.group(1).strip() if m else p.stem


def build_tree() -> dict:
    """Walk COOKBOOK_DIR; group top-level .md and category folders.

    Returns a JSON-serialisable dict.
    """
    root = settings.COOKBOOK_DIR
    if not root.exists():
        return {"root_files": [], "categories": []}

    root_files: list[TreeFile] = []
    categories: list[TreeCategory] = []

    for entry in sorted(root.iterdir()):
        if entry.is_file() and entry.suffix == ".md":
            root_files.append(TreeFile(path=entry.name, title=_read_title(entry)))
        elif entry.is_dir():
            files: list[TreeFile] = []
            for f in sorted(entry.iterdir()):
                if f.is_file() and f.suffix == ".md":
                    rel = f.relative_to(root).as_posix()
                    files.append(TreeFile(path=rel, title=_read_title(f)))
            if files:
                cat_title = _read_title(entry / "README.md") if (entry / "README.md").exists() else entry.name
                categories.append(TreeCategory(slug=entry.name, title=cat_title, files=files))

    return {
        "root_files": [f.__dict__ for f in root_files],
        "categories": [
            {"slug": c.slug, "title": c.title, "files": [f.__dict__ for f in c.files]}
            for c in categories
        ],
    }


def read_page(rel_path: str) -> str | None:
    """Read a single markdown file. Returns None if invalid / outside cookbook root."""
    root = settings.COOKBOOK_DIR.resolve()
    target = (root / rel_path).resolve()
    if not str(target).startswith(str(root) + "/") and target != root:
        return None
    if not target.exists() or target.suffix != ".md":
        return None
    return target.read_text(encoding="utf-8")


def split_chunks(text: str, file_path: str) -> list[dict]:
    """Split markdown by H2 headings into RAG-ready chunks."""
    parts: list[dict] = []
    current_heading = "Top"
    buf: list[str] = []
    title = ""

    for line in text.splitlines():
        if line.startswith("# ") and not title:
            title = line[2:].strip()
            continue
        if line.startswith("## "):
            if buf:
                parts.append({
                    "file_path": file_path,
                    "title": title,
                    "heading": current_heading,
                    "content": "\n".join(buf).strip(),
                })
                buf = []
            current_heading = line[3:].strip()
        else:
            buf.append(line)

    if buf:
        parts.append({
            "file_path": file_path,
            "title": title,
            "heading": current_heading,
            "content": "\n".join(buf).strip(),
        })

    return [c for c in parts if c["content"]]


def collect_all_chunks() -> list[dict]:
    root = settings.COOKBOOK_DIR
    chunks: list[dict] = []
    if not root.exists():
        return chunks
    for md in sorted(root.rglob("*.md")):
        rel = md.relative_to(root).as_posix()
        text = md.read_text(encoding="utf-8")
        chunks.extend(split_chunks(text, rel))
    return chunks
