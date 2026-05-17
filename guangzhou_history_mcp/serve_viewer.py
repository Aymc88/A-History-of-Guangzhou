"""
Tiny local HTTP server that:

  * serves the Guangzhou flipbook viewer at ``/``
  * exposes ``POST /api/openflipbook-image`` which proxies to a self-hosted
    openflipbook backend (default ``http://localhost:3000``) so the viewer
    can avoid CORS pain
  * sends permissive ``Access-Control-Allow-Origin: *`` headers — fine because
    we only listen on 127.0.0.1 by default

Run with::

    python -m guangzhou_history_mcp.serve_viewer
    python -m guangzhou_history_mcp.serve_viewer --port 8964 --openflipbook http://localhost:3000

…and open http://localhost:8964 in a browser.

This is a *companion* to the MCP server, not a replacement. The MCP server
still works standalone; this is what you run when you want the HTML viewer
to fetch AI-generated images from openflipbook in real time.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from .openflipbook_client import generate_page_image
from .viewer import build_html


def _make_handler(openflipbook_url: str):
    cached_html = build_html()

    class Handler(BaseHTTPRequestHandler):
        # ── HTML & status pages ────────────────────────────────────────────
        def _send(self, status: int, ctype: str, body: bytes,
                  extra_headers: dict | None = None):
            self.send_response(status)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.send_header("Cache-Control", "no-store")
            for k, v in (extra_headers or {}).items():
                self.send_header(k, v)
            self.end_headers()
            self.wfile.write(body)

        def _send_json(self, status: int, payload):
            self._send(status, "application/json; charset=utf-8",
                       json.dumps(payload, ensure_ascii=False).encode("utf-8"))

        # ── HTTP verbs ─────────────────────────────────────────────────────
        def do_OPTIONS(self):  # noqa: N802 — required name
            self._send(204, "text/plain", b"")

        def do_GET(self):  # noqa: N802
            if self.path in ("/", "/index.html"):
                self._send(200, "text/html; charset=utf-8",
                           cached_html.encode("utf-8"))
                return
            if self.path == "/healthz":
                self._send_json(200, {"ok": True,
                                      "openflipbook_url": openflipbook_url})
                return
            self._send(404, "text/plain", b"not found")

        def do_POST(self):  # noqa: N802
            if self.path != "/api/openflipbook-image":
                self._send(404, "text/plain", b"not found")
                return
            length = int(self.headers.get("Content-Length", "0"))
            try:
                req = json.loads(self.rfile.read(length) or b"{}")
            except json.JSONDecodeError:
                self._send_json(400, {"error": "invalid JSON"})
                return
            query = (req.get("query") or "").strip()
            if not query:
                self._send_json(400, {"error": "missing 'query'"})
                return
            lang = req.get("lang", "zh")
            aspect = req.get("aspect_ratio", "16:9")
            timeout = float(req.get("timeout_s", 180))
            result = generate_page_image(
                query, base_url=openflipbook_url,
                lang=lang, aspect_ratio=aspect, timeout_s=timeout,
            )
            payload = result.to_dict()
            payload["image_url"] = result.image_url  # may be data: URL
            self._send_json(200 if result.status == "ok" else 502, payload)

        # quieter access log
        def log_message(self, fmt, *args):
            sys.stderr.write("[serve_viewer] %s - %s\n" %
                             (self.address_string(), fmt % args))

    return Handler


def serve(host: str = "127.0.0.1", port: int = 8964,
          openflipbook_url: str | None = None,
          open_browser: bool = True) -> None:
    """Start the local HTTP server (blocks until Ctrl-C)."""
    openflipbook_url = (
        openflipbook_url
        or os.environ.get("OPENFLIPBOOK_URL")
        or "http://localhost:8000"
    )
    handler = _make_handler(openflipbook_url)
    server = ThreadingHTTPServer((host, port), handler)

    url = f"http://{host}:{port}"
    print(f"▸ Guangzhou flipbook viewer running at  {url}")
    print(f"▸ Proxying AI illustrations from        {openflipbook_url}")
    print("  (press Ctrl-C to stop)")

    if open_browser:
        threading.Timer(0.7, lambda: webbrowser.open(url)).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n▸ stopping…")
        server.server_close()


def _main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--host", default="127.0.0.1",
                    help="bind address (default: 127.0.0.1, loopback only)")
    ap.add_argument("--port", type=int, default=8964)
    ap.add_argument("--openflipbook",
                    help="upstream URL of your running openflipbook "
                         "(default: $OPENFLIPBOOK_URL or http://localhost:3000)")
    ap.add_argument("--no-browser", action="store_true",
                    help="don't auto-open the browser")
    args = ap.parse_args(argv)
    serve(host=args.host, port=args.port,
          openflipbook_url=args.openflipbook,
          open_browser=not args.no_browser)
    return 0


if __name__ == "__main__":
    raise SystemExit(_main(sys.argv[1:]))
