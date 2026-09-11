---
name: studio-status
description: Use when reporting a game workspace's studio status.
version: 1.0.0
author: Donchitos; Hermes adaptation by Aesir Codeworks
license: MIT
metadata:
  hermes:
    tags:
    - aesir-gameworks
    - game-development
    - status
    related_skills:
    - gameworks
---

> **Upstream:** Derived from Claude Code Game Studios by Donchitos (MIT). https://github.com/Donchitos/Claude-Code-Game-Studios

# Studio status

Read-only. Does not replace Hermes' native TUI status bar.

Run `${HERMES_SKILL_DIR}/scripts/status.sh <game-workspace>`.

Reports stage, sprint, milestone, branch, blockers, and source-file counts for the target workspace. A profile distribution repository must not be reported as a game in Production.
