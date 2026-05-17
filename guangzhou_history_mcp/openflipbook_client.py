"""
Thin client for a self-hosted openflipbook backend.

We don't bundle or redistribute any upstream code; we just call the HTTP API
documented in upstream `docs/STORY.md`:

    POST /api/iteratively-generate-next-page
    Body: { query, aspect_ratio, web_search, session_id, current_node_id,
            mode, parent_query, parent_title, image? }
    Response: SSE stream of progressive JPEG chunks + status events,
              terminating in a final image payload.

The upstream response shape isn't strictly versioned, so this client is
defensive: it accepts several plausible variants of where the final image
lands (data URL on a `result` event, `image_url`, or the last base64 chunk
in a `frame` / `image` event).

Tested against a stub server in tests; can be exercised against a real
backend via the `--probe` CLI flag.

Stdlib-only. No requests/httpx dependency.
"""

from __future__ import annotations

import base64
import json
import os
import sys
import uuid
from dataclasses import dataclass
from typing import Iterator
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


DEFAULT_URL = os.environ.get("OPENFLIPBOOK_URL", "http://localhost:8000")


@dataclass
class FlipbookImage:
    """The result of one generate-next-page call."""

    query: str
    image_url: str | None = None     # https://... or data:image/...;base64,...
    page_title: str | None = None
    raw_events: list[dict] | None = None
    status: str = "ok"               # "ok" | "timeout" | "no-image" | "error"
    error: str | None = None

    def to_dict(self) -> dict:
        return {
            "query": self.query,
            "image_url": self.image_url,
            "page_title": self.page_title,
            "status": self.status,
            "error": self.error,
            "event_count": len(self.raw_events) if self.raw_events else 0,
        }


# ---------------------------------------------------------------------------
# Low-level SSE iterator over a urllib response
# ---------------------------------------------------------------------------

def _iter_sse(stream) -> Iterator[dict]:
    """Yield decoded SSE events as dicts.

    Each yielded event has shape::

        {"event": "<name>" | None, "data": "<payload string>"}

    A pure-stdlib re-implementation of the trivial SSE wire format.
    """
    event: str | None = None
    data_lines: list[str] = []

    while True:
        raw = stream.readline()
        if not raw:
            break
        line = raw.decode("utf-8", errors="replace").rstrip("\n").rstrip("\r")

        if line == "":
            if data_lines:
                yield {"event": event, "data": "\n".join(data_lines)}
                event, data_lines = None, []
            continue
        if line.startswith(":"):
            continue  # SSE comment / keep-alive
        if line.startswith("event:"):
            event = line[len("event:"):].strip()
            continue
        if line.startswith("data:"):
            data_lines.append(line[len("data:"):].lstrip(" "))
            continue
        # Some servers send `id:`, `retry:` — we ignore.

    # flush trailing event
    if data_lines:
        yield {"event": event, "data": "\n".join(data_lines)}


# ---------------------------------------------------------------------------
# Result extraction
# ---------------------------------------------------------------------------

_IMAGE_URL_KEYS = (
    "image_url", "imageUrl", "url", "final_image_url",
    "image", "final_image", "image_data_url",
)
_TITLE_KEYS = ("page_title", "title", "page_title_zh", "page_title_en")


def _looks_like_image(s: str) -> bool:
    return (
        s.startswith("data:image/")
        or s.startswith("http://") or s.startswith("https://")
    )


