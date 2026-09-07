#!/usr/bin/env bash
set -euo pipefail
. "$(cd "$(dirname "$0")" && pwd)/lib.sh"
aesir_read_payload
if ! aesir_is_game_workspace; then
  aesir_emit_empty
  exit 0
fi
marker=$(aesir_once_file session-start)
if [ -f "$marker" ]; then
  aesir_emit_empty
  exit 0
fi
touch "$marker" 2>/dev/null || true
cwd=$(aesir_json_get cwd)
[ -z "$cwd" ] && cwd="."
branch=$(git -C "$cwd" rev-parse --abbrev-ref HEAD 2>/dev/null || echo "no-git")
commits=$(git -C "$cwd" log -5 --oneline 2>/dev/null | tr '\n' '; ' || true)
sprint=""
if [ -d "$cwd/production/sprints" ]; then
  sprint=$(ls -1 "$cwd/production/sprints" 2>/dev/null | tail -1 || true)
fi
active="absent"
if [ -f "$cwd/production/session-state/active.md" ]; then
  active="present"
fi
stage=""
[ -f "$cwd/production/stage.txt" ] && stage=$(head -1 "$cwd/production/stage.txt" | tr -d '\r\n')
msg="Aesir session: workspace=$cwd branch=$branch"
[ -n "$stage" ] && msg="$msg stage=$stage"
[ -n "$sprint" ] && msg="$msg sprint=$sprint"
msg="$msg active.md=$active"
[ -n "$commits" ] && msg="$msg recent=[$commits]"
msg="$msg Inspect game-workspace sprint/milestone files if present. No writes."
aesir_context "$msg"
exit 0
