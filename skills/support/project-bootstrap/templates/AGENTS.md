> **Upstream:** Derived from Claude Code Game Studios by Donchitos (MIT). https://github.com/Donchitos/Claude-Code-Game-Studios — adapted for Hermes Agent / Aesir Gameworks.

# Game workspace instructions

Hermes loads this file as workspace context (`.hermes.md` → `AGENTS.md` → `CLAUDE.md`). It is read as raw UTF-8. Do not use `@` imports; they are not expanded.

`/setup-engine` fills the Technology Stack. Keep `docs/technical-preferences.md` in sync with it.

## Technology Stack

- **Engine**: [CHOOSE]
- **Language**: [CHOOSE]
- **Build System**: [CHOOSE]
- **Asset Pipeline**: [CHOOSE]

## Engine Version Reference

Before suggesting engine APIs, read `docs/engine-reference/<engine>/VERSION.md` in this game workspace (created by `/setup-engine`). Do not invent post-cutoff APIs.

## Project standards

Naming conventions, performance budgets, input/platform, and specialist routing live in `docs/technical-preferences.md`. If that file still contains `[TO BE CONFIGURED]`, run `/setup-engine`.

## Collaboration

The user owns creative and strategic decisions. Read-only discovery needs no extra permission. An explicit request to implement a stated changeset authorizes its edits and verification. Ask at new scope or unresolved decision boundaries. Delegated children return decisions and blockers to the coordinator, not directly to the user.
