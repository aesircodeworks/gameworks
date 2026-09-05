#!/usr/bin/env bash
# Shared Hermes hook helpers for Aesir Gameworks.
# Payload keys: hook_event_name, tool_name, tool_input, session_id, cwd, extra

aesir_read_payload() {
  AESIR_PAYLOAD=$(cat)
}

aesir_json_get() {
  python3 -c 'import json,sys
path=sys.argv[1].split(".")
raw=sys.stdin.read() or "{}"
try:
    data=json.loads(raw)
except Exception:
    print("")
    raise SystemExit(0)
cur=data
for part in path:
    if isinstance(cur, dict):
        cur=cur.get(part)
    else:
        cur=None
        break
if cur is None:
    print("")
else:
    print(cur if not isinstance(cur,(dict,list)) else json.dumps(cur))
' "$1" <<<"$AESIR_PAYLOAD"
}

aesir_emit() {
  printf '%s\n' "$1"
}

aesir_emit_empty() {
  printf '%s\n' '{}'
}

aesir_block() {
  python3 -c 'import json,sys; print(json.dumps({"action":"block","message":sys.argv[1]}))' "$1"
}

aesir_context() {
  python3 -c 'import json,sys; print(json.dumps({"context":sys.argv[1]}))' "$1"
}

aesir_once_file() {
  local sid cwd
  sid=$(aesir_json_get session_id)
  cwd=$(aesir_json_get cwd)
  [ -z "$cwd" ] && cwd="."
  mkdir -p "$cwd/production/session-state" 2>/dev/null || true
  printf '%s\n' "${cwd}/production/session-state/.aesir-${1}-${sid:-unknown}"
}

aesir_is_game_workspace() {
  local cwd
  cwd=$(aesir_json_get cwd)
  [ -z "$cwd" ] && cwd="."
  if [ -f "$cwd/distribution.yaml" ] || [ -d "$cwd/skills/studio" ]; then
    return 1
  fi
  return 0
}
