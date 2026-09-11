---
name: onboard
description: Onboard a contributor to a project role.
version: 1.0.0
author: Donchitos; Hermes adaptation by Aesir Codeworks
license: MIT
metadata:
  hermes:
    tags:
    - aesir-gameworks
    - game-development
    - workflow
    related_skills:
    - gameworks
---

> **Upstream:** Derived from Claude Code Game Studios by Donchitos (MIT). https://github.com/Donchitos/Claude-Code-Game-Studios — adapted for Hermes Agent / Aesir Gameworks.

## Phase 1: Load Project Context

**Model tier:** Light

Read `AGENTS.md` for project overview and standards.

Read `docs/technical-preferences.md` if present for engine, language, and specialist routing. If the file is missing, treat the engine as unset.

If a specific role is specified, load that role skill from the installed profile with `skill_view('<role>')` (`skills/agents/<role>/SKILL.md`). Do not read `(game-workspace)/agents/` — role skills live in the profile, not the game workspace.

---

## Phase 2: Scan Relevant Area

- For programmers: scan `src/` for architecture, patterns, key files
- For designers: scan `design/` for existing design documents
- For narrative: scan `design/narrative/` for world-building and story docs
- For QA: scan `tests/` for existing test coverage
- For production: scan `production/` for current sprint and milestone

Read recent changes (git log if available) to understand current momentum.

---

## Phase 3: Generate Onboarding Document

```markdown
# Onboarding: [Role/Area]

## Project Summary
[2-3 sentence summary of what this game is and its current state]

## Your Role
[What this role does on this project, key responsibilities, who you report to]

## Project Architecture
[Relevant architectural overview for this role]

### Key Directories
| Directory | Contents | Your Interaction |
|-----------|----------|-----------------|

### Key Files
| File | Purpose | Read Priority |
|------|---------|--------------|

## Current Standards and Conventions
[Summary of conventions relevant to this role from `AGENTS.md`, `docs/technical-preferences.md`, and the role skill]

## Current State of Your Area
[What has been built, what is in progress, what is planned next]

## Current Sprint Context
[What the team is working on now and what is expected of this role]

## Key Dependencies
[What other roles/systems this role interacts with most]

## Common Pitfalls
[Things that trip up new contributors in this area]

## First Tasks
[Suggested first tasks to get oriented and productive]

1. [Read these documents first]
2. [Review this code/content]
3. [Start with this small task]

## Questions to Ask
[Questions the new contributor should ask to get fully oriented]
```

---

## Phase 4: Save Document

Present the onboarding document to the user.

If writing this target is not already authorized, ask: "May I write this to `production/onboarding/onboard-[role]-[date].md`?"

If yes, write the file, creating the directory if needed.

---

## Phase 5: Next Steps

Verdict: **COMPLETE** — onboarding document generated.

- Share the onboarding doc with the new contributor before their first session.
- Run `/sprint-status` to show the new contributor current progress.
- Run `/studio-help` if the contributor needs guidance on what to work on next.
