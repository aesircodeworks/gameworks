#!/usr/bin/env bash
set -euo pipefail
. "$(cd "$(dirname "$0")" && pwd)/lib.sh"
aesir_read_payload
if ! aesir_is_game_workspace; then
  aesir_emit_empty
  exit 0
fi
marker=$(aesir_once_file session-start)
if [ -f "$marker" ]; then
  aesir_emit_empty
  exit 0
fi
touch "$marker" 2>/dev/null || true
cwd=$(aesir_json_get cwd)
[ -z "$cwd" ] && cwd="."
branch=$(git -C "$cwd" rev-parse --abbrev-ref HEAD 2>/dev/null || echo "no-git")
aesir_context "Aesir session: workspace=$cwd branch=$branch. Inspect game-workspace sprint/milestone files if present. No writes."
exit 0
