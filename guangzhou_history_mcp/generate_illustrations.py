"""
One-shot AI illustration generator for the Guangzhou flipbook.

Walks every TOPIC in ``content.py`` and asks an image-generation provider
to render a single 16:9 illustration in the "isometric hand-painted
watercolor infographic on rice paper" style — the same look as the
flipbook.page reference image the project is chasing. Each result is
written to ``assets/illustrations/<topic_id>.png``. The viewer picks
those PNGs up automatically (see ``svg_library.illustration_for``).

Three providers are supported, all callable from stdlib (no `httpx`):

    openrouter   Google Gemini 2.5 Flash Image via OpenRouter.
                 Best style match to the flipbook.page reference. ~$0.04/img.
                 Needs OPENROUTER_API_KEY.

    fal          Flux 1.1 [pro] via fal.ai. Slightly more photographic
                 than the reference but very high fidelity. ~$0.05/img.
                 Needs FAL_KEY.

    stub         Writes a tiny placeholder PNG per topic so the rest of
                 the pipeline can be verified end-to-end without an API
                 key or network. Useful in tests / sandboxes.

CLI examples:

    # See the prompts that would be sent, without calling anything
    python -m guangzhou_history_mcp.generate_illustrations --list

    # Generate everything with stub provider (instant, free, ugly)
    python -m guangzhou_history_mcp.generate_illustrations --provider stub

    # Real generation via OpenRouter (Gemini Image)
    OPENROUTER_API_KEY=sk-or-... \\
      python -m guangzhou_history_mcp.generate_illustrations --provider openrouter

    # Real generation via fal.ai (Flux Pro)
    FAL_KEY=... \\
      python -m guangzhou_history_mcp.generate_illustrations --provider fal

    # Re-generate only a few topics
    python -m guangzhou_history_mcp.generate_illustrations --provider openrouter \\
        --only canton-tower howqua yum-cha

    # Force-overwrite even when a PNG already exists
    python -m guangzhou_history_mcp.generate_illustrations --provider openrouter --force

After the script finishes, regenerate the HTML so the new PNGs are baked
in as data: URLs:

    python -c "from guangzhou_history_mcp.viewer import build_html; \\
               import pathlib; pathlib.Path('flipbook.html').write_text(build_html(), encoding='utf-8')"

…or just call the ``open_flipbook`` MCP tool again.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path

from .content import TOPICS


# =========================================================================
# Prompt library — all 12 topics
# =========================================================================

# One consistent style preamble. Keep image-model-friendly English only;
# avoid Chinese characters in the prompt because every image model on the
# market still mangles them. The negative phrasing at the end is what
# actually keeps text artefacts (like the "san-rindiny ramnts" gibberish
# in the flipbook.page reference) off the canvas.
STYLE = (
    "Isometric hand-painted watercolor infographic illustration on textured "
    "cream rice paper background. Bird's-eye three-quarter perspective. "
    "Soft natural daylight. Muted earthy Lingnan palette: terracotta red, "
    "jade green, antique gold, ink black and bone white. Fine sepia ink "
    "linework with delicate watercolor wash and subtle paper grain. "
    "Intricate architectural detail. Banyan trees, kapok flowers and "
    "subtropical vegetation where they fit. Clean composition with one "
    "central subject and a few supporting elements. "
    "STRICTLY no text of any kind in the image: no captions, no labels, "
    "no watermarks, no signage, no Chinese characters, no English words, "
    "no numerals — the bubble labels are added separately afterwards."
)


# Subject lines — what goes in the middle of the page. Original prose;
# every detail is something we can actually point a viewer at when the
# image arrives.
SUBJECTS: dict[str, str] = {
    "nanyue-king": (
        "An ancient Han-dynasty Chinese royal capital at dawn: a fortified "
        "palace complex of the Nanyue Kingdom near 200 BCE in southern "
        "China. Crenellated tamped-earth walls, tile-roofed gatehouses, "
        "tiered wooden pavilions on a low hill. In the immediate "
        "foreground a large jade bi-disc and a small bronze imperial seal "
        "rest on a stone altar. Misty mountains and calm river beyond."
    ),
    "panyu-founding": (
        "A Qin-dynasty walled Chinese frontier town under construction on "
        "a bluff above a wide southern river, 214 BCE. Wooden scaffolding "
        "around tamped-earth ramparts, soldiers in early imperial armor "
        "supervising, ox carts hauling stones, surveyors with bamboo rods. "
        "Subtropical hills, banyan and palm in the distance."
    ),
    "maritime-silk-road": (
        "A bustling Tang–Song dynasty Chinese port on the Pearl River, "
        "around the 10th century. A tall stone cylindrical lighthouse "
        "minaret rises on the near shore. Three large wooden Chinese "
        "junks with red battened sails ride at anchor, an Arabian dhow "
        "with a lateen sail glides in the distance. Dockworkers unload "
        "spice baskets, silk bolts and porcelain jars; warehouses with "
        "curved tile roofs line the wharf."
    ),
    "thirteen-hongs": (
        "A row of eight European-style two-story trading factory "
        "warehouses along the Pearl River waterfront in 1820 Canton "
        "(Guangzhou). Pastel-painted facades with colonnaded ground "
        "floors and arched windows, slate roofs with chimneys. Flags of "
        "Britain, the Netherlands, France, Sweden, Denmark and the early "
        "United States fly from tall poles in front of the buildings. "
        "Tea chests, silver sycee ingots and silk bales are stacked on "
        "the wooden dock. Chinese sampans and a tall Western three-masted "
        "sailing ship in the river."
    ),
    "howqua": (
        "Interior of a wealthy 19th-century Cantonese hong merchant's "
        "counting house. A polished carved-wood desk, stacks of wooden "
        "tea chests stencilled with shipping marks, piled silver sycee "
        "boat-shaped ingots, a large wooden abacus, brush-and-ink "
        "ledgers, hanging silk calligraphy scrolls. Warm late-afternoon "
        "light slants in through a Manchu stained-glass lattice window."
    ),
    "shamian": (
        "A row of late-19th-century European colonial townhouses on a "
        "small sandbar island in southern China: three-story neoclassical "
        "and baroque buildings with deep arcaded ground floors, louvred "
        "French shutters, wrought-iron juliet balconies, dentil cornices, "
        "rosette pediments. Palm trees, banyans, ornate cast-iron gas "
        "lamps and benches line a stone embankment. A small river "
        "steamboat with a tall black funnel passes in the river."
    ),
    "xiguan": (
        "A late-Qing wealthy Cantonese merchant district at dusk. A "
        "traditional Xiguan mansion with grey-brick walls on granite "
        "plinths, the three-piece front: foot door, sliding trellis "
        "trundle gate, heavy main door. Manchu stained-glass lattice "
        "windows. A neighbouring pot-ear gable house. A row of qilou "
        "arcade houses with first-floor colonnades lining a narrow "
        "stone-paved street. A banyan tree, a paper lantern."
    ),
    "whampoa-academy": (
        "A 1924 Chinese republican military academy on a small island in "
        "the Pearl River: a long two-story neoclassical academy building "
        "with white columns and a tile roof, a parade ground with cadets "
        "drilling in early Republic of China uniforms, two flags on "
        "tall poles, a stone wharf with two motor launches tied up. "
        "Banyan trees frame the courtyard; the wide river is behind."
    ),
    "sun-yatsen-hall": (
        "An imposing octagonal Chinese ceremonial hall with a double-"
        "eaved cobalt-blue glazed-tile roof, white columned drum and a "
        "three-arched entrance — the early-1930s Sun Yat-sen Memorial "
        "Hall in Guangzhou. A broad stone plaza in front with a statue "
        "of a Chinese statesman in long robes, ornamental shrubs and "
        "palace lanterns. A mountain park rises behind, with the small "
        "silhouette of an old fortified tower on the highest peak."
    ),
    "canton-fair": (
        "A vast modern Chinese exhibition centre on a river island, "
        "morning of a major trade fair. Multiple glass-and-steel "
        "pavilion halls connected by sky-bridges, a wide forecourt "
        "filled with international visitors pulling rolling luggage, "
        "shuttle buses, flutter of banners. Tall modern Tianhe CBD "
        "skyscrapers across the river in the distance."
    ),
    "canton-tower": (
        "The 600-metre Canton Tower in Guangzhou at dusk: a slender "
        "hyperboloid steel mesh tower with an illuminated observation "
        "ring at its narrow waist, glowing in warm purple-and-orange "
        "light against a deep dusk sky. The Pearl River below reflects "
        "the tower. A backdrop of the modern Tianhe CBD skyline — the "
        "IFC and CTF Finance Centre towers, an LED-skinned skyscraper. "
        "A small sightseeing river boat strung with warm lights glides "
        "past. A burst of fireworks above the river."
    ),
    "yum-cha": (
        "Interior of a busy Cantonese yum cha (dim sum) restaurant on a "
        "bright weekend morning. A large round wooden table with a lazy "
        "Susan: three stacked bamboo steamers of har gow shrimp dumplings "
        "and another stack of siu mai topped with crab roe; a clay teapot "
        "pouring oolong; small cups; a plate of char siu bao buns; a "
        "rolled cheung fun rice noodle dish. Warm pendant lanterns "
        "overhead, a Manchu stained-glass lattice window behind."
    ),
}


def build_prompt(topic_id: str) -> str:
    subject = SUBJECTS.get(topic_id)
    if not subject:
        raise KeyError(f"no prompt subject for topic {topic_id!r}")
    return f"{subject}\n\nStyle:\n{STYLE}"


# =========================================================================
# Provider abstraction
# =========================================================================

@dataclass
class GenerationResult:
    topic_id: str
    path: Path
    bytes_written: int
    provider: str
    elapsed_s: float
    cached: bool = False
    error: str | None = None


class ImageProvider:
    name = "base"

    def generate(self, prompt: str) -> bytes:  # noqa: D401
        raise NotImplementedError


# ── stub: tiny placeholder PNG, no network, deterministic ───────────────
class StubProvider(ImageProvider):
    """Emits a 1-pixel valid PNG (different colour per topic) — purely
    for verifying the pipeline. The PNG header bytes are computed by hand
    so we don't pull in Pillow."""
    name = "stub"

    def __init__(self) -> None:
        self._counter = 0

    def generate(self, prompt: str) -> bytes:  # noqa: D401
        # Pick a colour deterministically from the prompt length so the
        # placeholder PNGs are visibly distinct per topic.
        self._counter += 1
        h = (abs(hash(prompt)) >> 8) & 0xFFFFFF
        r, g, b = (h >> 16) & 0xFF, (h >> 8) & 0xFF, h & 0xFF
        return _solid_png(r, g, b)


