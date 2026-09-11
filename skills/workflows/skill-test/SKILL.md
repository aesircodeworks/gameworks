---
name: skill-test
description: Validate studio skill structure and behavior.
version: 1.0.0
author: Donchitos; Hermes adaptation by Aesir Codeworks
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

# Skill Test

**Model tier:** Medium

Validates the live skill tree in **this distribution or installed profile** —
`skills/<category>/<name>/SKILL.md` — for structural compliance and behavioral
correctness. It tests the framework, not a game. Game workspaces have no
`skills/` tree.

Use Hermes tools only: `read_file`, `search_files` (params: `query`, `file_glob`,
`context` — not `glob` or `-C`), `write_file`, `patch`, `terminal`,
`delegate_task`, `clarify`. Do not invoke Claude tools (`Glob`, `Grep`, `Read`,
`Write`, `Edit`, `Task`).

**Four modes:**

| Mode | Command | Purpose | Token Cost |
|------|---------|---------|------------|
| `static` | `/skill-test static [name\|all]` | Structural linter — 7 compliance checks per skill | Low (~1k/skill) |
| `spec` | `/skill-test spec [name]` | Behavioral verifier — evaluates assertions in the skill's behavior spec | Medium (~5k/skill) |
| `category` | `/skill-test category [name\|all]` | Category rubric — checks skill against its category-specific metrics | Low (~2k/skill) |
| `audit` | `/skill-test audit` | Coverage report — 73 workflow skills + 49 role skills, specs, last test dates | Low (~3k total) |

---

## Phase 1: Parse Arguments and Locate the Tree

Determine mode from the first argument:

- `static [name]` → run 7 structural checks on one skill
- `static all` → run 7 structural checks on every live skill
- `spec [name]` → read skill + test spec, evaluate assertions
- `category [name]` → run category-specific rubric from `skill_view('framework-qa', file_path='references/quality-rubric.md')`
- `category all` → run category rubric for every catalog entry that has a `category:`
- `audit` (or no argument) → read catalog, list workflow skills and role skills, show coverage

If the first argument is present but unrecognized, output usage and stop.

### Locate the distribution / profile root

This skill lints **this** distribution or installed profile. It does not lint a game.

1. Confirm `skills/studio` exists at the current working root (distribution repo or
   installed Hermes profile).
2. If `skills/studio` is absent, this is a **game workspace**. Stop:

   > `/skill-test` tests the framework skill tree, not a game. Run it from the
   > distribution repository or the installed profile (a root that contains
   > `skills/studio`). Do not search `(game-workspace)/skills/*/SKILL.md` —
   > game workspaces have no `skills/` tree.

3. Locate skills with `search_files`:
   - `file_glob`: `skills/*/*/SKILL.md`
   - `query`: the skill name, or `.` for `all`
   - `context`: omit or a small integer
   - Do **not** pass `glob` or `-C`

   A hit is `skills/<category>/<name>/SKILL.md`. Role skills are
   `skills/agents/<name>/SKILL.md`.

4. Read catalog and rubric via skill_view paths:
   - `skill_view('framework-qa', file_path='references/catalog.yaml')`
   - `skill_view('framework-qa', file_path='references/quality-rubric.md')`

   On disk that is `skills/quality/framework-qa/references/`.

---

## Phase 2A: Static Mode — Structural Linter

Keep **exactly 7** checks. For each skill, `read_file` its `SKILL.md` fully and
run all 7:

### Check 1 — Required Frontmatter Fields
The YAML frontmatter must contain:
- `name:`
- `description:`
- `metadata.hermes`

**FAIL** if any of those three are absent.

Do **not** require Claude-only keys: `argument-hint`, `user-invocable`,
`allowed-tools`, `context`, `model`, `tools`. Their absence is not a failure.
If this check treats those keys as required, the check itself **FAIL**s
(checker error) — the live schema does not include them.

### Check 2 — Multiple Phases
The skill must have ≥2 numbered phase headings. Look for patterns like:
- `## Phase N` or `## Phase N:`
- `## N.` (numbered top-level sections)
- At least 2 distinct `##` headings if phases aren't explicitly numbered

**FAIL** if fewer than 2 phase-like headings are found.

### Check 3 — Verdict Keywords
The skill must contain at least one of: `PASS`, `FAIL`, `CONCERNS`, `APPROVED`,
`BLOCKED`, `COMPLETE`, `READY`, `COMPLIANT`, `NON-COMPLIANT`

