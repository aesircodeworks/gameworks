#!/usr/bin/env bash
set -euo pipefail
. "$(cd "$(dirname "$0")" && pwd)/lib.sh"
aesir_read_payload
if ! aesir_is_game_workspace; then
  aesir_emit_empty
  exit 0
fi
marker=$(aesir_once_file restore)
if [ -f "$marker" ]; then
  aesir_emit_empty
  exit 0
fi
touch "$marker" 2>/dev/null || true
cwd=$(aesir_json_get cwd)
[ -z "$cwd" ] && cwd="."
state="$cwd/production/session-state/active.md"
if [ -f "$state" ]; then
  aesir_context "Restored existing game-workspace session state from production/session-state/active.md. Hermes has no post-compression hook; this runs on first pre_llm_call."
else
  aesir_emit_empty
fi
exit 0