def _solid_png(r: int, g: int, b: int) -> bytes:
    """Build a 16×9 solid-colour PNG using only stdlib."""
    import struct
    import zlib

    width, height = 16, 9
    # raw scanlines: 1 byte filter (0) per row + RGB bytes
    raw = b"".join(b"\x00" + bytes((r, g, b)) * width for _ in range(height))

    def chunk(tag: bytes, data: bytes) -> bytes:
        return (struct.pack(">I", len(data)) + tag + data
                + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF))

    sig = b"\x89PNG\r\n\x1a\n"
    ihdr = chunk(b"IHDR",
                 struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
    idat = chunk(b"IDAT", zlib.compress(raw, level=9))
    iend = chunk(b"IEND", b"")
    return sig + ihdr + idat + iend


# ── OpenRouter: Gemini 2.5 Flash Image (nano-banana) ───────────────────
class OpenRouterProvider(ImageProvider):
    name = "openrouter"

    def __init__(self, api_key: str,
                 model: str = "google/gemini-2.5-flash-image-preview",
                 timeout_s: float = 180.0) -> None:
        self.api_key = api_key
        self.model = model
        self.timeout_s = timeout_s

    def generate(self, prompt: str) -> bytes:  # noqa: D401
        body = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "modalities": ["image", "text"],
        }
        req = urllib.request.Request(
            "https://openrouter.ai/api/v1/chat/completions",
            data=json.dumps(body).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://github.com/wilson8369/guangzhou-history-mcp",
                "X-Title": "Guangzhou History Flipbook",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=self.timeout_s) as resp:
            data = json.loads(resp.read())
        # OpenRouter routes image output into message.images[].image_url.url
        # for image-enabled models. We accept either the structured field
        # or a data URL embedded in the message content.
        msg = data["choices"][0]["message"]
        url = None
        for img in (msg.get("images") or []):
            url = img.get("image_url", {}).get("url")
            if url:
                break
        if not url:
            content = msg.get("content") or ""
            if isinstance(content, str) and content.startswith("data:image"):
                url = content
        if not url:
            raise RuntimeError(
                "OpenRouter response had no image. Full response: "
                + json.dumps(data, ensure_ascii=False)[:400]
            )
        return _bytes_from_url(url, timeout_s=self.timeout_s)


