> **Upstream:** Derived from Claude Code Game Studios by Donchitos (MIT). https://github.com/Donchitos/Claude-Code-Game-Studios — adapted for Hermes Agent / Aesir Gameworks.

# Skill Test Spec: /studio-help

**Model tier:** Light

## Skill Summary

`/studio-help` is a read-only navigator. It reads `production/stage.txt`, catalog artifacts, and session state, then prints a fact block, exactly one Next, at most one Optional, and `studio-help done.`

It is not a full audit (`/project-stage-detect`) and not a sprint snapshot (`/sprint-status`). A topic argument (e.g. `/studio-help testing`) may retarget Next or Optional; it does not print a skill list.

No files are written. No director gates. Verdict line is always `studio-help done.`

---

## Static Assertions (Structural)

Verified automatically by `/skill-test static` — no fixture needed.

- [ ] Has required frontmatter fields: `name`, `description`, `metadata.hermes`
- [ ] Has ≥2 phase headings
- [ ] Contains verdict keyword: COMPLETE
- [ ] Instructs the done line `studio-help done.`
- [ ] Does NOT contain "May I write" language (skill is read-only)
- [ ] Does NOT instruct "Also installed", "Where You Are", "Coming up", or "fresh session"
- [ ] Has a next-step handoff: exactly one `Next:` line in the output template

---

## Director Gate Checks

None. `/studio-help` is a read-only navigation skill. No director gates apply.

---

## Test Cases

### Case 1: Happy Path — Production stage with active sprint

**Fixture:**
- `production/stage.txt` contains `Production`
- `production/sprints/sprint-004.md` exists with in-progress stories
- `production/session-state/active.md` has a recent checkpoint

**Input:** `/studio-help`

**Expected behavior:**
1. Skill reads stage.txt and sprint / `sprint-status.yaml`
2. Output matches the fact / Next / Optional / done shape
3. `Phase  Production` is present
4. A Sprint fact line includes the sprint identity and in-progress count
5. `Focus` names the active artifact when `active.md` has one
6. Exactly one `Next:` line, a Production command with a named story or path (e.g. `/dev-story`)
7. No Done list, Coming up, Also installed, or gate warning
8. Last line is `studio-help done.`

**Assertions:**
- [ ] Current stage is shown as `Phase  Production`
- [ ] Sprint identity and in-progress count appear on a fact line
- [ ] Exactly one `Next:` line
- [ ] Next is a Production-stage command with a named target
- [ ] Output has no "Also installed", "Coming up", or "✓ Done"
- [ ] Last line is `studio-help done.`
- [ ] No files are written

---

### Case 2: Concept Stage — Engine set, concept missing

**Fixture:**
- `production/stage.txt` contains `Concept`
- No sprint files, no GDD files
- `docs/technical-preferences.md` is configured (engine selected)

**Input:** `/studio-help`

**Expected behavior:**
1. Skill reads stage.txt — Concept
2. Fact lines cover engine / concept status, not a workflow map
3. `Next:` is `/brainstorm` or `/setup-engine` as the first incomplete required step
4. No Production-stage commands as Next

**Assertions:**
- [ ] Stage is `Phase  Concept`
- [ ] Fact lines note concept missing and/or engine configured
- [ ] Exactly one `Next:` line; not `/dev-story`
- [ ] Last line is `studio-help done.`

---

### Case 3: No stage.txt — Fresh project

**Fixture:**
- No `production/stage.txt`
- No sprint files
- `docs/technical-preferences.md` has placeholders or is absent

**Input:** `/studio-help`

**Expected behavior:**
1. Skill infers Concept from missing artifacts
2. Does not print a Concept-through-Release map
3. `Next: /studio-start`

**Assertions:**
- [ ] Skill does not crash when stage.txt is absent
- [ ] No full workflow overview
- [ ] `Next: /studio-start`
- [ ] Last line is `studio-help done.`

---

### Case 4: Topic query — testing

**Fixture:**
- `production/stage.txt` contains `Production`
- Active sprint has a story with `Status: In Review`

**Input:** `/studio-help testing`

**Expected behavior:**
1. Facts stay Production (sprint / focus)
2. Next is one testing command that can run now (e.g. `/test-evidence-review` on the in-review story), or Next stays the required step and the testing command is Optional
3. Does not list three testing skills
4. Does not make `/sprint-plan` Next

**Assertions:**
- [ ] `Phase  Production` is present
- [ ] Exactly one `Next:` line
- [ ] Next or Optional is a testing-relevant command with a named target
- [ ] No list of 3+ testing skills
- [ ] Last line is `studio-help done.`

---

### Case 5: Director Gate Check — No gate; help is read-only navigation

**Fixture:**
- Any project state

**Input:** `/studio-help`

**Expected behavior:**
1. Skill prints the fact / Next / done shape
2. No director agents are spawned
3. No gate IDs appear in output
4. No write tool is called

**Assertions:**
- [ ] No director gate is invoked
- [ ] No write tool is called
- [ ] No gate skip messages appear
- [ ] Last line is `studio-help done.` without a gate check

---

### Case 6: Systems Design — facts then one review

**Fixture:**
- `production/stage.txt` contains `Systems Design`
- Eight GDDs written; one Approved; seven Designed
- `production/session-state/active.md` points at `design/gdd/audio.md` with review queued

**Input:** `/studio-help`

**Expected behavior:**
1. `Phase  Systems Design`
2. One GDD fact line with written / approved / Designed counts (named approved system)
3. `Focus  design/gdd/audio.md — review queued`
4. Does not `clarify` on `design-system`; index/GDD counts are enough
5. `Next: /design-review  design/gdd/audio.md`
6. Optional `/consistency-check` only if it can run now; if catalog order is after an incomplete `/review-all-gdds` and session queued it, include `(does not replace /design-review)`
7. No `/review-all-gdds` or `/gate-check` except as Next when that step is the blocker
8. No "fresh session"

**Assertions:**
- [ ] Fact line is counts, not a Done list
- [ ] Next names `design/gdd/audio.md`
- [ ] Does not `clarify`
- [ ] `/gate-check` and `/review-all-gdds` are absent unless they are Next
- [ ] Last line is `studio-help done.`

---

## Protocol Compliance

- [ ] Reads stage, sprint, and session state before printing
- [ ] Output is facts + one `Next:` row + optional Optional + `studio-help done.`
- [ ] A required catalog step with no `command:` still uses `Next: [imperative]  [named path]`, not a paragraph
- [ ] Topic query does not expand into a skill list
- [ ] Does not write any files
- [ ] Last line is `studio-help done.` in all cases

---

## Coverage Notes

- A completed sprint (all stories Done) is not separately tested; Next would be `/sprint-plan`.
- The skill does not validate that suggested skills are installed.
- Stage fallback when stage.txt is absent uses the same inference as `/project-stage-detect` and is not re-tested in detail.
