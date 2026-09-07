# Open work

Tracking only. Do not treat this file as a spec.

Until the framework has a name, say **the framework**. Do not use a brand name in new writing.

---

## Role and tier → model mapping

Hermes can run on any model. The framework still talks in Claude Code tiers (Opus / Sonnet / Haiku) and Claude model IDs. None of that is wired.

- Role skills and workflow skills have no `model:` field.
- `config.yaml` `delegation:` only sets `max_concurrent_children`.
- Team skills tell the parent to pass `subagent_type: <role>`. That is the Claude Code `Task` API. Hermes `delegate_task` takes `goal` + `context`; children inherit the parent model unless the profile sets `delegation.model`.
- Need a user-configurable map (role, tier, or both → provider/model) that works for whatever the profile actually runs.

## Path mapping

Path-rule skills and most workflows assume a fixed game-workspace layout (`src/gameplay/**`, `design/gdd/**`, `docs/architecture/`, `production/`, `assets/data/**`, …). That will not match Godot / Unity / Unreal trees or games that already have their own layout.

- Path rules are Hermes skills with “use when editing \<glob\>” descriptions. They are not auto-injected on file match.
- `/adopt`, `/studio-help`, `/gate-check`, and hooks look in the same hardcoded paths. `/adopt` does not remap; “non-standard location” stops.
- `technical-preferences.md` has no directory remap table.
- Need a global, per-game map from framework path roles (gameplay code, GDDs, ADRs, stories, assets, tests, …) to the workspace’s real paths, and every rule / workflow / hook / catalog glob must read that map.

## Strip Claude Code-only behavior

Everything has to work as Hermes. Leftovers found so far:

- Claude model IDs and Haiku/Sonnet/Opus assignments in roster, director gates, coordination rules, and workflow behavior specs.
- `subagent_type:` / `Task` spawn language in team skills and engine specialists.
- `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` in coordination rules.
- `rules-reference.md` still describes Claude Code path-rule auto-injection from `(game-workspace)/rules/`.
- Settings / bootstrap templates still talk `settings.local.json`, `CLAUDE.local.md`, Claude permission modes.
- Hook docs still describe PreCompact / PostCompact / PreToolUse Bash-Write payloads. Hermes has no compact hooks; the port already uses `pre_verify` + first-turn `pre_llm_call` restore.
- Workflow guide still lists `pre-compact.sh` / `post-compact.sh` as if they exist.

Audit and replace or delete. Do not leave dual-runtime instructions.

## How to use the framework

Need real Hermes-facing teaching material: what the framework is, how to install the profile, how to run it against a game workspace, how the seven phases and slash commands fit, how roles are delegated, how gates and review modes work, and how brownfield adoption is supposed to go.

Existing `SKILL.md` files, `workflow-guide.md`, `workflow-catalog.yaml`, and `examples/` are a start. They still mix Claude Code vocabulary and assume the hardcoded layout. Rewrite for Hermes users, with howtos that someone can follow without reading seventy-three skills first.

## Name

The framework needs a name. Until one is chosen, call it the framework in new writing. Existing files still use the old brand; leave them until a rename pass.
