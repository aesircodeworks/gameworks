> **Upstream:** Derived from Claude Code Game Studios by Donchitos (MIT). https://github.com/Donchitos/Claude-Code-Game-Studios — adapted for Hermes Agent / Aesir Gameworks.

# Skill Test Spec: /[skill-name]

## Skill Summary

[One paragraph: what this skill does, when to use it, what it produces. Include
the primary output artifact, the verdict format it uses, and which pipeline stage
it belongs to.]

---

## Static Assertions (Structural)

Verified automatically by `/skill-test static` — no fixture needed.

- [ ] Has required frontmatter fields: `name`, `description`, `metadata.hermes`
- [ ] Has ≥2 phase headings (`## Phase N` or numbered `##` sections)
- [ ] Contains verdict keywords: [list the ones expected, e.g., PASS, FAIL, CONCERNS]
- [ ] If the body instructs `write_file` or `patch`: scoped write-authorization language is present
- [ ] Has a next-step handoff at the end
- [ ] `metadata.hermes.tags` includes a framework tag (e.g. `aesir-gameworks`) or `related_skills` is a list
- [ ] `description` is a specific capability sentence; body does not invoke `Glob`, `Grep`, `Read`, `Write`, `Edit`, or `Task`

---

## Test Cases

### Case 1: Happy Path — [short description]

**Fixture:** [Describe the assumed project state. Which files exist? What do they
contain? E.g., "game-concept.md exists with all 8 required sections complete.
systems-index.md exists. All MVP GDDs are present and individually reviewed."]

**Input:** `/[skill-name] [args]`

**Expected behavior:**
1. [Phase 1 action — what the skill should read or check]
2. [Phase 2 action — what the skill should evaluate]
3. [Phase N action — what the skill should output]

**Assertions:**
- [ ] Skill reads [specific file] before producing output
- [ ] Output includes verdict keyword [PASS/FAIL/etc.]
- [ ] Output lists [specific content] from the fixture
- [ ] Skill asks for approval before writing any file

---

### Case 2: Failure Path — [short description, e.g., "Missing required artifact"]

**Fixture:** [Describe the failure state. E.g., "game-concept.md is missing.
No files exist in design/gdd/."]

**Input:** `/[skill-name] [args]`

**Expected behavior:**
1. [Phase 1: skill detects missing file]
2. [Phase 2: skill surfaces the gap rather than assuming OK]
3. [Output: FAIL or BLOCKED verdict with specific blocker named]

**Assertions:**
- [ ] Skill does NOT output PASS when the fixture is incomplete
- [ ] Skill names the specific missing artifact
- [ ] Skill suggests a remediation action (e.g., "Run /[other-skill]")
- [ ] Skill does not create files to fill in the gap without asking

---

### Case 3: Edge Case — [short description, e.g., "No argument provided"]

**Fixture:** [State of project files for this case]

**Input:** `/[skill-name]` (no argument)

**Expected behavior:**
1. [What the skill should do when invoked without arguments]

**Assertions:**
- [ ] [assertion]

---

## Protocol Compliance

- [ ] Uses scoped write authorization before `write_file` / `patch`
- [ ] Presents findings or report before asking for write approval
- [ ] Ends with a recommended next step or follow-up skill as bullets after a done line (not a closing `clarify` menu)
- [ ] If the skill can mutate an artifact it just scored, a post-write done line does not reprint the pre-write verdict as live status
- [ ] Never auto-creates files without explicit user approval
- [ ] Does not skip phases or jump straight to a verdict without checking

---

## Coverage Notes

[Document what is intentionally NOT tested in this spec and why. Examples:
- "Case 3 (all-mode) is not covered because it runs too many checks to evaluate
  in a single spec — test each sub-mode individually."
- "The database integration path is not covered as it requires a live environment."
- "Edge cases involving corrupted YAML files are deferred to a future spec."]
