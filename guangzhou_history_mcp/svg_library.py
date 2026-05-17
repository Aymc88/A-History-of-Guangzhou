"""
Rich illustrated SVGs for the Guangzhou viewer.

Each illustration is a scene composition (sky + landscape + architecture +
foreground props), not a single icon — closer in spirit to the
"infographic page" look used by flipbook.page. All viewBoxes are 600×400,
all colours come from the same Lingnan palette so the book reads as one
volume.

Two indices are exposed:

    CHAPTER_SVG[motif_id]  ->  default illustration for a chapter
    TOPIC_SVG[topic_id]    ->  optional override for a specific topic

`svg_for(topic_id, motif)` returns the best match.

No external assets; everything is inline SVG. Stdlib-friendly strings.
"""

from __future__ import annotations

import base64
from pathlib import Path


# Shared <defs> we re-use across illustrations. Inlining per-SVG so each
# illustration is self-contained when extracted.
_PALETTE = {
    "paper":     "#f3e7cc",
    "paper_dim": "#e0cd9c",
    "ink":       "#2b1d10",
    "ink_soft":  "#54402a",
    "jade":      "#5e8a6b",
    "jade_dark": "#3f6149",
    "terra":     "#b85c2f",
    "terra_dk":  "#8b4421",
    "opera":     "#c14a3a",
    "opera_dk":  "#7c2c22",
    "gold":      "#c9a35a",
    "gold_dk":   "#8a6f2f",
    "indigo":    "#2c4a6e",
    "indigo_dk": "#1a2e47",
    "pot":       "#6b5d4f",
    "tile":      "#3d5266",
    "tile_dk":   "#243646",
}


# =========================================================================
# Chapter-level illustrations
# =========================================================================

CHAPTER_SVG: dict[str, str] = {}


# ── 1. NANYUE · Ancient Panyu / Imperial seal ──────────────────────────
CHAPTER_SVG["nanyue"] = """
<svg viewBox="0 0 600 400" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <defs>
    <linearGradient id="nyue-sky" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0"   stop-color="#f5e8c4"/>
      <stop offset="1"   stop-color="#ead7a7"/>
    </linearGradient>
    <linearGradient id="nyue-water" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0" stop-color="#7d9b86"/>
      <stop offset="1" stop-color="#4f6e5b"/>
    </linearGradient>
    <linearGradient id="nyue-wall" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0" stop-color="#a8917a"/>
      <stop offset="1" stop-color="#6b5239"/>
    </linearGradient>
    <linearGradient id="nyue-roof" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0" stop-color="#8a3a2a"/>
      <stop offset="1" stop-color="#5a261b"/>
    </linearGradient>
    <linearGradient id="nyue-seal" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0" stop-color="#c14a3a"/>
      <stop offset="1" stop-color="#7c2c22"/>
    </linearGradient>
    <radialGradient id="nyue-sun" cx=".5" cy=".5" r=".5">
      <stop offset="0"   stop-color="#fff5dd" stop-opacity=".9"/>
      <stop offset="1"   stop-color="#fff5dd" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <!-- sky + sun -->
  <rect width="600" height="260" fill="url(#nyue-sky)"/>
  <circle cx="470" cy="100" r="80" fill="url(#nyue-sun)"/>
  <circle cx="470" cy="100" r="22" fill="#f8d27a" opacity=".85"/>

  <!-- distant mountain layers -->
  <path d="M0 200 L60 150 L130 180 L210 130 L290 175 L360 140 L440 175 L520 145 L600 180 L600 260 L0 260 Z"
        fill="#7d8a6b" opacity=".55"/>
  <path d="M0 230 L80 195 L160 220 L240 180 L320 215 L400 185 L480 220 L560 195 L600 215 L600 280 L0 280 Z"
        fill="#5e7a5a" opacity=".7"/>

  <!-- river -->
  <rect x="0" y="260" width="600" height="80" fill="url(#nyue-water)"/>
  <g stroke="#fff5dd" stroke-width=".8" opacity=".35" fill="none">
    <path d="M0 285 Q60 280 120 285 T240 285 T360 285 T480 285 T600 285"/>
    <path d="M0 300 Q60 296 120 300 T240 300 T360 300 T480 300 T600 300"/>
    <path d="M0 315 Q60 312 120 315 T240 315 T360 315 T480 315 T600 315"/>
  </g>

  <!-- riverbank with reed -->
  <rect x="0" y="335" width="600" height="65" fill="#b69a64"/>
  <g stroke="#5e7a5a" stroke-width="1.4" stroke-linecap="round">
    <line x1="40"  y1="340" x2="38"  y2="320"/>
    <line x1="50"  y1="340" x2="52"  y2="318"/>
    <line x1="60"  y1="340" x2="58"  y2="322"/>
    <line x1="540" y1="340" x2="538" y2="322"/>
    <line x1="550" y1="340" x2="552" y2="318"/>
    <line x1="560" y1="340" x2="558" y2="323"/>
  </g>

  <!-- city walls (left + right of central gate) -->
  <g stroke="#3a2410" stroke-width="1.3">
    <rect x="60"  y="200" width="160" height="60"  fill="url(#nyue-wall)"/>
    <rect x="380" y="200" width="160" height="60"  fill="url(#nyue-wall)"/>
    <!-- crenellations -->
    <path d="M60 200 v-10 h16 v6 h12 v-6 h16 v6 h12 v-6 h16 v6 h12 v-6 h16 v6 h12 v-6 h16 v6 h12 v-6 h0 v10 Z"
          fill="url(#nyue-wall)"/>
    <path d="M380 200 v-10 h16 v6 h12 v-6 h16 v6 h12 v-6 h16 v6 h12 v-6 h16 v6 h12 v-6 h16 v6 h12 v-6 h0 v10 Z"
          fill="url(#nyue-wall)"/>
    <!-- brick courses -->
    <line x1="60"  y1="215" x2="220" y2="215" opacity=".55"/>
    <line x1="60"  y1="230" x2="220" y2="230" opacity=".55"/>
    <line x1="60"  y1="245" x2="220" y2="245" opacity=".55"/>
    <line x1="380" y1="215" x2="540" y2="215" opacity=".55"/>
    <line x1="380" y1="230" x2="540" y2="230" opacity=".55"/>
    <line x1="380" y1="245" x2="540" y2="245" opacity=".55"/>
  </g>

  <!-- central gatehouse -->
  <g stroke="#3a2410" stroke-width="1.5">
    <!-- lower podium -->
    <rect x="220" y="200" width="160" height="60" fill="#7a5a3a"/>
    <!-- arched gate -->
    <path d="M280 260 V218 a20 20 0 0 1 40 0 V260 Z" fill="#1f1610"/>
    <!-- gate doors highlight -->
    <line x1="300" y1="220" x2="300" y2="260" stroke="#c9a35a" stroke-width="1.2"/>
    <!-- upper pavilion -->
    <rect x="240" y="150" width="120" height="50" fill="#9a7c52"/>
    <line x1="240" y1="170" x2="360" y2="170" opacity=".7"/>
    <!-- columns -->
    <line x1="258" y1="150" x2="258" y2="200" opacity=".75"/>
    <line x1="288" y1="150" x2="288" y2="200" opacity=".75"/>
    <line x1="312" y1="150" x2="312" y2="200" opacity=".75"/>
    <line x1="342" y1="150" x2="342" y2="200" opacity=".75"/>
    <!-- upturned eave -->
    <path d="M230 150 Q300 110 370 150 Z" fill="url(#nyue-roof)"/>
    <path d="M226 150 L230 144 L370 144 L374 150 Z" fill="#3a1810"/>
    <!-- ridge ornament -->
    <path d="M295 110 q5 -10 10 0 z" fill="#c9a35a"/>
  </g>

  <!-- pagoda peeking behind right wall -->
  <g stroke="#3a2410" stroke-width="1.2">
    <rect x="455" y="105" width="40" height="90" fill="#a8917a"/>
    <path d="M450 145 H500 M448 170 H502" stroke-width="1"/>
    <path d="M450 105 L475 75 L500 105 Z" fill="url(#nyue-roof)"/>
    <line x1="475" y1="75" x2="475" y2="60" stroke-width="1.4"/>
    <circle cx="475" cy="56" r="4" fill="#c9a35a"/>
  </g>

  <!-- imperial seal stamp, foreground left -->
  <g transform="translate(110 290) rotate(-6)">
    <rect x="0" y="0" width="78" height="78" rx="6" fill="url(#nyue-seal)"
          stroke="#3a1810" stroke-width="2"/>
    <rect x="6" y="6" width="66" height="66" rx="4" fill="none"
          stroke="#f5e8c4" stroke-width="2" opacity=".75"/>
    <!-- abstracted seal-script glyph (purely decorative) -->
    <g stroke="#f5e8c4" stroke-width="3" stroke-linecap="round" fill="none" opacity=".95">
      <path d="M18 24 H60 M22 36 H56 M30 48 V64 M48 48 V64 M26 56 H52"/>
    </g>
    <!-- corner gilt -->
    <rect x="-3" y="-3" width="18" height="18" fill="#c9a35a" opacity=".8"/>
  </g>

  <!-- jade bi disc, foreground right -->
  <g transform="translate(490 300)">
    <circle r="34" fill="none" stroke="#5e8a6b" stroke-width="14" opacity=".9"/>
    <circle r="34" fill="none" stroke="#3f6149" stroke-width="2"/>
    <circle r="20" fill="none" stroke="#3f6149" stroke-width="1.5"/>
    <circle r="10" fill="none" stroke="#3f6149" stroke-width="1.2"/>
    <!-- highlight -->
    <path d="M-22 -20 a30 30 0 0 1 28 -10" stroke="#a8d2b3" stroke-width="3" fill="none" opacity=".7"/>
  </g>

  <!-- frame -->
  <rect x="2" y="2" width="596" height="396" fill="none"
        stroke="#3a2410" stroke-width="1" opacity=".4"/>
</svg>
"""


