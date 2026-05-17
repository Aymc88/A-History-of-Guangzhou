# Guangzhou Flipbook Fork

把 [`eren23/openflipbook`](https://github.com/eren23/openflipbook) 改造成「广州 · 城市记忆」翻页书的覆盖层。本目录**不复制上游代码**，只提供：

- 一个 `setup.sh`：在你 Mac 上克隆上游仓库
- 一个 `apply-overlay.sh`：把广州主题的 prompt / 主题 CSS / env 模板叠加上去
- `overlay/`：所有自写的覆盖文件

上游 fork 之后，所有页面（图像、标题、标签）都会被引导到广州主题。

A drop-in overlay that turns upstream [`eren23/openflipbook`](https://github.com/eren23/openflipbook) into a "Guangzhou · Memory of a City" flipbook. This folder **does not redistribute upstream code** — it only ships:

- `setup.sh` — clones upstream on your Mac
- `apply-overlay.sh` — lays the Guangzhou prompt / theme CSS / env templates on top
- `overlay/` — every file we author ourselves

After applying, every generated page (image, title, callouts) is biased toward Guangzhou.

---

## 目录 / Layout

```
guangzhou-flipbook-fork/
├── README.md                       # this file
├── setup.sh                        # clone + apply
├── apply-overlay.sh                # idempotent re-apply
└── overlay/
    ├── env/
    │   ├── modal-backend.env.example
    │   └── web.env.local.example
    ├── prompts/
    │   ├── guangzhou-system.zh.md  # page-planner system prompt (CN)
    │   └── guangzhou-system.en.md  # page-planner system prompt (EN)
    ├── theme/
    │   └── guangzhou.css           # Lingnan palette + fonts override
    └── seeds/
        └── seed-queries.json       # default + chip suggestions + graph hints
```

---

## 前置依赖 / Prerequisites

| 工具 / Tool | 用途 / Purpose | 装一下 / Install |
| --- | --- | --- |
| `git`     | 拉上游 / clone upstream            | 系统自带 / built-in |
| `docker`  | 一键 `compose up` / one-shot up   | Docker Desktop |
| `pnpm`    | 前端依赖 / Next.js deps           | `brew install pnpm` |
| `uv`      | Python 虚拟环境 / venv            | `brew install uv` |
| `modal`   | 可选 · 部署到 Modal / optional    | `brew install modal-cli` |

你还需要这些 API 密钥 / You'll also need API keys:

- **`FAL_KEY`** — 图像 / 视频生成（[fal.ai](https://fal.ai/dashboard/keys)）
- **`OPENROUTER_API_KEY`** — 规划器 LLM + 视觉点击解析（[openrouter.ai](https://openrouter.ai/keys)）
- **Cloudflare R2**（任何 S3 兼容存储也行）— 存生成的图像
- **MongoDB**——`docker compose` 默认会拉一个，本地用直接留默认即可

---

## 一键安装 / One-shot install

```bash
cd "guangzhou-flipbook-fork"
./setup.sh
```

这会：

1. 检查 `git / docker / pnpm / uv / modal` 是否存在（缺的会警告但不致命）
2. `git clone https://github.com/eren23/openflipbook ./openflipbook`
3. 跑 `apply-overlay.sh`，把覆盖层落到上游里
4. 打印你要手动填的密钥位置

What it does:

1. Checks for `git / docker / pnpm / uv / modal` (warns if missing, not fatal)
2. `git clone https://github.com/eren23/openflipbook ./openflipbook`
3. Runs `apply-overlay.sh` to lay the overlay onto upstream
4. Prints exactly which keys you have to fill in by hand

> 上游版权归 `eren23/openflipbook` 维护者；请遵循其 LICENSE。本覆盖层（`overlay/` 下所有文件）由本项目原创，可自由按 MIT 使用。
>
> Upstream is copyrighted to its maintainer; follow its LICENSE. The overlay (everything under `overlay/`) is original to this project, MIT-licensed.

---

## 装完之后的三个集成点 / Three integration hooks

`apply-overlay.sh` 是**纯增量**的——它只丢新文件、从不改上游源代码。所以装完后你要在上游里手动加三处「引用」，把我们的覆盖层接上：

`apply-overlay.sh` is purely additive — it drops new files, it never edits upstream source. After applying, add these three references in upstream code:

### 1. 前端引主题 CSS / Frontend imports theme CSS

`apps/web/src/app/layout.tsx`（或等价的 root layout）顶部：

```tsx
import "../../public/themes/guangzhou.css";
```

### 2. 空态拉种子查询 / Empty state loads seed chips

在你的搜索空态组件里：

```ts
useEffect(() => {
  fetch("/themes/seed-queries.json")
    .then(r => r.json())
    .then(s => setSeeds(s.suggestions_zh));
}, []);
```

### 3. 规划器读系统 prompt / Page planner reads our system prompt

`apps/modal-backend` 里那段调 OpenRouter 规划下一页的代码：

```python
import os, pathlib
SYS = pathlib.Path(os.environ["GUANGZHOU_SYSTEM_PROMPT_PATH"]).read_text()

messages = [{"role": "system", "content": SYS}, *user_messages]
```

就这三处。其它都是 drop-in。

---

## 启动 / Run

```bash
cd ./openflipbook
docker compose up -d --build
open http://localhost:3000/play
```

如果 mongo / backend 不在 compose 里，按上游 README 里说的命令逐个启。

If mongo / backend aren't part of the compose file in your checkout, fall back to upstream README's per-service start commands.

---

## 升级 / Upgrading

上游有新版？

```bash
cd ./openflipbook && git pull
cd .. && ./apply-overlay.sh
```

`apply-overlay.sh` 是幂等的——重跑只会覆盖我们自己的 overlay 文件，不会动你已经填好的 `.env`（已存在时会跳过，并额外写一个 `.guangzhou.example` 供你 diff）。

`apply-overlay.sh` is idempotent. Re-running only re-stamps our own overlay; if you've filled in `.env`, it stays untouched (a `.guangzhou.example` sibling is written so you can diff).

---

## 卸载 / Rollback

```bash
rm -rf ./openflipbook
```

完事。我们的覆盖层留在 `guangzhou-flipbook-fork/overlay/`，下次想换个目录重装直接 `./setup.sh /some/other/path` 即可。

That's it. Our overlay stays in `guangzhou-flipbook-fork/overlay/`, so re-installing somewhere else is just `./setup.sh /some/other/path`.

---

## 跟我们的 MCP 服务器的关系 / Relationship to the MCP server

本项目还有一个独立的 **MCP 服务器** (`../guangzhou_history_mcp/`)——纯本地、零依赖、能直接给 Claude Desktop 用，包含 12 个广州主题的精校内容。两者互补：

- **MCP server**：精校文本 + 手绘 SVG，给 Claude 这种 LLM 当工具用，离线可跑
- **Fork**：上游全套基础设施 + AI 图像生成，体验 = 浏览器里点击翻页探索

This project also ships a standalone **MCP server** (`../guangzhou_history_mcp/`) — fully local, zero deps, plugs into Claude Desktop, with 12 hand-curated Guangzhou topics. The two are complementary:

- **MCP server** — curated text + hand-drawn SVGs, served as tools to an LLM, runs offline
- **Fork** — full upstream stack + AI image generation, experience = click-to-explore in a browser
