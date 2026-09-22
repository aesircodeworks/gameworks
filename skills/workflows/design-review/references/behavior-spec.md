# Skill Test Spec: /design-review

**Model tier:** Medium

## Skill Summary

`/design-review` reads a game design document (GDD) and evaluates it against
the project's 8-section design standard (Overview, Player Fantasy, Detailed
Rules, Formulas, Edge Cases, Dependencies, Tuning Knobs, Acceptance Criteria).
It checks internal consistency and implementability under a closure contract:
the verdict is the first section of every review output; blocking is a closed
five-item list (wrong-buildable meaning, rule contradiction, wrong/degenerate
formula, untestable stated AC, missing required section); everything else is a
suggestion and never gates the verdict. Verdicts are APPROVED, APPROVED WITH
SUGGESTIONS, NEEDS REVISION, MAJOR REVISION NEEDED — both approved verdicts
write `Approved` status. Default depth is `lean` (no delegation); `full` adds
the specialist panel and creative-director; `solo` returns at Phase 4. After
approved fixes the skill runs a delta re-review (patched sections plus direct
consumers) in the same invocation, under a convergence cap: from the second
scored pass, reviewers rule only on prior blockers and defects the patches
introduced. Unresolved design decisions are surfaced through one consolidated
decision menu with proposed defaults before fixes; a user-accepted Open
Question parking is decided and never re-opens. One review-log entry per
invocation; systems-index statuses are Draft / In Review / Approved.

---

## Static Assertions (Structural)

Verified automatically by `/skill-test static` — no fixture needed.

- [ ] Has required frontmatter fields: `name`, `description`, `metadata.hermes`
- [ ] Has ≥2 phase headings or numbered steps
- [ ] Contains verdict keywords: APPROVED, APPROVED WITH SUGGESTIONS, NEEDS REVISION, MAJOR REVISION NEEDED
- [ ] Contains the closure contract section with the closed blocking list
- [ ] Default `--depth` is `lean`
- [ ] If the body instructs `write_file` or `patch`, scoped write-authorization language is present (Phase 5 changeset approval). Phase 4 is read-only.
- [ ] Output format is documented (review template shown in skill body, verdict first)

---

## Test Cases

### Case 1: Happy Path — Complete GDD, all 8 sections present

**Fixture:** `design/gdd/light-manipulation.md` (use
`_fixtures/minimal-game-concept.md` as a stand-in) with all 8 sections, at
least one formula with defined variables, and ≥3 testable criteria.

**Input:** `/design-review design/gdd/light-manipulation.md`

**Assertions:**
- [ ] Skill reads the target file before producing any output
- [ ] Verdict section appears first: APPROVED (clean) or APPROVED WITH SUGGESTIONS (advisory items found)
- [ ] Output shows "Completeness: 8/8 sections present"
- [ ] Advisory items appear under Suggestions, never as blockers
- [ ] No specialist agents are spawned (lean is the default)
- [ ] Output states `Specialists consulted: none (--depth lean)`

### Case 2: Failure Path — Incomplete GDD (4/8 sections)

**Fixture:** GDD with 4 of 8 sections (Formulas, Edge Cases, Tuning Knobs,
Acceptance Criteria missing) from `_fixtures/incomplete-gdd.md`.

**Input:** `/design-review design/gdd/light-manipulation.md`

**Assertions:**
- [ ] Verdict first: MAJOR REVISION NEEDED (≥3 sections missing)
- [ ] Output names each missing section
- [ ] Output does not claim the document is implementation-ready
- [ ] No files are written on this path

### Case 3: Partial Path — 7/8 sections, minor issues only

**Fixture:** All sections except Formulas; described behavior mentions numeric
values without formulas; ACs are vague ("feels good").

**Assertions:**
- [ ] Missing Formulas section is blocking (closed-list item 5)
- [ ] Verdict is NEEDS REVISION, with the missing section as the blocking item
- [ ] Vague ACs are flagged (closed-list item 4 when an AC is stated; phrasing-only issues are suggestions)
- [ ] Decision menu precedes the changeset question when a blocking item needs a design decision

### Case 4: Edge Case — File not found

**Assertions:**
- [ ] Clear error naming the missing file; suggests checking the path or listing `design/gdd/`
- [ ] No verdict is produced

### Case 5: Pedantry gate — advisory findings never block

**Fixture:** Complete, consistent GDD whose only findings are citation
labeling, phrasing, near-duplicate ACs, and scoping parentheticals.