**FAIL** if none are present.

### Check 4 — Collaborative Protocol Language
Inspect the skill **body** (not frontmatter). If the body instructs `write_file`
or `patch`, it must include scoped write-authorization language. Look for:
- authorization or approved scope covering writes
- `"May I write"` only when authorization is missing
- `"before writing"` or `"approval"` near file-write instructions when scope is unresolved

**FAIL** if the body instructs `write_file` or `patch` but no scoped-authorization
language is found.
**WARN** if that language is absent on a read-only skill (body does not instruct
`write_file` or `patch` — many read-only skills legitimately skip this).

Do not score a tools allowlist. Write capability is whatever the body instructs.

### Check 5 — Next-Step Handoff
The skill must end with a recommended next action or follow-up path. Look for:
- A final section mentioning another skill (e.g., `/story-done`, `/gate-check`)
- "Recommended next" or "next step" phrasing
- A "Follow-Up" or "After this" section

**WARN** if absent.

### Check 6 — Hermes Metadata
Inspect `metadata.hermes`:
- **PASS** if `tags` includes a framework tag (e.g. `aesir-gameworks`) **or**
  `related_skills` is a list
- **WARN** if `tags` is missing or empty (even when `related_skills` is a list)

Do not inspect `context: fork`. Do not FAIL for missing fork context.

### Check 7 — Description and Invocable Tools
`description` must be a non-empty capability sentence (imperative, ends with a
period, ≤57 characters). Do not start with `Use when`.

**FAIL** if `description` is empty.
**WARN** if `description` starts with `Use when`, exceeds 57 characters, or is
generic (just the skill name, or "A helper skill").
**FAIL** if the skill copy-pastes Claude tools as invocables: `Glob`, `Grep`,
`Read`, `Write`, `Edit`, `Task`. Hermes invocables are `read_file`,
`search_files`, `write_file`, `patch`, `terminal`, `delegate_task`, `clarify`.
Historical/upstream mentions of Claude Code are not invocables. A prohibition
("do not invoke `Glob`") is not an invocable.

---

### Static Mode Output Format

For a single skill:
```
=== Skill Static Check: /[name] ===

Check 1 — Frontmatter Fields:     PASS
Check 2 — Multiple Phases:        PASS (7 phases found)
Check 3 — Verdict Keywords:       PASS (PASS, FAIL, CONCERNS)
Check 4 — Collaborative Protocol: PASS (scoped write authorization found)
Check 5 — Next-Step Handoff:      WARN (no follow-up section found)
Check 6 — Hermes Metadata:        PASS (tag: aesir-gameworks; related_skills list)
Check 7 — Description / Tools:    PASS

Verdict: WARNINGS (1 warning, 0 failures)
Recommended: Add a "Follow-Up Actions" section at the end of the skill.
```

For `static all`, count files from `search_files` `file_glob: skills/*/*/SKILL.md`.
Do not claim 52 or 72.

```
=== Skill Static Check: Live tree (N skills) ===

Skill                  | Result       | Issues
-----------------------|--------------|-------
gate-check             | COMPLIANT    |
design-review          | COMPLIANT    |
story-readiness        | WARNINGS     | Check 5: no handoff
...

Summary: N COMPLIANT, N WARNINGS, N NON-COMPLIANT
Aggregate Verdict: N WARNINGS / N FAILURES
```

Static mode writes no files.

---

## Phase 2B: Spec Mode — Behavioral Verifier

### Step 1 — Locate Files

Find the skill at `skills/<category>/<name>/SKILL.md` using the Phase 1
`search_files` glob.

Look up the spec path from `skill_view('framework-qa', file_path='references/catalog.yaml')` — use the
`spec:` field for the matching entry under `skills:` or `agents:`. Catalog paths
look like `skills/workflows/<name>/references/behavior-spec.md` or
`skills/agents/<name>/references/behavior-spec.md`.

If either is missing:
- Missing skill: "Skill '[name]' not found under `skills/*/*/SKILL.md` in this
  distribution/profile."
- Missing spec path in catalog: "No spec path set for '[name]' in catalog.yaml."
- Spec file not found at path: "Spec file missing at [path]. Run `/skill-test audit`
  to see coverage gaps."

Do not open `(game-workspace)/skills/` or a nested `skills/gate/` spec tree.

### Step 2 — Read Both Files

`read_file` the skill file and test spec file completely.

### Step 3 — Evaluate Assertions

For each **Test Case** in the spec:

