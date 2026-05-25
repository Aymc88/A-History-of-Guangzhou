"""
Self-contained two-mode viewer for the Guangzhou History MCP.

`build_html()` returns a single string of HTML embedding two modes:

  1. QUERY MODE (default) — inspired by flipbook.page:
        a search bar at the top, a cream illustrated canvas below,
        breadcrumb history of past queries, "Clear" button, and
        suggested-topic chips on the empty state. Type a topic
        (e.g. "广州塔", "Whampoa", "十三行") and the viewer renders
        an annotated illustration page about it.

  2. BOOK MODE — the original Lingnan-style page-turning flipbook:
        cover → 6 chapters → timeline → back cover, with realistic
        CSS 3D rotateY page-flip animation.

Keyboard:
  Enter       submit query (query mode)
  F           toggle Query ↔ Book
  ← / →       flip pages (book mode)
  Space       next page (book mode)
  L           toggle 中文 / English
  T           jump to timeline (book mode)
  Esc         clear query (query mode)
  Home / End  cover / back-cover (book mode)
"""

from __future__ import annotations

import html
import json

from .content import CHAPTERS, TIMELINE, TOPICS, Chapter, suggested_topics
from .svg_library import (
    baked_png_ids,
    illustration_for as _rich_illus_for,
    svg_for as _rich_svg_for,
)


# ---------------------------------------------------------------------------
# Illustrations are sourced from ``svg_library`` — see that module.
# ---------------------------------------------------------------------------


def _svg_for(motif: str, topic_id: str | None = None) -> str:
    """Return the best illustration source string for a topic.

    Resolution order (handled by ``svg_library.illustration_for``):
        1. AI-baked PNG at  assets/illustrations/<topic_id>.png   (data URL)
        2. AI-baked PNG at  assets/illustrations/<motif>.png      (data URL)
        3. Topic-specific hand-drawn SVG override                 (markup)
        4. Chapter-level hand-drawn SVG                           (markup)

    The viewer's JS sniffs whether the string starts with ``data:`` or
    ``<svg`` and renders an ``<img>`` or inlines the SVG accordingly.
    """
    return _rich_illus_for(topic_id, motif)


# Real QR code PNGs loaded dynamically for the Guangzhou project link
def _load_qr_data_url() -> str:
    import base64
    from pathlib import Path
    path = Path(__file__).parent.parent / "assets" / "illustrations" / "project-qr.png"
    if path.exists():
        encoded = base64.b64encode(path.read_bytes()).decode("utf-8")
        return f"data:image/png;base64,{encoded}"
    return ""

def _load_game_qr_data_url() -> str:
    import base64
    from pathlib import Path
    path = Path(__file__).parent.parent / "assets" / "illustrations" / "game-qr.png"
    if path.exists():
        encoded = base64.b64encode(path.read_bytes()).decode("utf-8")
        return f"data:image/png;base64,{encoded}"
    return ""

QR_DATA_URL = _load_qr_data_url()
GAME_QR_DATA_URL = _load_game_qr_data_url()


# ---------------------------------------------------------------------------
# HTML builder
# ---------------------------------------------------------------------------