def _extract_image(events: list[dict]) -> tuple[str | None, str | None]:
    """Walk the captured events end-to-start, return (image_url, title)."""
    image, title = None, None

    def maybe(value):
        nonlocal image
        if isinstance(value, str) and _looks_like_image(value):
            image = value

    for ev in events:
        try:
            payload = json.loads(ev["data"])
        except (json.JSONDecodeError, KeyError):
            continue
        if not isinstance(payload, dict):
            continue
        for k in _IMAGE_URL_KEYS:
            if k in payload:
                maybe(payload[k])
        # base64 chunk pattern: {"frame":"...", "mime":"image/jpeg"}
        b64 = payload.get("frame") or payload.get("base64") or payload.get("b64")
        mime = payload.get("mime") or payload.get("content_type") or "image/jpeg"
        if isinstance(b64, str) and len(b64) > 200:
            image = f"data:{mime};base64,{b64}"
        for k in _TITLE_KEYS:
            if k in payload and isinstance(payload[k], str):
                title = title or payload[k]

    return image, title


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def generate_page_image(
    query: str,
    *,
    base_url: str = DEFAULT_URL,
    lang: str = "zh",
    aspect_ratio: str = "16:9",
    web_search: bool = True,
    session_id: str | None = None,
    timeout_s: float = 180.0,
    keep_raw: bool = False,
) -> FlipbookImage:
    """Call openflipbook's generate endpoint and return the final image.

    Parameters
    ----------
    query : the natural-language topic, e.g. "广州塔" / "Whampoa Academy"
    base_url : where openflipbook's backend is listening, e.g.
        "http://localhost:8000". Override via OPENFLIPBOOK_URL env var.
    lang : "zh" or "en" — only used for response metadata
    aspect_ratio : "16:9" (default) | "1:1" | "9:16"
    timeout_s : how long to wait for the SSE stream to finish
    keep_raw : if True, attach the raw events list to the return value

    Returns a FlipbookImage. ``status="ok"`` means we extracted an image_url.
    Other statuses ("timeout", "no-image", "error") still return the object —
    inspect ``error`` for details.
    """
    url = base_url.rstrip("/") + "/sse/generate"
    body = {
        "query": query,
        "aspect_ratio": aspect_ratio,
        "web_search": web_search,
        "session_id": session_id or f"gz_{uuid.uuid4().hex[:12]}",
        "mode": "query",
    }
    req = Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Accept": "text/event-stream, application/json",
        },
        method="POST",
    )

    events: list[dict] = []
    try:
        with urlopen(req, timeout=timeout_s) as resp:
            for ev in _iter_sse(resp):
                events.append(ev)
    except HTTPError as e:
        return FlipbookImage(query=query, status="error",
                             error=f"HTTP {e.code}: {e.reason}",
                             raw_events=events if keep_raw else None)
    except URLError as e:
        return FlipbookImage(query=query, status="error",
                             error=f"URL error: {e.reason}",
                             raw_events=events if keep_raw else None)
    except TimeoutError:
        return FlipbookImage(query=query, status="timeout",
                             error=f"timed out after {timeout_s}s",
                             raw_events=events if keep_raw else None)
    except Exception as e:  # noqa: BLE001 — surface whatever
        return FlipbookImage(query=query, status="error", error=repr(e),
                             raw_events=events if keep_raw else None)

    image_url, title = _extract_image(events)
    if image_url is None:
        return FlipbookImage(
            query=query, status="no-image",
            error="no image_url found in SSE stream",
            page_title=title,
            raw_events=events if keep_raw else None,
        )
    return FlipbookImage(
        query=query, image_url=image_url, page_title=title,
        status="ok", raw_events=events if keep_raw else None,
    )


# ---------------------------------------------------------------------------
# CLI / probe
# ---------------------------------------------------------------------------

def _main(argv: list[str]) -> int:
    import argparse
    ap = argparse.ArgumentParser(
        description="Probe a running openflipbook backend.")
    ap.add_argument("query", help="topic to send, e.g. '广州塔'")
    ap.add_argument("--url", default=DEFAULT_URL,
                    help=f"backend base URL (default {DEFAULT_URL})")
    ap.add_argument("--lang", default="zh", choices=("zh", "en"))
    ap.add_argument("--aspect", default="16:9")
    ap.add_argument("--timeout", type=float, default=60.0)
    ap.add_argument("--raw", action="store_true",
                    help="dump every SSE event")
    args = ap.parse_args(argv)

    r = generate_page_image(
        args.query, base_url=args.url, lang=args.lang,
        aspect_ratio=args.aspect, timeout_s=args.timeout, keep_raw=args.raw,
    )
    print(json.dumps(r.to_dict(), ensure_ascii=False, indent=2))
    if args.raw and r.raw_events:
        print("--- raw events ---", file=sys.stderr)
        for ev in r.raw_events:
            print(json.dumps(ev, ensure_ascii=False), file=sys.stderr)
    return 0 if r.status == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(_main(sys.argv[1:]))
