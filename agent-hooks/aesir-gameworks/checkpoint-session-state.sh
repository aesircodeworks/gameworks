#!/usr/bin/env bash
set -euo pipefail
. "$(cd "$(dirname "$0")" && pwd)/lib.sh"
aesir_read_payload
cwd=$(aesir_json_get cwd)
[ -z "$cwd" ] && cwd="."
mkdir -p "$cwd/production/session-state" 2>/dev/null || true
if aesir_is_game_workspace; then
  date > "$cwd/production/session-state/.aesir-checkpoint" 2>/dev/null || true
fi
aesir_emit_empty
exit 0