def build_html(title: str = "广州两千八百年 · Guangzhou History Flipbook") -> str:
    """Return the entire viewer as a single HTML string (query + book modes)."""

    # Serialise chapters, topics & timeline for the in-page JS to consume.
    chapter_payload = [
        {
            "id": c.id,
            "era_zh": c.era_zh, "era_en": c.era_en,
            "title_zh": c.title_zh, "title_en": c.title_en,
            "body_zh": c.body_zh, "body_en": c.body_en,
            "motif": c.motif,
            "svg": _svg_for(c.motif),
        }
        for c in CHAPTERS
    ]
    chapter_by_id = {c["id"]: c for c in chapter_payload}

    topics_payload = []
    for t in TOPICS:
        ch = chapter_by_id[t["chapter"]]
        # Topic-specific illustration if available, else fall back to the
        # chapter's motif (svg_library.svg_for handles this).
        topic_svg = _svg_for(ch["motif"], t["id"])
        topics_payload.append({
            "id": t["id"],
            "aliases": t["aliases"],
            "title_zh": t["title_zh"], "title_en": t["title_en"],
            "era_zh": ch["era_zh"], "era_en": ch["era_en"],
            "body_zh": ch["body_zh"], "body_en": ch["body_en"],
            "motif": ch["motif"], "svg": topic_svg,
            "highlights_zh": t["highlights_zh"],
            "highlights_en": t["highlights_en"],
            "chapter_id": t["chapter"],
        })

    payload = {
        "chapters": chapter_payload,
        "timeline": TIMELINE,
        "topics": topics_payload,
        "suggested_zh": suggested_topics("zh"),
        "suggested_en": [t["aliases"][1] if len(t["aliases"]) > 1
                        and not any('一' <= ch <= '鿿' for ch in t["aliases"][1])
                        else t["aliases"][0]
                        for t in TOPICS[:8]],
        "qr_svg": QR_DATA_URL,
        "game_qr": GAME_QR_DATA_URL,
    }
    payload_json = json.dumps(payload, ensure_ascii=False)

    css = _CSS
    js = _JS

    return (
        f'<!doctype html>\n'
        f'<html lang="zh-Hans">\n'
        f'<head>\n'
        f'  <meta charset="utf-8">\n'
        f'  <meta name="viewport" content="width=device-width,initial-scale=1">\n'
        f'  <title>{html.escape(title)}</title>\n'
        f'  <style>{css}</style>\n'
        f'</head>\n'
        f'<body data-mode="query">\n'
        f'  <header class="topbar">\n'
        f'    <div class="brand">\n'
        f'      <span class="seal">廣</span>\n'
        f'      <div class="brand-text">\n'
        f'        <strong data-zh="广州两千八百年" data-en="Guangzhou · 2,800 Years"></strong>\n'
        f'        <small data-zh="岭南风查询书 · 中英双语" data-en="Lingnan flipbook · bilingual"></small>\n'
        f'      </div>\n'
        f'    </div>\n'
        f'    <nav class="controls">\n'
        f'      <button id="modeToggle" class="ghost" title="切换模式 / Toggle mode (F)">\n'
        f'        <span class="mode-label" data-zh="翻页书" data-en="Flipbook"></span>\n'
        f'      </button>\n'
        f'      <button id="lang" class="ghost" title="切换语言 / Toggle language (L)">中 / EN</button>\n'
        f'    </nav>\n'
        f'  </header>\n'
        f'\n'
        f'  <!-- ─────────────────────────  QUERY MODE  ───────────────────────── -->\n'
        f'  <main class="stage stage-query" id="stageQuery">\n'
        f'    <div class="window">\n'
        f'      <div class="window-bar">\n'
        f'        <span class="dots"><i></i><i></i><i></i></span>\n'
        f'        <div class="address">\n'
        f'          <div class="crumbs" id="crumbs"></div>\n'
        f'          <input id="q" class="search" autocomplete="off"\n'
        f'                 spellcheck="false"\n'
        f'                 data-placeholder-zh="试试：广州塔 / 十三行 / 黄埔军校 / 沙面 …"\n'
        f'                 data-placeholder-en="Try: Canton Tower / Whampoa / Shamian / Howqua …">\n'
        f'          <span class="continue"\n'
        f'                data-zh="Continue this session"\n'
        f'                data-en="Continue this session"></span>\n'
        f'        </div>\n'
        f'        <button id="clearBtn" class="pill" hidden\n'
        f'                data-zh="清空" data-en="Clear"></button>\n'
        f'        <button class="round" title="share" tabindex="-1" aria-hidden="true">⤴</button>\n'
        f'      </div>\n'
        f'      <div class="window-body" id="canvas">\n'
        f'        <!-- empty state / result rendered by JS -->\n'
        f'      </div>\n'
        f'      <div class="window-footnote"\n'
        f'           data-zh="Tap anywhere on the page to expand"\n'
        f'           data-en="Tap anywhere on the page to expand"></div>\n'
        f'    </div>\n'
        f'    <div class="hint"\n'
        f'         data-zh="Enter 查询 · F 翻页书 · L 切换语言 · Esc 清空"\n'
        f'         data-en="Enter search · F flipbook · L language · Esc clear"></div>\n'
        f'  </main>\n'
        f'\n'
        f'  <!-- ─────────────────────────  BOOK MODE  ────────────────────────── -->\n'
        f'  <main class="stage stage-book" id="stageBook" hidden>\n'
        f'    <nav class="book-controls">\n'
        f'      <button id="prev">‹</button>\n'
        f'      <span id="pageNum">1 / 1</span>\n'
        f'      <button id="next">›</button>\n'
        f'    </nav>\n'
        f'    <div class="book" id="book" aria-live="polite"></div>\n'
        f'    <div class="hint" data-zh="← → 翻页 · ↑↓ 首尾页 · L 切换语言 · T 时间线 · Q 二维码 · F 返回查询"\n'
        f'                      data-en="← → flip · ↑↓ start/end · L language · T timeline · Q QR codes · F back to search"></div>\n'
        f'  </main>\n'
        f'\n'
        f'  <script id="payload" type="application/json">{payload_json}</script>\n'
        f'  <script>{js}</script>\n'
        f'</body>\n'
        f'</html>\n'
    )


# ---------------------------------------------------------------------------
# Static assets (kept as module-level strings so build_html() is pure).
# ---------------------------------------------------------------------------

