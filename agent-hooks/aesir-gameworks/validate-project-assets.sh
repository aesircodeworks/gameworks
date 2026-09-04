#!/usr/bin/env bash
set -euo pipefail
. "$(cd "$(dirname "$0")" && pwd)/lib.sh"
aesir_read_payload
path=$(aesir_json_get tool_input.path)
case "$path" in
  */assets/*|assets/*)
    aesir_emit_empty
    ;;
  *)
    aesir_emit_empty
    ;;
esac
exit 0
