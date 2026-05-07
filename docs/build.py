#!/usr/bin/env python3
"""Build a single self-contained index.html for the cookbook repo page.

Reads ../cookbooks/*.md, inlines marked.js + highlight.js (from _vendor/),
substitutes placeholders in template.html, and writes index.html.

If _vendor/marked.min.js or _vendor/highlight.min.js is missing, downloads
them once from jsDelivr. After a successful run the _vendor/ files are
expected to be committed so future builds work fully offline.

Usage:
    python build.py
"""
from __future__ import annotations

import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COOKBOOKS = (ROOT.parent / "cookbooks").resolve()
VENDOR = ROOT / "_vendor"
TEMPLATE = ROOT / "template.html"
OUTPUT = ROOT / "index.html"

# Pinned versions for reproducibility
MARKED_URL = "https://cdn.jsdelivr.net/npm/marked@12.0.2/marked.min.js"
HIGHLIGHT_URL = "https://cdn.jsdelivr.net/npm/@highlightjs/cdn-assets@11.10.0/highlight.min.js"

H1_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)


def read_title(text: str, fallback: str) -> str:
    m = H1_RE.search(text)
    return m.group(1).strip() if m else fallback


def collect_files() -> list[dict]:
    if not COOKBOOKS.exists():
        sys.exit(f"❌ cookbooks directory not found at {COOKBOOKS}")

    files: list[dict] = []
    for md in sorted(COOKBOOKS.rglob("*.md")):
        rel = md.relative_to(COOKBOOKS).as_posix()
        text = md.read_text(encoding="utf-8")
        files.append({
            "path": rel,
            "title": read_title(text, md.stem),
            "content": text,
        })
    return files


def fetch(url: str, dest: Path) -> None:
    print(f"  ↓ downloading {url}")
    req = urllib.request.Request(url, headers={"User-Agent": "cookbook-build/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:  # noqa: S310
        dest.write_bytes(resp.read())


def ensure_vendor() -> tuple[str, str]:
    VENDOR.mkdir(parents=True, exist_ok=True)
    marked = VENDOR / "marked.min.js"
    hljs = VENDOR / "highlight.min.js"
    if not marked.exists():
        fetch(MARKED_URL, marked)
    if not hljs.exists():
        fetch(HIGHLIGHT_URL, hljs)
    return marked.read_text(encoding="utf-8"), hljs.read_text(encoding="utf-8")


def safe_inline(script_body: str) -> str:
    """Make a JS string safe to put inside <script>...</script>.

    Browsers terminate the current <script> when they see a literal `</script>`
    in the body. We escape any such occurrence (rare in minified bundles, but
    the safe transform is to insert a backslash before the slash).
    """
    return script_body.replace("</script>", "<\\/script>")


def main() -> None:
    print(f"📂 scanning {COOKBOOKS}")
    files = collect_files()
    print(f"  ✓ {len(files)} markdown files")

    print("📦 ensuring vendor libs ...")
    marked_js, hljs_js = ensure_vendor()
    print(f"  ✓ marked.min.js   ({len(marked_js):,} bytes)")
    print(f"  ✓ highlight.min.js ({len(hljs_js):,} bytes)")

    if not TEMPLATE.exists():
        sys.exit(f"❌ template not found: {TEMPLATE}")

    template = TEMPLATE.read_text(encoding="utf-8")
    cookbook_json = json.dumps({"files": files}, ensure_ascii=False, separators=(",", ":"))

    # Important: replace JSON first so the marker stays unique
    html = template.replace("__COOKBOOK_DATA__", safe_inline(cookbook_json))
    html = html.replace("__MARKED_JS__", safe_inline(marked_js))
    html = html.replace("__HIGHLIGHT_JS__", safe_inline(hljs_js))

    OUTPUT.write_text(html, encoding="utf-8")
    size_kb = OUTPUT.stat().st_size / 1024
    print(f"✅ wrote {OUTPUT.name} — {size_kb:.1f} KB")
    print(f"   open it directly in a browser, or commit + enable GitHub Pages.")


if __name__ == "__main__":
    main()
