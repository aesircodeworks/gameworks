#!/usr/bin/env bash
set -euo pipefail
. "$(cd "$(dirname "$0")" && pwd)/lib.sh"
aesir_read_payload
cwd=$(aesir_json_get cwd)
[ -z "$cwd" ] && cwd="."
logdir="$cwd/production/session-logs"
mkdir -p "$logdir" 2>/dev/null || true
python3 -c 'import json,sys,datetime
p=json.loads(sys.stdin.read() or "{}")
open(sys.argv[1],"a",encoding="utf-8").write(json.dumps({"event":"subagent_start","ts":datetime.datetime.utcnow().isoformat(),"session":p.get("session_id")})+"\n")
' "$logdir/subagents.jsonl" <<<"$AESIR_PAYLOAD" 2>/dev/null || true
aesir_emit_empty
exit 0
