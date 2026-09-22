---
name: design-review
description: Review a game design document for handoff.
version: 2.0.0
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

# Design Review

**Model tier:** Medium

Reviews one GDD for handoff: completeness against the 8-section standard,
internal consistency, and implementability. The invocation ends in exactly one
of two states:

1. **Approved** — the verdict leads the output. Suggestions ride along inside
   an approved verdict; they never block.
2. **A decision request** — one consolidated menu of the unresolved design
   decisions that block approval, each with a proposed default, asked via one
   `clarify` call. The user's answer is the resolution.

Never close by filing findings into a report or log while the decision stays
buried in prose.

## Closure contract

- **Verdict first.** `### Verdict:` is the first section of every review output,
  on the first pass and every re-review.
- **Blocking is a closed list.** Only these block:
  1. A programmer would build the wrong thing from the text as written.
  2. Two rules contradict (within this GDD, or between this GDD and a dependency).
  3. A formula is mathematically wrong or degenerates at plausible input bounds.
  4. A stated acceptance criterion is untestable as written.
  5. A required section of the 8-section standard is missing.
- Everything else — wording, labels, citation hygiene, scoping parentheticals,
  near-duplicate criteria, style, hypothetical edge cases — is a **suggestion**.
  Suggestions appear in the review and the log but never change the verdict.
- **Open Questions need consent.** A finding may be parked as an Open Question
  only if the user accepted that parking through the decision menu. A parked
  OQ the user accepted is **decided** (record in the GDD: `Decided: <choice>
  (<date>)`) and never re-opens in a later review. Silent parking is forbidden.

## Phase 0: Parse Arguments

Extract `--depth [lean|full|solo]`. **Default is `lean`.** `--depth` controls
this skill's analysis only — never read the global review-mode file. Preserve
the depth across every pass in this invocation.

- **`lean`** (default): all phases, no delegation — the main reviewer performs
  the whole review and any re-review.
- **`full`**: adds the adversarial specialist panel (Phase 3b). Opt in with
  `--depth full`, or offer it after a lean pass finds rule- or formula-level
  blockers — offer, never switch implicitly.
- **`solo`**: Phases 1–4 only; return the review to the caller. No Phase 5,
  no writes, no revision loop.

## Phase 1: Load Documents

Read the target GDD in full, `AGENTS.md`, and the GDDs it depends on (check
`design/gdd/`). Validate the dependency graph: flag declared dependencies whose
GDD file does not exist. Read `design/gdd/game-concept.md` or
`design/narrative/` for tone/pillar conflicts if present. If
`design/gdd/reviews/[doc-name]-review-log.md` exists, read the latest entry —
this is a re-review; track whether prior blocking items were addressed.

## Phase 2: Completeness Check

Evaluate against the Design Document Standard:

- [ ] Overview (one-paragraph summary)
- [ ] Player Fantasy (intended feeling)
- [ ] Detailed Rules (unambiguous mechanics)
- [ ] Formulas (all math defined with variables)
- [ ] Edge Cases (unusual situations handled)
- [ ] Dependencies (other systems listed)
- [ ] Tuning Knobs (configurable values identified)
- [ ] Acceptance Criteria (testable success conditions)

## Phase 3: Consistency and Implementability

- Do formulas produce values matching described behavior? Any degenerate
  outputs at min/max plausible inputs?
- Do edge cases contradict the main rules?
- Are rules precise enough to implement without guessing? Any hand-wave sections?
- Does this conflict with existing mechanics, or the game's tone and pillars?

## Phase 3b: Adversarial Panel (full mode only)

Skip in `lean` or `solo`. Before spawning, print:
> "Full review: spawning specialist agents in parallel. This typically takes
> 8–15 minutes. The default `--depth lean` is a faster single-session review."

**Step 1 — Pick specialists.** Spawn only the domains the GDD actually
touches: costs/economy → `economy-designer`; combat stats → `game-designer` +
`systems-designer`; AI → `ai-programmer`; levels → `level-designer`;
progression → `economy-designer`; UI → `ux-designer`; narrative →
`narrative-director`; feel/timing → `gameplay-programmer`; multiplayer →
`network-programmer`; audio → `audio-director`; performance →
`performance-analyst`; acceptance criteria → `qa-lead`; data schemas →
`systems-designer`. `game-designer` is the baseline for any gameplay system;
`systems-designer` for anything with formulas. Neither is required for pure
UI, audio, or lore documents.

