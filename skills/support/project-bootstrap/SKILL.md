---
name: project-bootstrap
description: Use when creating a new game workspace for Aesir workflows.
version: 1.0.0
author: Donchitos; Hermes adaptation by Aesir Gameworks
license: MIT
metadata:
  hermes:
    tags:
    - aesir-gameworks
    - game-development
    - bootstrap
    related_skills:
    - gameworks
    - project-templates
---

> **Upstream:** Derived from Claude Code Game Studios by Donchitos (MIT). https://github.com/Donchitos/Claude-Code-Game-Studios

# Project bootstrap

Create project-local artifacts only after the user chooses a workspace path and approves each file.

This distribution repository and `$HERMES_HOME` are not game projects.

## Linked files

- `templates/AGENTS.md` — game-workspace agent instructions (Hermes-native; rewritten from the CCGS local template)

## Required behavior

1. Ask for the target game workspace with `clarify` if it is not already chosen.
2. Show the exact paths to create.
3. Wait for approval.
4. Write only approved paths, using `project-templates` for document scaffolds.