# ── 2. SILK-ROAD · Maritime trade · Guangta minaret + junk ─────────────
CHAPTER_SVG["silk-road"] = """
<svg viewBox="0 0 600 400" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <defs>
    <linearGradient id="sr-sky" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0" stop-color="#fbe9c2"/>
      <stop offset=".55" stop-color="#f4d99a"/>
      <stop offset="1" stop-color="#e8b86d"/>
    </linearGradient>
    <linearGradient id="sr-sea" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0" stop-color="#7d9aa6"/>
      <stop offset="1" stop-color="#3e5d6c"/>
    </linearGradient>
    <linearGradient id="sr-mast" x1="0" x2="1" y1="0" y2="0">
      <stop offset="0" stop-color="#c14a3a"/>
      <stop offset="1" stop-color="#7c2c22"/>
    </linearGradient>
    <linearGradient id="sr-sail" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0" stop-color="#f5e8c4"/>
      <stop offset="1" stop-color="#c9a35a"/>
    </linearGradient>
    <linearGradient id="sr-tower" x1="0" x2="1" y1="0" y2="0">
      <stop offset="0" stop-color="#e8dcc5"/>
      <stop offset="1" stop-color="#a8917a"/>
    </linearGradient>
  </defs>

  <!-- sky -->
  <rect width="600" height="240" fill="url(#sr-sky)"/>
  <!-- low sun -->
  <circle cx="420" cy="135" r="40" fill="#fff5dd" opacity=".95"/>
  <circle cx="420" cy="135" r="22" fill="#f4a04a" opacity=".75"/>
  <!-- horizon line clouds -->
  <g fill="#fff5dd" opacity=".55">
    <ellipse cx="120" cy="100" rx="60" ry="8"/>
    <ellipse cx="220" cy="80" rx="80" ry="6"/>
    <ellipse cx="540" cy="110" rx="50" ry="7"/>
  </g>

  <!-- distant junks on horizon -->
  <g fill="#1f1610" opacity=".5">
    <path d="M70 235 l16 -22 l10 22 z"/>
    <path d="M150 240 l14 -18 l10 18 z"/>
    <path d="M510 240 l16 -22 l10 22 z"/>
  </g>

  <!-- sea -->
  <rect x="0" y="240" width="600" height="160" fill="url(#sr-sea)"/>
  <!-- wave lines -->
  <g stroke="#f5e8c4" stroke-width=".8" opacity=".4" fill="none">
    <path d="M0 270 Q60 264 120 270 T240 270 T360 270 T480 270 T600 270"/>
    <path d="M0 290 Q60 285 120 290 T240 290 T360 290 T480 290 T600 290"/>
    <path d="M0 310 Q60 304 120 310 T240 310 T360 310 T480 310 T600 310"/>
    <path d="M0 335 Q60 330 120 335 T240 335 T360 335 T480 335 T600 335"/>
    <path d="M0 365 Q60 360 120 365 T240 365 T360 365 T480 365 T600 365"/>
  </g>

  <!-- Guangta minaret on left shore -->
  <g stroke="#3a2410" stroke-width="1.5">
    <!-- rocky base -->
    <path d="M40 280 Q70 268 95 272 Q120 270 130 280 V310 H40 Z" fill="#6b5d4f"/>
    <!-- tower shaft -->
    <rect x="68" y="120" width="34" height="170" fill="url(#sr-tower)"/>
    <!-- horizontal banding -->
    <g stroke-width="1" opacity=".7">
      <line x1="68" y1="160" x2="102" y2="160"/>
      <line x1="68" y1="200" x2="102" y2="200"/>
      <line x1="68" y1="240" x2="102" y2="240"/>
    </g>
    <!-- arched windows -->
    <g fill="#3a2410" opacity=".55">
      <path d="M78 175 V165 a7 7 0 0 1 14 0 V175 Z"/>
      <path d="M78 215 V205 a7 7 0 0 1 14 0 V215 Z"/>
      <path d="M78 255 V245 a7 7 0 0 1 14 0 V255 Z"/>
    </g>
    <!-- cap with finial -->
    <path d="M62 120 L85 85 L108 120 Z" fill="#b85c2f"/>
    <line x1="85" y1="85" x2="85" y2="65" stroke-width="1.5"/>
    <circle cx="85" cy="62" r="4" fill="#c9a35a"/>
    <!-- glowing top lantern -->
    <circle cx="85" cy="105" r="6" fill="#fff5dd" opacity=".9"/>
  </g>

  <!-- main junk ship, mid-foreground -->
  <g stroke="#3a2410" stroke-width="1.6">
    <!-- hull -->
    <path d="M210 330 Q310 305 460 330 L440 372 L230 372 Z" fill="#5e3a22"/>
    <!-- planking lines -->
    <path d="M225 340 Q310 320 445 340" stroke="#3a1d10" stroke-width="1" fill="none" opacity=".7"/>
    <path d="M232 358 Q310 342 438 358" stroke="#3a1d10" stroke-width="1" fill="none" opacity=".7"/>
    <!-- eye on bow -->
    <ellipse cx="448" cy="335" rx="6" ry="3" fill="#f5e8c4"/>
    <circle  cx="448" cy="335" r="1.6" fill="#1f1610"/>
    <!-- masts -->
    <line x1="290" y1="330" x2="290" y2="160" stroke="url(#sr-mast)" stroke-width="3"/>
    <line x1="380" y1="330" x2="380" y2="190" stroke="url(#sr-mast)" stroke-width="3"/>
    <!-- main sail with battens -->
    <path d="M290 165 Q360 175 360 320 L290 320 Z" fill="url(#sr-sail)"/>
    <g stroke="#8a6f2f" stroke-width="1" opacity=".7">
      <line x1="290" y1="185" x2="354" y2="195"/>
      <line x1="290" y1="210" x2="356" y2="217"/>
      <line x1="290" y1="240" x2="357" y2="245"/>
      <line x1="290" y1="270" x2="358" y2="272"/>
      <line x1="290" y1="295" x2="359" y2="298"/>
    </g>
    <!-- foresail -->
    <path d="M380 195 Q436 208 436 320 L380 320 Z" fill="url(#sr-sail)" opacity=".95"/>
    <g stroke="#8a6f2f" stroke-width="1" opacity=".6">
      <line x1="380" y1="218" x2="432" y2="225"/>
      <line x1="380" y1="245" x2="434" y2="250"/>
      <line x1="380" y1="275" x2="435" y2="278"/>
      <line x1="380" y1="305" x2="435" y2="307"/>
    </g>
    <!-- mast pennants -->
    <path d="M290 155 l22 8 l-22 6 z" fill="#c14a3a"/>
    <path d="M380 185 l18 6 l-18 5 z" fill="#c14a3a"/>
  </g>

  <!-- warehouse on far right shore -->
  <g stroke="#3a2410" stroke-width="1.3">
    <rect x="495" y="240" width="80" height="60" fill="#e8dcc5"/>
    <path d="M491 240 L535 215 L579 240 Z" fill="#8a3a2a"/>
    <rect x="510" y="265" width="14" height="35" fill="#3a2410" opacity=".7"/>
    <rect x="540" y="265" width="14" height="35" fill="#3a2410" opacity=".7"/>
    <!-- amphorae stacked -->
    <g fill="#7a5a3a">
      <ellipse cx="500" cy="320" rx="9" ry="11"/>
      <ellipse cx="515" cy="320" rx="9" ry="11"/>
      <ellipse cx="530" cy="320" rx="9" ry="11"/>
      <ellipse cx="508" cy="305" rx="9" ry="11"/>
      <ellipse cx="523" cy="305" rx="9" ry="11"/>
    </g>
  </g>

  <!-- foreground reflection sparkle -->
  <g fill="#fff5dd" opacity=".5">
    <circle cx="100" cy="370" r="1.5"/>
    <circle cx="180" cy="385" r="1"/>
    <circle cx="260" cy="395" r="1.2"/>
    <circle cx="500" cy="380" r="1.5"/>
  </g>

  <rect x="2" y="2" width="596" height="396" fill="none"
        stroke="#3a2410" stroke-width="1" opacity=".4"/>
</svg>
"""


