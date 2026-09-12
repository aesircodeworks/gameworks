---
name: gameworks
description: Choose Aesir workflows or approval scope.
version: 1.0.0
author: Donchitos; Hermes adaptation by Aesir Codeworks
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

An explicit request to implement a stated changeset authorizes its edits and verification; do not repeat per-file approval. Read-only requests do not authorize writes. Ask at new scope or unresolved decision boundaries, and preserve substantive workflow gates.

Load `references/collaborative-design-principle.md` when determining approval scope, planning design decisions, or coordinating delegated writes. It defines the canonical policy, including Question → Options → Decision → Draft → Approval → Write for unresolved design choices.

## Task routing

Start with the matching task workflow or path rule; load additional relevant skills as required. Consultation does not require delegation.

| Task | Start here | Specialist when needed |
|---|---|---|
| Game code review | `code-review`; matching path rule | `lead-programmer` for cross-system findings |
| UI/input | `ux-review` or `team-ui`; `ui-code` | `ui-programmer` for implementation; matching engine UI specialist |
| Simulation/timing | `code-review`; `gameplay-code` | `gameplay-programmer`; `performance-analyst` for measured timing issues |
| Audio | `team-audio` or `asset-spec` | `audio-director` for direction; `sound-designer` for assets |
| Game design | `quick-design` or `design-system` | `game-designer`; `systems-designer` for interacting mechanics |
| Framework/Hermes | `framework-qa`; installed `hermes-agent` for runtime questions | `tools-programmer` for framework tooling; keep game workspaces separate |
| Engine APIs | `engine-reference` | Existing Godot, Unity, Unreal, or Three.js specialist matching the requested API |

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
- `references/technical-preferences.md` — template copied into the game workspace as `docs/technical-preferences.md`
- `references/collaborative-design-principle.md` — approval model
- `references/review-workflow.md` — review routing
- `examples/README.md` — worked sessions

## Delegation

Batch independent `delegate_task` calls. Pass role text, approved scope, and decisions in `delegate_task.context`. Do not pass Claude Code `subagent_type` or `Task` fields.

**Parent (talks to the user):** use `clarify` for unresolved design choices. Question → Options → Decision → Draft → Approval → Write.

**Child (running under `delegate_task`):** `clarify` is unavailable. Do not interview the user. Return only to the coordinator. If a director gate was requested, begin with `[GATE-ID]: TOKEN` on its own line, then:

```
status: ...
findings: ...
recommendations: ...
blockers: ...
artifacts: ...
```

Coordinators parse the first-line gate token when present, then the five fields. Surface `blockers` and missing decisions to the user; do not assume the child asked them. Blocked child results halt dependent phases.
