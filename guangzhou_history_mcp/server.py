"""
Guangzhou History MCP server.

Exposes a small set of tools — all bilingual (zh / en) — backed by the
chapter & timeline data in ``content.py`` and the self-contained flipbook
in ``viewer.py``.

Run directly with::

    python -m guangzhou_history_mcp

…or wire into Claude Desktop / any MCP-aware client; see README.md.
"""

from __future__ import annotations

import os
import sys
import tempfile
import webbrowser
from pathlib import Path
from typing import Literal

from mcp.server.fastmcp import FastMCP

from .content import (
    CHAPTERS,
    TIMELINE,
    TOPICS,
    chapter_index,
    query_topic as _query_topic,
    search,
    suggested_topics,
)
from .openflipbook_client import (
    DEFAULT_URL as OPENFLIPBOOK_DEFAULT_URL,
    generate_page_image,
)
from .viewer import build_html

Lang = Literal["zh", "en"]


mcp = FastMCP(
    name="guangzhou-history",
    instructions=(
        "Tools for exploring the 2,200-year history of Guangzhou (廣州). "
        "Every tool accepts a `lang` parameter — 'zh' for Simplified Chinese, "
        "'en' for English. Use `list_chapters` first to discover chapter IDs, "
        "then `get_chapter` for full text. Use `open_flipbook` when the user "
        "wants a visual, page-turning experience."
    ),
)


# ---------------------------------------------------------------------------
# Resources
# ---------------------------------------------------------------------------

@mcp.resource("guangzhou://about")
def about() -> str:
    """Short description of this server."""
    return (
        "Guangzhou History MCP\n"
        "=====================\n"
        f"Chapters: {len(CHAPTERS)}\n"
        f"Timeline entries: {len(TIMELINE)}\n"
        "Languages: zh, en\n"
    )


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------

@mcp.tool()
def list_chapters(lang: Lang = "zh") -> list[dict]:
    """List all chapters in chronological order.

    Returns one dict per chapter with ``id``, ``era`` and ``title`` in the
    requested language. Use the ``id`` with ``get_chapter`` to read the body.
    """
    out: list[dict] = []
    for c in CHAPTERS:
        out.append({
            "id": c.id,
            "era": c.era_zh if lang == "zh" else c.era_en,
            "title": c.title_zh if lang == "zh" else c.title_en,
        })
    return out


@mcp.tool()
def get_chapter(chapter_id: str, lang: Lang = "zh") -> dict:
    """Return the full text of one chapter.

    Parameters
    ----------
    chapter_id : str
        One of the IDs returned by ``list_chapters`` (e.g. "thirteen-hongs").
    lang : "zh" | "en"
        Language of the returned title / era / body.
    """
    idx = chapter_index()
    if chapter_id not in idx:
        raise ValueError(
            f"Unknown chapter_id {chapter_id!r}. "
            f"Valid IDs: {sorted(idx)}"
        )
    c = idx[chapter_id]
    return {
        "id": c.id,
        "era": c.era_zh if lang == "zh" else c.era_en,
        "title": c.title_zh if lang == "zh" else c.title_en,
        "body": c.body_zh if lang == "zh" else c.body_en,
    }


@mcp.tool()
def search_history(query: str, lang: Lang = "zh") -> list[dict]:
    """Substring-search every chapter (both languages) for ``query``.

    Returns a list of hits, each with ``id``, ``era``, ``title`` and a
    short ``snippet`` around the first match — all rendered in ``lang``.
    """
    return search(query, lang=lang)


@mcp.tool()
def query_topic(query: str, lang: Lang = "zh") -> dict:
    """Resolve a free-text query to a structured "flipbook page" result.

    Mimics the search-bar interaction of `flipbook.page`: the user types
    something like "广州塔", "Whampoa Academy", "十三行" or "yum cha", and
    the server returns a single illustrated page about that topic.

    Returns a dict with::

        {
          "query": "...",
          "matched_via": "alias" | "alias-partial" | "chapter-fuzzy",
          "chapter_id": "<one of list_chapters>",
          "title":   "...",   # query-specific page title
          "era":     "...",
          "body":    "...",   # full prose for the era
          "motif":   "...",   # which SVG illustration to use
          "highlights": [...] # 2-4 short factoid chips
          "related":    [...] # other topic strings the user might explore
        }

    If nothing matches, ``matched_via`` will be ``"none"`` and the rest of
    the fields will be empty strings / empty lists. Use ``list_topics``
    to see what's recognised, or ``search_history`` for a broader scan.
    """
    r = _query_topic(query, lang=lang)
    if r is None:
        return {
            "query": query, "matched_via": "none",
            "chapter_id": "", "title": "", "era": "", "body": "",
            "motif": "", "highlights": [], "related": suggested_topics(lang),
        }
    return r


