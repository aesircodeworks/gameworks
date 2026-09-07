#!/usr/bin/env bash
set -euo pipefail
. "$(cd "$(dirname "$0")" && pwd)/lib.sh"
aesir_read_payload
cwd=$(aesir_json_get cwd)
[ -z "$cwd" ] && cwd="."
if aesir_is_game_workspace; then
  logdir="$cwd/production/session-logs"
  mkdir -p "$logdir" 2>/dev/null || true
  python3 -c 'import json,sys,datetime
p=json.loads(sys.stdin.read() or "{}")
open(sys.argv[1],"a",encoding="utf-8").write(json.dumps({"event":"session_end","ts":datetime.datetime.utcnow().isoformat(),"session":p.get("session_id"),"cwd":p.get("cwd")})+"\n")
' "$logdir/sessions.jsonl" <<<"$AESIR_PAYLOAD" 2>/dev/null || true
fi
notify="$(cd "$(dirname "$0")" && pwd)/notify-session.sh"
if [ -x "$notify" ] || [ -f "$notify" ]; then
  printf '%s' "$AESIR_PAYLOAD" | bash "$notify" >/dev/null 2>&1 || true
fi
aesir_emit_empty
exit 0