# ── fal.ai: Flux 1.1 Pro (sync endpoint) ───────────────────────────────
class FalProvider(ImageProvider):
    name = "fal"

    def __init__(self, api_key: str,
                 model: str = "fal-ai/flux-pro/v1.1",
                 timeout_s: float = 180.0) -> None:
        self.api_key = api_key
        self.model = model
        self.timeout_s = timeout_s

    def generate(self, prompt: str) -> bytes:  # noqa: D401
        body = {
            "prompt": prompt,
            "image_size": "landscape_16_9",
            "num_images": 1,
            "enable_safety_checker": False,
            "output_format": "png",
        }
        req = urllib.request.Request(
            f"https://fal.run/{self.model}",
            data=json.dumps(body).encode("utf-8"),
            headers={
                "Authorization": f"Key {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=self.timeout_s) as resp:
            data = json.loads(resp.read())
        images = data.get("images") or []
        if not images:
            raise RuntimeError(
                "fal response had no images. Full response: "
                + json.dumps(data, ensure_ascii=False)[:400]
            )
        url = images[0].get("url")
        if not url:
            raise RuntimeError("fal response image had no url field")
        return _bytes_from_url(url, timeout_s=self.timeout_s)


def _bytes_from_url(url: str, *, timeout_s: float) -> bytes:
    """Resolve either an http(s) URL or a data:image/* URL to raw bytes."""
    if url.startswith("data:"):
        # data:[<mime>];base64,<data>
        try:
            header, payload = url.split(",", 1)
        except ValueError as e:
            raise RuntimeError(f"malformed data URL: {url[:80]}") from e
        if ";base64" in header:
            return base64.b64decode(payload)
        return payload.encode("utf-8")
    with urllib.request.urlopen(url, timeout=timeout_s) as r:
        return r.read()


# =========================================================================
# Driver
# =========================================================================

def default_assets_dir() -> Path:
    """The project-root assets dir we write to / read from."""
    # generate_illustrations.py lives in guangzhou_history_mcp/, project
    # root is one level up.
    return Path(__file__).resolve().parent.parent / "assets" / "illustrations"


def topic_ids() -> list[str]:
    return [t["id"] for t in TOPICS]


def _make_provider(name: str, args) -> ImageProvider:
    if name == "stub":
        return StubProvider()
    if name == "openrouter":
        key = args.key or os.environ.get("OPENROUTER_API_KEY")
        if not key:
            raise SystemExit(
                "openrouter provider needs --key or OPENROUTER_API_KEY")
        return OpenRouterProvider(
            api_key=key,
            model=args.model or "google/gemini-2.5-flash-image-preview",
            timeout_s=args.timeout,
        )
    if name == "fal":
        key = args.key or os.environ.get("FAL_KEY")
        if not key:
            raise SystemExit("fal provider needs --key or FAL_KEY")
        return FalProvider(
            api_key=key,
            model=args.model or "fal-ai/flux-pro/v1.1",
            timeout_s=args.timeout,
        )
    raise SystemExit(f"unknown provider {name!r}")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__.split("\n\n")[0],
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="See module docstring for full examples.",
    )
    ap.add_argument("--provider", choices=("openrouter", "fal", "stub"),
                    default="stub",
                    help="image-generation backend (default: stub)")
    ap.add_argument("--key",
                    help="API key (else read from OPENROUTER_API_KEY / FAL_KEY)")
    ap.add_argument("--model", help="override provider's default model id")
    ap.add_argument("--out", type=Path, default=default_assets_dir(),
                    help=f"output directory (default: {default_assets_dir()})")
    ap.add_argument("--only", nargs="+", metavar="TOPIC_ID",
                    help="generate only the named topics")
    ap.add_argument("--force", action="store_true",
                    help="overwrite even if the PNG already exists")
    ap.add_argument("--dry-run", action="store_true",
                    help="don't call the provider, just print what would happen")
    ap.add_argument("--list", action="store_true",
                    help="print every topic + its prompt and exit")
    ap.add_argument("--timeout", type=float, default=180.0,
                    help="per-request timeout in seconds (default: 180)")
    args = ap.parse_args(argv)

    if args.list:
        for tid in topic_ids():
            print(f"== {tid} ==")
            print(build_prompt(tid))
            print()
        return 0

    targets = args.only or topic_ids()
    unknown = [t for t in targets if t not in SUBJECTS]
    if unknown:
        raise SystemExit(f"unknown topic ids: {unknown}")

    args.out.mkdir(parents=True, exist_ok=True)

    if args.dry_run:
        provider = None
        print(f"[dry-run] provider={args.provider}  out={args.out}")
    else:
        provider = _make_provider(args.provider, args)
        print(f"▸ provider: {provider.name}   "
              f"model: {getattr(provider, 'model', '-')}   "
              f"out: {args.out}")

    results: list[GenerationResult] = []
    for tid in targets:
        png_path = args.out / f"{tid}.png"
        if png_path.exists() and not args.force:
            size = png_path.stat().st_size
            print(f"  · {tid:<22}  cached ({size:,} bytes)  — pass --force "
                  f"to regenerate")
            results.append(GenerationResult(
                topic_id=tid, path=png_path, bytes_written=size,
                provider="cache", elapsed_s=0.0, cached=True,
            ))
            continue

        prompt = build_prompt(tid)
        if args.dry_run:
            print(f"  · {tid:<22}  would generate "
                  f"({len(prompt)} chars of prompt)")
            continue

        t0 = time.monotonic()
        try:
            data = provider.generate(prompt)
            png_path.write_bytes(data)
            dt = time.monotonic() - t0
            print(f"  ✓ {tid:<22}  {len(data):>8,} bytes   {dt:5.1f}s")
            results.append(GenerationResult(
                topic_id=tid, path=png_path, bytes_written=len(data),
                provider=provider.name, elapsed_s=dt,
            ))
        except (urllib.error.HTTPError, urllib.error.URLError,
                RuntimeError, OSError) as e:
            dt = time.monotonic() - t0
            print(f"  ✗ {tid:<22}  ERROR  {e}", file=sys.stderr)
            results.append(GenerationResult(
                topic_id=tid, path=png_path, bytes_written=0,
                provider=provider.name, elapsed_s=dt, error=str(e),
            ))

    if not args.dry_run:
        ok = sum(1 for r in results if r.bytes_written > 0)
        cached = sum(1 for r in results if r.cached)
        errs = sum(1 for r in results if r.error)
        total_bytes = sum(r.bytes_written for r in results if not r.cached)
        print()
        print(f"summary: {ok} written  ·  {cached} cached  ·  {errs} errors  "
              f"·  {total_bytes:,} new bytes  →  {args.out}")
        print()
        print("next step:  regenerate the HTML so the new PNGs are baked in")
        print('  python -c "from guangzhou_history_mcp.viewer import build_html; '
              'import pathlib; pathlib.Path(\'flipbook.html\').write_text('
              'build_html(), encoding=\'utf-8\')"')
        return 1 if errs else 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
