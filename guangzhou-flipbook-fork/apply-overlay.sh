#!/usr/bin/env bash
# =============================================================================
# Guangzhou Flipbook · apply-overlay.sh
# -----------------------------------------------------------------------------
# Idempotently copies the Guangzhou-specific overlay onto a cloned openflipbook
# tree. Discovers upstream paths dynamically (uses `find`) so it stays robust
# across upstream refactors.
#
# What it does:
#   - drops prompts/         into <upstream>/apps/modal-backend/prompts/
#   - drops themes/          into <upstream>/apps/web/public/themes/
#   - copies env templates   to apps/{web/.env.local, modal-backend/.env}
#     **only if the target does not already exist** (so it never wipes your
#     filled-in keys)
#
# Re-run after `git pull` upstream. Safe to run repeatedly.
#
# Usage:
#   ./apply-overlay.sh [<upstream-dir>]
#   (defaults to ./openflipbook relative to this script)
# =============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OVERLAY="${SCRIPT_DIR}/overlay"
UP="${1:-${SCRIPT_DIR}/openflipbook}"

C_OK="\033[1;32m"; C_INFO="\033[1;36m"; C_WARN="\033[1;33m"; C_ERR="\033[1;31m"; C_OFF="\033[0m"
say()  { printf "${C_INFO}▸${C_OFF} %s\n" "$*"; }
ok()   { printf "${C_OK}✓${C_OFF} %s\n" "$*"; }
warn() { printf "${C_WARN}!${C_OFF} %s\n" "$*"; }
fail() { printf "${C_ERR}✗${C_OFF} %s\n" "$*" >&2; exit 1; }

[[ -d "$UP" ]]  || fail "Upstream directory not found: $UP"
[[ -d "$OVERLAY" ]] || fail "Overlay directory missing: $OVERLAY"

# -- locate upstream sub-dirs flexibly ----------------------------------------
discover() {
  # $1: glob pattern relative to upstream; prints first matching path or empty
  find "$UP" -path '*/node_modules' -prune -o -type d -name "$1" -print 2>/dev/null \
    | head -n1
}

BACKEND_DIR="$(discover 'modal-backend' || true)"
WEB_DIR="$(discover 'web' || true)"

# Fallback: walk apps/* directly
if [[ -z "$BACKEND_DIR" && -d "$UP/apps/modal-backend" ]]; then
  BACKEND_DIR="$UP/apps/modal-backend"
fi
if [[ -z "$WEB_DIR" && -d "$UP/apps/web" ]]; then
  WEB_DIR="$UP/apps/web"
fi

[[ -n "$BACKEND_DIR" ]] || warn "Couldn't locate modal-backend dir; skipping backend overlay."
[[ -n "$WEB_DIR" ]]     || warn "Couldn't locate web dir; skipping web overlay."

# -- 1. backend: prompts + env -----------------------------------------------
if [[ -n "$BACKEND_DIR" ]]; then
  say "Backend dir: $BACKEND_DIR"

  mkdir -p "$BACKEND_DIR/prompts"
  cp -f "$OVERLAY/prompts/guangzhou-system.zh.md" "$BACKEND_DIR/prompts/"
  cp -f "$OVERLAY/prompts/guangzhou-system.en.md" "$BACKEND_DIR/prompts/"
  ok "Wrote prompts → $BACKEND_DIR/prompts/"

  ENV_TARGET="$BACKEND_DIR/.env"
  ENV_TEMPLATE="$OVERLAY/env/modal-backend.env.example"
  if [[ -e "$ENV_TARGET" ]]; then
    warn "Backend .env already exists; leaving it untouched."
    warn "  (template available at $ENV_TEMPLATE for comparison)"
    cp -f "$ENV_TEMPLATE" "$BACKEND_DIR/.env.guangzhou.example"
    ok "Wrote .env.guangzhou.example for reference."
  else
    cp -f "$ENV_TEMPLATE" "$ENV_TARGET"
    warn "Created $ENV_TARGET — you must fill FAL_KEY and OPENROUTER_API_KEY."
  fi
fi

# -- 2. web: theme + seeds + env ---------------------------------------------
if [[ -n "$WEB_DIR" ]]; then
  say "Web dir: $WEB_DIR"

  mkdir -p "$WEB_DIR/public/themes"
  cp -f "$OVERLAY/theme/guangzhou.css"            "$WEB_DIR/public/themes/"
  cp -f "$OVERLAY/seeds/seed-queries.json"        "$WEB_DIR/public/themes/"
  ok "Wrote theme + seeds → $WEB_DIR/public/themes/"

  ENV_TARGET="$WEB_DIR/.env.local"
  ENV_TEMPLATE="$OVERLAY/env/web.env.local.example"
  if [[ -e "$ENV_TARGET" ]]; then
    warn "Web .env.local already exists; leaving it untouched."
    cp -f "$ENV_TEMPLATE" "$WEB_DIR/.env.local.guangzhou.example"
    ok "Wrote .env.local.guangzhou.example for reference."
  else
    cp -f "$ENV_TEMPLATE" "$ENV_TARGET"
    warn "Created $ENV_TARGET — you must fill R2 creds + MONGODB_URI."
  fi
fi

# -- 3. summary ---------------------------------------------------------------
cat <<EOF

${C_OK}Overlay applied.${C_OFF}

  To wire the theme into the Next.js app, add this single import once in
  apps/web/src/app/layout.tsx (or equivalent root layout):

      import "../../public/themes/guangzhou.css";

  And in your empty-state component, fetch the seeds JSON:

      fetch("/themes/seed-queries.json").then(r => r.json()).then(setSeeds);

  And in your page-planner call (backend), read the system prompt:

      with open(os.environ["GUANGZHOU_SYSTEM_PROMPT_PATH"]) as f:
          system = f.read()

  These are the only three integration hooks. Everything else is plain
  drop-in.
EOF
