#!/usr/bin/env bash
set -euo pipefail
. "$(cd "$(dirname "$0")" && pwd)/lib.sh"
aesir_read_payload
if ! aesir_is_game_workspace; then
  aesir_emit_empty
  exit 0
fi
path=$(aesir_json_get tool_input.path)
[ -z "$path" ] && { aesir_emit_empty; exit 0; }
case "$path" in
  */assets/*|assets/*)
    ;;
  *)
    aesir_emit_empty
    exit 0
    ;;
esac
base=$(basename "$path")
case "$base" in
  *" "*)
    aesir_block "BLOCKED: asset filename has spaces: $path"
    exit 2
    ;;
esac
cwd=$(aesir_json_get cwd)
[ -z "$cwd" ] && cwd="."
full="$path"
case "$path" in
  /*) ;;
  *) full="$cwd/$path" ;;
esac
case "$path" in
  *.json)
    python_cmd=""
    for cmd in python3 python py; do
      if command -v "$cmd" >/dev/null 2>&1; then python_cmd=$cmd; break; fi
    done
    if [ -n "$python_cmd" ] && [ -f "$full" ]; then
      if ! "$python_cmd" -m json.tool "$full" >/dev/null 2>&1; then
        aesir_block "BLOCKED: $path is not valid JSON"
        exit 2
      fi
    fi
    ;;
esac
aesir_emit_empty
exit 0
