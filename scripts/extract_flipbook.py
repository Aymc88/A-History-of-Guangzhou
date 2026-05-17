#!/usr/bin/env python3
"""Extract Guangzhou viewer pages → 独立 flipbook HTML (SVG as data URIs)."""

import json
import re
import urllib.request
import sys
import textwrap

data = urllib.request.urlopen("http://localhost:8964/").read().decode("utf-8")
m = re.search(
    r'<script id="payload" type="application/json">(.*?)</script>', data, re.DOTALL
)
if not m:
    print("No payload found!")
    sys.exit(1)

payload = json.loads(m.group(1))
chapters = payload.get("chapters", [])

# Also check if the viewer's own HTML has pre-rendered pages
# Let's extract pages from the viewer's book mode
# The pages are in the DOM inside #book

PAGE_TPL = """
  <div class="page" id="page-{i}">
    <div class="page-illus">
      {svg_embed}
    </div>
    <div class="page-body">
      <div class="page-era">{era}</div>
      <h2 class="page-title">{title}</h2>
      <p class="page-text">{body}</p>
    </div>
  </div>"""

pages_html = ""
nav_links = ""
for i, ch in enumerate(chapters):
    era = ch.get("era_zh", "")
    title = ch.get("title_zh", "")
    body = ch.get("body_zh", "")
    svg = ch.get("svg", "")

    if len(svg) < 500:
        # Placeholder when no SVG available
        svg_embed = '<div class="svg-placeholder"></div>'
    else:
        # Embed SVG inline.  Prefix all IDs so gradient/clip refs don't collide
        # when multiple SVGs share the same HTML page.
        prefix = "s%d-" % i
        def _prefix_ids(m):
            return m.group(0).replace('id="', 'id="' + prefix).replace('url(#', 'url(#' + prefix)
        svg = re.sub(r'\b(id="[^"]+")|url\(#[^)]+\)', _prefix_ids, svg)
        svg = svg.replace('aria-hidden="true"', '').replace('<svg', '<svg width="100%"')
        svg_embed = svg

    pages_html += PAGE_TPL.format(
        i=i, svg_embed=svg_embed, title=title, era=era, body=body
    )
    nav_links += '<a href="#page-%d">%s</a>' % (i, title)

TEMPLATE_HEAD = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>广州两千两百年 · Guangzhou History</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    background: linear-gradient(180deg, #2b1d10 0%, #1b1108 100%);
    font-family: "Noto Serif SC", "Songti SC", serif;
    color: #3a2a18;
    padding: 20px;
    min-height: 100vh;
  }
  .book {
    max-width: 900px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    gap: 40px;
    padding-bottom: 80px;
  }
  .cover {
    text-align: center;
    padding: 60px 20px;
  }
  .cover h1 {
    font-size: 2.8rem;
    color: #f3e7cc;
    letter-spacing: 0.15em;
    margin-bottom: 10px;
  }
  .cover .sub {
    color: #c9a35a;
    font-size: 1rem;
    letter-spacing: 0.3em;
    border-top: 1px solid #c9a35a;
    border-bottom: 1px solid #c9a35a;
    display: inline-block;
    padding: 6px 20px;
  }
  .page {
    background: #f3e7cc;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(0,0,0,0.5), 0 2px 0 #e0cd9c inset;
  }
  .page-illus {
    width: 100%;
    min-height: 200px;
    background: #e8dcc0;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .page-illus svg {
    width: 100%;
    height: auto;
    display: block;
  }
  .svg-placeholder {
    font-size: 4rem;
    padding: 60px 0;
    opacity: 0.4;
  }
  .page-body {
    padding: 28px 32px;
  }
  .page-era {
    font-size: 0.8rem;
    color: #b85c2f;
    letter-spacing: 0.1em;
    margin-bottom: 4px;
  }
  .page-title {
    font-size: 1.5rem;
    color: #2b1d10;
    margin-bottom: 14px;
    line-height: 1.3;
  }
  .page-text {
    font-size: 0.95rem;
    line-height: 1.9;
    color: #54402a;
    text-indent: 2em;
  }
  .nav-bar {
    position: fixed;
    bottom: 0; left: 0; right: 0;
    background: rgba(27,17,8,0.92);
    backdrop-filter: blur(8px);
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 8px;
    padding: 10px 16px;
    border-top: 1px solid #4a3622;
    z-index: 100;
    flex-wrap: wrap;
  }
  .nav-bar a {
    color: #c9a35a;
    text-decoration: none;
    font-size: 0.75rem;
    padding: 4px 8px;
    border-radius: 4px;
    white-space: nowrap;
  }
  .nav-bar a:hover { background: #3a2814; color: #f3e7cc; }
  .nav-bar .nav-prev,
  .nav-bar .nav-next {
    font-weight: 600;
    padding: 6px 14px;
    background: #3a2814;
    border-radius: 6px;
    color: #f3e7cc;
  }
  @media (max-width: 600px) {
    .cover h1 { font-size: 1.8rem; }
    .page-body { padding: 18px; }
    .page-title { font-size: 1.2rem; }
    .page-text { font-size: 0.85rem; }
  }
</style>
</head>
<body>
<div class="book">
  <div class="cover">
    <h1>广州历史</h1>
    <div class="sub">两千两百年画卷</div>
  </div>
"""

TEMPLATE_TAIL = """</div>
<div class="nav-bar">
  <a href="#" class="nav-prev" id="navPrev">◀ 上一页</a>
  NAV_PLACEHOLDER
  <a href="#" class="nav-next" id="navNext">下一页 ▶</a>
</div>
<script>
(function() {
  var pages = document.querySelectorAll('.page');
  var prev = document.getElementById('navPrev');
  var next = document.getElementById('navNext');
  var cur = -1;
  function go(i) {
    if (i < 0 || i >= pages.length) return;
    cur = i;
    pages[i].scrollIntoView({ behavior: 'smooth', block: 'start' });
    setTimeout(function() { window.scrollBy(0, -60); }, 400);
  }
  prev.addEventListener('click', function(e) { e.preventDefault(); go(cur-1); });
  next.addEventListener('click', function(e) { e.preventDefault(); go(cur+1); });
  var obs = new IntersectionObserver(function(entries) {
    entries.forEach(function(e) {
      if (e.isIntersecting) cur = Array.prototype.indexOf.call(pages, e.target);
    });
  }, { threshold: 0.3 });
  pages.forEach(function(p) { obs.observe(p); });
  document.querySelectorAll('.nav-bar a[href^="#"]').forEach(function(a) {
    a.addEventListener('click', function(e) {
      e.preventDefault();
      var el = document.getElementById(this.getAttribute('href').slice(1));
      if (el) go(Array.prototype.indexOf.call(pages, el));
    });
  });
  if (pages.length) go(0);
})();
</script>
</body>
</html>"""

html_out = TEMPLATE_HEAD + pages_html + TEMPLATE_TAIL.replace(
    "NAV_PLACEHOLDER", nav_links
)

with open("guangzhou_flipbook.html", "w", encoding="utf-8") as f:
    f.write(html_out)

svg_count = sum(1 for ch in chapters if len(ch.get("svg", "")) > 500)
print(f"生成成功: guangzhou_flipbook.html ({len(html_out)//1024}KB)")
print(f"页数: {len(chapters)} (含 {svg_count} 幅 SVG 插图)")
print(f"缺失插图: {len(chapters) - svg_count} 页")
