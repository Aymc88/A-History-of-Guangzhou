#!/usr/bin/env python3
"""
广州历史 Flipbook — 一次性生成 12 页并烘入独立 HTML。

无需任何 API key — 图片使用本地后端免费生成 (HF FLUX)。
页面包含预撰写的高质量中文画面描述。

用法:
  python scripts/generate_flipbook.py
  python scripts/generate_flipbook.py --out my_flipbook.html
  python scripts/generate_flipbook.py --resume
"""

from __future__ import annotations

import argparse
import asyncio
import base64
import html
import json
import os
import re
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# 广州历史 12 主题
# ---------------------------------------------------------------------------

TOPICS: list[dict[str, str]] = [
    {
        "id": "nanyue",
        "title": "南越国宫署",
        "era": "公元前204年 — 南越国宫殿",
        "prompt_en": (
            "Ancient Nanyue Kingdom palace in Guangzhou, 200 BC. Rammed-earth "
            "terraces with red palace walls and golden roof tiles. Bronze ritual "
            "vessels in the courtyard. King in silk robes with court officials. "
            "Distant Pearl River and green Yuexiu Mountain. Warm golden sunset "
            "light. Chinese ink-wash watercolor style, isometric aerial view, "
            "masterpiece quality, exquisite architectural detail."
        ),
    },
    {
        "id": "silk-road",
        "title": "海上丝绸之路",
        "era": "唐宋时期 — 通商世界",
        "prompt_en": (
            "Tang dynasty Guangzhou port bustling with trading ships. Arabian "
            "dhows and Chinese junks on the Pearl River. Foreign merchants in "
            "colorful robes trading spices, ivory, silk and porcelain at the "
            "Fanfang district. Dock workers carrying cargo. The minaret of "
            "Huaisheng Mosque in the distance. Golden sunset on the water. "
            "Isometric watercolor illustration, warm earthy palette."
        ),
    },
    {
        "id": "guangxiao",
        "title": "光孝寺",
        "era": "1700年古刹 — 禅宗祖庭",
        "prompt_en": (
            "Guangxiao Temple's main hall, 1700-year-old Buddhist temple in "
            "Guangzhou. Two giant Bodhi trees casting dappled morning light. "
            "Incense smoke curling from bronze burners. Grey-robed monks walking "
            "around a stone pagoda. Green glazed tiles and red walls. Serene "
            "peaceful atmosphere. Chinese ink-wash watercolor, soft green and "
            "gold tones, masterpiece quality."
        ),
    },
    {
        "id": "zhenhai",
        "title": "镇海楼",
        "era": "明代洪武 — 五层楼望珠江",
        "prompt_en": (
            "The five-story Zhenhai Tower atop Yuexiu Hill in Guangzhou. "
            "Red sandstone walls with green glazed eaves. Ming dynasty cannons "
            "in front. A general in armor surveys the ancient walled city below. "
            "Traditional houses stretching to the Pearl River. Dramatic clouds "
            "at golden hour. Chinese watercolor painting, warm autumn tones, "
            "isometric perspective."
        ),
    },
    {
        "id": "thirteen-factories",
        "title": "十三行商馆",
        "era": "清代 — 一口通商 天子南库",
        "prompt_en": (
            "The Thirteen Factories along the Pearl River, circa 1800. "
            "Neoclassical Western trading houses with Chinese architectural "
            "details. Flags of trading nations flying. Tea chests and porcelain "
            "piles on the quay. Qing officials in mandarin robes, European "
            "merchants in tricorn hats. Morning mist on the river. Historical "
            "documentary illustration style, warm sepia tones."
        ),
    },
    {
        "id": "chen-clan",
        "title": "陈家祠",
        "era": "清代光绪 — 岭南建筑瑰宝",
        "prompt_en": (
            "Chen Clan Ancestral Hall interior, Guangzhou. Magnificent ridge "
            "beams adorned with Shiwan ceramic figurines telling stories. "
            "Intricate gold-lacquered wood carvings on columns. Exquisite brick "
            "carvings and painted murals. Moss-covered stone steps in the "
            "courtyard. Sunlight streaming through carved screen doors. Rich "
            "vermilion and gold palette, warm side lighting."
        ),
    },
    {
        "id": "sun-yat-sen",
        "title": "中山纪念堂",
        "era": "1931年 — 无柱穹顶的丰碑",
        "prompt_en": (
            "Sun Yat-sen Memorial Hall in Guangzhou, 1931. Massive octagonal "
            "azure blue glazed dome without a single interior column. White "
            "granite base. Bronze statue of Sun Yat-sen at entrance. Ancient "
            "trees and lush lawns. Citizens in 1930s attire walking past. "
            "Clear blue sky, bright open composition. Watercolor style, "
            "translucent light effects, masterpiece quality."
        ),
    },
    {
        "id": "uprising",
        "title": "广州起义",
        "era": "1927年 — 红色广州",
        "prompt_en": (
            "The Guangzhou Uprising of December 1927. Revolutionary soldiers "
            "with red armbands storming the city government building. "
            "Barricades in the streets made of sandbags. Red flags flying. "
            "Muzzle flashes and smoke in the night. Surrounding qilou buildings "
            "with bullet holes. Dramatic chiaroscuro lighting, flames "
            "illuminating the scene. Historical documentary painting style."
        ),
    },
    {
        "id": "qilou",
        "title": "骑楼老街",
        "era": "民国 — 南洋风 骑楼底商",
        "prompt_en": (
            "Bustling Qilou arcade street in 1930s Guangzhou. Nanyang-style "
            "shophouses with ornate facades, arched verandas, colourful "
            "signboards. Rickshaws, bicycles, pedestrians under the continuous "
            "covered walkway. Warm amber and teal palette. Cinematic street "
            "perspective looking down the arcade. Rich historical atmosphere, "
            "watercolor illustration style."
        ),
    },
    {
        "id": "dimsum",
        "title": "广府早茶",
        "era": "百年传承 — 一盅两件",
        "prompt_en": (
            "Traditional Cantonese tea house at morning rush hour in Guangzhou. "
            "Bamboo steamer baskets of har gow and siu mai stacked high. "
            "Old master pouring oolong tea with a long-spout copper kettle. "
            "Tea drinkers around round tables reading newspapers. Warm steam "
            "in the morning light filtering through lattice windows. Rich warm "
            "amber and gold palette. Cozy nostalgic atmosphere."
        ),
    },
    {
        "id": "pearl-river",
        "title": "珠江夜景",
        "era": "一江两岸 流光溢彩",
        "prompt_en": (
            "Night view of the Pearl River in modern Guangzhou. The Lie De "
            "Bridge spanning like a rainbow. Skyscrapers glittering with "
            "colourful lights. Canton Tower's neon reflection in the dark water. "
            "A tourist boat creating golden ripples. Deep blue to purple night "
            "sky gradient. Vibrant yet elegant nightscape. Watercolor style, "
            "nocturnal urban atmosphere."
        ),
    },
    {
        "id": "canton-tower",
        "title": "广州塔",
        "era": "2010年 — 城市新中轴",
        "prompt_en": (
            "The Canton Tower soaring above Guangzhou's skyline, 2010. "
            "Hyperboloid steel lattice with gradient LED lighting. Surrounded "
            "by Zhujiang New City skyscrapers. Green Huacheng Square park below "
            "with citizens strolling. Haixinsha island in the river. Twilight "
            "blue hour, deep purple to orange gradient sky. Modern Chinese "
            "watercolor style, grand urban composition."
        ),
    },
]

