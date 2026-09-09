> **Upstream:** Derived from Claude Code Game Studios by Donchitos (MIT). https://github.com/Donchitos/Claude-Code-Game-Studios — adapted for Hermes Agent / Aesir Gameworks.

# Skill Test Spec: /skill-test

**Model tier:** Medium

## Skill Summary

`/skill-test` validates the live skill tree in this distribution or installed
profile (`skills/<category>/<name>/SKILL.md`) for structural correctness,
behavioral compliance, and category-rubric scoring. It tests the framework, not
a game. Game workspaces have no `skills/` tree.

It operates in four modes:

- **static**: Checks a skill file for 7 structural requirements (Hermes
  frontmatter, phase headings, verdict keywords, scoped authorization when the
  body instructs `write_file`/`patch`, next-step handoff, Hermes tags /
  related_skills, description when-to-use and no Claude tool invocables).
  Produces a per-check PASS/FAIL table. Writes nothing.
- **spec**: Reads the behavior spec at the catalog `spec:` path and evaluates
  the skill against each test case assertion (reasoning check, not code
  execution). May `write_file`/`patch` results under `skill_view('framework-qa', file_path='references/results/')`
  after scoped authorization.
- **category**: Scores the skill against `skill_view('framework-qa', file_path='references/quality-rubric.md')`.
- **audit**: Coverage table of **73 workflow skills** + **49 role skills** from
  `skill_view('framework-qa', file_path='references/catalog.yaml')`. Specs live at catalog `spec:` paths
  (`skills/<category>/<name>/references/behavior-spec.md`). Does not enumerate
  `(game-workspace)/skills/` or `(game-workspace)/agents/`.

---

## Static Assertions (Structural)

Verified automatically by `/skill-test static` — no fixture needed.

- [ ] Has required frontmatter fields: `name`, `description`, `metadata.hermes` only (Claude-only keys are not required)
- [ ] Has ≥2 phase headings
- [ ] Contains verdicts: COMPLIANT, NON-COMPLIANT, WARNINGS (static mode); PASS, FAIL, PARTIAL (spec mode); COMPLETE (audit mode)
- [ ] Body instructs `write_file` or `patch` for optional result/catalog writes and includes scoped write-authorization language
- [ ] Has a next-step handoff (e.g., `/skill-improve` to fix issues found)
- [ ] `metadata.hermes.tags` includes a framework tag (e.g. `aesir-gameworks`) or `related_skills` is a list
- [ ] `description` is non-empty and states when to use; body does not invoke `Glob`, `Grep`, `Read`, `Write`, `Edit`, or `Task`

---

## Director Gate Checks

None. `/skill-test` is a meta-utility skill. No director gates apply.

---

## Test Cases

### Case 1: Static Mode — Well-formed skill, all 7 checks pass, COMPLIANT

**Fixture:**
- Cwd is the distribution or installed profile (`skills/studio` exists)
- `search_files` with `file_glob: skills/*/*/SKILL.md` finds `skills/workflows/brainstorm/SKILL.md`
- That file is well-formed:
  - Frontmatter has `name`, `description`, `metadata.hermes` (no Claude-only keys required)
  - Has ≥2 phase headings
  - Has verdict keywords
  - Has scoped write-authorization rules (existing approval accepted; new scope requires approval)
  - Has a next-step handoff
  - `tags` includes `aesir-gameworks` or `related_skills` is a list
  - `description` states when to use; no Claude tool invocables
  - Documents director gates and gate mode behavior (lean/solo skips)

**Input:** `/skill-test static brainstorm`

**Expected behavior:**
1. Skill locates `skills/workflows/brainstorm/SKILL.md` via `search_files` (not a game-workspace glob)
2. Skill runs all 7 structural checks
3. All 7 checks pass
4. Skill outputs a PASS/FAIL table with all 7 checks marked PASS
5. Verdict is COMPLIANT

**Assertions:**
- [ ] Exactly 7 structural checks are reported
- [ ] All 7 are marked PASS
- [ ] Verdict is COMPLIANT
- [ ] No files are written

---

### Case 2: Static Mode — Write-Capable Skill Missing Scoped Authorization Rules

**Fixture:**
- Cwd is the distribution or installed profile
- `skills/workflows/some-skill/SKILL.md` exists (located via `search_files` `file_glob: skills/*/*/SKILL.md`)
- The skill **body** instructs `write_file` or `patch`
- The skill body has no policy checking existing approval or requiring approval for new write scope

**Input:** `/skill-test static some-skill`

**Expected behavior:**
1. Skill reads `skills/workflows/some-skill/SKILL.md`
2. Check 4 (collaborative write protocol) fails: body instructs `write_file` or
   `patch` but no scoped write-authorization policy found
3. All other checks may pass
4. Verdict is NON-COMPLIANT with Check 4 as the failing assertion
5. Output lists Check 4 as FAIL with explanation

**Assertions:**
- [ ] Check 4 is marked FAIL
- [ ] Explanation identifies the mismatch (body instructs `write_file`/`patch` without scoped write-authorization rules)
- [ ] A variant with existing-approval and new-scope rules passes Check 4 even without the literal "May I write" phrase; this is a structural check, not proof of live compliance
- [ ] Verdict is NON-COMPLIANT
- [ ] Other passing checks are shown (not only the failure)
- [ ] Check 4 does not inspect a tools allowlist

