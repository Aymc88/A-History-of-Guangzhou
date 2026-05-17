#!/usr/bin/env bash
# =============================================================================
# Guangzhou Flipbook · setup.sh
# -----------------------------------------------------------------------------
# One-shot installer that:
#   1. checks prereqs (only git is hard-required; everything else is soft)
#   2. clones upstream openflipbook into ./openflipbook   (skips if present)
#   3. runs apply-overlay.sh to drop Guangzhou customisations on top
#   4. prints the next steps the user has to do by hand (API keys, etc.)
#
# Everything written by this script is *additive*: it never edits files in
# upstream openflipbook, only adds new ones under prompts/, themes/, etc.
# To roll back, delete the cloned directory.
#
# Usage:
#   ./setup.sh                       # interactive, default ./openflipbook
#   ./setup.sh /path/to/somewhere    # clone into a custom directory
#   ./setup.sh -y                    # non-interactive; skip the y/N prompt
#   ./setup.sh -y /custom/path       # both
# =============================================================================
set -euo pipefail

# parse flags ------------------------------------------------------------------
ASSUME_YES=0
POSARGS=()
for arg in "$@"; do
  case "$arg" in
    -y|--yes) ASSUME_YES=1 ;;
    -h|--help)
      cat <<'HELP'
Guangzhou Flipbook · setup.sh

Clones eren23/openflipbook into ./openflipbook and lays the Guangzhou
overlay (prompts + theme + env templates) on top. The overlay is purely
additive — it never edits upstream files.

Usage:
  ./setup.sh                    interactive, default target ./openflipbook
  ./setup.sh /custom/path       clone into a custom directory
  ./setup.sh -y                 non-interactive (skip the y/N prompt)
  ./setup.sh -y /custom/path    both

Prereqs:
  HARD   git
  LATER  docker  (only if you want `docker compose up`)
         pnpm    (only for non-docker dev loop)
         uv      (only for non-docker dev loop)
         modal   (only to deploy to Modal cloud)
HELP
      exit 0 ;;
    *) POSARGS+=("$arg") ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OVERLAY_DIR="${SCRIPT_DIR}/overlay"
TARGET_DIR="${POSARGS[0]:-${SCRIPT_DIR}/openflipbook}"
UPSTREAM_REPO="https://github.com/eren23/openflipbook"

C_OK="\033[1;32m"; C_INFO="\033[1;36m"; C_WARN="\033[1;33m"; C_ERR="\033[1;31m"; C_DIM="\033[2m"; C_OFF="\033[0m"
say()    { printf "${C_INFO}▸${C_OFF} %s\n" "$*"; }
ok()     { printf "${C_OK}✓${C_OFF} %s\n" "$*"; }
warn()   { printf "${C_WARN}!${C_OFF} %s\n" "$*"; }
dim()    { printf "${C_DIM}  %s${C_OFF}\n" "$*"; }
fatal()  { printf "${C_ERR}✗${C_OFF} %s\n" "$*" >&2; exit 1; }

# -- 1. prereqs ---------------------------------------------------------------
# Tiered:
#   HARD     -- git           (no way to clone without it)
#   LATER    -- docker        (only needed to `docker compose up`)
#   LATER    -- pnpm / uv     (only needed for non-docker dev loop)
#   LATER    -- modal         (only needed if deploying to Modal cloud)
# We never abort on LATER tools; we just remind the user what they unlock.
say "Checking prerequisites…"

probe_tool() {
  local name="$1" purpose="$2" how="$3"
  if command -v "$name" >/dev/null 2>&1; then
    ok "$name  $(command -v "$name")"
    return 0
  else
    # Build the colour codes inside printf's format string so they aren't
    # eaten by %s expansion.
    printf "${C_WARN}!${C_OFF} %s ${C_DIM}— needed for %s${C_OFF}\n" \
      "$name not found" "$purpose"
    dim "install: $how"
    return 1
  fi
}

probe_tool git    "cloning upstream"          "system git, or 'brew install git'" \
  || fatal "git is required for this script. Install it and re-run."

probe_tool docker "running 'docker compose up'  (the one-shot dev path)" \
  "Docker Desktop — https://www.docker.com/products/docker-desktop/" \
  || NEED_DOCKER=1
probe_tool pnpm   "running the Next.js dev server outside docker" \
  "brew install pnpm" || true
probe_tool uv     "creating the Python venv for the modal-backend outside docker" \
  "brew install uv  (or: curl -LsSf https://astral.sh/uv/install.sh | sh)" || true
probe_tool modal  "deploying the streaming backend to Modal cloud (optional)" \
  "brew install modal-cli  (or: pip install modal)" || true

if [[ "${NEED_DOCKER:-0}" == "1" ]]; then
  echo
  warn "Without docker you'll have to start Mongo, the backend and the web app"
  warn "yourself instead of 'docker compose up'. Setup itself still works fine."
fi

# Confirm — but only if interactive AND something soft is missing.
if [[ "$ASSUME_YES" == "0" && -t 0 && "${NEED_DOCKER:-0}" == "1" ]]; then
  echo
  printf "Proceed with clone + overlay anyway? [Y/n] "
  read -r ans
  case "${ans:-Y}" in
    [Nn]*) fatal "Aborted by user. Re-run with -y to skip this prompt." ;;
  esac
fi

# -- 2. clone openflipbook ----------------------------------------------------
if [[ -d "$TARGET_DIR/.git" ]]; then
  ok "Upstream already cloned at: $TARGET_DIR"
  say "Pulling latest…"
  git -C "$TARGET_DIR" pull --ff-only || warn "git pull failed; continuing with current checkout"
else
  say "Cloning $UPSTREAM_REPO  →  $TARGET_DIR"
  git clone --depth 50 "$UPSTREAM_REPO" "$TARGET_DIR"
fi

# -- 3. apply overlay ---------------------------------------------------------
say "Applying Guangzhou overlay…"
"$SCRIPT_DIR/apply-overlay.sh" "$TARGET_DIR"

# -- 4. next steps ------------------------------------------------------------
cat <<EOF

${C_OK}===========================================================================${C_OFF}
  Guangzhou Flipbook fork is ready at:
    ${TARGET_DIR}

  Next:
    1. Fill the keys you skipped in:
         ${TARGET_DIR}/apps/modal-backend/.env
         ${TARGET_DIR}/apps/web/.env.local

       You need at minimum:
         · FAL_KEY               (https://fal.ai/dashboard/keys)
         · OPENROUTER_API_KEY    (https://openrouter.ai/keys)
         · R2_*                  (Cloudflare R2, or any S3-compatible)
         · MONGODB_URI           (compose ships one; leave default if you use it)

    2. Spin everything up (mongo + backend + web):
         cd "${TARGET_DIR}"
         docker compose up -d --build
         open http://localhost:3000/play

    3. To re-apply the Guangzhou overlay later (after git pull etc.):
         "${SCRIPT_DIR}/apply-overlay.sh" "${TARGET_DIR}"

  Tips:
    · The overlay only adds files under prompts/, themes/ and uses *.example
      env templates — it never overwrites upstream code.
    · Delete ${TARGET_DIR} to wipe everything and start over.
${C_OK}===========================================================================${C_OFF}
EOF
