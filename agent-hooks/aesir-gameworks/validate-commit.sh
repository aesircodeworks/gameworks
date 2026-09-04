#!/usr/bin/env bash
set -euo pipefail
# shellcheck source=lib.sh
. "$(cd "$(dirname "$0")" && pwd)/lib.sh"
aesir_read_payload
command=$(aesir_json_get tool_input.command)
case "$command" in
  git\ commit*|git\ commit)
    ;;
  *)
    aesir_emit_empty
    exit 0
    ;;
esac
cwd=$(aesir_json_get cwd)
[ -z "$cwd" ] && cwd="."
if ! git -C "$cwd" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  aesir_emit_empty
  exit 0
fi
staged=$(git -C "$cwd" diff --cached --name-only 2>/dev/null || true)
[ -z "$staged" ] && { aesir_emit_empty; exit 0; }
python_cmd=""
for cmd in python3 python py; do
  if command -v "$cmd" >/dev/null 2>&1; then python_cmd=$cmd; break; fi
done
while IFS= read -r file; do
  [ -z "$file" ] && continue
  path="$cwd/$file"
  case "$file" in
    assets/data/*.json)
      if [ -n "$python_cmd" ] && [ -f "$path" ]; then
        if ! "$python_cmd" -m json.tool "$path" >/dev/null 2>&1; then
          aesir_block "BLOCKED: $file is not valid JSON"
          exit 2
        fi
      fi
      ;;
    src/*)
      if [ -f "$path" ] && grep -nE '(TODO|FIXME|HACK)[^(]' "$path" >/dev/null 2>&1; then
        aesir_block "BLOCKED: $file has TODO/FIXME without owner tag. Use TODO(name) format."
        exit 2
      fi
      ;;
  esac
done <<<"$staged"
aesir_emit_empty
exit 0
