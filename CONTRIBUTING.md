# Contributing to Aesir Gameworks

Aesir Gameworks is a Hermes Agent profile distribution derived from Claude Code Game Studios by Donchitos (MIT). Contributions are welcome for bug fixes, missing workflows, hook fixes, and documentation corrections.

## What this repo is

A distributable Hermes profile. It is not a place to store games built with it. Keep GDDs, ADRs, and game code in a separate game workspace.

Root `AGENTS.md` is for agents working on this distribution. It is not a game-workspace file and is not part of `distribution_owned`. Game workspaces get their own `AGENTS.md` from `skills/support/project-bootstrap/templates/AGENTS.md`.

## Rules

- Skills live in `skills/<category>/<name>/SKILL.md` with Hermes frontmatter (`name`, `description`, `metadata.hermes`).
- Do not prefix skill names with `aesir-`. Rename only exact Hermes slash collisions (`help` → `studio-help`, `start` → `studio-start`).
- Use Hermes tools (`read_file`, `search_files`, `write_file`, `patch`, `terminal`, `delegate_task`, `clarify`).
- Load skill-bundled files with `skill_view('skill-name', file_path='...')`. Never write `` `skillname folder/file` `` as a path; Hermes concatenates the space into a fake directory.
- Hooks must speak the Hermes JSON wire protocol and stay profile-name agnostic via `"$HERMES_HOME"`.
- Custom Hermes skins live in `skins/<name>.yaml`. List the **file** in `distribution_owned`, not `skins/` — owning the directory would delete user-added skins on update. The filename stem must match `name` and `display.skin`.
- Do not commit `.env`, `auth.json`, memories, sessions, state databases, or live profile data.
- Preserve upstream attribution in `NOTICE.md`.

## Release hygiene

The framework version is `distribution.yaml` → `version:`. Skill frontmatter `version:` is per-skill.

On any behavior, skill, hook, or packaging change, note it under `CHANGELOG.md` **Unreleased**. Do not bump the version while still iterating.

Do not bump every skill's frontmatter `version` unless that skill's contract changed.

## Release

Run this when the user says release, ship, create a release, or bump the version. This is a distribution ship, not a game `/team-release`.

**Shipped** = named `distribution.yaml` version + folded changelog + commit + `gameworks` profile updated from this tree.

1. Confirm this repo is the distribution (`distribution.yaml` at the root, `skills/studio/` present). If this is a game workspace, stop.
2. Read `distribution.yaml` (`version`, `hermes_requires`), `CHANGELOG.md` **Unreleased**, and `git status` / `git diff`.
3. If Unreleased is empty and there is no uncommitted behavior/skill/hook/packaging change, stop: nothing to ship.
4. Choose the bump from Unreleased (or use the version the user named):
   - **patch** — fixes, path/docs/hygiene
   - **minor** — new or changed workflow behavior
   - **major** — breaks existing skills, commands, or layout
5. If the change needs a newer Hermes, bump `hermes_requires` in the same edit.
6. Set `distribution.yaml` `version:` to the new number.
7. Move Unreleased bullets under `## X.Y.Z — <short title>`. Leave an empty `## Unreleased` heading above it.
8. Commit `distribution.yaml`, `CHANGELOG.md`, and the files that belong to this version. Do not commit `.grok/`, `.env`, `auth.json`, memories, or sessions.
9. Point `gameworks` at this tree:
   - `hermes profile info gameworks` — if the recorded source is this directory, run `hermes profile update gameworks --yes`
   - otherwise `hermes profile install <this-repo-path> --name gameworks --force --yes`
   - Do not pass `--force-config` unless the user asked to reset `config.yaml`
10. Report: new version, changelog heading, commit, whether `gameworks` was updated.

Do not create a GitHub Release, git tag, or CI job unless the user asked for one.

Feature requests submitted as PRs will be closed. Open an issue instead.