1. Read the **Fixture** description (assumed state of project files)
2. Read the **Expected behavior** steps
3. Read each **Assertion** checkbox

For each assertion, evaluate whether the skill's written instructions, if
followed correctly given the fixture state, would satisfy it. This is a
**reasoning check**, not code execution.

Mark each assertion:
- **PASS** — skill instructions clearly satisfy this assertion
- **PARTIAL** — skill instructions partially address it, but with ambiguity
- **FAIL** — skill instructions would NOT satisfy this assertion given the fixture

For **Protocol Compliance** assertions (always present):
- Check whether the skill requires scoped write authorization before `write_file`
  or `patch` (ask only when authorization is missing)
- Check whether the skill presents findings before requesting approval
- Check whether the skill ends with a recommended next step
- Check whether the skill avoids auto-creating files without approval

### Step 4 — Build Report

```
=== Skill Spec Test: /[name] ===
Date: [date]
Spec: skills/<category>/<name>/references/behavior-spec.md

Case 1: [Happy Path — name]
  Fixture: [summary]
  Assertions:
    [PASS] [assertion text]
    [FAIL] [assertion text]
       Reason: The skill's Phase 3 says "..." but the fixture state means "..."
  Case Verdict: FAIL

Case 2: [Edge Case — name]
  ...
  Case Verdict: PASS

Protocol Compliance:
  [PASS] Uses scoped write authorization before write_file/patch
  [PASS] Presents findings before asking approval
  [WARN] No explicit next-step handoff at end

Overall Verdict: FAIL (1 case failed, 1 warning)
```

### Step 5 — Offer to Write Results

If writing these targets is not already authorized, ask:

"May I write these results to `skill_view('framework-qa', file_path='references/results/skill-test-spec-[name]-[date].md')`
and update `skill_view('framework-qa', file_path='references/catalog.yaml')`?"

If yes:
- `write_file` or `patch` the results file at that skill_view path
  (`skills/quality/framework-qa/references/results/` on disk)
- `patch` the matching entry in `skill_view('framework-qa', file_path='references/catalog.yaml')`:
  - `last_spec: [date]`
  - `last_spec_result: PASS|PARTIAL|FAIL`

Do not write into a game workspace.

---

## Phase 2D: Category Mode — Rubric Evaluation

### Step 1 — Locate Skill and Category

Find the skill at `skills/<category>/<name>/SKILL.md` (Phase 1 glob).
Look up `category:` in `skill_view('framework-qa', file_path='references/catalog.yaml')` (`skills:` or
`agents:`).

If skill not found: "Skill '[name]' not found in this distribution/profile."
If no `category:` field: "No category assigned for '[name]' in catalog.yaml.
Add `category: [name]` to the skill entry first."

For `category all`: collect catalog `skills:` entries that have `category:` and
process each. `category: utility` skills are evaluated against U1 (static checks
pass) and U2 (gate mode correct if applicable) only — run static mode for U1.

### Step 2 — Read Rubric Section

`read_file` `skill_view('framework-qa', file_path='references/quality-rubric.md')`.
Extract the section matching the catalog category (e.g., `### gate`, `### team`,
`### director`).

### Step 3 — Read Skill

`read_file` the skill's `SKILL.md` fully.

### Step 4 — Evaluate Rubric Metrics

For each metric in the category's rubric table:
1. Check whether the skill's written instructions clearly satisfy the criterion
2. Mark PASS, FAIL, or WARN
3. For FAIL/WARN, identify the exact gap in the skill text (quote the relevant section
   or note its absence)

Honor rubric D4/L3/S4/E4/O4/Q4: state **Model tier: Light**, **Medium**, or
**Heavy** per `agent-roster.md` and `coordination-rules.md`. Directors
(`creative-director`, `technical-director`, `producer`) are Heavy;
`art-director` and leads are Medium; specialists are Medium except Light for
`qa-tester`, `devops-engineer`, `accessibility-specialist`, and
`community-manager`. Workflows use the same three names. Do not introduce
Claude model IDs. Never use Default as a model tier; use Medium.

### Step 5 — Output Report

```
=== Skill Category Check: /[name] ([category]) ===

Metric G1 — Review mode read:      PASS
Metric G2 — Full mode directors:   FAIL
  Gap: Phase 3 spawns only CD-PHASE-GATE; TD-PHASE-GATE, PR-PHASE-GATE, AD-PHASE-GATE absent
Metric G3 — Lean mode: PHASE-GATE only: PASS
Metric G4 — Solo mode: no directors:    PASS
Metric G5 — No auto-advance:       PASS

Verdict: FAIL (1 failure, 0 warnings)
Fix: Add TD-PHASE-GATE, PR-PHASE-GATE, and AD-PHASE-GATE to the full-mode director
     panel in Phase 3.
```

