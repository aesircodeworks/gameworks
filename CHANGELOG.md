# Changelog

## Unreleased

## 1.1.0 — Hermes runtime alignment

- Dropped `aesir-` prefixes from skill names and folders. Commands are `/brainstorm`, roles are `game-designer`. Hermes collisions: `/studio-help`, `/studio-start`. Brand remains on the profile, hooks, and distribution name.
- Replaced Claude model IDs with **Model tier: Light / Medium / Heavy** on roles, workflows, specs, roster, and command tables. Medium is the fallback; Default is not a model tier.
- Removed Agent Teams. `team-*` skills stay as department orchestration.
- Deleted unused Claude leftovers: `profile-settings-template.md`, `original-studio-architecture.md`, and `references/upstream/` (`UPGRADING-CCGS.md`, `claude-settings.json`).
- Skills, hooks, and docs now use Hermes tools and profile hook events. Game workspaces stay separate from this distribution.

## 1.0.0 — Hermes profile conversion

- Converted 73 workflow skills, 49 agent roles, and 11 path rules into prefixed Hermes skills.
- Ported 12 lifecycle scripts to the Hermes shell-hook JSON wire protocol.
- Packaged the studio as a Hermes profile distribution with `distribution.yaml`.
- Preserved the upstream MIT license and Donchitos / Claude Code Game Studios attribution.
