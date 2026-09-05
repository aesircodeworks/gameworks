---
name: gameworks
description: Use when routing Aesir studio workflows, roles, and collaboration rules.
version: 1.0.0
author: Donchitos; Hermes adaptation by Aesir Gameworks
license: MIT
metadata:
  hermes:
    tags:
    - aesir-gameworks
    - game-development
    - core
    related_skills:
    - project-bootstrap
    - project-templates
    - engine-reference
    - framework-qa
    - studio-status
    - memory-policy
---

> **Upstream:** Derived from Claude Code Game Studios by Donchitos (MIT). https://github.com/Donchitos/Claude-Code-Game-Studios

# Aesir Gameworks

Load this skill for studio operating context. Use workflows only in the selected **game workspace**, never treat `$HERMES_HOME` or this distribution repository as the game.

## Collaboration

Question → Options → Decision → Draft → Approval → Write. Do not write without the user's approval of the stated path or changeset.

## Linked references

Load with `skill_view('gameworks', file_path='...')` when needed:

- `references/quick-start.md` — first-run orientation
- `references/workflow-guide.md` — end-to-end studio pipeline
- `references/workflow-catalog.yaml` — command catalog
- `references/agent-roster.md` — role roster
- `references/agent-coordination-map.md` — escalation
- `references/director-gates.md` — director verdicts
- `references/coordination-rules.md` — multi-agent rules
- `references/coding-standards.md` — code standards for game workspaces
- `references/context-management.md` — what to load
- `references/directory-structure.md` — game workspace layout
- `references/hooks-reference.md` — lifecycle hooks
- `references/rules-reference.md` — path rules index
- `references/setup-requirements.md` — prerequisites
- `references/skills-reference.md` — workflow index
- `references/technical-preferences.md` — engine/language placeholders for a game workspace
- `references/collaborative-design-principle.md` — approval model
- `references/review-workflow.md` — review routing
- `examples/README.md` — worked sessions
- `references/upstream/` — historical CCGS material; not executable

## Delegation

Batch independent `delegate_task` calls. Pass role text in `delegate_task.context`. Blocked child results halt dependent phases.