# ── 3. THIRTEEN-HONGS · Row of factories with flags ────────────────────
CHAPTER_SVG["thirteen-hongs"] = """
<svg viewBox="0 0 600 400" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <defs>
    <linearGradient id="th-sky" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0" stop-color="#f6dca0"/>
      <stop offset="1" stop-color="#e8a86d"/>
    </linearGradient>
    <linearGradient id="th-river" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0" stop-color="#6e8a90"/>
      <stop offset="1" stop-color="#3a5260"/>
    </linearGradient>
    <linearGradient id="th-fac1" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0" stop-color="#fdf2d8"/>
      <stop offset="1" stop-color="#e8d6a3"/>
    </linearGradient>
    <linearGradient id="th-fac2" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0" stop-color="#f8e8c0"/>
      <stop offset="1" stop-color="#dfc183"/>
    </linearGradient>
  </defs>

  <!-- sunset sky -->
  <rect width="600" height="220" fill="url(#th-sky)"/>
  <circle cx="120" cy="80" r="32" fill="#ffe8b5" opacity=".9"/>
  <!-- chimney smoke -->
  <g fill="#fff5dd" opacity=".5">
    <ellipse cx="200" cy="80" rx="40" ry="8"/>
    <ellipse cx="450" cy="60" rx="60" ry="9"/>
  </g>

  <!-- distant Western ship -->
  <g stroke="#1f1610" stroke-width="1" opacity=".75">
    <path d="M460 215 Q480 213 510 215 L505 224 L465 224 Z" fill="#3a2410"/>
    <line x1="473" y1="215" x2="473" y2="170"/>
    <line x1="488" y1="215" x2="488" y2="160"/>
    <line x1="503" y1="215" x2="503" y2="172"/>
    <path d="M465 178 H481 M465 188 H481 M465 198 H481" stroke-width=".8" opacity=".75"/>
    <path d="M483 168 H493 M483 178 H493 M483 188 H493 M483 198 H493" stroke-width=".8" opacity=".75"/>
    <path d="M495 180 H511 M495 190 H511 M495 200 H511" stroke-width=".8" opacity=".75"/>
  </g>

  <!-- river -->
  <rect x="0" y="220" width="600" height="50" fill="url(#th-river)"/>
  <g stroke="#fff5dd" stroke-width=".8" opacity=".35" fill="none">
    <path d="M0 240 Q60 236 120 240 T240 240 T360 240 T480 240 T600 240"/>
    <path d="M0 256 Q60 252 120 256 T240 256 T360 256 T480 256 T600 256"/>
  </g>
  <!-- sampan -->
  <g fill="#3a2410">
    <path d="M310 260 q12 -4 28 0 l-3 6 l-22 0 z"/>
    <line x1="324" y1="250" x2="324" y2="260" stroke="#3a2410" stroke-width="1"/>
  </g>

  <!-- dock + factories row -->
  <rect x="0" y="270" width="600" height="20" fill="#a8917a"/>
  <line x1="0" y1="270" x2="600" y2="270" stroke="#3a2410" stroke-width="1"/>

  <!-- five factories — slightly varied roofs / cornices -->
  <g stroke="#3a2410" stroke-width="1.3">
    <!-- factory A -->
    <rect x="40"  y="135" width="95"  height="135" fill="url(#th-fac1)"/>
    <rect x="40"  y="135" width="95"  height="14"  fill="#a8917a"/>
    <path d="M36 135 L87 110 L139 135 Z" fill="#8a3a2a"/>
    <!-- sash windows -->
    <g fill="#2c4a6e" opacity=".85">
      <rect x="56"  y="160" width="20" height="26"/>
      <rect x="86"  y="160" width="20" height="26"/>
      <rect x="116" y="160" width="20" height="26"/> <!-- mistake: keep inside -->
    </g>
    <!-- ground arches -->
    <g fill="#3a2410" opacity=".7">
      <path d="M52  270 V230 a13 13 0 0 1 26 0 V270 Z"/>
      <path d="M85  270 V230 a13 13 0 0 1 26 0 V270 Z"/>
      <path d="M118 270 V230 a13 13 0 0 1 26 0 V270 Z"/>
    </g>

    <!-- factory B -->
    <rect x="155" y="125" width="95" height="145" fill="url(#th-fac2)"/>
    <rect x="155" y="125" width="95" height="14" fill="#a8917a"/>
    <path d="M151 125 L202 100 L254 125 Z" fill="#8a3a2a"/>
    <g fill="#2c4a6e" opacity=".85">
      <rect x="171" y="150" width="20" height="26"/>
      <rect x="201" y="150" width="20" height="26"/>
      <rect x="231" y="150" width="20" height="26"/>
    </g>
    <g fill="#2c4a6e" opacity=".7">
      <rect x="171" y="190" width="20" height="22"/>
      <rect x="201" y="190" width="20" height="22"/>
      <rect x="231" y="190" width="20" height="22"/>
    </g>
    <g fill="#3a2410" opacity=".7">
      <path d="M167 270 V230 a13 13 0 0 1 26 0 V270 Z"/>
      <path d="M200 270 V230 a13 13 0 0 1 26 0 V270 Z"/>
      <path d="M233 270 V230 a13 13 0 0 1 26 0 V270 Z"/>
    </g>

    <!-- factory C — tallest -->
    <rect x="270" y="115" width="95" height="155" fill="url(#th-fac1)"/>
    <rect x="270" y="115" width="95" height="14" fill="#a8917a"/>
    <path d="M266 115 L317 88 L369 115 Z" fill="#8a3a2a"/>
    <g fill="#2c4a6e" opacity=".85">
      <rect x="286" y="140" width="20" height="26"/>
      <rect x="316" y="140" width="20" height="26"/>
      <rect x="346" y="140" width="20" height="26"/>
    </g>
    <g fill="#2c4a6e" opacity=".7">
      <rect x="286" y="180" width="20" height="22"/>
      <rect x="316" y="180" width="20" height="22"/>
      <rect x="346" y="180" width="20" height="22"/>
    </g>
    <g fill="#3a2410" opacity=".7">
      <path d="M282 270 V230 a13 13 0 0 1 26 0 V270 Z"/>
      <path d="M315 270 V230 a13 13 0 0 1 26 0 V270 Z"/>
      <path d="M348 270 V230 a13 13 0 0 1 26 0 V270 Z"/>
    </g>

    <!-- factory D -->
    <rect x="385" y="130" width="95" height="140" fill="url(#th-fac2)"/>
    <rect x="385" y="130" width="95" height="14" fill="#a8917a"/>
    <path d="M381 130 L432 105 L484 130 Z" fill="#8a3a2a"/>
    <g fill="#2c4a6e" opacity=".85">
      <rect x="401" y="155" width="20" height="26"/>
      <rect x="431" y="155" width="20" height="26"/>
      <rect x="461" y="155" width="20" height="26"/>
    </g>
    <g fill="#3a2410" opacity=".7">
      <path d="M397 270 V230 a13 13 0 0 1 26 0 V270 Z"/>
      <path d="M430 270 V230 a13 13 0 0 1 26 0 V270 Z"/>
      <path d="M463 270 V230 a13 13 0 0 1 26 0 V270 Z"/>
    </g>

    <!-- factory E -->
    <rect x="500" y="140" width="80" height="130" fill="url(#th-fac1)"/>
    <rect x="500" y="140" width="80" height="14" fill="#a8917a"/>
    <path d="M496 140 L540 117 L584 140 Z" fill="#8a3a2a"/>
    <g fill="#2c4a6e" opacity=".85">
      <rect x="514" y="165" width="20" height="26"/>
      <rect x="546" y="165" width="20" height="26"/>
    </g>
    <g fill="#3a2410" opacity=".7">
      <path d="M510 270 V230 a12 12 0 0 1 24 0 V270 Z"/>
      <path d="M548 270 V230 a12 12 0 0 1 24 0 V270 Z"/>
    </g>
  </g>

  <!-- flag poles + flags -->
  <g stroke="#3a2410" stroke-width="1.2">
    <line x1="87"  y1="110" x2="87"  y2="56"/>
    <line x1="202" y1="100" x2="202" y2="44"/>
    <line x1="317" y1="88"  x2="317" y2="30"/>
    <line x1="432" y1="105" x2="432" y2="48"/>
    <line x1="540" y1="117" x2="540" y2="62"/>
  </g>
  <!-- Sweden -->
  <rect x="87"  y="56" width="40" height="22" fill="#2c4a6e"/>
  <rect x="100" y="56" width="6"  height="22" fill="#c9a35a"/>
  <rect x="87"  y="64" width="40" height="6"  fill="#c9a35a"/>
  <!-- Netherlands -->
  <rect x="202" y="44" width="40" height="22" fill="#c14a3a"/>
  <rect x="202" y="52" width="40" height="6"  fill="#f5e8c4"/>
  <rect x="202" y="58" width="40" height="8"  fill="#2c4a6e"/>
  <!-- UK union jack abstracted -->
  <rect x="317" y="30" width="40" height="22" fill="#2c4a6e"/>
  <path d="M317 30 L357 52 M317 52 L357 30" stroke="#f5e8c4" stroke-width="2"/>
  <path d="M337 30 V52 M317 41 H357" stroke="#c14a3a" stroke-width="2"/>
  <!-- France -->
  <rect x="432" y="48" width="40" height="22" fill="#f5e8c4"/>
  <rect x="432" y="48" width="13" height="22" fill="#2c4a6e"/>
  <rect x="459" y="48" width="13" height="22" fill="#c14a3a"/>
  <!-- USA stars-and-stripes abstracted -->
  <rect x="540" y="62" width="40" height="22" fill="#f5e8c4"/>
  <g fill="#c14a3a">
    <rect x="540" y="62" width="40" height="3"/>
    <rect x="540" y="68" width="40" height="3"/>
    <rect x="540" y="74" width="40" height="3"/>
    <rect x="540" y="80" width="40" height="3"/>
  </g>
  <rect x="540" y="62" width="16" height="12" fill="#2c4a6e"/>

  <!-- foreground tea chests + bales -->
  <g stroke="#3a2410" stroke-width="1.3">
    <rect x="20"  y="320" width="60" height="50" fill="#8a6a3a"/>
    <rect x="20"  y="320" width="60" height="8"  fill="#3a2410" opacity=".4"/>
    <text x="50" y="352" text-anchor="middle" font-family="serif" font-size="14"
          fill="#f5e8c4">茶</text>
    <rect x="90"  y="332" width="56" height="38" fill="#a8917a"/>
    <line x1="90" y1="350" x2="146" y2="350" opacity=".6"/>
    <rect x="500" y="318" width="58" height="52" fill="#8a6a3a"/>
    <text x="529" y="352" text-anchor="middle" font-family="serif" font-size="14"
          fill="#f5e8c4">絲</text>
  </g>

  <rect x="2" y="2" width="596" height="396" fill="none"
        stroke="#3a2410" stroke-width="1" opacity=".4"/>
</svg>
"""


