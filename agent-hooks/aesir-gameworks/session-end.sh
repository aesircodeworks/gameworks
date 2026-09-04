#!/usr/bin/env bash
set -euo pipefail
. "$(cd "$(dirname "$0")" && pwd)/lib.sh"
aesir_read_payload
aesir_emit_empty
exit 0