# ---------------------------------------------------------------------------
# 数据结构
# ---------------------------------------------------------------------------

@dataclass
class GeneratedPage:
    topic_id: str
    title: str
    era: str
    prompt_en: str
    image_data_url: str = ""
    success: bool = False
    error: str = ""


# ---------------------------------------------------------------------------
# 图片生成 — Pollinations.ai (完全免费, 无需 API key)
# ---------------------------------------------------------------------------

class PollinationsProvider:
    """调用 Pollinations.ai 的 flux 模型 (免费, 无 key 需求)."""

    BASE = "https://image.pollinations.ai/prompt"

    async def generate_image(self, topic: dict[str, str]) -> GeneratedPage:
        import httpx
        page = GeneratedPage(
            topic_id=topic["id"],
            title=topic["title"],
            era=topic["era"],
            prompt_en=topic["prompt_en"],
        )
        try:
            # Pollinations API: GET /prompt/{text} with query params
            url = f"{self.BASE}/{topic['prompt_en']}"
            params = {
                "width": 1024,
                "height": 768,
                "model": "flux",
                "nologo": "true",
                "seed": hash(topic["id"]) % 100000,
            }
            async with httpx.AsyncClient(timeout=120.0) as client:
                resp = await client.get(url, params=params)
                if resp.status_code != 200:
                    page.error = f"HTTP {resp.status_code}"
                    return page
                import base64
                b64 = base64.b64encode(resp.content).decode("ascii")
                page.image_data_url = f"data:image/jpeg;base64,{b64}"
                page.success = True
                print(f"  [{topic['id']}] OK ({len(resp.content)//1024}KB)")
        except Exception as e:
            page.error = str(e)
            print(f"  [{topic['id']}] EXCEPTION: {e}")
        return page


# ---------------------------------------------------------------------------
# HTML Flipbook
# ---------------------------------------------------------------------------