# ── 4. TREATY-PORT · Shamian concession ────────────────────────────────
CHAPTER_SVG["treaty-port"] = """
<svg viewBox="0 0 600 400" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <defs>
    <linearGradient id="tp-sky" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0" stop-color="#cbd6dd"/>
      <stop offset="1" stop-color="#e8d6a3"/>
    </linearGradient>
    <linearGradient id="tp-river" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0" stop-color="#6e7e85"/>
      <stop offset="1" stop-color="#3d4e58"/>
    </linearGradient>
    <linearGradient id="tp-bldg" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0" stop-color="#fff5dd"/>
      <stop offset="1" stop-color="#e0cd9c"/>
    </linearGradient>
    <linearGradient id="tp-bldg2" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0" stop-color="#f8e8d4"/>
      <stop offset="1" stop-color="#d2b07c"/>
    </linearGradient>
  </defs>

  <!-- overcast sky -->
  <rect width="600" height="220" fill="url(#tp-sky)"/>
  <!-- gulls -->
  <g stroke="#3a2410" stroke-width="1.4" fill="none">
    <path d="M100 60 q6 -6 12 0 q6 -6 12 0"/>
    <path d="M180 80 q5 -5 10 0 q5 -5 10 0"/>
    <path d="M450 50 q6 -6 12 0 q6 -6 12 0"/>
  </g>

  <!-- distant Whampoa pagoda -->
  <g stroke="#3a2410" stroke-width="1" opacity=".6">
    <rect x="510" y="160" width="14" height="50" fill="#a8917a"/>
    <path d="M508 160 H526 M508 170 H526 M508 180 H526 M508 190 H526 M508 200 H526"/>
    <path d="M504 160 L517 145 L530 160 Z" fill="#8a3a2a"/>
  </g>

  <!-- Shamian row of three buildings -->
  <g stroke="#3a2410" stroke-width="1.4">
    <!-- left building -->
    <rect x="40"  y="125" width="160" height="155" fill="url(#tp-bldg)"/>
    <line x1="40" y1="160" x2="200" y2="160" opacity=".7"/>
    <line x1="40" y1="200" x2="200" y2="200" opacity=".7"/>
    <line x1="40" y1="240" x2="200" y2="240" opacity=".7"/>
    <!-- arches ground floor -->
    <g fill="#1f1610" opacity=".65">
      <path d="M55  280 V250 a14 14 0 0 1 28 0 V280 Z"/>
      <path d="M93  280 V250 a14 14 0 0 1 28 0 V280 Z"/>
      <path d="M131 280 V250 a14 14 0 0 1 28 0 V280 Z"/>
      <path d="M169 280 V250 a14 14 0 0 1 28 0 V280 Z"/>
    </g>
    <!-- 2F shuttered windows -->
    <g fill="#5e8a6b" stroke-width="1">
      <rect x="60"  y="172" width="24" height="22"/>
      <rect x="98"  y="172" width="24" height="22"/>
      <rect x="136" y="172" width="24" height="22"/>
      <rect x="174" y="172" width="24" height="22"/>
    </g>
    <!-- 3F balcony rail -->
    <g stroke-width="1" opacity=".75">
      <line x1="40" y1="220" x2="200" y2="220"/>
      <g fill="#3a2410">
        <rect x="50"  y="210" width="3" height="12"/>
        <rect x="70"  y="210" width="3" height="12"/>
        <rect x="90"  y="210" width="3" height="12"/>
        <rect x="110" y="210" width="3" height="12"/>
        <rect x="130" y="210" width="3" height="12"/>
        <rect x="150" y="210" width="3" height="12"/>
        <rect x="170" y="210" width="3" height="12"/>
      </g>
    </g>
    <!-- pediment -->
    <path d="M30 125 L120 95 L210 125 Z" fill="#8a3a2a"/>
    <rect x="30" y="125" width="180" height="6" fill="#a8917a"/>

    <!-- centre building (taller) -->
    <rect x="220" y="105" width="180" height="175" fill="url(#tp-bldg2)"/>
    <line x1="220" y1="140" x2="400" y2="140" opacity=".7"/>
    <line x1="220" y1="180" x2="400" y2="180" opacity=".7"/>
    <line x1="220" y1="220" x2="400" y2="220" opacity=".7"/>
    <line x1="220" y1="250" x2="400" y2="250" opacity=".7"/>
    <g fill="#1f1610" opacity=".65">
      <path d="M232 280 V250 a14 14 0 0 1 28 0 V280 Z"/>
      <path d="M272 280 V250 a14 14 0 0 1 28 0 V280 Z"/>
      <path d="M312 280 V250 a14 14 0 0 1 28 0 V280 Z"/>
      <path d="M352 280 V250 a14 14 0 0 1 28 0 V280 Z"/>
    </g>
    <g fill="#5e8a6b">
      <rect x="240" y="152" width="22" height="22"/>
      <rect x="276" y="152" width="22" height="22"/>
      <rect x="312" y="152" width="22" height="22"/>
      <rect x="348" y="152" width="22" height="22"/>
      <rect x="380" y="152" width="14" height="22"/>
    </g>
    <g fill="#2c4a6e" opacity=".75">
      <rect x="240" y="190" width="22" height="22"/>
      <rect x="276" y="190" width="22" height="22"/>
      <rect x="312" y="190" width="22" height="22"/>
      <rect x="348" y="190" width="22" height="22"/>
    </g>
    <!-- central pediment with clock -->
    <path d="M210 105 L310 70 L410 105 Z" fill="#8a3a2a"/>
    <circle cx="310" cy="92" r="8" fill="#fff5dd" stroke="#3a2410" stroke-width="1"/>
    <line x1="310" y1="92" x2="310" y2="86" stroke="#3a2410" stroke-width=".8"/>
    <line x1="310" y1="92" x2="314" y2="94" stroke="#3a2410" stroke-width=".8"/>

    <!-- right building -->
    <rect x="420" y="135" width="140" height="145" fill="url(#tp-bldg)"/>
    <line x1="420" y1="170" x2="560" y2="170" opacity=".7"/>
    <line x1="420" y1="210" x2="560" y2="210" opacity=".7"/>
    <line x1="420" y1="245" x2="560" y2="245" opacity=".7"/>
    <g fill="#1f1610" opacity=".65">
      <path d="M432 280 V250 a13 13 0 0 1 26 0 V280 Z"/>
      <path d="M468 280 V250 a13 13 0 0 1 26 0 V280 Z"/>
      <path d="M504 280 V250 a13 13 0 0 1 26 0 V280 Z"/>
      <path d="M540 280 V250 a12 12 0 0 1 24 0 V280 Z"/>
    </g>
    <g fill="#5e8a6b">
      <rect x="440" y="182" width="22" height="22"/>
      <rect x="476" y="182" width="22" height="22"/>
      <rect x="512" y="182" width="22" height="22"/>
    </g>
    <path d="M410 135 L490 110 L570 135 Z" fill="#8a3a2a"/>
  </g>

  <!-- gas lamp foreground -->
  <g stroke="#3a2410" stroke-width="1.6">
    <line x1="30" y1="290" x2="30" y2="370"/>
    <rect x="22" y="270" width="16" height="22" fill="#c9a35a"/>
    <path d="M18 270 H42 L38 262 H22 Z" fill="#3a2410"/>
    <circle cx="30" cy="281" r="3" fill="#fff5dd"/>
  </g>

  <!-- willow trees -->
  <g stroke="#3a2410" stroke-width="1.4">
    <line x1="225" y1="370" x2="225" y2="300"/>
    <g stroke="#5e8a6b" stroke-width="1.2" stroke-linecap="round">
      <path d="M225 300 q-10 6 -16 26"/>
      <path d="M225 300 q-4 8 -8 30"/>
      <path d="M225 300 q4 8 -2 32"/>
      <path d="M225 300 q12 6 14 28"/>
      <path d="M225 300 q18 4 20 26"/>
    </g>
  </g>

  <!-- river + steamer -->
  <rect x="0" y="290" width="600" height="110" fill="url(#tp-river)"/>
  <g stroke="#fff5dd" stroke-width=".8" opacity=".3" fill="none">
    <path d="M0 320 Q60 316 120 320 T240 320 T360 320 T480 320 T600 320"/>
    <path d="M0 345 Q60 340 120 345 T240 345 T360 345 T480 345 T600 345"/>
    <path d="M0 375 Q60 370 120 375 T240 375 T360 375 T480 375 T600 375"/>
  </g>
  <!-- steamer -->
  <g stroke="#3a2410" stroke-width="1.4">
    <path d="M340 360 Q420 340 510 360 L495 380 L355 380 Z" fill="#3a2410"/>
    <rect x="395" y="330" width="60" height="30" fill="#e0cd9c"/>
    <rect x="395" y="330" width="60" height="6"  fill="#8a3a2a"/>
    <rect x="402" y="340" width="10" height="14" fill="#2c4a6e"/>
    <rect x="418" y="340" width="10" height="14" fill="#2c4a6e"/>
    <rect x="434" y="340" width="10" height="14" fill="#2c4a6e"/>
    <!-- funnel -->
    <rect x="455" y="295" width="14" height="40" fill="#3a2410"/>
    <rect x="458" y="305" width="8"  height="6"  fill="#c14a3a"/>
    <path d="M455 290 q10 -28 4 -50 q14 6 8 50" fill="#a8917a" opacity=".55"/>
  </g>

  <rect x="2" y="2" width="596" height="396" fill="none"
        stroke="#3a2410" stroke-width="1" opacity=".4"/>
</svg>
"""


# ── 5. REVOLUTION · Sun Yat-sen Memorial Hall + Yuexiu ─────────────────
CHAPTER_SVG["revolution"] = """
<svg viewBox="0 0 600 400" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <defs>
    <linearGradient id="rv-sky" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0" stop-color="#f8e8c0"/>
      <stop offset="1" stop-color="#f0d49a"/>
    </linearGradient>
    <linearGradient id="rv-roof" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0" stop-color="#3a5e8a"/>
      <stop offset="1" stop-color="#1f3556"/>
    </linearGradient>
    <linearGradient id="rv-drum" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0" stop-color="#c14a3a"/>
      <stop offset="1" stop-color="#7c2c22"/>
    </linearGradient>
    <linearGradient id="rv-plaza" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0" stop-color="#d4b884"/>
      <stop offset="1" stop-color="#a8916a"/>
    </linearGradient>
    <radialGradient id="rv-glow" cx=".5" cy=".5" r=".5">
      <stop offset="0" stop-color="#fff5dd" stop-opacity=".9"/>
      <stop offset="1" stop-color="#fff5dd" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <rect width="600" height="280" fill="url(#rv-sky)"/>
  <circle cx="500" cy="80" r="60" fill="url(#rv-glow)"/>
  <circle cx="500" cy="80" r="22" fill="#fff0c0"/>

  <!-- mountain layers (Yuexiu) -->
  <path d="M0 220 L100 160 L200 200 L320 145 L430 195 L530 170 L600 200 L600 280 L0 280 Z"
        fill="#7d8a6b" opacity=".55"/>
  <path d="M0 250 L120 215 L240 245 L350 205 L470 240 L600 215 L600 290 L0 290 Z"
        fill="#5e7a5a" opacity=".75"/>

  <!-- Zhenhai tower silhouette on a peak -->
  <g fill="#5a3a22" opacity=".75">
    <rect x="345" y="160" width="20" height="40"/>
    <path d="M341 160 H369 L365 152 H345 Z"/>
    <rect x="348" y="148" width="14" height="14"/>
    <path d="M345 148 H365 L362 141 H348 Z"/>
  </g>

  <!-- plaza ground -->
  <rect x="0" y="280" width="600" height="120" fill="url(#rv-plaza)"/>
  <g stroke="#8a6f2f" stroke-width=".7" opacity=".5">
    <line x1="0" y1="300" x2="600" y2="300"/>
    <line x1="0" y1="320" x2="600" y2="320"/>
    <line x1="0" y1="345" x2="600" y2="345"/>
    <line x1="0" y1="375" x2="600" y2="375"/>
  </g>

  <!-- the hall -->
  <g stroke="#3a2410" stroke-width="1.5">
    <!-- platform -->
    <rect x="180" y="270" width="240" height="20" fill="#a8917a"/>
    <line x1="180" y1="280" x2="420" y2="280" opacity=".7"/>

    <!-- octagonal drum (lower) -->
    <path d="M210 270 L210 215 L240 195 L360 195 L390 215 L390 270 Z" fill="url(#rv-drum)"/>
    <!-- column row -->
    <g fill="#f5e8c4">
      <rect x="225" y="220" width="8" height="50"/>
      <rect x="250" y="220" width="8" height="50"/>
      <rect x="275" y="220" width="8" height="50"/>
      <rect x="300" y="220" width="8" height="50"/>
      <rect x="325" y="220" width="8" height="50"/>
      <rect x="350" y="220" width="8" height="50"/>
      <rect x="375" y="220" width="8" height="50"/>
    </g>
    <!-- big door -->
    <path d="M275 270 V230 a25 25 0 0 1 50 0 V270 Z" fill="#3a1810"/>
    <line x1="300" y1="240" x2="300" y2="270" stroke="#c9a35a" stroke-width="1"/>

    <!-- blue tile roof – lower eave -->
    <path d="M198 215 L240 175 L360 175 L402 215 Z" fill="url(#rv-roof)"/>
    <path d="M198 215 H402" stroke-width="2"/>
    <!-- eave underlay -->
    <path d="M194 215 L196 209 L404 209 L406 215 Z" fill="#3a1d10"/>
    <!-- middle drum -->
    <rect x="250" y="135" width="100" height="40" fill="url(#rv-drum)"/>
    <g fill="#f5e8c4">
      <rect x="262" y="142" width="6" height="26"/>
      <rect x="278" y="142" width="6" height="26"/>
      <rect x="294" y="142" width="6" height="26"/>
      <rect x="310" y="142" width="6" height="26"/>
      <rect x="326" y="142" width="6" height="26"/>
    </g>
    <!-- upper roof -->
    <path d="M238 135 L300 95 L362 135 Z" fill="url(#rv-roof)"/>
    <path d="M232 135 L234 130 L366 130 L368 135 Z" fill="#3a1d10"/>
    <!-- top finial -->
    <line x1="300" y1="95" x2="300" y2="72" stroke-width="2"/>
    <rect x="294" y="68" width="12" height="8" fill="#c9a35a"/>
    <circle cx="300" cy="60" r="5" fill="#c9a35a"/>
  </g>

  <!-- Sun Yat-sen statue silhouette on plaza -->
  <g fill="#3a2410">
    <rect x="296" y="320" width="8" height="22"/>
    <circle cx="300" cy="316" r="4"/>
    <rect x="290" y="342" width="20" height="14"/>
  </g>

  <!-- decorative lanterns at plaza entrance -->
  <g stroke="#3a2410" stroke-width="1.2">
    <line x1="120" y1="370" x2="120" y2="320"/>
    <ellipse cx="120" cy="313" rx="9" ry="11" fill="#c14a3a"/>
    <line x1="480" y1="370" x2="480" y2="320"/>
    <ellipse cx="480" cy="313" rx="9" ry="11" fill="#c14a3a"/>
  </g>

  <!-- five-pointed star floating in sky -->
  <g transform="translate(80 90)">
    <polygon points="0,-22 6,-7 22,-7 9,4 14,20 0,11 -14,20 -9,4 -22,-7 -6,-7"
             fill="#c14a3a" stroke="#3a2410" stroke-width="1.2"/>
  </g>

  <rect x="2" y="2" width="596" height="396" fill="none"
        stroke="#3a2410" stroke-width="1" opacity=".4"/>
</svg>
"""


