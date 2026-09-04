#!/usr/bin/env bash
set -euo pipefail
. "$(cd "$(dirname "$0")" && pwd)/lib.sh"
aesir_read_payload
path=$(aesir_json_get tool_input.path)
name=$(aesir_json_get tool_input.name)
case "$path$name" in
  *aesir-*|*skills/aesir*)
    aesir_context "Aesir skill changed. Consider running /aesir-skill-test. No files were mutated by this hook."
    ;;
  *)
    aesir_emit_empty
    ;;
esac
exit 0