**Assertions:**
- [ ] Verdict is APPROVED WITH SUGGESTIONS, never NEEDS REVISION
- [ ] Suggestions are listed and source-tagged but do not gate the verdict
- [ ] The skill does not propose a revision loop for suggestion-only findings

### Case 6: Full mode — delta re-review after approved fixes

**Fixture:** NEEDS REVISION in pass 1 (full); user approves fixes and
conditional index transitions; the delta re-review approves the patched text.

**Assertions:**
- [ ] Pass 1 spawns the relevant specialists, then creative-director synthesis; verdict first in both Phase 4 outputs
- [ ] Re-review covers the patched sections and their direct consumers — not a full-panel respawn of the whole document
- [ ] Full panel respawn happens only when fixes touched rules, formulas, or added/removed systems
- [ ] Convergence cap: pass 2 rules only on prior blockers and patch-introduced defects; findings on untouched text are logged as suggestions and do not block
- [ ] Both Phase 4 reports are presented; no done line between passes
- [ ] `Approved` is written only after the re-review approves, within the displayed authorization
- [ ] Closes with `Design review is done. Verdict: APPROVED WITH SUGGESTIONS.` or `Verdict: APPROVED.`

### Case 7: Companion approval — fixes and tracking in one decision

**Fixture:** NEEDS REVISION GDD with an existing systems-index row.
**Input:** Approve fixes + conditional index transitions.

**Assertions:**
- [ ] Decision menu (design decisions with defaults) precedes the changeset question when needed
- [ ] One `clarify` call collects the action (max 4 choices); no question about writing the review log — it is appended automatically
- [ ] Applies and verifies GDD and index changes without another prompt; appends the single review-log entry at invocation end
- [ ] No scoring-pass log format exists (one entry per invocation)
- [ ] With all applicable writes already authorized, performs them without re-asking

### Case 8: Companion boundaries

**Variants and assertions:**
- [ ] Row already `In Review`: skips the no-op write; the conditional `Approved` transition may be offered with fixes
- [ ] Index or row missing: skips/reports; creates neither
- [ ] Unpatched APPROVED / APPROVED WITH SUGGESTIONS: offers `Approved`; appends the log automatically; writes `Approved` only after authorization
- [ ] All writes declined: stays read-only, no repeated permission question
- [ ] Approval limited to `In Review` does not authorize `Approved`

### Case 9: Decision menu — Open Questions surfaced and decided

**Fixture:** Blocking items that are unresolved design decisions; the skill
proposes defaults.

**Assertions:**
- [ ] One consolidated `clarify` (max 5 questions, 4 choices each, default first) — decisions are never buried in report prose
- [ ] Accepted decisions become fix content and close their Open Questions as `Decided: <choice> (<date>)`
- [ ] A decided OQ does not re-open in the same or a later pass
- [ ] Parking a finding as an OQ without user acceptance is a contract violation

### Case 10: Lean mode — default depth, same cycle, no delegation

**Assertions:**
- [ ] No `--depth` flag behaves as lean
- [ ] After approved fixes, the main reviewer re-reviews the delta in the same invocation
- [ ] No specialist or creative-director is ever spawned; no fabricated Senior Verdict
- [ ] A lean pass finding rule- or formula-level blockers may offer `--depth full`; it never switches implicitly

### Case 11: Solo mode — return the review without Phase 5

**Assertions:**
- [ ] Runs Phases 1–4 without delegation; verdict first
- [ ] Returns the review to the caller; no writes, no revision loop, no decision menu

### Case 12: Interrupted re-review — no stale or fabricated verdict

**Fixture:** GDD patched, but the delta re-review cannot complete.

**Assertions:**
- [ ] Reports the actual failure; does not silently switch depth
- [ ] Tracking stays `In Review`; no `Approved` is written
- [ ] Done line reports the pre-patch score as history and `Live verdict: unscored`
- [ ] The single log entry reads `unscored — re-review pending`

---

## Protocol Compliance

- [ ] No writes during Phase 4; Phase 5 writes only with scoped authorization
- [ ] Verdict is the first section of every review output
- [ ] Full/lean end with a done line and follow-up bullets (no closing `clarify`); solo returns Phase 4 to its caller
- [ ] One review-log entry per invocation; systems-index uses Draft / In Review / Approved only

---

## Coverage Notes

- Cross-system consistency across multiple GDDs is covered by the
  `/review-all-gdds` spec, not here.
- These cases check the written workflow contract, not live model behavior or
  delegation performance. Runtime execution requires a game workspace.
- Cases 5, 6, and 9 cover the pedantry gate, delta re-review with convergence
  cap, and the decision menu — the closure contract's three new behaviors.