# ── 6. REFORM · Canton Tower at dusk + CBD skyline ─────────────────────
CHAPTER_SVG["reform"] = """
<svg viewBox="0 0 600 400" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <defs>
    <linearGradient id="rf-sky" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0"  stop-color="#3a2c5e"/>
      <stop offset=".5" stop-color="#9e5a6a"/>
      <stop offset="1"  stop-color="#f0a865"/>
    </linearGradient>
    <linearGradient id="rf-tower" x1="0" x2="1" y1="0" y2="0">
      <stop offset="0" stop-color="#c14a3a"/>
      <stop offset=".5" stop-color="#e8a86d"/>
      <stop offset="1" stop-color="#c14a3a"/>
    </linearGradient>
    <linearGradient id="rf-river" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0" stop-color="#2c3a5a"/>
      <stop offset="1" stop-color="#1a2336"/>
    </linearGradient>
    <linearGradient id="rf-glow" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0" stop-color="#fff5dd" stop-opacity=".55"/>
      <stop offset="1" stop-color="#fff5dd" stop-opacity="0"/>
    </linearGradient>
  </defs>

  <!-- dusk sky -->
  <rect width="600" height="280" fill="url(#rf-sky)"/>
  <!-- stars -->
  <g fill="#fff5dd">
    <circle cx="60"  cy="40"  r="1"/>
    <circle cx="120" cy="30"  r="1.2"/>
    <circle cx="80"  cy="80"  r=".9"/>
    <circle cx="540" cy="35"  r="1.1"/>
    <circle cx="500" cy="60"  r=".9"/>
  </g>
  <!-- distant moon -->
  <circle cx="80" cy="60" r="22" fill="#fff5dd" opacity=".85"/>
  <circle cx="76" cy="56" r="22" fill="url(#rf-sky)"/>

  <!-- fireworks -->
  <g stroke-width="1.4" stroke-linecap="round" fill="none">
    <g stroke="#f8d27a">
      <path d="M200 50 v-14 M200 50 v14 M200 50 h-14 M200 50 h14 M192 42 l-8 -8 M208 42 l8 -8 M192 58 l-8 8 M208 58 l8 8"/>
    </g>
    <g stroke="#c14a3a" opacity=".9">
      <path d="M460 110 v-12 M460 110 v12 M460 110 h-12 M460 110 h12 M453 103 l-7 -7 M467 103 l7 -7 M453 117 l-7 7 M467 117 l7 7"/>
    </g>
    <g stroke="#5e8a6b" opacity=".9">
      <path d="M380 50 v-10 M380 50 v10 M380 50 h-10 M380 50 h10 M373 43 l-7 -7 M387 43 l7 -7"/>
    </g>
  </g>

  <!-- CBD skyline behind -->
  <g fill="#1a2030">
    <rect x="0"   y="200" width="40" height="80"/>
    <rect x="42"  y="180" width="35" height="100"/>
    <!-- IFC-like -->
    <rect x="80"  y="150" width="34" height="130"/>
    <polygon points="80,150 97,135 114,150"/>
    <rect x="118" y="195" width="28" height="85"/>
    <rect x="150" y="170" width="30" height="110"/>
    <rect x="184" y="200" width="26" height="80"/>
    <!-- right side -->
    <rect x="400" y="190" width="28" height="90"/>
    <!-- CTF-like -->
    <rect x="432" y="130" width="36" height="150"/>
    <polygon points="432,130 450,118 468,130"/>
    <rect x="472" y="165" width="32" height="115"/>
    <rect x="508" y="190" width="28" height="90"/>
    <rect x="540" y="175" width="32" height="105"/>
    <rect x="574" y="205" width="26" height="75"/>
  </g>
  <!-- window grid on skyline -->
  <g fill="#fff5dd" opacity=".75">
    <rect x="86"  y="160" width="3" height="3"/>
    <rect x="92"  y="160" width="3" height="3"/>
    <rect x="98"  y="160" width="3" height="3"/>
    <rect x="104" y="160" width="3" height="3"/>
    <rect x="86"  y="172" width="3" height="3"/>
    <rect x="92"  y="172" width="3" height="3"/>
    <rect x="104" y="172" width="3" height="3"/>
    <rect x="86"  y="184" width="3" height="3"/>
    <rect x="98"  y="184" width="3" height="3"/>
    <rect x="438" y="140" width="3" height="3"/>
    <rect x="444" y="140" width="3" height="3"/>
    <rect x="450" y="140" width="3" height="3"/>
    <rect x="456" y="140" width="3" height="3"/>
    <rect x="438" y="155" width="3" height="3"/>
    <rect x="450" y="155" width="3" height="3"/>
    <rect x="462" y="155" width="3" height="3"/>
    <rect x="438" y="170" width="3" height="3"/>
    <rect x="450" y="170" width="3" height="3"/>
  </g>

  <!-- Canton Tower — detailed hyperboloid mesh -->
  <g>
    <!-- two outer envelope curves -->
    <path d="M275 280 Q300 165 285 110 Q280 70 270 30" stroke="url(#rf-tower)" stroke-width="3" fill="none"/>
    <path d="M325 280 Q300 165 315 110 Q320 70 330 30" stroke="url(#rf-tower)" stroke-width="3" fill="none"/>
    <!-- diagonal mesh, left-to-right and right-to-left -->
    <g stroke="#c14a3a" stroke-width=".8" opacity=".8">
      <line x1="275" y1="280" x2="330" y2="30"/>
      <line x1="282" y1="280" x2="325" y2="30"/>
      <line x1="290" y1="280" x2="320" y2="30"/>
      <line x1="298" y1="280" x2="315" y2="30"/>
      <line x1="306" y1="280" x2="310" y2="30"/>
      <line x1="314" y1="280" x2="305" y2="30"/>
      <line x1="322" y1="280" x2="300" y2="30"/>
      <line x1="325" y1="280" x2="270" y2="30"/>
      <line x1="318" y1="280" x2="275" y2="30"/>
      <line x1="310" y1="280" x2="280" y2="30"/>
      <line x1="302" y1="280" x2="285" y2="30"/>
      <line x1="294" y1="280" x2="290" y2="30"/>
      <line x1="286" y1="280" x2="295" y2="30"/>
      <line x1="278" y1="280" x2="300" y2="30"/>
    </g>
    <!-- ring lights -->
    <g stroke="#f8d27a" stroke-width="1.5" fill="none" opacity=".9">
      <ellipse cx="300" cy="220" rx="22" ry="3"/>
      <ellipse cx="300" cy="180" rx="16" ry="2.5"/>
      <ellipse cx="300" cy="140" rx="12" ry="2"/>
      <ellipse cx="300" cy="100" rx="9"  ry="1.6"/>
      <ellipse cx="300" cy="65"  rx="6"  ry="1.2"/>
    </g>
    <!-- waist-cap observation deck -->
    <ellipse cx="300" cy="115" rx="14" ry="3" fill="#c9a35a" stroke="#3a2410" stroke-width="1"/>
    <!-- antenna -->
    <line x1="300" y1="30" x2="300" y2="10" stroke="#3a2410" stroke-width="1.5"/>
    <circle cx="300" cy="8" r="2" fill="#f8d27a"/>
  </g>
  <!-- glow around tower -->
  <ellipse cx="300" cy="200" rx="80" ry="120" fill="url(#rf-glow)"/>

  <!-- Pearl River -->
  <rect x="0" y="280" width="600" height="120" fill="url(#rf-river)"/>
  <!-- tower reflection -->
  <g opacity=".5">
    <path d="M275 280 Q300 350 290 396" stroke="#c14a3a" stroke-width="2" fill="none"/>
    <path d="M325 280 Q300 350 310 396" stroke="#c14a3a" stroke-width="2" fill="none"/>
  </g>
  <!-- skyline reflection -->
  <g fill="#1a2030" opacity=".55">
    <rect x="80" y="280" width="34" height="60"/>
    <rect x="432" y="280" width="36" height="80"/>
  </g>
  <!-- river highlights -->
  <g stroke="#f8d27a" stroke-width=".8" opacity=".55" fill="none">
    <path d="M0 320 Q60 316 120 320 T240 320 T360 320 T480 320 T600 320"/>
    <path d="M0 355 Q60 350 120 355 T240 355 T360 355 T480 355 T600 355"/>
    <path d="M0 385 Q60 380 120 385 T240 385 T360 385 T480 385 T600 385"/>
  </g>

  <!-- sightseeing boat -->
  <g stroke="#3a2410" stroke-width="1.4">
    <path d="M80 350 Q130 340 190 350 L180 368 L90 368 Z" fill="#c9a35a"/>
    <rect x="100" y="332" width="70" height="20" fill="#fff5dd"/>
    <line x1="100" y1="340" x2="170" y2="340"/>
    <g fill="#2c4a6e">
      <rect x="106" y="342" width="8" height="8"/>
      <rect x="118" y="342" width="8" height="8"/>
      <rect x="130" y="342" width="8" height="8"/>
      <rect x="142" y="342" width="8" height="8"/>
      <rect x="154" y="342" width="8" height="8"/>
    </g>
    <!-- string lights -->
    <path d="M80 350 q55 -25 110 0" stroke="#f8d27a" stroke-width="1" fill="none"/>
    <g fill="#f8d27a">
      <circle cx="100" cy="343" r="1.6"/>
      <circle cx="130" cy="338" r="1.6"/>
      <circle cx="160" cy="343" r="1.6"/>
    </g>
  </g>

  <rect x="2" y="2" width="596" height="396" fill="none"
        stroke="#3a2410" stroke-width="1" opacity=".4"/>
</svg>
"""


# =========================================================================
# Topic-specific overrides (richer detail for the most iconic topics)
# =========================================================================

TOPIC_SVG: dict[str, str] = {}