_CSS = r"""
:root{
  --paper:#f3e7cc;
  --paper-edge:#e0cd9c;
  --ink:#2b1d10;
  --ink-soft:#54402a;
  --jade:#5e8a6b;
  --terracotta:#b85c2f;
  --opera-red:#c14a3a;
  --gold:#c9a35a;
  --indigo:#2c4a6e;
}
*{box-sizing:border-box}
html,body{height:100%;margin:0;font-family:"Noto Serif SC","Songti SC","Source Han Serif SC",
  "Times New Roman",serif;background:
  radial-gradient(circle at 30% 20%, #3a2814 0%, #1b1108 70%);
  color:var(--ink);}
.topbar{
  display:flex;align-items:center;justify-content:space-between;
  padding:14px 22px;background:linear-gradient(180deg,#1b1108,#2b1d10);
  border-bottom:1px solid #4a3622;color:var(--paper);
}
.brand{display:flex;align-items:center;gap:14px}
.seal{
  display:inline-grid;place-items:center;width:46px;height:46px;
  background:var(--opera-red);color:var(--paper);font-weight:700;font-size:24px;
  border:2px solid var(--gold);border-radius:6px;
  box-shadow:inset 0 0 0 2px #7c2c22, 2px 2px 0 #000;
  font-family:"Songti SC",serif;
}
.brand-text strong{display:block;font-size:18px;letter-spacing:.04em}
.brand-text small{opacity:.7;font-size:12px;letter-spacing:.1em}
.controls{display:flex;align-items:center;gap:10px}
.controls button{
  background:var(--paper);color:var(--ink);border:1px solid var(--paper-edge);
  border-radius:6px;padding:6px 12px;font-size:14px;cursor:pointer;
  font-family:inherit;
  transition:transform .08s ease,background .15s ease;
}
.controls button.ghost{
  background:transparent;color:var(--paper);border:1px solid #4a3622;
}
.controls button:hover{background:#fff5dd;color:var(--ink)}
.controls button:active{transform:translateY(1px)}

.book-controls{
  display:flex;align-items:center;gap:10px;position:absolute;top:18px;right:24px;z-index:20;
}
.book-controls button{
  background:var(--paper);color:var(--ink);border:1px solid var(--paper-edge);
  border-radius:6px;padding:6px 12px;font-size:18px;cursor:pointer;
  font-family:inherit;
}
.book-controls button:hover{background:#fff5dd}
#pageNum{color:var(--paper);font-variant-numeric:tabular-nums;min-width:64px;text-align:center}

.stage{
  height:calc(100vh - 76px);
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  position:relative;perspective:2200px;padding:24px;
}
body[data-mode="query"] .stage-book{display:none !important}
body[data-mode="book"]  .stage-query{display:none !important}

/* ──────────────── Query-mode window (flipbook.page-style) ──────────────── */
.window{
  width:min(1160px, 96vw);
  height:min(82vh, 760px);
  background:var(--paper);
  border-radius:18px;
  border:1px solid #d8c28e;
  box-shadow:0 24px 60px rgba(0,0,0,.45), inset 0 0 0 1px rgba(255,255,255,.4);
  display:flex;flex-direction:column;overflow:hidden;position:relative;
}
.window-bar{
  display:flex;align-items:center;gap:12px;
  padding:14px 18px;border-bottom:1px solid #e2cf9c;
  background:linear-gradient(180deg,#fbeed1,#f3e7cc);
}
.window-bar .dots{display:inline-flex;gap:6px;align-items:center;margin-right:4px}
.window-bar .dots i{
  width:11px;height:11px;border-radius:50%;
  background:#d6bf85;border:1px solid #b89d63;display:inline-block;
}
.address{
  flex:1;display:flex;align-items:center;gap:10px;min-width:0;
  border:1px solid #d8c28e;background:#fff8e0;border-radius:10px;
  padding:6px 14px;height:36px;
  font-family:"Songti SC","Noto Serif SC",serif;
}
.address .crumbs{
  display:flex;gap:6px;align-items:center;flex-shrink:0;
  font-size:14px;color:var(--ink);max-width:55%;overflow:hidden;
}
.address .crumbs .crumb{
  cursor:pointer;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;
  max-width:260px;
}
.address .crumbs .crumb:hover{text-decoration:underline}
.address .crumbs .crumb.current{color:var(--ink);font-weight:600;cursor:default}
.address .crumbs .crumb.current:hover{text-decoration:none}
.address .crumbs .sep{color:var(--ink-soft);opacity:.55;flex-shrink:0}
.address .search{
  flex:1;border:0;background:transparent;outline:none;
  font:16px/1.4 inherit;color:var(--ink);min-width:60px;
}
.address .search::placeholder{color:#8d7048;font-style:italic;opacity:.85}
.address .continue{
  color:#8d7048;font-size:13px;white-space:nowrap;opacity:.85;
}
.window-bar .pill{
  background:#1f1610;color:var(--paper);border:0;border-radius:18px;
  padding:6px 14px;font-size:13px;cursor:pointer;font-family:inherit;
  letter-spacing:.06em;
}
.window-bar .pill:hover{background:#34251a}
.window-bar .round{
  width:34px;height:34px;border-radius:50%;
  background:#fff8e0;border:1px solid #d8c28e;color:var(--ink-soft);
  cursor:default;font-size:15px;
}
.window-body{
  flex:1;position:relative;overflow:hidden;
  background:
    radial-gradient(ellipse at 50% 40%, #fff7e0 0%, #f3e7cc 60%, #e8d6a3 100%);
}
.window-body::before{
  /* paper fibre */
  content:"";position:absolute;inset:0;pointer-events:none;opacity:.6;
  background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='200' height='200'><filter id='n'><feTurbulence baseFrequency='0.85' numOctaves='2' seed='7'/><feColorMatrix values='0 0 0 0 0.3  0 0 0 0 0.22  0 0 0 0 0.1  0 0 0 0.05 0'/></filter><rect width='100%25' height='100%25' filter='url(%23n)'/></svg>");
}
.window-footnote{
  position:absolute;bottom:8px;left:0;right:0;text-align:center;
  font-size:12px;color:#8d7048;opacity:.7;pointer-events:none;
}

/* Empty state */
.empty{
  position:absolute;inset:0;display:flex;flex-direction:column;
  align-items:center;justify-content:center;text-align:center;padding:24px;gap:20px;
}
.empty .empty-title{
  font-size:22px;color:var(--ink);max-width:560px;line-height:1.5;
  font-family:"Songti SC","Noto Serif SC",serif;
}
.empty .upload{
  display:inline-flex;align-items:center;gap:8px;
  background:#fff8e0;border:1px solid #d8c28e;border-radius:8px;
  padding:8px 16px;color:var(--ink);font-family:inherit;font-size:14px;cursor:default;
}
.empty .upload-icon{
  display:inline-block;width:16px;height:14px;border:1.5px solid var(--ink-soft);
  border-radius:2px;position:relative;
}
.empty .upload-icon::after{
  content:"";position:absolute;left:3px;bottom:2px;width:5px;height:5px;
  background:var(--ink-soft);border-radius:50%;
}
.empty .chips{
  display:flex;flex-wrap:wrap;gap:8px;justify-content:center;max-width:720px;
}
.empty .chips small{
  width:100%;font-size:12px;color:#8d7048;letter-spacing:.18em;margin-bottom:2px;
}
.chip{
  background:#fff8e0;border:1px solid #d8c28e;border-radius:18px;
  padding:5px 14px;color:var(--ink);font-family:inherit;font-size:13px;cursor:pointer;
  transition:background .12s ease, transform .08s ease;
}
.chip:hover{background:#fbeed1}
.chip:active{transform:translateY(1px)}

/* Result card */
.result{
  position:absolute;inset:0;display:grid;
  grid-template-columns:1.15fr 1fr;gap:28px;
  padding:34px 44px 50px;
}
.result .era{
  grid-column:1 / -1;
  color:var(--terracotta);font-size:12px;letter-spacing:.3em;
  text-transform:uppercase;font-family:inherit;
}
.result h1{
  grid-column:1 / -1;
  margin:-6px 0 0;font-size:34px;line-height:1.2;color:var(--ink);
  font-family:"Songti SC","Noto Serif SC",serif;letter-spacing:.03em;
}
.result .body{
  font-size:15px;line-height:1.85;color:var(--ink-soft);
  text-align:justify;align-self:start;overflow:auto;max-height:100%;
}
.result .illus-wrap{
  position:relative;display:flex;align-items:center;justify-content:center;
  min-height:200px;
}
.result .illus-wrap svg{width:100%;height:auto;max-height:300px}
.result .illus-wrap img.ai-illus{
  width:100%;height:auto;max-height:340px;object-fit:contain;
  border:1px solid var(--paper-edge);border-radius:8px;
  box-shadow:0 6px 18px rgba(0,0,0,.25);
  animation:fade-in .35s ease;
}
@keyframes fade-in{from{opacity:0;transform:scale(.98)}to{opacity:1;transform:none}}
.result .illus-wrap.loading::after{
  content:"";position:absolute;left:50%;top:50%;
  width:34px;height:34px;margin:-17px 0 0 -17px;
  border:3px solid #d8c28e;border-top-color:var(--terracotta);
  border-radius:50%;animation:spin .9s linear infinite;
}
.result .illus-wrap .ai-badge{
  position:absolute;left:8px;bottom:8px;
  background:rgba(31,22,16,.85);color:#fff8e0;
  font-size:10px;letter-spacing:.2em;padding:3px 8px;border-radius:10px;
  text-transform:uppercase;pointer-events:none;
}
@keyframes spin{to{transform:rotate(360deg)}}
.result .highlights{
  grid-column:1 / -1;display:flex;flex-wrap:wrap;gap:10px;margin-top:auto;
}
.result .hl{
  background:#fff8e0;border:1px solid #d8c28e;border-radius:8px;
  padding:8px 12px;font-size:12.5px;color:var(--ink);line-height:1.4;
  max-width:280px;position:relative;
}
.result .hl::before{
  content:"";position:absolute;left:-1px;top:6px;bottom:6px;width:3px;
  background:var(--terracotta);border-radius:2px;
}
.result .related{
  grid-column:1 / -1;display:flex;flex-wrap:wrap;gap:8px;align-items:center;
  border-top:1px dashed #d8c28e;padding-top:14px;
}
.result .related small{
  font-size:11px;letter-spacing:.2em;color:#8d7048;margin-right:4px;
}
.result .nomatch{
  grid-column:1 / -1;text-align:center;color:var(--ink-soft);font-size:15px;
  line-height:1.7;padding:40px 0;
}
@media (max-width: 820px){
  .result{grid-template-columns:1fr;padding:24px 22px 40px;gap:18px}
  .result .illus-wrap{order:-1}
  .result .illus-wrap svg{max-height:200px}
  .result h1{font-size:24px}
  .address .continue{display:none}
}

.hint{
  position:absolute;bottom:14px;left:0;right:0;text-align:center;color:#d8c8a0;
  font-size:12px;letter-spacing:.18em;opacity:.7;
}
.book{
  width:min(880px, 96vw);
  height:min(620px, 78vh);
  position:relative;transform-style:preserve-3d;
}

.page{
  position:absolute;inset:0;
  background:
    repeating-linear-gradient(0deg, rgba(0,0,0,.025) 0 1px, transparent 1px 3px),
    radial-gradient(ellipse at 80% 30%, #fff7e3 0%, var(--paper) 55%, var(--paper-edge) 100%);
  border:1px solid var(--paper-edge);
  border-radius:8px;
  box-shadow:
    0 30px 50px rgba(0,0,0,.55),
    inset 0 0 60px rgba(120,80,30,.18),
    inset 8px 0 18px -10px rgba(60,30,10,.45);
  padding:46px 52px 36px;
  display:flex;flex-direction:column;gap:18px;
  transform-origin:left center;
  backface-visibility:hidden;
  transition:transform .9s cubic-bezier(.45,.05,.25,1), box-shadow .9s;
}
.page.flipped{transform:rotateY(-178deg);box-shadow:0 30px 50px rgba(0,0,0,.25);}
.page.active{z-index:5}
.page::before{
  /* elegant thin gold gradient line at top */
  content:"";position:absolute;top:14px;left:46px;right:46px;height:2px;
  background:linear-gradient(90deg, transparent, var(--gold) 20%, var(--gold) 80%, transparent);
  opacity:.6;
}
.page::after{
  /* faux border at bottom */
  content:"";position:absolute;bottom:14px;left:46px;right:46px;height:6px;
  background:linear-gradient(90deg, var(--gold), transparent 50%, var(--gold));
  opacity:.5;border-radius:2px;
}
.page .era{
  margin-top:18px;color:var(--terracotta);font-size:13px;letter-spacing:.25em;
  text-transform:uppercase;
}
.page h1{
  margin:0;font-size:30px;line-height:1.25;color:var(--ink);
  font-family:"Songti SC","Noto Serif SC",serif;letter-spacing:.04em;
}
.page-content{
  display:flex;
  gap:28px;
  align-items:stretch;
  flex:1;
  min-height:0;
  margin-top:4px;
}
.page .body{
  flex:1.2;
  font-size:15.5px;
  line-height:1.85;
  color:var(--ink-soft);
  text-align:justify;
  overflow-y:auto;
  padding-right:4px;
}
.page .illus{
  flex:1;
  display:flex;
  align-items:center;
  justify-content:center;
  position:relative;
  min-width:0;
}
.page .illus svg, .page .illus img{
  max-width:100%;
  max-height:260px;
  width:auto;
  height:auto;
  object-fit:contain;
  border-radius:8px;
}
.page .illus img.ai-illus{
  box-shadow:0 8px 20px rgba(0,0,0,0.15);
  border:1px solid var(--paper-edge);
}
.page .illus .ai-badge{
  position:absolute;
  bottom:6px;
  right:6px;
  background:var(--terracotta);
  color:var(--paper);
  font-size:10px;
  padding:2px 6px;
  border-radius:4px;
  font-family:inherit;
  letter-spacing:0.05em;
  box-shadow:0 2px 4px rgba(0,0,0,0.1);
}
.page .folio{
  position:absolute;bottom:22px;right:42px;color:var(--ink-soft);
  font-variant-numeric:tabular-nums;font-size:12px;letter-spacing:.18em;
}
.page .author{
  position:absolute;bottom:22px;left:42px;color:var(--ink-soft);
  font-size:12px;letter-spacing:.06em;opacity:.8;
}

/* Cover page */
.page.cover{
  background:
    radial-gradient(ellipse at 50% 30%, #fff5dd 0%, #ead7a7 50%, #c69d52 100%);
}
.page.cover .seal-lg{
  align-self:center;margin-top:30px;width:160px;height:160px;
  background:var(--opera-red);color:var(--paper);
  display:flex;flex-direction:column;align-items:center;justify-content:center;line-height:1.1;
  font-family:"Songti SC",serif;font-size:54px;font-weight:700;
  border:6px solid var(--gold);border-radius:14px;
  box-shadow:inset 0 0 0 4px #7c2c22, 6px 6px 0 #3a2410;
}
.page.cover h1{font-size:46px;text-align:center;margin-top:18px;letter-spacing:.1em}
.page.cover .subtitle{
  text-align:center;color:var(--ink-soft);font-size:18px;letter-spacing:.3em;
}
.page.cover .footer{
  margin-top:auto;text-align:center;color:var(--ink-soft);font-size:13px;
}

/* Timeline page */
.page.timeline ol{
  list-style:none;margin:0;padding:0;
  display:grid;grid-template-columns:1fr 1fr;gap:5px 16px;
  font-size:12.5px;line-height:1.4;
}
.page.timeline li{
  display:grid;grid-template-columns:84px 1fr;gap:8px;align-items:start;
  border-left:2px solid var(--terracotta);padding:2px 0 2px 8px;
}
.page.timeline li b{color:var(--terracotta);font-variant-numeric:tabular-nums}

/* Back cover */
.page.back{
  background:radial-gradient(ellipse at 50% 70%, #ead7a7 0%, #c69d52 100%);
  text-align:center;justify-content:center;
}
.page.back h1{font-size:32px}
.page.back p{color:var(--ink-soft);font-size:15px;line-height:1.8;max-width:520px;margin:0 auto}

/* QR codes page */
.page.qr{
  background:radial-gradient(ellipse at 50% 50%, #f5ead0 0%, #e8d4a0 100%);
  display:flex;align-items:center;justify-content:center;
}
.qr-page-content{
  display:flex;gap:48px;align-items:center;justify-content:center;
  flex:1;padding:20px;
}
.qr-item{
  display:flex;flex-direction:column;align-items:center;gap:14px;
}
.qr-item .qr-wrap{
  width:200px;height:200px;padding:12px;
  background:#fff;border-radius:16px;
  box-shadow:0 8px 28px rgba(0,0,0,0.12);
  border:1px solid var(--paper-edge);
  display:flex;align-items:center;justify-content:center;
}
.qr-item .qr-wrap img{
  width:100%;height:100%;object-fit:contain;border-radius:4px;
}
.qr-item small{
  color:var(--ink-soft);font-size:12px;opacity:.85;
  letter-spacing:0.05em;text-align:center;
}

/* Subtle paper fibre texture using svg data URI */
.page{
  background-image:
    url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='160' height='160'><filter id='n'><feTurbulence baseFrequency='0.9' numOctaves='2' seed='4'/><feColorMatrix values='0 0 0 0 0.3  0 0 0 0 0.22  0 0 0 0 0.1  0 0 0 0.06 0'/></filter><rect width='100%25' height='100%25' filter='url(%23n)'/></svg>"),
    radial-gradient(ellipse at 80% 30%, #fff7e3 0%, var(--paper) 55%, var(--paper-edge) 100%);
}

@media (max-width: 720px){
  .book{height:min(560px,70vh)}
  .page{padding:36px 28px 28px}
  .page h1{font-size:24px}
  .page .body{font-size:15px;line-height:1.7}
  .page.cover h1{font-size:30px}
  .page.cover .seal-lg{width:120px;height:120px;font-size:42px}
  .page.timeline ol{grid-template-columns:1fr}
}
"""

