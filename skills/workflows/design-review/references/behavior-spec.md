> **Upstream:** Derived from Claude Code Game Studios by Donchitos (MIT). https://github.com/Donchitos/Claude-Code-Game-Studios — adapted for Hermes Agent / Aesir Gameworks.

# Skill Test Spec: /design-review

**Model tier:** Medium

## Skill Summary

`/design-review` reads a game design document (GDD) and evaluates it against
the project's 8-section design standard (Overview, Player Fantasy, Detailed
Rules, Formulas, Edge Cases, Dependencies, Tuning Knobs, Acceptance Criteria).
It checks for internal consistency, implementability, and cross-system
conflicts. It produces a verdict of APPROVED, NEEDS REVISION, or MAJOR
REVISION NEEDED. Phase 4 is read-only. Phase 5 may write the GDD on an
authorized Revise now path that explicitly includes applicable systems-index
updates, plus an independently optional review log. Full and lean repeat the
review after approved fixes in the same invocation, preserving the selected
`--depth`: full respawns specialists then creative-director; lean delegates
neither. Solo stops at Phase 4 without writes or a revision loop. A verdict
always describes the text actually reviewed, never a later unreviewed edit.

---

## Static Assertions (Structural)

Verified automatically by `/skill-test static` — no fixture needed.

- [ ] Has required frontmatter fields: `name`, `description`, `metadata.hermes`
- [ ] Has ≥2 phase headings or numbered steps
- [ ] Contains verdict keywords: APPROVED, NEEDS REVISION, MAJOR REVISION NEEDED
- [ ] If the body instructs `write_file` or `patch`, scoped write-authorization language is present (Phase 5 Revise now and tracking writes). Phase 4 is read-only.
- [ ] Output format is documented (review template shown in skill body)

---

## Test Cases

### Case 1: Happy Path — Complete GDD, all 8 sections present

**Fixture:**
- `design/gdd/light-manipulation.md` exists (use `_fixtures/minimal-game-concept.md`
  as a stand-in — represents a complete document with all required content)
- All 8 required sections are populated with substantive content
- Formulas section contains at least one formula with defined variables
- Acceptance Criteria section contains at least 3 testable criteria

**Input:** `/design-review design/gdd/light-manipulation.md`

**Expected behavior:**
1. Skill reads the target document in full
2. Skill reads AGENTS.md for project context and standards
3. Skill evaluates all 8 required sections (present/absent check)
4. Skill checks internal consistency (formulas match described behavior)
5. Skill checks implementability (rules are precise enough to code)
6. Skill outputs structured review with section-by-section status
7. Skill outputs APPROVED verdict

**Assertions:**
- [ ] Skill reads the target file before producing any output
- [ ] Output includes a "Completeness" section showing X/8 sections present
- [ ] Output includes an "Internal Consistency" section
- [ ] Output includes an "Implementability" section
- [ ] Output ends with a verdict line: APPROVED / NEEDS REVISION / MAJOR REVISION NEEDED
- [ ] APPROVED verdict is given when all 8 sections are present and consistent

---

### Case 2: Failure Path — Incomplete GDD (4/8 sections)

**Fixture:**
- `design/gdd/light-manipulation.md` exists using content from
  `tests/skills/_fixtures/incomplete-gdd.md` (4 of 8 sections populated;
  Formulas, Edge Cases, Tuning Knobs, Acceptance Criteria are missing)

**Input:** `/design-review design/gdd/light-manipulation.md`

**Expected behavior:**
1. Skill reads the document
2. Skill identifies 4 missing sections
3. Skill outputs "Completeness: 4/8 sections present"
4. Skill lists specifically which 4 sections are missing
5. Skill outputs MAJOR REVISION NEEDED verdict (not APPROVED or NEEDS REVISION)

**Assertions:**
- [ ] Output shows "4/8" in the completeness section (not a higher number)
- [ ] Output explicitly names each missing section (Formulas, Edge Cases, Tuning Knobs, Acceptance Criteria)
- [ ] Verdict is MAJOR REVISION NEEDED (not APPROVED or NEEDS REVISION) when ≥3 sections are missing
- [ ] Output does not suggest the document is implementation-ready
- [ ] Skill does not write any files on this path (no Revise now)

---

### Case 3: Partial Path — 7/8 sections, minor inconsistency

**Fixture:**
- GDD has all sections except Formulas
- The described behavior mentions numeric values but no formulas are defined
- Acceptance Criteria exist but are vague ("feels good" rather than measurable)

**Input:** `/design-review design/gdd/[document].md`

**Expected behavior:**
1. Skill identifies missing Formulas section
2. Skill flags vague acceptance criteria as an implementability issue
3. Skill outputs NEEDS REVISION verdict (not APPROVED, not MAJOR REVISION NEEDED)
4. Skill provides specific remediation notes for each issue