# ── Howqua · tea chests + silver ingots + ledger ────────────────────────
TOPIC_SVG["howqua"] = """
<svg viewBox="0 0 600 400" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <defs>
    <linearGradient id="hq-bg" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0" stop-color="#f8e8c0"/>
      <stop offset="1" stop-color="#d6b884"/>
    </linearGradient>
    <linearGradient id="hq-wood" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0" stop-color="#a8753a"/>
      <stop offset="1" stop-color="#6b4520"/>
    </linearGradient>
    <linearGradient id="hq-silver" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0" stop-color="#f5f5f0"/>
      <stop offset=".5" stop-color="#cdcdc0"/>
      <stop offset="1" stop-color="#8e8e80"/>
    </linearGradient>
    <linearGradient id="hq-paper" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0" stop-color="#fff5dd"/>
      <stop offset="1" stop-color="#e0cd9c"/>
    </linearGradient>
  </defs>

  <rect width="600" height="400" fill="url(#hq-bg)"/>
  <!-- wall + counter -->
  <rect x="0" y="0" width="600" height="220" fill="#bfa46f" opacity=".4"/>
  <rect x="0" y="220" width="600" height="180" fill="#9a7c48"/>
  <line x1="0" y1="220" x2="600" y2="220" stroke="#3a2410" stroke-width="1.4"/>

  <!-- back wall: scroll calligraphy + abacus -->
  <g stroke="#3a2410" stroke-width="1.2">
    <rect x="40" y="40" width="100" height="150" fill="#fff5dd"/>
    <rect x="40" y="40" width="100" height="8"  fill="#8a6f2f"/>
    <rect x="40" y="182" width="100" height="8" fill="#8a6f2f"/>
    <!-- calligraphy lines (decorative, not real characters) -->
    <g stroke="#1f1610" stroke-width="2" stroke-linecap="round" opacity=".85">
      <line x1="65" y1="65" x2="65"  y2="78"/>
      <line x1="60" y1="82" x2="70"  y2="82"/>
      <line x1="63" y1="86" x2="67"  y2="92"/>
      <line x1="62" y1="100" x2="68" y2="100"/>
      <line x1="65" y1="100" x2="65" y2="118"/>
      <line x1="60" y1="122" x2="70" y2="122"/>
      <line x1="63" y1="130" x2="67" y2="138"/>
      <line x1="60" y1="146" x2="70" y2="146"/>
      <line x1="65" y1="146" x2="65" y2="170"/>
    </g>
    <!-- seal stamp -->
    <rect x="100" y="155" width="20" height="20" fill="#c14a3a"/>
  </g>
  <!-- abacus -->
  <g stroke="#3a2410" stroke-width="1.2">
    <rect x="430" y="50" width="140" height="120" fill="#7a5a3a"/>
    <line x1="430" y1="100" x2="570" y2="100"/>
    <g stroke-width="1" opacity=".8">
      <line x1="445" y1="55" x2="445" y2="165"/>
      <line x1="465" y1="55" x2="465" y2="165"/>
      <line x1="485" y1="55" x2="485" y2="165"/>
      <line x1="505" y1="55" x2="505" y2="165"/>
      <line x1="525" y1="55" x2="525" y2="165"/>
      <line x1="545" y1="55" x2="545" y2="165"/>
    </g>
    <!-- beads -->
    <g fill="#c9a35a">
      <circle cx="445" cy="70" r="5"/><circle cx="445" cy="80" r="5"/>
      <circle cx="445" cy="120" r="5"/><circle cx="445" cy="130" r="5"/><circle cx="445" cy="140" r="5"/>
      <circle cx="465" cy="70" r="5"/><circle cx="465" cy="80" r="5"/>
      <circle cx="465" cy="125" r="5"/><circle cx="465" cy="135" r="5"/><circle cx="465" cy="145" r="5"/>
      <circle cx="485" cy="70" r="5"/><circle cx="485" cy="80" r="5"/>
      <circle cx="485" cy="120" r="5"/><circle cx="485" cy="130" r="5"/><circle cx="485" cy="140" r="5"/>
      <circle cx="505" cy="70" r="5"/><circle cx="505" cy="80" r="5"/>
      <circle cx="505" cy="125" r="5"/><circle cx="505" cy="135" r="5"/><circle cx="505" cy="145" r="5"/>
      <circle cx="525" cy="70" r="5"/><circle cx="525" cy="80" r="5"/>
      <circle cx="525" cy="120" r="5"/><circle cx="525" cy="130" r="5"/><circle cx="525" cy="140" r="5"/>
      <circle cx="545" cy="70" r="5"/><circle cx="545" cy="80" r="5"/>
      <circle cx="545" cy="125" r="5"/><circle cx="545" cy="135" r="5"/><circle cx="545" cy="145" r="5"/>
    </g>
  </g>

  <!-- big tea chest, foreground left -->
  <g stroke="#3a2410" stroke-width="1.5">
    <rect x="50"  y="230" width="160" height="140" fill="url(#hq-wood)"/>
    <!-- planks + nails -->
    <line x1="50"  y1="260" x2="210" y2="260" stroke-width="1" opacity=".5"/>
    <line x1="50"  y1="295" x2="210" y2="295" stroke-width="1" opacity=".5"/>
    <line x1="50"  y1="330" x2="210" y2="330" stroke-width="1" opacity=".5"/>
    <g fill="#3a2410">
      <circle cx="60" cy="240" r="1.5"/>
      <circle cx="200" cy="240" r="1.5"/>
      <circle cx="60" cy="360" r="1.5"/>
      <circle cx="200" cy="360" r="1.5"/>
    </g>
    <!-- stencilled label -->
    <rect x="80" y="280" width="100" height="60" fill="#f5e8c4"/>
    <text x="130" y="312" text-anchor="middle"
          font-family="serif" font-size="34" font-weight="bold"
          fill="#1f1610">茶</text>
    <text x="130" y="330" text-anchor="middle"
          font-family="serif" font-size="10"
          fill="#7c2c22" letter-spacing="2">HOWQUA</text>
  </g>

  <!-- silver ingots (sycee) stacked, middle -->
  <g stroke="#3a2410" stroke-width="1.2">
    <g transform="translate(260 320)">
      <path d="M0 0 q20 -14 60 0 q-14 20 -60 0 z" fill="url(#hq-silver)"/>
      <path d="M10 -5 q20 -10 40 0" fill="none" stroke-width="1" opacity=".6"/>
    </g>
    <g transform="translate(252 296)">
      <path d="M0 0 q22 -16 76 0 q-16 22 -76 0 z" fill="url(#hq-silver)"/>
      <path d="M14 -5 q22 -11 48 0" fill="none" stroke-width="1" opacity=".6"/>
    </g>
    <g transform="translate(244 268)">
      <path d="M0 0 q24 -16 92 0 q-18 22 -92 0 z" fill="url(#hq-silver)"/>
      <path d="M16 -5 q24 -11 60 0" fill="none" stroke-width="1" opacity=".6"/>
    </g>
  </g>

  <!-- ledger book + brush, foreground right -->
  <g stroke="#3a2410" stroke-width="1.4">
    <!-- book -->
    <g transform="translate(390 280) rotate(-5)">
      <rect x="0" y="0" width="160" height="100" fill="url(#hq-paper)"/>
      <line x1="80" y1="0" x2="80" y2="100" opacity=".6"/>
      <g stroke="#1f1610" stroke-width="1.4" opacity=".8">
        <line x1="10" y1="20" x2="74" y2="20"/>
        <line x1="10" y1="32" x2="74" y2="32"/>
        <line x1="10" y1="44" x2="74" y2="44"/>
        <line x1="10" y1="56" x2="74" y2="56"/>
        <line x1="10" y1="68" x2="74" y2="68"/>
        <line x1="86" y1="20" x2="150" y2="20"/>
        <line x1="86" y1="32" x2="150" y2="32"/>
        <line x1="86" y1="44" x2="150" y2="44"/>
        <line x1="86" y1="56" x2="150" y2="56"/>
        <line x1="86" y1="68" x2="150" y2="68"/>
      </g>
      <!-- red seal on page -->
      <rect x="124" y="74" width="22" height="22" fill="#c14a3a"/>
    </g>
    <!-- brush -->
    <g transform="translate(460 240) rotate(35)">
      <rect x="0" y="0" width="80" height="6" fill="#3a1810"/>
      <path d="M80 -3 q14 6 0 14 q-10 -4 -10 -6 q4 -2 10 -8" fill="#1f1610"/>
    </g>
    <!-- inkwell -->
    <ellipse cx="540" cy="350" rx="22" ry="8" fill="#5e3a22"/>
    <ellipse cx="540" cy="346" rx="20" ry="6" fill="#1f1610"/>
  </g>

  <rect x="2" y="2" width="596" height="396" fill="none"
        stroke="#3a2410" stroke-width="1" opacity=".4"/>
</svg>
"""