# JavaScript: handles BOTH query mode and book mode from one payload.
_JS = r"""
(() => {
  const payload = JSON.parse(document.getElementById("payload").textContent);

  // ── shared state ──────────────────────────────────────────────────────
  let lang = "zh";                 // 'zh' | 'en'
  let mode = "query";              // 'query' | 'book'
  const session = [];              // breadcrumb stack of resolved results
  let cursor = -1;                 // index in `session` currently shown

  // build alias → topic map once
  const aliasMap = new Map();
  payload.topics.forEach(t => {
    t.aliases.forEach(a => aliasMap.set(a.toLowerCase(), t));
  });

  // ── DOM ───────────────────────────────────────────────────────────────
  const $ = id => document.getElementById(id);
  const body       = document.body;
  const btnMode    = $("modeToggle");
  const btnLang    = $("lang");
  // query mode
  const inputQ     = $("q");
  const crumbs     = $("crumbs");
  const canvas     = $("canvas");
  const continueEl = document.querySelector(".address .continue");
  const clearBtn   = $("clearBtn");
  // book mode
  const bookEl     = $("book");
  const pageNumEl  = $("pageNum");
  const btnPrev    = $("prev");
  const btnNext    = $("next");

  function el(html) {
    const t = document.createElement("template");
    t.innerHTML = html.trim();
    return t.content.firstElementChild;
  }
  function escAttr(s){
    return String(s).replace(/&/g,"&amp;").replace(/"/g,"&quot;")
                    .replace(/</g,"&lt;").replace(/>/g,"&gt;");
  }
  function escText(s){
    return String(s).replace(/[&<>]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;"}[c]));
  }
  // Detect whether an illustration string is a data: URL (AI-baked PNG)
  // or inline SVG markup, and emit the right HTML.
  function renderIllustration(src){
    if (typeof src !== "string") return "";
    const head = src.slice(0, 12).trim().toLowerCase();
    if (head.startsWith("data:image") || head.startsWith("http")) {
      return `<img class="ai-illus" src="${escAttr(src)}" alt="">`;
    }
    return src;  // assume already-trusted <svg>…</svg>
  }

  // ── language ──────────────────────────────────────────────────────────
  function applyLang() {
    document.documentElement.lang = (lang === "zh") ? "zh-Hans" : "en";
    document.querySelectorAll("[data-zh],[data-en]").forEach(node => {
      const v = (lang === "zh") ? node.getAttribute("data-zh")
                                : node.getAttribute("data-en");
      if (v != null) node.textContent = v;
    });
    if (inputQ) {
      const ph = (lang === "zh")
        ? inputQ.getAttribute("data-placeholder-zh")
        : inputQ.getAttribute("data-placeholder-en");
      inputQ.placeholder = ph || "";
    }
    // re-render the current result so its text picks up the new language
    if (mode === "query" && cursor >= 0) renderResult(session[cursor]);
    if (mode === "query" && cursor < 0)  renderEmpty();
  }

  // ── mode switching ────────────────────────────────────────────────────
  function setMode(m) {
    mode = m;
    body.dataset.mode = m;
    $("stageQuery").hidden = (m !== "query");
    $("stageBook").hidden  = (m !== "book");
    const lbl = btnMode.querySelector(".mode-label");
    if (m === "query") { lbl.setAttribute("data-zh","翻页书");
                         lbl.setAttribute("data-en","Flipbook"); }
    else               { lbl.setAttribute("data-zh","查询");
                         lbl.setAttribute("data-en","Search"); }
    applyLang();
    if (m === "book" && bookPages.length === 0) initBook();
  }

  // ── query mode: search + render ───────────────────────────────────────
  function resolveQuery(q) {
    const qn = (q || "").trim().toLowerCase();
    if (!qn) return null;
    // 1) exact alias
    if (aliasMap.has(qn)) return { kind: "topic", t: aliasMap.get(qn), query: q };
    // 2) alias substring (either way)
    for (const [a, t] of aliasMap) {
      if (a.includes(qn) || qn.includes(a)) return { kind: "topic", t, query: q };
    }
    // 3) chapter substring fallback
    const hay = c => (c.title_zh + " " + c.title_en + " " +
                      c.body_zh  + " " + c.body_en).toLowerCase();
    for (const c of payload.chapters) {
      if (hay(c).includes(qn)) {
        return {
          kind: "chapter", t: {
            id: "chapter:" + c.id,
            aliases: [],
            title_zh: c.title_zh, title_en: c.title_en,
            era_zh: c.era_zh,    era_en: c.era_en,
            body_zh: c.body_zh,  body_en: c.body_en,
            motif: c.motif,      svg: c.svg,
            highlights_zh: [],   highlights_en: [],
            chapter_id: c.id,
          }, query: q
        };
      }
    }
    return null;
  }

  function submitQuery(q) {
    const hit = resolveQuery(q);
    const entry = { query: q, hit };
    // if the user navigated back and submits a new query, trim forward history
    if (cursor < session.length - 1) session.splice(cursor + 1);
    session.push(entry);
    cursor = session.length - 1;
    renderCrumbs();
    if (hit) renderResult(entry); else renderNoMatch(q);
    clearBtn.hidden = false;
    inputQ.value = "";
    continueEl.style.display = "";
  }

  function renderCrumbs() {
    crumbs.innerHTML = "";
    session.forEach((e, i) => {
      const c = el(`<span class="crumb${i === cursor ? " current":""}">${escText(e.query)}</span>`);
      c.addEventListener("click", () => {
        if (i === cursor) return;
        cursor = i; renderCrumbs();
        if (session[i].hit) renderResult(session[i]); else renderNoMatch(session[i].query);
      });
      crumbs.appendChild(c);
      if (i < session.length - 1) crumbs.appendChild(el(`<span class="sep">/</span>`));
    });
    if (session.length) crumbs.appendChild(el(`<span class="sep">/</span>`));
  }

  function renderEmpty() {
    crumbs.innerHTML = "";
    clearBtn.hidden = true;
    continueEl.style.display = "none";
    const suggested = (lang === "zh") ? payload.suggested_zh : payload.suggested_en;
    const chips = suggested.map(s =>
      `<button class="chip" data-q="${escAttr(s)}">${escText(s)}</button>`).join("");
    canvas.innerHTML = "";
    const node = el(`
      <div class="empty">
        <div class="empty-title"
             data-zh="在搜索框输入主题，或任选一个开始探索广州两千八百年的悠久历史。"
             data-en="Type a topic in the search bar, or pick one to start exploring 2,800 years of Guangzhou."></div>
        <button class="upload" tabindex="-1">
          <span class="upload-icon"></span>
          <span data-zh="Upload image" data-en="Upload image"></span>
        </button>
        <div class="chips">
          <small data-zh="试试这些主题" data-en="Try these topics"></small>
          ${chips}
        </div>
      </div>
    `);
    canvas.appendChild(node);
    node.querySelectorAll(".chip").forEach(c => {
      c.addEventListener("click", () => submitQuery(c.dataset.q));
    });
    applyLang();
  }

  // When served over http(s) by serve_viewer.py, ask the backend for an
  // AI-generated illustration. When opened as a file:// URL, skip and
  // keep the local SVG.
  const canFetchAiImage = (location.protocol === "http:" ||
                           location.protocol === "https:");
  // Cache image URLs across language toggles so we don't re-hit the backend.
  const aiImageCache = new Map();   // query → image_url | "FAILED"

  async function tryLoadAiImage(query, container) {
    if (!canFetchAiImage || !container) return;
    const cached = aiImageCache.get(query);
    if (cached === "FAILED") return;
    if (cached) { applyAiImage(container, cached); return; }
    container.classList.add("loading");
    try {
      const r = await fetch("/api/openflipbook-image", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({query, lang, aspect_ratio: "16:9",
                              timeout_s: 75}),
      });
      const j = await r.json();
      if (j && j.status === "ok" && j.image_url) {
        aiImageCache.set(query, j.image_url);
        applyAiImage(container, j.image_url);
      } else {
        aiImageCache.set(query, "FAILED");
      }
    } catch (e) {
      aiImageCache.set(query, "FAILED");
    } finally {
      container.classList.remove("loading");
    }
  }

  function applyAiImage(container, url) {
    // Replace the SVG with an <img>, keep our terracotta "AI" badge.
    container.innerHTML = `
      <img class="ai-illus" src="${escAttr(url)}" alt="">
      <span class="ai-badge">AI · openflipbook</span>`;
  }

  function renderResult(entry) {
    const t = entry.hit.t;
    const era      = (lang === "zh") ? t.era_zh      : t.era_en;
    const title    = (lang === "zh") ? t.title_zh    : t.title_en;
    const bodyText = (lang === "zh") ? t.body_zh     : t.body_en;
    const hls      = (lang === "zh") ? t.highlights_zh : t.highlights_en;
    const hlHtml   = (hls || []).map(h =>
      `<div class="hl">${escText(h)}</div>`).join("");
    // related = sibling topics that share an era, then anything else
    const others = payload.topics
      .filter(x => x.id !== t.id)
      .sort((a,b) => (a.chapter_id===t.chapter_id?-1:1)
                    -(b.chapter_id===t.chapter_id?-1:1));
    const rel = others.slice(0, 6).map(x => {
      const lbl = x.aliases[0];
      return `<button class="chip" data-q="${escAttr(lbl)}">${escText(lbl)}</button>`;
    }).join("");

    canvas.innerHTML = "";
    const node = el(`
      <div class="result">
        <div class="era">${escText(era)}</div>
        <h1>${escText(title)}</h1>
        <div class="body">${escText(bodyText)}</div>
        <div class="illus-wrap">${renderIllustration(t.svg)}</div>
        ${hlHtml ? `<div class="highlights">${hlHtml}</div>` : ``}
        <div class="related">
          <small data-zh="相关主题" data-en="Related"></small>
          ${rel}
        </div>
      </div>
    `);
    canvas.appendChild(node);
    node.querySelectorAll(".chip").forEach(c => {
      c.addEventListener("click", () => submitQuery(c.dataset.q));
    });
    applyLang();
    // Fire-and-forget: replace SVG with AI illustration when available.
    tryLoadAiImage(entry.query, node.querySelector(".illus-wrap"));
  }

  function renderNoMatch(q) {
    canvas.innerHTML = "";
    const node = el(`
      <div class="result">
        <div class="nomatch">
          <div data-zh="没找到匹配的主题:" data-en="No matching topic for:"></div>
          <h1 style="margin:8px 0 18px">「${escText(q)}」</h1>
          <div data-zh="试试这些:" data-en="Try these:"></div>
          <div class="related" style="justify-content:center;margin-top:14px;border:0;padding:0">
            ${payload.suggested_zh.map(s =>
              `<button class="chip" data-q="${escAttr(s)}">${escText(s)}</button>`).join("")}
          </div>
        </div>
      </div>
    `);
    canvas.appendChild(node);
    node.querySelectorAll(".chip").forEach(c => {
      c.addEventListener("click", () => submitQuery(c.dataset.q));
    });
    applyLang();
  }

  function clearSession() {
    session.length = 0; cursor = -1;
    renderEmpty();
  }

  // ── book mode (kept from original viewer) ─────────────────────────────
  let bookPages = [];
  let bookCurrent = 0;

  function initBook() {
    bookPages = [];
    bookPages.push({ kind:"cover" });
    payload.chapters.forEach(c => bookPages.push({ kind:"chapter", data:c }));
    bookPages.push({ kind:"timeline", data: payload.timeline });
    bookPages.push({ kind:"qr" });
    bookPages.push({ kind:"back" });
    bookEl.innerHTML = "";
    bookPages.forEach((p, i) => {
      const node = renderBookPage(p, i);
      node.style.zIndex = bookPages.length - i;
      const authorEl = document.createElement("div");
      authorEl.className = "author";
      authorEl.setAttribute("data-zh", "陈一鸣");
      authorEl.setAttribute("data-en", "Amanda Chen");
      node.appendChild(authorEl);
      bookEl.appendChild(node);
    });
    applyLang();
    updateFlipState();
  }

  function renderBookPage(p, i) {
    const folio = `<div class="folio">${i + 1} / ${bookPages.length}</div>`;
    if (p.kind === "cover") {
      return el(`
        <section class="page cover">
          <div class="seal-lg"><div>廣</div><div>府</div></div>
          <h1 data-zh="广州" data-en="Guangzhou"></h1>
          <div class="subtitle"
               data-zh="两千八百年 · 一座海上之城"
               data-en="Twenty-Eight Centuries · A City of the Sea"></div>
          <div class="footer"
               data-zh="点击翻页 · 或按方向键 · 按 L 切换语言"
               data-en="Click a page to flip · arrow keys · press L for language"></div>
          ${folio}
        </section>`);
    }
    if (p.kind === "chapter") {
      const c = p.data;
      return el(`
        <section class="page chapter" data-id="${c.id}">
          <div class="era"  data-zh="${escAttr(c.era_zh)}"   data-en="${escAttr(c.era_en)}"></div>
          <h1               data-zh="${escAttr(c.title_zh)}" data-en="${escAttr(c.title_en)}"></h1>
          <div class="page-content">
            <div class="body" data-zh="${escAttr(c.body_zh)}"  data-en="${escAttr(c.body_en)}"></div>
            <div class="illus">${renderIllustration(c.svg)}</div>
          </div>
          ${folio}
        </section>`);
    }
    if (p.kind === "timeline") {
      const items = p.data.map(t => `
        <li><b>${escText(t.year)}</b>
          <span data-zh="${escAttr(t.zh)}" data-en="${escAttr(t.en)}"></span></li>`).join("");
      return el(`
        <section class="page timeline">
          <div class="era" data-zh="时间线" data-en="Timeline"></div>
          <h1 data-zh="广州大事记" data-en="A Brief Chronology"></h1>
          <ol>${items}</ol>
          ${folio}
        </section>`);
    }
    if (p.kind === "qr") {
      return el(`
        <section class="page qr">
          <div class="qr-page-content">
            <div class="qr-item">
              <div class="qr-wrap">
                <img src="${payload.qr_svg}" alt="Project QR">
              </div>
              <small data-zh="扫码探索广州项目" data-en="Scan to explore Guangzhou Project"></small>
            </div>
            <div class="qr-item">
              <div class="qr-wrap">
                <img src="${payload.game_qr}" alt="Game QR">
              </div>
              <small data-zh="扫码体验互动游戏" data-en="Scan to play the game"></small>
            </div>
          </div>
          ${folio}
        </section>`);
    }
    return el(`
      <section class="page back">
        <div class="page-content" style="align-items: center; justify-content: center; height: 100%;">
          <div class="back-text" style="flex: 1; display: flex; flex-direction: column; gap: 16px; justify-content: center; height: 100%; min-width: 0;">
            <h1 data-zh="谢谢观赏" data-en="Thank You" style="font-size: 38px; margin: 0; color: var(--ink);"></h1>
            <p data-zh="广州的故事远不止于此。下次来，请去陈家祠看看砖雕，在沙面散步，到永庆坊喝一盅早茶，再去珠江夜游看小蛮腰。"
               data-en="There is far more to Guangzhou than these pages. Next time, drift through Chen Clan Hall's brick carvings, stroll Shamian, take yum cha in Yongqingfang, and see the Canton Tower light the Pearl River at night."
               style="font-size: 15.5px; line-height: 1.85; color: var(--ink-soft); text-align: justify; margin: 0;"></p>
          </div>
        </div>
        ${folio}
      </section>`);
  }

  function updateFlipState(){
    bookEl.querySelectorAll(".page").forEach((node, i) => {
      node.classList.toggle("flipped", i < bookCurrent);
      node.classList.toggle("active",  i === bookCurrent);
    });
    if (pageNumEl) pageNumEl.textContent = `${bookCurrent + 1} / ${bookPages.length}`;
  }

  function goBook(delta) {
    const target = Math.max(0, Math.min(bookPages.length - 1, bookCurrent + delta));
    if (target === bookCurrent) return;
    bookCurrent = target; updateFlipState();
  }
  function jumpBook(kind) {
    const idx = bookPages.findIndex(p => p.kind === kind);
    if (idx >= 0) { bookCurrent = idx; updateFlipState(); }
  }

  // ── wiring ────────────────────────────────────────────────────────────
  btnLang.addEventListener("click", () => { lang = (lang==="zh")?"en":"zh"; applyLang(); });
  btnMode.addEventListener("click", () => setMode(mode === "query" ? "book" : "query"));

  inputQ.addEventListener("keydown", e => {
    if (e.key === "Enter") { e.preventDefault(); submitQuery(inputQ.value); }
    else if (e.key === "Escape") { inputQ.value = ""; clearSession(); }
  });
  clearBtn.addEventListener("click", clearSession);

  if (btnPrev) btnPrev.addEventListener("click", () => goBook(-1));
  if (btnNext) btnNext.addEventListener("click", () => goBook(+1));

  document.addEventListener("keydown", e => {
    // global shortcuts that should work even when typing in the search box
    if (e.key === "f" || e.key === "F") {
      if (e.target === inputQ) return;
      e.preventDefault(); setMode(mode === "query" ? "book" : "query"); return;
    }
    if (e.key === "l" || e.key === "L") {
      if (e.target === inputQ) return;
      lang = (lang==="zh")?"en":"zh"; applyLang(); return;
    }
    if (e.target.closest("input,textarea")) return;
    if (mode === "book") {
      switch (e.key) {
        case "ArrowRight": case " ": e.preventDefault(); goBook(+1); break;
        case "ArrowLeft":            e.preventDefault(); goBook(-1); break;
        case "ArrowUp":              e.preventDefault(); bookCurrent = 0; updateFlipState(); break;
        case "ArrowDown":            e.preventDefault(); bookCurrent = bookPages.length - 1; updateFlipState(); break;
        case "t": case "T":          jumpBook("timeline"); break;
        case "q": case "Q":          jumpBook("qr"); break;
        case "Home":                 bookCurrent = 0; updateFlipState(); break;
        case "End":                  bookCurrent = bookPages.length - 1; updateFlipState(); break;
      }
    }
  });

  // Book click: right half = next, left = prev
  if (bookEl) bookEl.addEventListener("click", e => {
    const page = e.target.closest(".page");
    if (!page) return;
    const rect = page.getBoundingClientRect();
    if (e.clientX - rect.left > rect.width / 2) goBook(+1); else goBook(-1);
  });

  // ── boot ──────────────────────────────────────────────────────────────
  setMode("query");
  renderEmpty();
  inputQ.focus();
})();
"""
