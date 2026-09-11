# Changelog

## Unreleased

- Skill frontmatter `description` is a capability sentence (imperative, ≤57 characters), not a `Use when` trigger. `/skill-test` Check 7 warns on `Use when`, over-length, or generic copy.
- Hermes profile name in docs is `gameworks`. `SOUL.md` identity is a studio-lead role, not the product name. Skill frontmatter author is `Hermes adaptation by Aesir Codeworks`; tags stay `aesir-gameworks`. Hook session strings use `Gameworks session:` / `Gameworks gap check`.
- Default `agent.verify_on_stop` to `false` so stop does not run the upstream verify pass.
- Removed the session-end macOS toast (`notify-session.sh`). `session-end.sh` still appends `production/session-logs/sessions.jsonl`.
- Ship the `gameworks` Hermes CLI/TUI skin (`skins/gameworks.yaml`) as distribution-owned. Fresh installs set `display.skin: gameworks`. The owned path is the skin file, not `skins/`, so user-added skins in that directory survive updates.
- Game-workspace `AGENTS.md` is the workspace context file the profile writes. The bootstrap template no longer documents a compatibility load chain.
- Skills no longer use spaced skill-folder path shorthands (`` `gameworks references/` ``, `` `project-templates templates/` ``, `` `framework-qa references/` ``). Hermes treated those as a write path (`gameworksreferences/`). Bundled files load via `skill_view('skill-name', file_path='...')`.
- `/setup-engine` writes engine prefs only to the game-workspace file `docs/technical-preferences.md`. It copies the profile template through `skill_view`; it does not write into the installed profile.
- Root `AGENTS.md` and `CONTRIBUTING.md` now state profile-development rules, including changelog + `distribution.yaml` version bumps. The root file is not `distribution_owned`.
- Release is a documented procedure (`CONTRIBUTING.md` ## Release): bump `distribution.yaml`, fold Unreleased, commit, `hermes profile update gameworks`. No GitHub release or tag unless asked.
- README covers install, update, game-workspace use, and profile-development / release pointers.

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