---

### Case 3: Spec Mode — gate-check Skill Evaluated Against Spec

**Fixture:**
- Catalog entry `gate-check` has `spec: skills/workflows/gate-check/references/behavior-spec.md`
- That spec exists and contains 5 test cases
- `skills/workflows/gate-check/SKILL.md` exists

**Input:** `/skill-test spec gate-check`

**Expected behavior:**
1. Skill reads both the skill file and the spec file from the catalog `spec:` path
2. Skill evaluates each of the 5 test case assertions against the skill's behavior (reasoning check)
3. For each case: PASS if skill behavior matches spec assertions, FAIL if not
4. Skill produces a case-by-case result table
5. Overall verdict: PASS (all 5), PARTIAL (some), or FAIL (majority failing)
6. Offers to write results to `skill_view('framework-qa', file_path='references/results/')` after scoped authorization (does not write until authorized)

**Assertions:**
- [ ] Spec path comes from catalog.yaml `spec:` (not `tests/skills/` and not a nested `skills/gate/` tree)
- [ ] All 5 test cases from the spec are evaluated
- [ ] Each case has an individual PASS/FAIL result
- [ ] Overall verdict is PASS, PARTIAL, or FAIL based on case results
- [ ] No files are written until the user authorizes the results path

---

### Case 4: Audit Mode — Coverage Table of Workflow Skills and Role Skills

**Fixture:**
- Cwd is the distribution or installed profile (`skills/studio` exists)
- `skill_view('framework-qa', file_path='references/catalog.yaml')` lists **73** workflow skills and **49** role skills
- Each entry has a `spec:` path under `skills/<category>/<name>/references/behavior-spec.md`
- `search_files` `file_glob: skills/*/*/SKILL.md` can confirm those files
- There is **no** `(game-workspace)/skills/` tree and **no** `(game-workspace)/agents/` tree — fixtures must not require them

**Input:** `/skill-test audit`

**Expected behavior:**
1. If cwd has no `skills/studio`, the skill stops and tells the user to run from
   the distribution or installed profile (does not glob a game workspace)
2. Otherwise it reads the catalog and reports 73 workflow skills + 49 role skills
3. Spec existence is checked at each catalog `spec:` path
4. Skill produces a coverage table (Has Spec, last test dates, results)
5. Verdict is COMPLETE

**Assertions:**
- [ ] Reports 73 workflow skills and 49 role skills (not 52 or 72)
- [ ] Role skills are `skills/agents/<name>/SKILL.md`, not `(game-workspace)/agents/[name].md`
- [ ] "Has Spec" uses catalog `spec:` paths next to each skill
- [ ] Does not glob `(game-workspace)/skills/` or `(game-workspace)/agents/`
- [ ] Verdict is COMPLETE
- [ ] No files are written

---

### Case 5: Category Mode — Gate Skill Evaluated Against Quality Rubric

**Fixture:**
- `skill_view('framework-qa', file_path='references/quality-rubric.md')` has a `### gate` section with metrics G1–G5
- Catalog assigns `gate-check` `category: gate`
- `skills/workflows/gate-check/SKILL.md` exists

**Input:** `/skill-test category gate-check`

**Expected behavior:**
1. Skill reads `skill_view('framework-qa', file_path='references/quality-rubric.md')` and identifies the gate section
2. Skill evaluates `skills/workflows/gate-check/SKILL.md` against criteria G1–G5
3. Each criterion is scored: PASS, PARTIAL, or FAIL
4. Overall category score is computed
5. Verdict is COMPLIANT (all pass), WARNINGS (some partial), or NON-COMPLIANT (failures)

**Assertions:**
- [ ] All gate criteria (G1–G5) from quality-rubric.md are evaluated
- [ ] Each criterion has an individual score
- [ ] Overall verdict reflects the score distribution
- [ ] Rubric is read from `skill_view('framework-qa', file_path='references/quality-rubric.md')`, not `tests/skills/`
- [ ] No files are written until catalog-update authorization is granted

---

## Protocol Compliance

- [ ] Static mode checks exactly 7 structural assertions
- [ ] Spec mode evaluates each test case from the spec file individually (reasoning check)
- [ ] Audit mode covers 73 workflow skills AND 49 role skills from the catalog
- [ ] Category mode reads quality-rubric.md to get criteria (not hardcoded)
- [ ] Static and audit write no files; spec/category write only after scoped authorization to `skill_view('framework-qa', file_path='references/results/')` and/or `catalog.yaml`
- [ ] Suggests `/skill-improve` as the next step when issues are found
- [ ] Refuses to run against a game workspace that has no `skills/studio`

---

## Coverage Notes

- The skill-test skill is self-referential (it can test itself). The static
  mode case for skill-test's own SKILL.md is not separately fixture-tested to
  avoid infinite recursion in test design.
- The specific 7 structural checks are defined in the skill body; only Check 4
  (scoped write authorization when the body instructs `write_file`/`patch`) is
  individually tested here because it has the most nuanced logic.
- Audit counts are **73 workflow + 49 role** from `catalog.yaml`, not 52/72.
  Specs live next to each skill; do not assume a nested `skills/gate/` tree or
  a game-workspace `skills/` / `agents/` tree.
- Check 7 (Claude tool invocables) is covered by static assertions rather than
  a dedicated case.