**Step 2 — Spawn all in parallel with `delegate_task`.** Never simulate a
specialist internally. Prompt adversarially ("find what is wrong,
underspecified, or missing"), and give each the materiality bar: *report
everything, but mark BLOCKING only if it meets the closed list in the closure
contract; everything else is a SUGGESTION.* Targeted prompts: `game-designer`
anchors to the stated Player Fantasy; `systems-designer` plugs boundary values
into every formula; `qa-lead` flags acceptance criteria that are not
independently testable.

**Step 3 — Synthesis.** After specialists respond, spawn `creative-director`
with the GDD, all findings, and any disagreements. Its synthesis backs the
Phase 4 verdict.

**Step 4 — Surface disagreements** explicitly in Phase 4; never silently pick
one side. Tag every finding with its source: `[game-designer]`,
`[economy-designer]`, `[creative-director]`, etc.

## Phase 4: Output Review

```
## Design Review: [Document Title]

### Verdict: [APPROVED / APPROVED WITH SUGGESTIONS / NEEDS REVISION / MAJOR REVISION NEEDED]

Specialists consulted: [list, or "none (--depth lean|solo)"]
Re-review: [Yes — prior verdict X on YYYY-MM-DD / No — first review]

### Completeness: [X/8 sections present]
### Dependency Graph
[each declared dependency: exists / NOT FOUND]
### Blocking Issues
[closed-list items only, each tagged with its source]
### Suggestions
[advisory items, source-tagged, ordered by value]
### Specialist Disagreements
[both sides, unresolved — user adjudicates]
### Open Questions needing a decision
[unresolved design decisions blocking approval, each with a proposed default]
### Scope Signal
[Rough scope signal: S/M/L/XL — producer should verify before sprint planning]
```

- **APPROVED** — no blocking issues, no suggestions.
- **APPROVED WITH SUGGESTIONS** — no blocking issues; suggestions listed. Both
  approved verdicts write `Approved` status.
- **NEEDS REVISION** — one or more blocking issues that are localized fixes.
- **MAJOR REVISION NEEDED** — ≥3 missing sections or a contradictory core loop.

No files are written in Phase 4. Present this after every pass. In `lean` and
`solo`, give the main reviewer's verdict; never attribute it to an unspawned
creative director. In `solo`, stop here and return the review.

## Phase 5: Decide, Fix, Re-review

`clarify` is for in-skill decisions and write authorization only — never a
closing menu. Follow the scoped-approval rules in `skill_view('gameworks',
file_path='references/collaborative-design-principle.md')`.

**Step 1 — Decision menu (before fixes).** If blocking items are unresolved
design decisions, present them in ONE `clarify` call (max 5 questions, 4
choices each), recommended default first. Accepted decisions become the fix
content and close their Open Questions as `Decided`. Never re-ask a decided
question.

**Step 2 — Changeset approval.** Read `design/gdd/systems-index.md` if present
and locate the row. Offer in one `clarify` (substituting real paths):

- `[A] Apply the proposed fixes and update this system in design/gdd/systems-index.md: In Review after editing, Approved only if the re-review approves`
- `[B] Apply the fixes only — leave the index unchanged`
- `[C] Leave the GDD unchanged; set this system to In Review`
- `[D] Skip GDD and index updates`

Plus append the review-log entry automatically at invocation end — review logs
are the skill's own record and never need a write prompt. Skip absent index
rows and no-ops; honor narrower approvals; never re-offer declined targets. A
review-only request authorizes no design-artifact writes. An APPROVED verdict
with no fixes skips to the status-change question.

**Step 3 — Apply fixes.** Work the approved blocking items, then verify by
re-reading the patched sections (blocker → fix applied table).

**Step 4 — Delta re-review in this invocation.** Re-review the **patched
sections and their direct consumers** — not the whole document.

- *lean*: the main reviewer re-reviews the delta.
- *full*: if fixes touched rules, formulas, or added/removed systems, respawn
  the specialists owning the touched domains plus `creative-director` on the
  delta with prior findings as context; otherwise one `creative-director`
  synthesis pass over the delta suffices.
- **Convergence cap:** from the second scored pass on, reviewers rule only on
  (a) whether prior blockers are resolved and (b) defects the patches
  introduced. Findings on untouched text are recorded as suggestions in the
  log — they never block and never trigger another pass.

**Step 5 — Close.** Present the new Phase 4 (verdict first). If approved,
apply the authorized `Approved` transition and finish. If blocking items
remain, present the decision menu and offer the next batch (Step 2). If fixes
are declined, close with the latest completed verdict.

## Review Log and Status

One entry per invocation, appended at invocation end:

```
## Review — [YYYY-MM-DD] — Verdict: [final verdict, or "unscored — re-review pending"]
Scope signal: [S/M/L/XL]
Specialists: [list]
Passes: [one line per scored pass: blockers found → fixed]
Suggestions: [count]
Decisions: [accepted decision-menu choices, or "none"]
```

systems-index statuses are `Draft` / `In Review` / `Approved`. `Approved` is
written only after a completed review at the selected depth approves the
current text. If the invocation ends with patches applied but the re-review
incomplete, log `unscored — re-review pending`, leave the status `In Review`,
and name the real path and `--depth` in the follow-up.

## Done

Print `Design review is done. Verdict: [X].` — the completed verdict, or
`Design review is done. Pre-patch score: [X]. Patched [N] blockers. Live
verdict: unscored.` when the re-review could not complete. Follow-ups as
bullets, real paths only, omitting any that do not apply:

- Complete the pending re-review: `/design-review <doc-path> --depth <depth>`
  (only when unscored)
- `/design-review <other-gdd-path>` — another GDD In Review
- `/consistency-check` — if ≥1 other GDD exists
- `/review-all-gdds` — if ≥2 GDDs exist
- `/design-system <next-system>` — next in design order

## Pitfalls

- **Mode leakage:** only `full` delegates. Never switch depth implicitly.
- **Verdict scope:** a verdict describes the text actually reviewed. A patched
  GDD is unscored until the delta re-review completes — editing alone never
  establishes APPROVED.
- **Pedantry:** findings outside the closed blocking list never gate a
  verdict, no matter how correct.
- **Burial:** decisions reach the user through the menu, not through report
  prose or logs.
