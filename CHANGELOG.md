# Changelog

## Unreleased

- Drop the per-skill `Upstream:` Donchitos attribution blockquote from all 140 `SKILL.md` files. Attribution stays in `NOTICE.md`, `LICENSE`, and `README.md`.

- `gameworks` skin: swap indigo accents for Tailwind orange-600 (`#F54900`); drop the AESIR wordmark. CRT hero art is unchanged.
- `gameworks` skin: selected menu rows (`completion_menu_current_bg`, `completion_menu_meta_current_bg`) use the same `#973004` fill as selected text.

- Batch companion writes into the original approval in `/design-review`, `/design-system`, `/architecture-decision`, `/architecture-review`, `/review-all-gdds`, `/asset-spec`, `/quick-design`, and `/test-flakiness`. Show target paths and changes up front, retain independent optional outputs, skip no-ops and repeat permission questions, and preserve substantive design/review gates. Patched GDDs remain `In Review`, not automatically `Approved`.

- Add a self-contained beginner HTML user guide covering all 73 workflows, 140 skills, hooks, project recipes, SVG diagrams, and bundled offline references.

- `/design-review` now repeats review → approved fixes → re-review within one invocation. `--depth full` respawns all relevant specialists then `creative-director` each pass; `lean` repeats the main review without delegation; `solo` returns at Phase 4 without edits. Preserve tracking approvals across passes, present each updated verdict, and reserve `Live verdict: unscored` for interrupted re-reviews.
- `/studio-help` prints a fact block, one Next, at most one Optional, and `studio-help done.` It no longer lists Done, Coming up, or Also installed.
- Removed leftover `/studio-status` (Claude Code statusline snapshot). Use `/studio-help` and `/sprint-status`.
- Skills no longer finish with a `clarify` "what next?" menu. When a workflow is done, it says so and lists real follow-ups as bullets (concrete names, no placeholders, no "open a fresh session" as a choice). `clarify` stays for in-skill write approvals, ambiguities, and error recovery.
- CI on `main` (`.github/workflows/release.yml`) tags `vX.Y.Z` from `distribution.yaml` and publishes the GitHub Release from the matching CHANGELOG heading when they do not already exist.

## 1.2.0 — Three.js engine and profile hygiene

- First-class Three.js engine support: `threejs-specialist`, `/setup-engine` / `/brainstorm` option, and `engine-reference/references/threejs/` pinned at r186 (`three@0.186.0`). Vanilla TypeScript + Vite + **WebGPURenderer** (`three/webgpu`, TSL) is the default app layer; **React Three Fiber** is a `/setup-engine` choice (`threejs r3f`). WebGLRenderer is the compatibility fallback. Rapier remains opt-in. Sidecar Three.js skill packs are not vendored.
- Skill frontmatter `description` is a capability sentence (imperative, ≤57 characters), not a `Use when` trigger. `/skill-test` Check 7 warns on `Use when`, over-length, or generic copy.
- Hermes profile name in docs is `gameworks`. `SOUL.md` identity is a studio-lead role, not the product name. Skill frontmatter author is `Hermes adaptation by Aesir Codeworks`; tags stay `aesir-gameworks`. Hook session strings use `Gameworks session:` / `Gameworks gap check`.
- Default `agent.verify_on_stop` to `false` so stop does not run the upstream verify pass.
- Removed the session-end macOS toast (`notify-session.sh`). `session-end.sh` still appends `production/session-logs/sessions.jsonl`.
- Ship the `gameworks` Hermes CLI/TUI skin (`skins/gameworks.yaml`) as distribution-owned. Fresh installs set `display.skin: gameworks`. The owned path is the skin file, not `skins/`, so user-added skins in that directory survive updates.
- Game-workspace `AGENTS.md` is the workspace context file the profile writes. The bootstrap template no longer documents a compatibility load chain.
- Skills no longer use spaced skill-folder path shorthands (`` `gameworks references/` ``, `` `project-templates templates/` ``, `` `framework-qa references/` ``). Hermes treated those as a write path (`gameworksreferences/`). Bundled files load via `skill_view('skill-name', file_path='...')`.
- `/setup-engine` writes engine prefs only to the game-workspace file `docs/technical-preferences.md`. It copies the profile template through `skill_view`; it does not write into the installed profile.
- Root `AGENTS.md` and `CONTRIBUTING.md` now state profile-development rules, including changelog + `distribution.yaml` version bumps. The root file is not `distribution_owned`.
- Release is a documented procedure (`CONTRIBUTING.md` ## Release): bump `distribution.yaml`, fold Unreleased, commit, push, tag `vX.Y.Z`, GitHub Release, `hermes profile update gameworks`. No CI job unless asked.
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