# ── shamian · close-up colonial arcade ──────────────────────────────────
TOPIC_SVG["shamian"] = """
<svg viewBox="0 0 600 400" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <defs>
    <linearGradient id="sh-sky" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0" stop-color="#d8dce0"/>
      <stop offset="1" stop-color="#f4e5b6"/>
    </linearGradient>
    <linearGradient id="sh-bldg" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0" stop-color="#fff5dd"/>
      <stop offset="1" stop-color="#d6b884"/>
    </linearGradient>
    <linearGradient id="sh-roof" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0" stop-color="#7c2c22"/>
      <stop offset="1" stop-color="#4a1810"/>
    </linearGradient>
  </defs>

  <!-- sky -->
  <rect width="600" height="280" fill="url(#sh-sky)"/>
  <!-- clouds -->
  <g fill="#fff5dd" opacity=".55">
    <ellipse cx="120" cy="50" rx="65" ry="10"/>
    <ellipse cx="220" cy="40" rx="55" ry="9"/>
    <ellipse cx="490" cy="60" rx="70" ry="10"/>
  </g>

  <!-- ground / road -->
  <rect x="0" y="320" width="600" height="80" fill="#a8916a"/>
  <g stroke="#7a5a3a" stroke-width="1" opacity=".5">
    <line x1="0" y1="340" x2="600" y2="340"/>
    <line x1="0" y1="360" x2="600" y2="360"/>
    <line x1="0" y1="380" x2="600" y2="380"/>
  </g>

  <!-- the building, very detailed -->
  <g stroke="#3a2410" stroke-width="1.6">
    <!-- main mass -->
    <rect x="60" y="100" width="480" height="220" fill="url(#sh-bldg)"/>
    <!-- string courses -->
    <line x1="60" y1="160" x2="540" y2="160" stroke-width="1.2" opacity=".7"/>
    <line x1="60" y1="220" x2="540" y2="220" stroke-width="1.2" opacity=".7"/>
    <line x1="60" y1="270" x2="540" y2="270" stroke-width="1.2" opacity=".7"/>

    <!-- ground floor: deep arcade -->
    <g fill="#1f1610" opacity=".75">
      <path d="M80  320 V280 a22 22 0 0 1 44 0 V320 Z"/>
      <path d="M138 320 V280 a22 22 0 0 1 44 0 V320 Z"/>
      <path d="M196 320 V280 a22 22 0 0 1 44 0 V320 Z"/>
      <path d="M254 320 V280 a22 22 0 0 1 44 0 V320 Z"/>
      <path d="M312 320 V280 a22 22 0 0 1 44 0 V320 Z"/>
      <path d="M370 320 V280 a22 22 0 0 1 44 0 V320 Z"/>
      <path d="M428 320 V280 a22 22 0 0 1 44 0 V320 Z"/>
      <path d="M486 320 V280 a18 18 0 0 1 36 0 V320 Z"/>
    </g>
    <!-- arch keystones -->
    <g fill="#c9a35a">
      <rect x="98"  y="276" width="8" height="8"/>
      <rect x="156" y="276" width="8" height="8"/>
      <rect x="214" y="276" width="8" height="8"/>
      <rect x="272" y="276" width="8" height="8"/>
      <rect x="330" y="276" width="8" height="8"/>
      <rect x="388" y="276" width="8" height="8"/>
      <rect x="446" y="276" width="8" height="8"/>
      <rect x="500" y="276" width="8" height="8"/>
    </g>

    <!-- second floor: arched french windows with louvred shutters -->
    <g>
      <g fill="#5e8a6b">
        <rect x="86"  y="175" width="32" height="42"/>
        <rect x="144" y="175" width="32" height="42"/>
        <rect x="202" y="175" width="32" height="42"/>
        <rect x="260" y="175" width="32" height="42"/>
        <rect x="318" y="175" width="32" height="42"/>
        <rect x="376" y="175" width="32" height="42"/>
        <rect x="434" y="175" width="32" height="42"/>
        <rect x="488" y="175" width="32" height="42"/>
      </g>
      <!-- louvres -->
      <g stroke="#3a2410" stroke-width=".8" opacity=".5">
        <line x1="86"  y1="182" x2="118" y2="182"/>
        <line x1="86"  y1="190" x2="118" y2="190"/>
        <line x1="86"  y1="198" x2="118" y2="198"/>
        <line x1="86"  y1="206" x2="118" y2="206"/>
        <line x1="144" y1="182" x2="176" y2="182"/>
        <line x1="144" y1="190" x2="176" y2="190"/>
        <line x1="144" y1="198" x2="176" y2="198"/>
        <line x1="144" y1="206" x2="176" y2="206"/>
        <line x1="202" y1="182" x2="234" y2="182"/>
        <line x1="202" y1="190" x2="234" y2="190"/>
        <line x1="202" y1="198" x2="234" y2="198"/>
        <line x1="202" y1="206" x2="234" y2="206"/>
        <line x1="260" y1="182" x2="292" y2="182"/>
        <line x1="260" y1="190" x2="292" y2="190"/>
        <line x1="260" y1="198" x2="292" y2="198"/>
        <line x1="260" y1="206" x2="292" y2="206"/>
        <line x1="318" y1="182" x2="350" y2="182"/>
        <line x1="318" y1="190" x2="350" y2="190"/>
        <line x1="318" y1="198" x2="350" y2="198"/>
        <line x1="318" y1="206" x2="350" y2="206"/>
        <line x1="376" y1="182" x2="408" y2="182"/>
        <line x1="376" y1="190" x2="408" y2="190"/>
        <line x1="376" y1="198" x2="408" y2="198"/>
        <line x1="376" y1="206" x2="408" y2="206"/>
        <line x1="434" y1="182" x2="466" y2="182"/>
        <line x1="434" y1="190" x2="466" y2="190"/>
        <line x1="434" y1="198" x2="466" y2="198"/>
        <line x1="434" y1="206" x2="466" y2="206"/>
        <line x1="488" y1="182" x2="520" y2="182"/>
        <line x1="488" y1="190" x2="520" y2="190"/>
        <line x1="488" y1="198" x2="520" y2="198"/>
        <line x1="488" y1="206" x2="520" y2="206"/>
      </g>
      <!-- wrought-iron juliet balconies -->
      <g stroke="#1f1610" stroke-width="1" opacity=".85">
        <line x1="86"  y1="225" x2="118" y2="225"/>
        <g fill="#1f1610">
          <rect x="88"  y="217" width="2" height="10"/>
          <rect x="94"  y="217" width="2" height="10"/>
          <rect x="100" y="217" width="2" height="10"/>
          <rect x="106" y="217" width="2" height="10"/>
          <rect x="112" y="217" width="2" height="10"/>
        </g>
      </g>
    </g>

    <!-- third floor: smaller rectangular windows -->
    <g fill="#3a4a6e" opacity=".85">
      <rect x="86"  y="235" width="32" height="28"/>
      <rect x="144" y="235" width="32" height="28"/>
      <rect x="202" y="235" width="32" height="28"/>
      <rect x="260" y="235" width="32" height="28"/>
      <rect x="318" y="235" width="32" height="28"/>
      <rect x="376" y="235" width="32" height="28"/>
      <rect x="434" y="235" width="32" height="28"/>
      <rect x="488" y="235" width="32" height="28"/>
    </g>

    <!-- cornice + dentils -->
    <rect x="56" y="92" width="488" height="14" fill="#c9a35a"/>
    <g fill="#3a2410">
      <rect x="62" y="98" width="4" height="6"/>
      <rect x="72" y="98" width="4" height="6"/>
      <rect x="82" y="98" width="4" height="6"/>
      <rect x="92" y="98" width="4" height="6"/>
      <rect x="102" y="98" width="4" height="6"/>
      <rect x="112" y="98" width="4" height="6"/>
      <rect x="122" y="98" width="4" height="6"/>
      <rect x="132" y="98" width="4" height="6"/>
      <rect x="142" y="98" width="4" height="6"/>
      <rect x="152" y="98" width="4" height="6"/>
      <rect x="162" y="98" width="4" height="6"/>
      <rect x="172" y="98" width="4" height="6"/>
      <rect x="182" y="98" width="4" height="6"/>
      <rect x="192" y="98" width="4" height="6"/>
      <rect x="202" y="98" width="4" height="6"/>
      <rect x="212" y="98" width="4" height="6"/>
      <rect x="222" y="98" width="4" height="6"/>
      <rect x="232" y="98" width="4" height="6"/>
      <rect x="242" y="98" width="4" height="6"/>
      <rect x="252" y="98" width="4" height="6"/>
      <rect x="262" y="98" width="4" height="6"/>
      <rect x="272" y="98" width="4" height="6"/>
      <rect x="282" y="98" width="4" height="6"/>
      <rect x="292" y="98" width="4" height="6"/>
      <rect x="302" y="98" width="4" height="6"/>
      <rect x="312" y="98" width="4" height="6"/>
      <rect x="322" y="98" width="4" height="6"/>
      <rect x="332" y="98" width="4" height="6"/>
      <rect x="342" y="98" width="4" height="6"/>
      <rect x="352" y="98" width="4" height="6"/>
      <rect x="362" y="98" width="4" height="6"/>
      <rect x="372" y="98" width="4" height="6"/>
      <rect x="382" y="98" width="4" height="6"/>
      <rect x="392" y="98" width="4" height="6"/>
      <rect x="402" y="98" width="4" height="6"/>
      <rect x="412" y="98" width="4" height="6"/>
      <rect x="422" y="98" width="4" height="6"/>
      <rect x="432" y="98" width="4" height="6"/>
      <rect x="442" y="98" width="4" height="6"/>
      <rect x="452" y="98" width="4" height="6"/>
      <rect x="462" y="98" width="4" height="6"/>
      <rect x="472" y="98" width="4" height="6"/>
      <rect x="482" y="98" width="4" height="6"/>
      <rect x="492" y="98" width="4" height="6"/>
      <rect x="502" y="98" width="4" height="6"/>
      <rect x="512" y="98" width="4" height="6"/>
      <rect x="522" y="98" width="4" height="6"/>
      <rect x="532" y="98" width="4" height="6"/>
    </g>

    <!-- pediment with rosette -->
    <path d="M50 92 L300 50 L550 92 Z" fill="url(#sh-roof)"/>
    <circle cx="300" cy="78" r="10" fill="#c9a35a"/>
    <circle cx="300" cy="78" r="4"  fill="#3a1810"/>
  </g>

  <!-- gas lamp foreground -->
  <g stroke="#3a2410" stroke-width="1.6">
    <line x1="35" y1="380" x2="35" y2="280"/>
    <rect x="25" y="258" width="20" height="24" fill="#c9a35a"/>
    <path d="M20 258 H50 L46 250 H24 Z" fill="#3a2410"/>
    <circle cx="35" cy="270" r="3.5" fill="#fff5dd"/>
  </g>

  <!-- palm tree right -->
  <g>
    <line x1="565" y1="380" x2="565" y2="220" stroke="#3a2410" stroke-width="3"/>
    <g stroke="#3a2410" stroke-width="1" opacity=".7">
      <line x1="555" y1="350" x2="575" y2="350"/>
      <line x1="555" y1="320" x2="575" y2="320"/>
      <line x1="555" y1="290" x2="575" y2="290"/>
      <line x1="555" y1="260" x2="575" y2="260"/>
    </g>
    <g fill="#5e8a6b" stroke="#3f6149" stroke-width=".8">
      <path d="M565 220 q-40 -8 -55 -36 q24 -2 60 28 z"/>
      <path d="M565 220 q-30 -28 -10 -64 q22 8 18 60 z"/>
      <path d="M565 220 q30 -8 56 -34 q-20 -10 -60 28 z"/>
      <path d="M565 220 q24 -32 0 -64 q-22 10 -10 60 z"/>
      <path d="M565 220 q-2 -32 16 -54 q12 18 -6 48 z"/>
    </g>
  </g>

  <rect x="2" y="2" width="596" height="396" fill="none"
        stroke="#3a2410" stroke-width="1" opacity=".4"/>
</svg>
"""


# ── canton-tower · close-up dusk shot ───────────────────────────────────
TOPIC_SVG["canton-tower"] = CHAPTER_SVG["reform"]  # already tower-centric


