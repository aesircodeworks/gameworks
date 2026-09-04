#!/usr/bin/env bash
# Aesir studio status — read-only, does not replace the Hermes TUI status bar.
set -euo pipefail
cwd=${1:-.}
cwd=$(cd "$cwd" && pwd)

if [ -f "$cwd/distribution.yaml" ] || [ -d "$cwd/skills/aesir-core" ]; then
  echo "workspace: profile-distribution ($cwd)"
  echo "stage: n/a (not a game project)"
  echo "sprint: n/a"
  echo "milestone: n/a"
  echo "branch: $(git -C "$cwd" rev-parse --abbrev-ref HEAD 2>/dev/null || echo none)"
  echo "blockers: none"
  echo "source-files: n/a"
  exit 0
fi

stage=""
[ -f "$cwd/production/stage.txt" ] && stage=$(head -1 "$cwd/production/stage.txt" | tr -d '\r\n')
if [ -z "$stage" ]; then
  if [ -f "$cwd/design/gdd/game-concept.md" ]; then stage="Concept"; else stage="New"; fi
  [ -f "$cwd/design/gdd/systems-index.md" ] && stage="Systems Design"
  tech=""
  for candidate in "$cwd/docs/technical-preferences.md" "$cwd/AGENTS.md"; do
    if [ -f "$candidate" ]; then
      if grep -m1 -E '^- \*\*Engine\*\*:|^\*\*Engine\*\*:' "$candidate" >/dev/null 2>&1; then
        tech=$(grep -m1 -E '^- \*\*Engine\*\*:|^\*\*Engine\*\*:' "$candidate" || true)
      fi
    fi
  done
  if [ -n "$tech" ] && ! echo "$tech" | grep -q "TO BE CONFIGURED"; then
    stage="Technical Setup"
  fi
fi
sprint="none"
milestone="none"
[ -d "$cwd/production/sprints" ] && sprint=$(ls "$cwd/production/sprints" 2>/dev/null | tail -1)
[ -f "$cwd/production/milestones.md" ] && milestone=present
branch=$(git -C "$cwd" rev-parse --abbrev-ref HEAD 2>/dev/null || echo none)
src=0
[ -d "$cwd/src" ] && src=$(find "$cwd/src" -type f 2>/dev/null | wc -l | tr -d ' ')
echo "workspace: game ($cwd)"
echo "stage: $stage"
echo "sprint: $sprint"
echo "milestone: $milestone"
echo "branch: $branch"
echo "blockers: inspect production/ and design/ for unresolved FAIL verdicts"
echo "source-files: $src"
