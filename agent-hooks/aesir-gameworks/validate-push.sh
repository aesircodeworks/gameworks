#!/usr/bin/env bash
set -euo pipefail
. "$(cd "$(dirname "$0")" && pwd)/lib.sh"
aesir_read_payload
command=$(aesir_json_get tool_input.command)
case "$command" in
  git\ push*|git\ push)
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
force=0
echo "$command" | grep -qE '(--force|-f)([[:space:]]|$)' && force=1
branch=$(git -C "$cwd" rev-parse --abbrev-ref HEAD 2>/dev/null || true)
protected=0
for name in develop main master; do
  if [ "$branch" = "$name" ] || echo "$command" | grep -qE "[[:space:]]${name}([[:space:]]|$)"; then
    protected=1
    MATCHED=$name
  fi
done
if [ "$force" -eq 1 ] && [ "$protected" -eq 1 ]; then
  aesir_block "BLOCKED: force push to protected branch '${MATCHED:-unknown}'"
  exit 2
fi
aesir_emit_empty
exit 0