@mcp.tool()
def list_topics(lang: Lang = "zh") -> list[dict]:
    """List every query topic this server recognises.

    Each entry has ``id``, the primary alias (``label``), the era it
    belongs to and the chapter it resolves to. Useful before calling
    ``query_topic``.
    """
    idx = chapter_index()
    out: list[dict] = []
    for t in TOPICS:
        ch = idx[t["chapter"]]
        out.append({
            "id": t["id"],
            "label": t["aliases"][0],
            "title": t["title_zh"] if lang == "zh" else t["title_en"],
            "era": ch.era_zh if lang == "zh" else ch.era_en,
            "chapter_id": t["chapter"],
            "aliases": t["aliases"],
        })
    return out


@mcp.tool()
def get_timeline(lang: Lang = "zh") -> list[dict]:
    """Return a compact chronological timeline of key events.

    Each entry has ``year`` and ``event``.
    """
    return [
        {"year": t["year"], "event": t["zh"] if lang == "zh" else t["en"]}
        for t in TIMELINE
    ]


@mcp.tool()
def fetch_openflipbook_image(
    query: str,
    lang: Lang = "zh",
    openflipbook_url: str | None = None,
    aspect_ratio: str = "16:9",
    timeout_s: float = 60.0,
) -> dict:
    """Ask a self-hosted openflipbook backend to generate an AI illustration.

    Requires a running openflipbook instance — by default at
    ``http://localhost:3000`` (override with the ``openflipbook_url``
    argument or the ``OPENFLIPBOOK_URL`` environment variable). The
    backend uses your FAL_KEY / OPENROUTER_API_KEY to plan a page and
    render an image; this tool returns the resulting image URL.

    Returns a dict::

        {
          "query":       "<echo>",
          "image_url":   "https://… or data:image/jpeg;base64,…" | null,
          "page_title":  "…" | null,
          "status":      "ok" | "no-image" | "timeout" | "error",
          "error":       "…" | null,
          "source":      "openflipbook",
        }

    On any non-ok status, ``image_url`` will be null — caller should fall
    back to ``query_topic`` for our local hand-drawn SVG.
    """
    r = generate_page_image(
        query,
        base_url=openflipbook_url or OPENFLIPBOOK_DEFAULT_URL,
        lang=lang,
        aspect_ratio=aspect_ratio,
        timeout_s=timeout_s,
    )
    out = r.to_dict()
    out["source"] = "openflipbook"
    return out


@mcp.tool()
def open_flipbook(
    out_path: str | None = None,
    open_in_browser: bool = True,
) -> dict:
    """Render the Lingnan-style bilingual flipbook to an HTML file.

    Parameters
    ----------
    out_path : str | None
        Where to write the HTML. If omitted, a file in the system temp
        directory is used. Existing files at ``out_path`` are overwritten.
    open_in_browser : bool
        When True (default), also pop the file in the user's default browser.

    Returns a dict with the absolute ``path`` and ``size_bytes`` of the
    file written. Keyboard controls inside the viewer:

      ←/→  flip pages  ·  Space  next  ·  L  toggle 中文/EN
      T    jump to timeline  ·  Home/End  cover / back
    """
    html_text = build_html()
    if out_path is None:
        fd, out_path = tempfile.mkstemp(
            prefix="guangzhou-flipbook-", suffix=".html"
        )
        os.close(fd)
    path = Path(out_path).expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html_text, encoding="utf-8")
    if open_in_browser:
        try:
            webbrowser.open(path.as_uri())
        except Exception:
            # Server context may have no browser; don't fail the tool.
            pass
    return {"path": str(path), "size_bytes": path.stat().st_size}


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

def main() -> None:
    """Run the MCP server over stdio (the transport Claude Desktop uses)."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