**Assertions:**
- [ ] Verdict is NEEDS REVISION (not APPROVED, not MAJOR REVISION NEEDED) for 7/8 with issues
- [ ] Output identifies the missing Formulas section specifically
- [ ] Output flags the vague acceptance criteria as an implementability gap
- [ ] Each flagged issue has a specific, actionable remediation note

---

### Case 4: Edge Case — File not found

**Fixture:**
- The path provided does not exist in the project

**Input:** `/design-review design/gdd/nonexistent.md`

**Expected behavior:**
1. Skill attempts to read the file
2. File not found
3. Skill outputs an error message naming the missing file
4. Skill suggests checking the path or listing files in `design/gdd/`
5. Skill does NOT produce a verdict

**Assertions:**
- [ ] Skill outputs a clear error when the file is not found
- [ ] Skill does NOT output APPROVED, NEEDS REVISION, or MAJOR REVISION NEEDED when file is missing
- [ ] Skill suggests a corrective action (check path, list available GDDs)

---

---

### Case 5: Director Gate — no gate spawned regardless of review mode

**Fixture:**
- `design/gdd/light-manipulation.md` exists with all 8 sections
- `production/session-state/review-mode.txt` exists with `full` (most permissive mode)

**Input:** `/design-review design/gdd/light-manipulation.md` (with full review mode active)

**Expected behavior:**
1. Skill reads the GDD document
2. Skill does NOT read `review-mode.txt` — this skill has no director gates
3. Skill produces the review output normally
4. No director gate agents are spawned at any point
5. Verdict is APPROVED (all 8 sections present in fixture)

**Assertions:**
- [ ] Skill does NOT spawn any director gate agent (CD-, TD-, PR-, AD- prefixed agents)
- [ ] Skill does NOT read `review-mode.txt` or equivalent mode file
- [ ] `--depth`, not global review mode or `--review`, selects the review pipeline.
- [ ] Output does not contain any "Gate: [GATE-ID]" entries.
- [ ] Full spawns creative-director as a senior reviewer after specialists, not as a director gate; lean and solo do not spawn it.

---

### Case 6: Full mode — Revise now, then review the updated GDD

**Fixture:**
- GDD receives NEEDS REVISION in the first pass
- User approves the displayed fixes and conditional index transitions; accepts logging
- The complete specialist and creative-director re-review approves the patched text

**Input:** `/design-review design/gdd/light-manipulation.md --depth full`

**Expected behavior:**
1. Specialists review in parallel, then `creative-director` synthesizes their findings
2. Phase 4 presents NEEDS REVISION before any changes are offered
3. Phase 5 applies approved fixes, verifies them, and sets the authorized index row to `In Review`
4. In the same invocation, reloads the current GDD and repeats Phases 1-4
5. Spawns all relevant specialists on the complete updated text, then a fresh creative-director review using the new findings
6. Presents Phase 4 again with the new APPROVED verdict
7. Applies the already-authorized `Approved` transition and appends the current review entry
8. Closes with `Design review is done. Verdict: APPROVED.`

**Assertions:**
- [ ] Default depth and explicit `--depth full` both use this cycle.
- [ ] Edit-verification alone never establishes APPROVED.
- [ ] A complete new specialist pass precedes the new creative-director synthesis.
- [ ] Updated text, prior findings, and applied fixes reach reviewers; old responses are not reused as current evidence.
- [ ] Re-review is not restricted to a targeted subset of the relevant specialists.
- [ ] Both Phase 4 reports are presented; no done line is printed between passes.
- [ ] No separate execution or re-review permission question is required after approved fixes.
- [ ] The final verdict describes the updated GDD, not the pre-patch score.
- [ ] `Approved` is written only after re-review and only within the displayed authorization.
- [ ] Logs distinguish the pre-patch score from the completed re-review; the latest entry is current.
- [ ] No same-file re-score follow-up appears after a completed re-review.

---

### Case 7: Companion approval — fixes and tracking in one decision

**Fixture:** A NEEDS REVISION GDD with an existing `Designed` systems-index row.
**Input:** Approve the displayed GDD fixes and `In Review` → conditional `Approved` transitions; decline logging.

**Assertions:**
- [ ] Before approval, shows concrete GDD/index paths, fixes, and current → proposed status.
- [ ] One `clarify` call collects the action and independent optional review-log choice.
- [ ] Applies and verifies the GDD and index changes without another index or log prompt.
- [ ] Does not write the declined review log; the patched GDD stays unscored until a complete re-review, and `Approved` requires that re-review to approve it.
- [ ] GDD-only approval is a selectable action, not dependent on free-text override; leaves the index unchanged and does not re-offer it.
- [ ] At most four action choices and five questions per call; dependent design decisions are resolved before write approval.
- [ ] With all applicable writes already authorized, performs them without another approval.