# ── yum-cha · dim sum table ─────────────────────────────────────────────
TOPIC_SVG["yum-cha"] = """
<svg viewBox="0 0 600 400" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <defs>
    <radialGradient id="yc-table" cx=".5" cy=".5" r=".6">
      <stop offset="0" stop-color="#d6b884"/>
      <stop offset="1" stop-color="#7a5a3a"/>
    </radialGradient>
    <linearGradient id="yc-bg" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0" stop-color="#5a1c14"/>
      <stop offset="1" stop-color="#8b3424"/>
    </linearGradient>
    <linearGradient id="yc-steam" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0" stop-color="#e8c887"/>
      <stop offset="1" stop-color="#a8753a"/>
    </linearGradient>
    <radialGradient id="yc-lantern" cx=".5" cy=".5" r=".5">
      <stop offset="0" stop-color="#fff5dd"/>
      <stop offset="1" stop-color="#c14a3a"/>
    </radialGradient>
  </defs>

  <!-- background: warm restaurant wall with Manchu window -->
  <rect width="600" height="400" fill="url(#yc-bg)"/>
  <!-- Manchu (套色) window -->
  <g transform="translate(60 50)" stroke="#3a1810" stroke-width="1.4">
    <rect width="160" height="120" fill="#3a2410"/>
    <g>
      <!-- diamond grid panes with alternating colours -->
      <path d="M0 60 L80 0 L160 60 L80 120 Z" fill="#c14a3a" opacity=".85"/>
      <path d="M0 0 L80 60 L0 120 Z" fill="#5e8a6b" opacity=".85"/>
      <path d="M160 0 L80 60 L160 120 Z" fill="#5e8a6b" opacity=".85"/>
      <path d="M0 0 L40 30 L0 60 Z M0 60 L40 90 L0 120 Z M160 0 L120 30 L160 60 Z M160 60 L120 90 L160 120 Z"
            fill="#c9a35a" opacity=".75"/>
    </g>
    <line x1="80" y1="0" x2="80" y2="120"/>
    <line x1="0" y1="60" x2="160" y2="60"/>
  </g>

  <!-- hanging red lantern -->
  <g transform="translate(420 30)">
    <line x1="0" y1="0" x2="0" y2="22" stroke="#3a1810" stroke-width="1.4"/>
    <ellipse cx="0" cy="55" rx="38" ry="32" fill="url(#yc-lantern)" stroke="#7c2c22" stroke-width="2"/>
    <rect x="-18" y="22" width="36" height="8" fill="#c9a35a" stroke="#3a1810" stroke-width="1"/>
    <rect x="-18" y="80" width="36" height="8" fill="#c9a35a" stroke="#3a1810" stroke-width="1"/>
    <!-- ribs -->
    <path d="M-38 55 Q0 70 38 55" fill="none" stroke="#7c2c22" stroke-width="1"/>
    <path d="M-38 55 Q0 40 38 55" fill="none" stroke="#7c2c22" stroke-width="1"/>
    <!-- tassel -->
    <line x1="0" y1="88" x2="0" y2="100" stroke="#c9a35a" stroke-width="2"/>
    <g stroke="#c9a35a" stroke-width="1.2">
      <line x1="-4" y1="100" x2="-6" y2="120"/>
      <line x1="0"  y1="100" x2="0"  y2="124"/>
      <line x1="4"  y1="100" x2="6"  y2="120"/>
    </g>
  </g>

  <!-- big round table -->
  <ellipse cx="300" cy="320" rx="280" ry="80" fill="url(#yc-table)" stroke="#3a1810" stroke-width="2"/>
  <ellipse cx="300" cy="310" rx="265" ry="72" fill="none" stroke="#5a3a22" stroke-width="1" opacity=".55"/>

  <!-- 3 bamboo steamers stacked, centre-left -->
  <g stroke="#3a2410" stroke-width="1.4">
    <g transform="translate(180 270)">
      <!-- steam wisps -->
      <g fill="none" stroke="#fff5dd" stroke-width="2" opacity=".7" stroke-linecap="round">
        <path d="M-30 -10 q5 -20 -2 -36 q12 -8 6 -36"/>
        <path d="M0 -10 q-4 -22 6 -40 q-8 -10 0 -34"/>
        <path d="M30 -10 q-6 -18 4 -36 q-12 -6 -2 -34"/>
      </g>
      <!-- top -->
      <ellipse cx="0" cy="0" rx="60" ry="14" fill="url(#yc-steam)"/>
      <ellipse cx="0" cy="0" rx="60" ry="14" fill="none"/>
      <g stroke-width=".8" opacity=".6">
        <line x1="-60" y1="0" x2="60" y2="0"/>
        <line x1="-54" y1="-5" x2="54" y2="-5"/>
      </g>
      <!-- har gow filling -->
      <g fill="#f8d2a0" stroke-width=".8">
        <ellipse cx="-30" cy="-2" rx="10" ry="6"/>
        <ellipse cx="-5"  cy="-3" rx="10" ry="6"/>
        <ellipse cx="20"  cy="-2" rx="10" ry="6"/>
      </g>
      <!-- ring 2 -->
      <ellipse cx="0" cy="18" rx="62" ry="14" fill="url(#yc-steam)"/>
      <line x1="-62" y1="18" x2="62" y2="18"/>
      <!-- ring 3 -->
      <ellipse cx="0" cy="36" rx="64" ry="14" fill="url(#yc-steam)"/>
      <line x1="-64" y1="36" x2="64" y2="36"/>
    </g>
  </g>

  <!-- single steamer with siu mai, right -->
  <g stroke="#3a2410" stroke-width="1.4" transform="translate(420 290)">
    <ellipse cx="0" cy="0" rx="55" ry="13" fill="url(#yc-steam)"/>
    <g fill="#c1832e" stroke-width=".8">
      <!-- 4 siu mai -->
      <ellipse cx="-32" cy="-4" rx="10" ry="7"/>
      <ellipse cx="-10" cy="-5" rx="10" ry="7"/>
      <ellipse cx="12"  cy="-4" rx="10" ry="7"/>
      <ellipse cx="32"  cy="-3" rx="10" ry="7"/>
      <!-- orange dot toppers -->
      <circle cx="-32" cy="-5" r="2.5" fill="#c14a3a"/>
      <circle cx="-10" cy="-6" r="2.5" fill="#c14a3a"/>
      <circle cx="12"  cy="-5" r="2.5" fill="#c14a3a"/>
      <circle cx="32"  cy="-4" r="2.5" fill="#c14a3a"/>
    </g>
    <ellipse cx="0" cy="14" rx="58" ry="14" fill="url(#yc-steam)"/>
    <line x1="-58" y1="14" x2="58" y2="14"/>
  </g>

  <!-- teapot, foreground centre -->
  <g stroke="#3a2410" stroke-width="1.5" transform="translate(290 320)">
    <!-- body -->
    <path d="M-40 0 q0 -45 40 -45 q40 0 40 45 q-4 18 -40 18 q-36 0 -40 -18 z"
          fill="#a04a2a"/>
    <!-- lid -->
    <ellipse cx="0" cy="-45" rx="22" ry="6" fill="#7c2c22"/>
    <ellipse cx="0" cy="-46" rx="22" ry="6" fill="none"/>
    <circle cx="0" cy="-52" r="5" fill="#c9a35a"/>
    <!-- spout -->
    <path d="M-40 -10 q-26 -2 -32 -22 q-10 -2 -10 8 q4 12 38 22 z" fill="#a04a2a"/>
    <!-- handle -->
    <path d="M40 -10 q26 -2 26 -22 q0 -10 -14 -10" fill="none" stroke-width="3"/>
    <!-- steam -->
    <g fill="none" stroke="#fff5dd" stroke-width="2" opacity=".7" stroke-linecap="round">
      <path d="M-66 -28 q4 -18 -4 -32"/>
    </g>
  </g>

  <!-- two tea cups -->
  <g stroke="#3a2410" stroke-width="1.4">
    <g transform="translate(140 330)">
      <ellipse cx="0" cy="0" rx="22" ry="8" fill="#fff5dd"/>
      <ellipse cx="0" cy="-3" rx="20" ry="7" fill="#a8753a"/>
      <ellipse cx="0" cy="0"  rx="22" ry="8" fill="none"/>
    </g>
    <g transform="translate(490 340)">
      <ellipse cx="0" cy="0" rx="22" ry="8" fill="#fff5dd"/>
      <ellipse cx="0" cy="-3" rx="20" ry="7" fill="#a8753a"/>
      <ellipse cx="0" cy="0"  rx="22" ry="8" fill="none"/>
    </g>
  </g>

  <!-- small dish with char siu bao -->
  <g stroke="#3a2410" stroke-width="1.2" transform="translate(310 280)">
    <ellipse cx="0" cy="0" rx="34" ry="10" fill="#fff5dd"/>
    <g fill="#f4d99a">
      <circle cx="-12" cy="-3" r="9"/>
      <circle cx="6"   cy="-4" r="9"/>
      <circle cx="20"  cy="-3" r="9"/>
    </g>
    <!-- bun cracks -->
    <g stroke="#a8753a" stroke-width=".8" opacity=".7">
      <path d="M-16 -8 q4 -2 8 0" fill="none"/>
      <path d="M2 -9 q4 -2 8 0" fill="none"/>
      <path d="M16 -8 q4 -2 8 0" fill="none"/>
    </g>
  </g>

  <rect x="2" y="2" width="596" height="396" fill="none"
        stroke="#3a2410" stroke-width="1" opacity=".4"/>
</svg>
"""


# =========================================================================
# Public lookup
# =========================================================================

def svg_for(topic_id: str | None, motif: str) -> str:
    """Return the best inline SVG: topic-specific override, else chapter."""
    if topic_id and topic_id in TOPIC_SVG:
        return TOPIC_SVG[topic_id].strip()
    return CHAPTER_SVG.get(motif, "").strip()


# ---------------------------------------------------------------------------
# PNG-aware lookup. Prefers a baked-in AI illustration on disk over the
# hand-drawn SVG fallback.
#
# Layout (project-root-relative):
#   assets/illustrations/<topic_id>.png   # generated by
#                                         # generate_illustrations.py
# ---------------------------------------------------------------------------

def _default_illustrations_dir() -> Path:
    """`<project_root>/assets/illustrations`."""
    return Path(__file__).resolve().parent.parent / "assets" / "illustrations"


def illustration_for(
    topic_id: str | None,
    motif: str,
    illustrations_dir: Path | None = None,
) -> str:
    """Return the best illustration for a topic.

    Resolution order, first hit wins:

    1. ``<illustrations_dir>/<topic_id>.png``  →  ``data:image/png;base64,…``
    2. ``<illustrations_dir>/<motif>.png``     →  ``data:image/png;base64,…``
    3. ``TOPIC_SVG[topic_id]``                 →  inline SVG markup
    4. ``CHAPTER_SVG[motif]``                  →  inline SVG markup

    The returned string is either ``<svg…>…</svg>`` or
    ``data:image/png;base64,…`` — the viewer's JS sniffs the first few
    chars and renders an ``<img>`` or inlines the SVG accordingly.
    """
    base = illustrations_dir or _default_illustrations_dir()
    for candidate in (topic_id, motif):
        if not candidate:
            continue
        png = base / f"{candidate}.png"
        if png.is_file():
            data = base64.b64encode(png.read_bytes()).decode("ascii")
            return f"data:image/png;base64,{data}"
    return svg_for(topic_id, motif)


# A flat sanity check used by tests.
def all_motifs() -> list[str]:
    return list(CHAPTER_SVG)


def all_topic_overrides() -> list[str]:
    return list(TOPIC_SVG)


def baked_png_ids(illustrations_dir: Path | None = None) -> list[str]:
    """List which topics currently have a baked-in AI PNG on disk."""
    base = illustrations_dir or _default_illustrations_dir()
    if not base.exists():
        return []
    return sorted(p.stem for p in base.glob("*.png"))