_HTML_HEADER = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>广州历史 — 两千两百年画卷</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    background: #1a1a1a;
    font-family: -apple-system, "Noto Serif SC", "Songti SC", serif;
    color: #e0d8c8;
    overflow-x: hidden;
  }
  .book {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 40px 20px 80px;
    gap: 60px;
    max-width: 1100px;
    margin: 0 auto;
  }
  .cover {
    text-align: center;
    padding: 80px 20px 40px;
    width: 100%;
  }
  .cover h1 {
    font-size: 3.2rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    color: #f0e6d0;
    margin-bottom: 20px;
    text-shadow: 0 2px 12px rgba(0,0,0,0.6);
  }
  .cover .subtitle {
    font-size: 1.1rem;
    color: #b8a88a;
    letter-spacing: 0.3em;
    border-top: 1px solid #b8a88a;
    border-bottom: 1px solid #b8a88a;
    display: inline-block;
    padding: 8px 24px;
  }
  .cover .intro {
    margin-top: 30px;
    color: #c8b898;
    font-size: 0.95rem;
    line-height: 1.8;
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
  }
  .page {
    width: 100%;
    background: #2a2824;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 8px 40px rgba(0,0,0,0.5);
    transition: transform 0.2s;
  }
  .page:hover { transform: translateY(-4px); }
  .page-image {
    width: 100%;
    display: block;
    aspect-ratio: 4/3;
    object-fit: cover;
    background: #333;
  }
  .page-content {
    padding: 28px 32px;
  }
  .page-title {
    font-size: 1.6rem;
    font-weight: 600;
    color: #f0e6d0;
    margin-bottom: 6px;
  }
  .page-era {
    font-size: 0.85rem;
    color: #a09070;
    margin-bottom: 14px;
  }
  .nav-bar {
    position: fixed;
    bottom: 0; left: 0; right: 0;
    background: rgba(26,26,26,0.92);
    backdrop-filter: blur(8px);
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 12px;
    padding: 12px 20px;
    border-top: 1px solid #333;
    z-index: 100;
    flex-wrap: wrap;
  }
  .nav-bar a {
    color: #b8a88a;
    text-decoration: none;
    font-size: 0.8rem;
    padding: 4px 10px;
    border-radius: 4px;
    transition: background 0.15s;
  }
  .nav-bar a:hover { background: #333; color: #f0e6d0; }
  .nav-bar .nav-prev,
  .nav-bar .nav-next {
    font-weight: 600;
    font-size: 0.9rem;
    padding: 6px 16px;
    background: #3a3530;
    border-radius: 6px;
  }
  .nav-bar .nav-prev:hover,
  .nav-bar .nav-next:hover { background: #4a4540; }
  @media (max-width: 600px) {
    .cover h1 { font-size: 2rem; }
    .page-content { padding: 16px 18px; }
    .page-title { font-size: 1.2rem; }
  }
  @keyframes scrollHint {
    0%, 100% { opacity: 0.3; transform: translateY(0); }
    50% { opacity: 1; transform: translateY(6px); }
  }
  .scroll-hint {
    text-align: center;
    color: #666;
    font-size: 0.8rem;
    margin-top: -20px;
    animation: scrollHint 2s ease-in-out infinite;
  }
</style>
</head>
<body>
<div class="book">
  <div class="cover">
    <h1>广州历史</h1>
    <div class="subtitle">两千两百年画卷</div>
    <p class="intro">
      从南越王宫到广州塔，跨越 2200 年的城市记忆。<br>
      十二幅画，十二段故事。
    </p>
  </div>
"""

_HTML_FOOTER = r"""  <div class="cover" style="padding:40px 20px 80px;">
    <p style="color:#666; font-size:0.85rem;">PLACEHOLDER_DATE</p>
  </div>
</div>
<div class="nav-bar" id="navbar">
  <a href="#" class="nav-prev" id="navPrev">◀ 上一页</a>
  PLACEHOLDER_NAV
  <a href="#" class="nav-next" id="navNext">下一页 ▶</a>
</div>
<script>
(function() {
  var pages = document.querySelectorAll('.page');
  var navPrev = document.getElementById('navPrev');
  var navNext = document.getElementById('navNext');
  var current = -1;
  function scrollToPage(idx) {
    if (idx < 0 || idx >= pages.length) return;
    current = idx;
    pages[idx].scrollIntoView({ behavior: 'smooth', block: 'start' });
    setTimeout(function() { window.scrollBy(0, -80); }, 300);
  }
  navPrev.addEventListener('click', function(e) {
    e.preventDefault();
    if (current > 0) scrollToPage(current - 1);
  });
  navNext.addEventListener('click', function(e) {
    e.preventDefault();
    if (current < pages.length - 1) scrollToPage(current + 1);
  });
  var observer = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        current = Array.prototype.indexOf.call(pages, entry.target);
      }
    });
  }, { threshold: 0.3 });
  pages.forEach(function(p) { observer.observe(p); });
})();
</script>
</body>
</html>"""


def build_flipbook(pages: list[GeneratedPage]) -> str:
    pages_html = ""
    nav_links = ""
    for i, p in enumerate(pages):
        img_src = p.image_data_url or ""
        pages_html += (
            '<div class="page" id="page-%d">\n'
            '    <img class="page-image" src="%s" alt="%s" loading="lazy">\n'
            '    <div class="page-content">\n'
            '      <div class="page-title">%s</div>\n'
            '      <div class="page-era">%s</div>\n'
            '    </div>\n'
            '  </div>'
        ) % (i, img_src, html.escape(p.title),
             html.escape(p.title), html.escape(p.era))
        nav_links += (
            '<a href="#page-%d" onclick="scrollToPage(%d);return false;">%s</a>'
        ) % (i, i, html.escape(p.title))

    return _HTML_HEADER + pages_html + _HTML_FOOTER.replace(
        "PLACEHOLDER_NAV", nav_links
    ).replace(
        "PLACEHOLDER_DATE", time.strftime("Generated %Y-%m-%d")
    )


# ---------------------------------------------------------------------------
# 进度保存 / 断点续传
# ---------------------------------------------------------------------------

STATE_FILE = ".generate_flipbook_state.json"


def _load_state() -> dict[str, Any]:
    sp = Path(STATE_FILE)
    return json.loads(sp.read_text()) if sp.exists() else {}


def _save_state(state: dict[str, Any]) -> None:
    Path(STATE_FILE).write_text(json.dumps(state, indent=2, ensure_ascii=False))


def _page_to_dict(p: GeneratedPage) -> dict[str, Any]:
    return {
        "topic_id": p.topic_id,
        "title": p.title,
        "era": p.era,
        "prompt_en": p.prompt_en,
        "image_data_url": p.image_data_url,
        "success": p.success,
        "error": p.error,
    }


def _page_from_dict(d: dict[str, Any]) -> GeneratedPage:
    p = GeneratedPage(
        topic_id=d["topic_id"],
        title=d["title"],
        era=d["era"],
        prompt_en=d.get("prompt_en", ""),
    )
    p.image_data_url = d.get("image_data_url", "")
    p.success = d.get("success", False)
    p.error = d.get("error", "")
    return p


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

async def main() -> None:
    parser = argparse.ArgumentParser(description="广州历史 Flipbook 生成器")
    parser.add_argument(
        "--out", default="guangzhou_flipbook.html",
        help="输出 HTML 文件路径",
    )
    parser.add_argument(
        "--resume", action="store_true",
        help="断点续传 (跳过已成功生成的页面)",
    )
    parser.add_argument(
        "--topics", type=int, default=12,
        help="生成前 N 个主题 (默认 12)",
    )
    args = parser.parse_args()

    provider = PollinationsProvider()
    state = _load_state() if args.resume else {}
    existing: dict[str, GeneratedPage] = {}
    for d in state.get("pages", []):
        p = _page_from_dict(d)
        if p.success:
            existing[p.topic_id] = p

    topics = TOPICS[:args.topics]
    session_id = state.get("session_id", f"batch-{uuid.uuid4().hex[:12]}")

    if args.resume and existing:
        print(f"续传: 已有 {len(existing)}/{len(topics)} 页, 继续生成剩余...")
        topics_to_gen = [t for t in topics if t["id"] not in existing]
    else:
        topics_to_gen = topics

    if not topics_to_gen:
        print("所有页面已完成!")
        pages = [existing[t["id"]] for t in topics]
    else:
        pages: list[GeneratedPage | None] = [
            existing.get(t["id"]) for t in topics
        ]
        pending = [i for i, p in enumerate(pages) if p is None]

        for idx in pending:
            topic = topics[idx]
            print(f"[{idx + 1}/{len(topics)}] {topic['title']} ({topic['era']})")
            p = await provider.generate_image(topic)
            pages[idx] = p
            state["session_id"] = session_id
            state["pages"] = [_page_to_dict(x) for x in pages if x is not None]
            _save_state(state)
            if not p.success:
                print(f"  FAIL: {p.error}")
            print()

        pages = [p for p in pages if p is not None]

    n_ok = sum(1 for p in pages if p.success)
    n_err = sum(1 for p in pages if not p.success)
    print(f"\n完成: {n_ok} 页成功, {n_err} 页失败")

    if n_ok == 0:
        print("没有成功页面.")
        sys.exit(1)

    html_out = build_flipbook(pages)
    out_path = Path(args.out)
    out_path.write_text(html_out, encoding="utf-8")
    print(f"Flipbook: {out_path.resolve()}")
    if n_err > 0:
        print(f"\n失败:")
        for p in pages:
            if not p.success:
                print(f"  - {p.title}: {p.error[:100]}")


if __name__ == "__main__":
    asyncio.run(main())
