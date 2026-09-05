# Aesir Gameworks

Hermes-native game studio workflow derived from **Claude Code Game Studios** by [Donchitos](https://github.com/Donchitos/Claude-Code-Game-Studios) (MIT).

Aesir Gameworks is a **Hermes Agent profile distribution**, not a game repository. Install it into a Hermes profile, then run workflows against a separate game workspace.

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

Existing credentials, memories, sessions, and unrelated skills are not part of `distribution_owned` and must be preserved. Do not use `--force-config` against a configured profile; merge policy keys with `scripts/apply_profile_config.py`.

## Use

Start a game workspace (not this repository) and load `/gameworks`. Design work follows Question → Options → Decision → Draft → Approval → Write.

Engine references for Godot, Unity, and Unreal live behind `/engine-reference`. Read that engine's `VERSION.md` before suggesting post-cutoff APIs.

## Compression-hook note

Hermes has no pre/post-compression shell-hook events. Aesir preserves the original intent with `pre_verify` checkpointing and first-turn `pre_llm_call` restore. That is a semantic adaptation, not a 1:1 Claude compact hook.

## License

MIT. See `LICENSE` and `NOTICE.md`.