### Step 6 — Offer to Update Catalog

If writing is not already authorized, ask:

"May I update `skill_view('framework-qa', file_path='references/catalog.yaml')` to record this category check
(`last_category`, `last_category_result`) for [name]?"

If yes, `patch` that file. Do not write into a game workspace.

---

## Phase 2C: Audit Mode — Coverage Report

### Step 1 — Read Catalog

`read_file` `skill_view('framework-qa', file_path='references/catalog.yaml')`. If missing, note that the
catalog doesn't exist yet (first-run state).

### Step 2 — Enumerate Workflow Skills and Role Skills

Audit the **catalog**, not a game workspace:

- **73 workflow skills** — `skills:` entries. Each lives at
  `skills/<category>/<name>/SKILL.md` (usually `skills/workflows/<name>/SKILL.md`).
- **49 role skills** — `agents:` entries. Each lives at
  `skills/agents/<name>/SKILL.md`.

Confirm files with `search_files` `file_glob: skills/*/*/SKILL.md`.
Do **not** glob `(game-workspace)/skills/` or `(game-workspace)/agents/`.
Do not claim 52 or 72.

### Step 3 — Build Workflow Coverage Table

For each catalog `skills:` entry:
- Check if the spec file exists at the catalog `spec:` path
  (e.g. `skills/workflows/<name>/references/behavior-spec.md`)
- Look up `last_static`, `last_static_result`, `last_spec`, `last_spec_result`,
  `last_category`, `last_category_result`, `category` (or mark as
  "never" / "—" if blank)
- Priority comes from catalog `priority:` (critical/high/medium/low)

### Step 3b — Build Role Coverage Table

For each catalog `agents:` entry:
- Role skill: `skills/agents/<name>/SKILL.md`
- Spec: catalog `spec:` path (e.g. `skills/agents/<name>/references/behavior-spec.md`)
- Look up `last_spec`, `last_spec_result`, `category`

### Step 4 — Output Report

```
=== Skill Test Coverage Audit ===
Date: [date]

WORKFLOW SKILLS (73 total)
Specs written: 73 (100%) | Never static tested: N | Never category tested: N

Skill                  | Cat      | Has Spec | Last Static | S.Result | Last Cat | C.Result | Priority
-----------------------|----------|----------|-------------|----------|----------|----------|----------
gate-check             | gate     | YES      | never       | —        | never    | —        | critical
design-review          | review   | YES      | never       | —        | never    | —        | critical
...

ROLE SKILLS (49 total)
Agent specs written: 49 (100%)

Role                   | Category   | Has Spec | Last Spec   | Result
-----------------------|------------|----------|-------------|--------
creative-director      | director   | YES      | never       | —
technical-director     | director   | YES      | never       | —
...

Top 5 Priority Gaps (workflow skills with no spec, critical/high priority):
(none if all specs are written)

Workflow coverage:  73/73 specs (100%)
Role coverage:      49/49 specs (100%)
```

No file writes in audit mode.

Offer: "Would you like to run `/skill-test static all` to check structural
compliance across the live tree? `/skill-test category all` to run category rubric
checks? Or `/skill-test spec [name]` to run a specific behavioral test?"

---

## Phase 3: Recommended Next Steps

After any mode completes, offer contextual follow-up:

- After `static [name]`: "Run `/skill-test spec [name]` to validate behavioral
  correctness if a test spec exists."
- After `static all` with failures: "Address NON-COMPLIANT skills first. Run
  `/skill-test static [name]` individually for detailed remediation guidance.
  Then `/skill-improve [name]`."
- After `spec [name]` PASS: "Update `skill_view('framework-qa', file_path='references/catalog.yaml')` to record this
  pass date. Consider running `/skill-test audit` to find the next spec gap."
- After `spec [name]` FAIL: "Review the failing assertions and update the skill
  or the test spec to resolve the mismatch."
- After `audit`: "Start with the critical-priority gaps. Use the spec template
  at `skill_view('framework-qa', file_path='templates/skill-test-spec.md')` to create new specs next to the
  skill (`skills/<category>/<name>/references/behavior-spec.md`)."
