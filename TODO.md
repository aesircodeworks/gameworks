# Open work

Tracking only. Do not treat this file as a spec.

Until the framework has a name, say **the framework**. Do not use a brand name in new writing.

---

## Closed (this pass)

- Deleted `skills/studio/gameworks/references/profile-settings-template.md` and `original-studio-architecture.md`.
- Deleted `skills/studio/gameworks/references/upstream/` (`UPGRADING-CCGS.md`, `claude-settings.json`) and unlinked it.
- Removed Agent Teams (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` and related copy). `team-*` skills stay; they are department orchestration, not Agent Teams.
- Replaced Claude model IDs (Opus / Sonnet / Haiku) with **Model tier: Light / Medium / Heavy**. Kept the Model field/column; never Default. Medium is the fallback.
- Removed “inherited from parent unless profile `delegation.model` is set”. Children still inherit approved write scope only.
- Role skills, workflow skills, specs, roster, and command tables now state **Model tier: Light / Medium / Heavy**.

Left on purpose: NOTICE / LICENSE CCGS attribution; `lead-programmer/references/upstream-memory.md` (role memory notes, not the deleted folder).

---

## Role and tier → model mapping

Hermes can run on any model. Roles and skills now *label* model tier **Light** / **Medium** / **Heavy**. That is a complexity label, not a provider or model ID. The labels are written into skills and docs; they are not wired to a runtime model.

- Role skills and workflow skills have no `model:` frontmatter field.
- `config.yaml` `delegation:` only sets `max_concurrent_children`.
- Need a user-configurable map (Light / Medium / Heavy → provider/model, or role → provider/model) that works for whatever the profile actually runs.

## Path mapping

Path-rule skills and most workflows assume a fixed game-workspace layout (`src/gameplay/**`, `design/gdd/**`, `docs/architecture/`, `production/`, `assets/data/**`, …). That will not match Godot / Unity / Unreal trees or games that already have their own layout.

- Path rules are Hermes skills with “use when editing \<glob\>” descriptions. They are not auto-injected on file match.
- `/adopt`, `/studio-help`, `/gate-check`, and hooks look in the same hardcoded paths. `/adopt` does not remap; “non-standard location” stops.
- `docs/technical-preferences.md` has no directory remap table.
- Need a global, per-game map from framework path roles (gameplay code, GDDs, ADRs, stories, assets, tests, …) to the workspace’s real paths, and every rule / workflow / hook / catalog glob must read that map.

Layout until a remap exists: engine pin in `AGENTS.md`; engine prefs in `docs/technical-preferences.md`; stories under `production/epics/`; playtests under `production/qa/playtests/`; concept reports at `prototypes/*-concept/REPORT.md`; vertical-slice reports at `prototypes/*-vertical-slice/REPORT.md`.

## How to use the framework

Need real Hermes-facing teaching material: what the framework is, how to install the profile, how to run it against a game workspace, how the seven phases and slash commands fit, how roles are delegated, how gates and review modes work, and how brownfield adoption is supposed to go.

Existing `SKILL.md` files, `workflow-guide.md`, `workflow-catalog.yaml`, and `examples/` are a start. They still assume the hardcoded layout. Rewrite for Hermes users, with howtos that someone can follow without reading seventy-three skills first.

## Name

The framework needs a name. Until one is chosen, call it the framework in new writing. Existing files still use the old brand; leave them until a rename pass.
