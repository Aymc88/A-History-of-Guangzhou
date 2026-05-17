# 广州历史 MCP · Guangzhou History MCP

一个借鉴 [eren23/openflipbook](https://github.com/eren23/openflipbook) 视觉概念的
**Model Context Protocol** 服务器，专门讲述广州两千两百年的故事。
内置一本**岭南风、中英双语、可键盘翻页**的电子翻页书。

A Model Context Protocol server about the 2,200-year history of **Guangzhou** (廣州),
inspired by the visual concept of [openflipbook](https://github.com/eren23/openflipbook).
Ships with a **bilingual, Lingnan-styled, keyboard-flippable** HTML flipbook viewer.

---

## 这个 MCP 提供什么 / What this MCP gives you

工具 (Tools)

| Tool | 作用 (Chinese) | Purpose (English) |
| --- | --- | --- |
| `list_chapters(lang)` | 列出 6 个章节的 id / 朝代 / 标题 | List the 6 chapters: id, era, title |
| `get_chapter(chapter_id, lang)` | 读取某章正文 | Read one chapter's full body |
| `search_history(query, lang)` | 跨中英文子串搜索 | Substring-search every chapter (both languages) |
| `query_topic(query, lang)` | 把自由查询(如「广州塔」「Whampoa」)解析为一张插画卡片 | Resolve a free-text query into a single illustrated card |
| `list_topics(lang)` | 列出 12 个可识别的主题及其别名 | List the 12 recognised topics and their aliases |
| `get_timeline(lang)` | 返回 15 条大事年表 | Return a 15-row chronology |
| `open_flipbook(out_path?, open_in_browser?)` | 生成查询书 HTML 并打开浏览器 | Render the viewer to disk and open it |

`lang` 取值为 `"zh"` 或 `"en"`，默认 `"zh"`。
`lang` accepts `"zh"` or `"en"`, default `"zh"`.

资源 (Resources)

- `guangzhou://about` — 一段元信息摘要。

---

## 查看器：两种模式 / The viewer: two modes

`open_flipbook` 会落地一个**完全自包含的 HTML 文件**（无外链 JS / CSS / 图片），里面同时包含两种模式：

`open_flipbook` writes a **fully self-contained HTML file** — no external JS / CSS / image deps — bundling two modes in one viewer:

### 1. 查询模式（默认 / default）· Query mode

借鉴 `flipbook.page` 的搜索栏交互：顶部一条搜索条，下方一个奶油色「窗口」画布。输入主题（例如「广州塔」「Whampoa」「十三行」「早茶」），即时渲染出一张带年代标签、SVG 插图、要点便笺、相关主题胶囊的卡片，并把每次查询作为面包屑保留在会话中。

Inspired by `flipbook.page`'s search-bar UX. Type a topic in the address bar
(e.g. "Canton Tower", "Whampoa", "Shamian", "yum cha") and the viewer renders
an illustrated card: era chip, title, SVG vignette, factoid highlights, and
related-topic chips. Every query stays in the breadcrumb session so you can
flip back and forth.

可识别主题（12 个 · 各带 4–7 个中英别名）：南越王 / 任嚣 / 海上丝绸之路 / 十三行 / 伍秉鉴 (Howqua) / 沙面 / 西关大屋 · 骑楼 / 黄埔军校 / 中山纪念堂 / 广交会 / 广州塔 · 小蛮腰 / 早茶。

Recognised topics (12, each with 4–7 zh/en aliases): Nanyue King / Ren Xiao /
Maritime Silk Road / Thirteen Hongs / Howqua / Shamian / Xiguan & Qilou /
Whampoa Academy / Sun Yat-sen Memorial Hall / Canton Fair / Canton Tower /
Yum Cha.

### 2. 翻页书模式 · Flipbook mode

按 `F` 切换。岭南风的真翻页书：封面 → 6 章 → 大事年表 → 封底，CSS 3D `rotateY` 翻页动画，每章一幅手绘 SVG 岭南插画（怀圣寺光塔、十三行洋行旗、沙面拱廊、中山纪念堂、小蛮腰…）。

Press `F` to switch. The Lingnan-styled page-turning book: cover → 6 chapters
→ timeline → back cover, with realistic CSS 3D `rotateY` page-flip animation
and a hand-drawn SVG per chapter.

### 键盘 / Keyboard

| Key | 查询模式 / Query | 翻页模式 / Book |
| --- | --- | --- |
| `Enter` | 提交查询 / submit | — |
| `Esc` | 清空会话 / clear session | — |
| `F` | 切到翻页模式 / to book | 回到查询 / back to query |
| `L` | 中 ↔ EN | 中 ↔ EN |
| `← / →` | — | 翻页 / flip |
| `Space` | — | 下一页 / next |
| `T` | — | 跳到时间线 / timeline |
| `Home` / `End` | — | 封面 / 封底 |

---

## 章节 / Chapters

1. **任嚣筑城,番禺立基** (秦汉) · *The Founding of Panyu (Pre-Qin · 214 BCE)*
2. **蕃坊云集,海丝起点** (唐宋) · *Lighthouse of the Maritime Silk Road (Tang–Song)*
3. **一口通商,十三行天下** (清 1757-1842) · *One Port, Thirteen Hongs (Qing)*
4. **火烧十三行,沙面立租界** (晚清) · *The Hongs Burn, Shamian Rises (Late Qing)*
5. **革命策源,黄埔扬帆** (民国) · *Cradle of Revolution, Whampoa Sets Sail (Republican)*
6. **春风南来,千年商都新生** (改革开放) · *Southern Spring (Reform Era · 1978-)*

---

## 安装 / Install

```bash
# 推荐使用 uv (https://github.com/astral-sh/uv)
# We recommend uv: https://github.com/astral-sh/uv
git clone <this repo, or just point uvx at the local folder>
cd "A History of Guangzhou"
uv pip install -e .
```

或者用普通 pip / Or with plain pip:

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -e .
```

依赖只有一个：`mcp>=1.2.0` (官方 Python SDK).
The only dependency is `mcp>=1.2.0` (the official Python SDK).

---

## 运行 / Run

直接跑（用 stdio 传输）:
Run directly (stdio transport):

```bash
python -m guangzhou_history_mcp
# or, after `pip install -e .`:
guangzhou-history-mcp
```

---

## 接入 Claude Desktop / Wire into Claude Desktop

编辑 `claude_desktop_config.json`（macOS 在 `~/Library/Application Support/Claude/`，
Windows 在 `%APPDATA%\Claude\`），加入：

Edit `claude_desktop_config.json` (macOS: `~/Library/Application Support/Claude/`,
Windows: `%APPDATA%\Claude\`) and add:

```json
{
  "mcpServers": {
    "guangzhou-history": {
      "command": "uvx",
      "args": [
        "--from",
        "/ABSOLUTE/PATH/TO/A History of Guangzhou",
        "guangzhou-history-mcp"
      ]
    }
  }
}
```

或者，如果你已经 `pip install -e .` 到某个虚拟环境：
Alternatively, if you've already installed into a venv:

```json
{
  "mcpServers": {
    "guangzhou-history": {
      "command": "/ABS/PATH/.venv/bin/python",
      "args": ["-m", "guangzhou_history_mcp"]
    }
  }
}
```

重启 Claude Desktop，就能在工具列表里看到 `guangzhou-history` 这五个 tool。
试着问："**用 guangzhou-history 打开广州历史翻页书**"。

Restart Claude Desktop and the five tools will appear under `guangzhou-history`.
Try: "**Open the Guangzhou history flipbook using guangzhou-history.**"

---

## 用 MCP Inspector 测试 / Test with the MCP Inspector

```bash
npx @modelcontextprotocol/inspector python -m guangzhou_history_mcp
```

---

## 与 openflipbook 的关系 / Relation to openflipbook

[openflipbook](https://github.com/eren23/openflipbook) 是一个用 AI 图像模型作为 UI 的
开源项目（每一页都是 VLM + 视频模型实时生成的画面）。本项目**只借鉴它的「翻页书 = UI」概念**，
并将其落到一个具体的人文主题——**广州历史**——之上：

- 我们用**手绘 SVG + 岭南纹样**替代生成式图像（无需 GPU、无依赖、可离线）。
- 我们把它包装成一个**MCP 服务器**，让 Claude 等模型可以查询数据 *并*打开可视化。

[openflipbook](https://github.com/eren23/openflipbook) is an open-source clone of
flipbook.page where every page is an AI-generated image. This project borrows only
its **page-as-UI** idea and applies it to a concrete subject — **the history of
Guangzhou**:

- We replace the generative imagery with **hand-drawn SVG in a Lingnan idiom**
  (no GPUs, no external services, fully offline).
- We wrap the whole thing in an **MCP server**, so Claude can query the data
  *and* open the visualization on demand.

---

## License

MIT.
