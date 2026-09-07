---
name: project-bootstrap
description: Use when creating an Aesir game workspace.
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

Create project-local artifacts only within the user's approved workspace and changeset. An explicit request naming the targets supplies approval; do not ask again per file. Load `gameworks` `references/collaborative-design-principle.md` when scope is unclear.

This distribution repository and `$HERMES_HOME` are not game projects.

## Linked files

- `templates/AGENTS.md` — game-workspace agent instructions (Hermes-native; rewritten from the CCGS local template)

## Required behavior

1. Ask for the target game workspace with `clarify` if it is not already chosen.
2. Identify the exact paths to create.
3. Obtain approval if the request has not already supplied it; ask about expanded scope.
4. Write only approved paths, using `project-templates` for document scaffolds.
