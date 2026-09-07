---
name: skill-improve
description: Use when improving a studio skill through test-fix loops.
version: 1.0.0
author: Donchitos; Hermes adaptation by Aesir Gameworks
license: MIT
metadata:
  hermes:
    tags:
    - aesir-gameworks
    - game-development
    - workflow
    related_skills:
    - gameworks
---

> **Upstream:** Derived from Claude Code Game Studios by Donchitos (MIT). https://github.com/Donchitos/Claude-Code-Game-Studios — adapted for Hermes Agent / Aesir Gameworks.

# Skill Improve

**Model tier:** Medium

Runs an improvement loop on a single skill in **this distribution or installed
profile**: test → fix → retest → keep or revert.

It tests the framework, not a game. Game workspaces have no `skills/` tree.
Do not write into a game-workspace skills tree.

Use Hermes tools only: `read_file`, `search_files` (params: `query`, `file_glob`,
`context` — not `glob` or `-C`), `write_file`, `patch`, `terminal`,
`delegate_task`, `clarify`. Do not invoke Claude tools (`Glob`, `Grep`, `Read`,
`Write`, `Edit`, `Task`). Do not add Claude-only frontmatter keys.

---

## Phase 1: Parse Argument and Locate the Skill

Read the skill name from the first argument. If missing, output usage and stop:

```
Usage: /skill-improve [skill-name]
Example: /skill-improve tech-debt
```

Confirm `skills/studio` exists at the current working root (distribution repo or
installed profile). If it is absent, this is a **game workspace**. Stop:

> `/skill-improve` edits framework skills, not a game. Run it from the
> distribution repository or the installed profile (a root that contains
> `skills/studio`). Do not write `(game-workspace)/skills/...`.

Locate `skills/<category>/<name>/SKILL.md` with `search_files`:
- `file_glob`: `skills/*/*/SKILL.md`
- `query`: the skill name
- `context`: omit or a small integer

Role skills are `skills/agents/<name>/SKILL.md`. If no match, stop with:
"Skill '[name]' not found in this distribution/profile."

---

## Phase 2: Baseline Test

Run `/skill-test static [name]` and record the baseline score:
- Count of FAILs
- Count of WARNs
- Which specific checks failed (Check 1–7)

Display to the user:
```
Static baseline:   [N] failures, [M] warnings
Failing: Check 4 (write_file/patch without scoped authorization), Check 5 (no handoff)
```

If baseline is 0 FAILs and 0 WARNs, note it and proceed to Phase 2b.

### Phase 2b: Category Baseline

Look up the skill's `category:` field in `framework-qa references/catalog.yaml`.

If no `category:` field is found, display:
"Category: not yet assigned — skipping category checks."
and skip to Phase 3.

If category is found, run `/skill-test category [name]` and record the category baseline:
- Count of FAILs
- Count of WARNs
- Which specific category rubric metrics failed

Display to the user:
```
Category baseline: [N] failures, [M] warnings  ([category] rubric)
```

If BOTH static and category baselines are 0 FAILs and 0 WARNs, stop:
"This skill already passes all static and category checks. No improvements needed."

---

## Phase 3: Diagnose

`read_file` the full skill at `skills/<category>/<name>/SKILL.md`.

For each failing or warning **static** check, identify the exact gap:

- **Check 1 fail** → which of `name`, `description`, `metadata.hermes` is missing.
  Do not treat Claude-only keys as required; do not propose adding them.
- **Check 2 fail** → how many phases found vs. minimum required
- **Check 3 fail** → no verdict keywords anywhere in the skill body
- **Check 4 fail** → body instructs `write_file` or `patch` but has no scoped
  write-authorization language
- **Check 4 warn** → read-only skill with no write-authorization language
- **Check 5 warn** → no follow-up or next-step section at the end
- **Check 6 warn** → `metadata.hermes.tags` missing or empty (no framework tag
  such as `aesir-gameworks`); `related_skills` is not a list
- **Check 7 warn** → `description` is generic and does not state when to use
- **Check 7 fail** → `description` is empty, or the skill copy-pastes Claude
  tools (`Glob`, `Grep`, `Read`, `Write`, `Edit`, `Task`) as invocables.
  Replace those with Hermes tools.

For each failing or warning **category** check (if category was assigned in Phase 2b),
identify the exact gap in the skill's text. For example:
- If G2 fails (gate mode, full directors not spawned): skill body never references all 4
  PHASE-GATE director prompts
- If A2 fails (authoring, no per-section write authorization): skill asks once at the end, not
  before each section write
- If T3 fails (team, BLOCKED not surfaced): skill doesn't halt dependent work on blocked agent
- If D4/L3/S4/E4/O4/Q4 fail: set **Model tier: Heavy** (creative-director,
  technical-director, producer), **Model tier: Medium** (art-director, leads,
  and most specialists), or **Model tier: Light** (`qa-tester`,
  `devops-engineer`, `accessibility-specialist`, `community-manager`). Workflows
  use the same three names per `coordination-rules.md`. Do not add Claude model
  IDs. Never use Default as a model tier; use Medium.

Show the full combined diagnosis to the user before proposing any changes.

---

## Phase 4: Propose Fix

Write a targeted fix for each failure and warning. Show the proposed changes
as clearly marked before/after blocks. Only change what is failing — do not
rewrite sections that are passing.

Do **not** add Claude-only frontmatter (`argument-hint`, `user-invocable`,
`allowed-tools`, `context: fork`, `model`, `tools`). Live frontmatter is
`name`, `description`, `metadata.hermes` (tags, related_skills).

The write target is `skills/<category>/<name>/SKILL.md` in this distribution or
profile. Never a game-workspace path.

If writing this target is not already authorized, ask: "May I write this improved version to `skills/<category>/<name>/SKILL.md`?"

If the user says no, stop here.

---

## Phase 5: Write and Retest

Record the current content of the skill file (for revert if needed).

`write_file` or `patch` the improved skill at `skills/<category>/<name>/SKILL.md`.

Re-run `/skill-test static [name]` and record the new static score.
If a category was assigned, also re-run `/skill-test category [name]` and record the new category score.

Display the comparison:
```
Static:   Before [N] failures, [M] warnings  →  After [N'] failures, [M'] warnings
Category: Before [N] failures, [M] warnings  →  After [N'] failures, [M'] warnings  (if applicable)
Combined change: improved / no change / worse
```

---

## Phase 6: Verdict

Count the combined failure total: static FAILs + category FAILs + static WARNs + category WARNs.

**If combined score improved (combined failure count is lower than baseline):**
Report: "Score improved. Changes kept."
Show a summary of what was fixed in each dimension.

**If combined score is the same or worse:**
Report: "Combined score did not improve."
Show what changed and why it may not have helped.
Ask: "May I revert `skills/<category>/<name>/SKILL.md` using git checkout?"
If yes: run `git checkout -- skills/<category>/<name>/SKILL.md` from the
distribution/profile root. Do not checkout a game-workspace path.

---

## Phase 7: Next Steps

- Run `/skill-test static all` to find the next skill with failures.
- Run `/skill-improve [next-name]` to continue the loop on another skill.
- Run `/skill-test audit` to see overall coverage progress (73 workflow + 49 role).
