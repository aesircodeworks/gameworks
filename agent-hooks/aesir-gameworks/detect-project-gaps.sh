#!/usr/bin/env bash
set -euo pipefail
. "$(cd "$(dirname "$0")" && pwd)/lib.sh"
aesir_read_payload
if ! aesir_is_game_workspace; then
  aesir_emit_empty
  exit 0
fi
marker=$(aesir_once_file gaps)
if [ -f "$marker" ]; then
  aesir_emit_empty
  exit 0
fi
touch "$marker" 2>/dev/null || true
cwd=$(aesir_json_get cwd)
[ -z "$cwd" ] && cwd="."
gaps=""
[ -f "$cwd/design/gdd/game-concept.md" ] || gaps="${gaps}missing game-concept; "
aesir_context "Aesir gap check (once): ${gaps:-no structural gaps detected}."
exit 0
