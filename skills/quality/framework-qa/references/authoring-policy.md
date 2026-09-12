> **Upstream:** Derived from Claude Code Game Studios by Donchitos (MIT). https://github.com/Donchitos/Claude-Code-Game-Studios — adapted for Hermes Agent / Aesir Gameworks.

# Framework QA authoring policy

This folder is the quality assurance layer for the framework. It is self-contained
and separate from any game project.

## Key files

| File | Purpose |
|------|---------|
| `catalog.yaml` | Master registry for all 73 workflow skills and 50 role skills. Contains category, spec path, and last-test tracking fields. Always read this first when running any test command. |
| `quality-rubric.md` | Category-specific pass/fail metrics. Read the matching `###` section for the skill's category when running `/skill-test category`. |
| `skills/<category>/<name>/references/behavior-spec.md` | Behavioral spec for a skill or role — 5 test cases + protocol compliance assertions. Lives next to the skill, not in this folder. |
| `templates/skill-test-spec.md` | Template for writing new skill spec files. |
| `templates/agent-test-spec.md` | Template for writing new role-skill spec files. |
| `results/` | Written by `/skill-test spec` when results are saved (`skill_view('framework-qa', file_path='references/results/')`). Gitignored. |

## Path conventions

- Skills: `skills/<category>/<name>/SKILL.md`
- Role skills: `skills/agents/<name>/SKILL.md`
- Specs: `skills/<category>/<name>/references/behavior-spec.md`
- Catalog: `skill_view('framework-qa', file_path='references/catalog.yaml')`
- Rubric: `skill_view('framework-qa', file_path='references/quality-rubric.md')`

The `spec:` field in `catalog.yaml` is the authoritative path for each skill/role spec.
Always read it rather than guessing the path. Do not look under a nested
`skills/gate/` tree or under `(game-workspace)/skills/` / `(game-workspace)/agents/`.

## Hermes frontmatter

Live skill frontmatter is:

- `name`
- `description`
- `metadata.hermes` (`tags`, `related_skills`)

Do not require `argument-hint`, `user-invocable`, `allowed-tools`, `context`,
`model`, or `tools`. State model tier as **Light**, **Medium**, or **Heavy**
(see `agent-roster.md` and `coordination-rules.md`).

Hermes tools: `read_file`, `search_files` (params: `query`, `file_glob`, `context`),
`write_file`, `patch`, `terminal`, `delegate_task`, `clarify`.

## Skill completion (no closing `clarify`)

Do not end a skill with a `clarify` menu. When the skill's work is finished:

1. Say that the skill is done (e.g. `Architecture review is done. Verdict: CONCERNS.`).
2. If there are real follow-ups, list them as bullets with concrete commands and names.
   Never `[system]` or another placeholder. Never "open a fresh session" as if it were
   a selectable action. Never "Stop here".
3. Do not call `clarify`. The user is not inside that workflow anymore.

`clarify` remains for in-skill decisions only: write approvals, ambiguous inputs,
error recovery, and optional continuation of *this* skill's remaining work
(e.g. revise the document just reviewed). A bullet list after a done line satisfies
`/skill-test` Check 5. A closing "what next?" widget does not.

`/create-architecture` Phase 8 is the reference handoff: done output, concrete
commands, no widget.

## Skill categories

```
gate        → gate-check
review      → design-review, architecture-review, review-all-gdds
authoring   → design-system, quick-design, architecture-decision, art-bible,
              create-architecture, ux-design, ux-review
readiness   → story-readiness, story-done
pipeline    → create-epics, create-stories, dev-story, create-control-manifest,
              propagate-design-change, map-systems
analysis    → consistency-check, balance-check, content-audit, code-review,
              tech-debt, scope-check, estimate, perf-profile, asset-audit,
              security-audit, test-evidence-review, test-flakiness
team        → team-combat, team-narrative, team-audio, team-level, team-ui,
              team-qa, team-release, team-polish, team-live-ops
sprint      → sprint-plan, sprint-status, milestone-review, retrospective,
              changelog, patch-notes
utility     → all remaining workflow skills
```

## Agent tiers

```
directors   → creative-director, technical-director, producer, art-director
leads       → lead-programmer, narrative-director, audio-director, ux-designer,
              qa-lead, release-manager, localization-lead
specialists → gameplay-programmer, engine-programmer, ui-programmer,
              tools-programmer, network-programmer, ai-programmer,
              level-designer, sound-designer, technical-artist
godot       → godot-specialist, godot-gdscript-specialist, godot-csharp-specialist,
              godot-shader-specialist, godot-gdextension-specialist
unity       → unity-specialist, unity-ui-specialist, unity-shader-specialist,
              unity-dots-specialist, unity-addressables-specialist
unreal      → unreal-specialist, ue-gas-specialist, ue-replication-specialist,
              ue-umg-specialist, ue-blueprint-specialist
threejs     → threejs-specialist
operations  → devops-engineer, security-engineer, performance-analyst,
              analytics-engineer, community-manager
creative    → writer, world-builder, game-designer, economy-designer,
              systems-designer, prototyper
```

## Workflow for testing a skill

`/skill-test` and `/skill-improve` test this distribution or installed profile,
not a game workspace. Run them from a root that contains `skills/studio`.

1. Read `catalog.yaml` to get the skill's `spec:` path and `category:`
2. Read the skill at `skills/<category>/<name>/SKILL.md`
3. Read the spec at the `spec:` path
4. Evaluate assertions case by case (reasoning check)
5. Offer to write results to `skill_view('framework-qa', file_path='references/results/')` and update `catalog.yaml`

## Workflow for improving a skill

Use `/skill-improve [name]`. It handles the full loop:
test → diagnose → propose fix → rewrite → retest → keep or revert.

Writes go to `skills/<category>/<name>/SKILL.md` in this distribution/profile.
Do not write into a game-workspace skills tree.

## Spec validity note

Specs describe **current behavior**, not ideal behavior. They were written by
reading the skills, so they may encode bugs. When a skill misbehaves in
practice, correct the skill first, then update the spec to match the fixed behavior.
Treat spec failures as "this needs investigation," not "the skill is definitively wrong."

## This folder is optional

Nothing in a game workspace imports from here. Removing
`skills/quality/framework-qa/` does not change workflow or role skills.
`/skill-test` and `/skill-improve` will report that `catalog.yaml` is missing
and guide the user to initialize it.
