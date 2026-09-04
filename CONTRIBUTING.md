# Contributing to Aesir Gameworks

Aesir Gameworks is a Hermes Agent profile distribution derived from Claude Code Game Studios by Donchitos (MIT). Contributions are welcome for bug fixes, missing workflows, hook fixes, and documentation corrections.

## What this repo is

A distributable Hermes profile. It is not a place to store games built with it. Keep GDDs, ADRs, and game code in a separate game workspace.

## Rules

- Skills live in `skills/aesir-*/<name>/SKILL.md` with Hermes frontmatter (`name`, `description`, `metadata.hermes`).
- Prefix migrated commands with `aesir-` so they never collide with Hermes built-ins.
- Use Hermes tools (`read_file`, `search_files`, `write_file`, `patch`, `terminal`, `delegate_task`, `clarify`).
- Hooks must speak the Hermes JSON wire protocol and stay profile-name agnostic via `"$HERMES_HOME"`.
- Do not commit `.env`, `auth.json`, memories, sessions, state databases, or live profile data.
- Preserve upstream attribution in `NOTICE.md` and converted skill metadata.

Feature requests submitted as PRs will be closed. Open an issue instead.
