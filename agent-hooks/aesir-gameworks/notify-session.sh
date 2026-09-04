#!/usr/bin/env bash
set -euo pipefail
. "$(cd "$(dirname "$0")" && pwd)/lib.sh"
aesir_read_payload
if command -v osascript >/dev/null 2>&1; then
  osascript -e 'display notification "Aesir session ended" with title "Aesir Gameworks"' >/dev/null 2>&1 || true
fi
aesir_emit_empty
exit 0