### Case 8: Companion boundaries — no-op, absent, declined, and partial writes

**Variants and assertions:**
- [ ] Row already `In Review`: skips that immediate no-op write; may offer the later conditional `Approved` transition with fixes.
- [ ] Index or row missing, including an untracked concept: skips/reports tracking; creates neither.
- [ ] Unpatched APPROVED: offers `Approved` plus optional log together, without automatically writing either.
- [ ] Unpatched NEEDS REVISION: tracking-only approval changes the row to `In Review`, not the GDD.
- [ ] All writes declined: stays read-only, with no repeated permission question.
- [ ] Index write fails after GDD write: reports the partial state, not synchronized success.
- [ ] A newly discovered design choice still needs resolution before the affected edit.
- [ ] Approval limited to `In Review` does not authorize a later `Approved` transition; obtain authorization for that new scope.

---

### Case 9: Lean mode — same revision cycle, no delegation

**Fixture:** First pass needs fixes; user approves GDD-only edits and declines logging; main review of the patched text approves it.
**Input:** `/design-review design/gdd/light-manipulation.md --depth lean`

**Assertions:**
- [ ] Repeats Phases 1-3 and 4 on the current text after approved fixes in the same invocation.
- [ ] Skips all of Phase 3b on every pass: neither specialists nor creative-director are spawned.
- [ ] Output states no specialists were consulted and does not fabricate a Senior Verdict.
- [ ] The main reviewer's new verdict is presented before closure.
- [ ] Declined index/log writes remain declined across all passes.
- [ ] Global review mode cannot upgrade lean to full.

### Case 10: Solo mode — return the review without Phase 5

**Variants:** APPROVED, NEEDS REVISION, and MAJOR REVISION NEEDED.
**Input:** `/design-review design/gdd/light-manipulation.md --depth solo`

**Assertions:**
- [ ] Runs Phases 1-3 and 4 without any delegation, even when global review mode is full.
- [ ] Returns the structured review and main reviewer's verdict to the caller.
- [ ] Does not enter Phase 5, prompt for edits, or write the GDD, index, or log.
- [ ] Does not begin a revision loop or fabricate specialist/director findings.

### Case 11: Further revisions — continue or decline inside this invocation

**Fixture:** The first patch is followed by a completed re-review that still needs revision.
**Variants:** `--depth full` and `--depth lean`; user approves another batch or declines it.

**Assertions:**
- [ ] Presents the new Phase 4 findings before offering the next batch of fixes.
- [ ] New design choices and changes outside the approved scope require approval.
- [ ] Approval repeats the same-depth review cycle; full retains the whole relevant panel and director, lean spawns neither.
- [ ] No arbitrary pass limit or automatic mode downgrade is introduced.
- [ ] Previously accepted/declined log and index choices are retained without repeat prompts.
- [ ] Declining further fixes closes with the latest completed verdict, not `unscored` or the initial score.
- [ ] Tracking-only selection does not cause another review of unchanged text.
- [ ] Prior pass findings are retained even if logging was declined.

### Case 12: Interrupted re-review — no stale or fabricated verdict

**Fixture:** A GDD was patched, but a required specialist/director (full) or main review (lean) cannot complete.

**Assertions:**
- [ ] Reports the actual failure and incomplete review; does not silently switch depth.
- [ ] Does not declare APPROVED from edit-verification, old findings, or partial specialist results.
- [ ] Leaves authorized tracking `In Review`, not `Approved`.
- [ ] Reports `Live verdict: unscored` and the pre-patch score as history.
- [ ] A recovery follow-up, if needed, names the real path and original `--depth`.

---

## Protocol Compliance

- [ ] Does NOT use write_file or patch during Phase 4. Phase 5 writes only with scoped authorization
- [ ] Presents complete findings before any verdict
- [ ] Does not ask for approval before producing the Phase 4 review (no writes to approve yet)
- [ ] Full/lean end with a done line and relevant follow-up bullets (no closing `clarify`); solo returns Phase 4 to its caller.
- [ ] After Revise now, the done line uses the completed re-review verdict, or `unscored` only when re-review could not complete.

---

## Coverage Notes

- Cross-system consistency checking (Case 3 in the skill's own phase list) is
  not directly tested here because it requires multiple GDD files to compare;
  this is covered by the `/review-all-gdds` spec instead.
- These cases check the written workflow contract, not live model behavior or
  delegation performance. Runtime execution requires a game workspace.
- Performance and edge cases involving very large GDD files are not in scope.
- Cases 6 and 9-12 cover full/lean revision cycles, solo isolation, decline, and
  interrupted re-review. Unpatched NEEDS REVISION retains its live verdict.
