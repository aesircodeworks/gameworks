> **Upstream:** Derived from Claude Code Game Studios by Donchitos (MIT). https://github.com/Donchitos/Claude-Code-Game-Studios — adapted for Hermes Agent / Aesir Gameworks.

# Active Hooks

Hooks are registered in the **installed profile** `config.yaml`, not in a game-workspace `settings.json`. Scripts live under `"$HERMES_HOME"/agent-hooks/aesir-gameworks/` and speak the Hermes JSON wire protocol (`context`, `action: block`, or `{}`).

Hermes has no PreCompact / PostCompact / Notification events. Session continuity uses `pre_verify` checkpointing and first-turn `pre_llm_call` restore.

| Script | Hermes event | Matcher | Action |
| ---- | ----- | ------- | ------ |
| `validate-commit.sh` | `pre_tool_call` | `terminal` (`git commit`) | Blocks invalid `assets/data/*.json` and unowned TODO/FIXME in `src/` |
| `validate-push.sh` | `pre_tool_call` | `terminal` (`git push`) | Warns on pushes to protected branches |
| `validate-project-assets.sh` | `post_tool_call` | `write_file\|patch` | On `assets/**`: rejects filenames with spaces; validates JSON |
| `validate-aesir-skill-change.sh` | `post_tool_call` | `write_file\|patch\|skill_manage` | Advises `/skill-test` after framework skill edits |
| `session-start.sh` | `pre_llm_call` (once per session) | — | Injects branch, recent commits, stage, sprint, `active.md` presence |
| `detect-project-gaps.sh` | `pre_llm_call` (once per session) | — | Notes missing `design/gdd/game-concept.md` |
| `restore-session-context.sh` | `pre_llm_call` (once per session) | — | If `production/session-state/active.md` exists, reminds the model to restore it |
| `checkpoint-session-state.sh` | `pre_verify` | — | Date-stamps `production/session-state/.aesir-checkpoint` |
| `session-end.sh` | `on_session_finalize` | — | Appends `production/session-logs/sessions.jsonl` |
| `log-subagent-start.sh` | `subagent_start` | — | Appends `production/session-logs/subagents.jsonl` |
| `log-subagent-stop.sh` | `subagent_stop` | — | Completes the subagent audit trail |

Game-workspace hooks never run against this distribution repository (`distribution.yaml` or `skills/studio` present).
