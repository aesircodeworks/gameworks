# Aesir Gameworks

Hermes-native game studio workflow derived from **Claude Code Game Studios** by [Donchitos](https://github.com/Donchitos/Claude-Code-Game-Studios) (MIT).

This repository is a **Hermes Agent profile distribution**, not a game. Install it into a Hermes profile, then run workflows against a **separate game workspace**.

Requires Hermes `>=0.21.0` (`distribution.yaml` → `hermes_requires`).

## Attribution

Upstream: https://github.com/Donchitos/Claude-Code-Game-Studios

The original MIT license and copyright notice are preserved in `LICENSE`. Aesir Gameworks does not claim authorship of the original framework content.

## What's included

| Category | Count | Description |
|----------|-------|-------------|
| Workflow skills | 73 | Studio commands (`/brainstorm`, `/dev-story`, …) |
| Role skills | 49 | Director, lead, and specialist roles for `delegate_task` |
| Rule skills | 11 | Path-aware practices for a target game workspace |
| Support/core skills | 7 | Routing, templates, bootstrap, engine reference, QA, status, memory policy |
| Shell hooks | 12 | Hermes wire-protocol lifecycle hooks |

## Install

```bash
hermes profile install /path/to/aesir-gameworks --name gamedev --force --yes
```

Existing credentials, memories, sessions, and unrelated skills are not part of `distribution_owned` and must be preserved. Do not use `--force-config` against a configured profile.

## Update

If `gamedev` was installed from this directory:

```bash
hermes profile update gamedev --yes
```

Confirm the recorded source with `hermes profile info gamedev`. If there is no source, use `install --force` again. Do not pass `--force-config` unless you want to reset local `config.yaml`.

## Use

Work in a **game workspace**, not this repository.

1. Create or open the game project directory.
2. Run Hermes as `gamedev`.
3. Load `/gameworks` or start with `/studio-start`.

Design work follows Question → Options → Decision → Draft → Approval → Write.

Game workspaces get `AGENTS.md` (engine pin) and `docs/technical-preferences.md` from `/project-bootstrap` and `/setup-engine`. Those files live in the game, not in this distribution.

Engine references for Godot, Unity, and Unreal live behind `/engine-reference`. Read that engine's `VERSION.md` before suggesting post-cutoff APIs.

Load skill-bundled files with `skill_view('skill-name', file_path='...')`. Never treat a spaced skill-folder string as a write path.

## Develop this profile

Root `AGENTS.md` is for agents working **on this distribution**. It is not installed into `gamedev`. Read `CONTRIBUTING.md` before editing skills or hooks.

On behavior, skill, hook, or packaging changes, note them under `CHANGELOG.md` **Unreleased**. To ship, say **release** and follow `CONTRIBUTING.md` ## Release (bump `distribution.yaml`, fold Unreleased, commit, `hermes profile update gamedev`).

## Session continuity

Hermes has no pre/post-compression shell-hook events. Aesir uses `pre_verify` checkpointing and first-turn `pre_llm_call` restore.

## License

MIT. See `LICENSE` and `NOTICE.md`.
