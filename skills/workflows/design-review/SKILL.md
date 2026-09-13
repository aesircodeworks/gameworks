---
name: design-review
description: Review a game design document for handoff.
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

## Phase 0: Parse Arguments

**Model tier:** Medium

Extract `--depth [full|lean|solo]` if present. Default is `full` when no flag is given.

**Note**: `--depth` controls the *analysis depth* of this skill (how many specialist agents are spawned). It is independent of the global review mode in `production/review-mode.txt`, which controls director gate spawning. These are two different concepts — `--depth` is about how thoroughly *this* skill analyses the document.

- **`full`**: Complete review — all phases + specialist agent delegation (Phase 3b)
- **`lean`**: All phases, no specialist agents — faster, single-session analysis
- **`solo`**: Phases 1-4 only, no delegation, no Phase 5 next-step prompt — use when called from within another skill

---

## Phase 1: Load Documents

Read the target design document in full. Read AGENTS.md to understand project context and standards. Read related design documents referenced or implied by the target doc (check `design/gdd/` for related systems).

**Dependency graph validation:** For every system listed in the Dependencies section, use search_files with `file_glob="design/gdd/*.md"` to check whether its GDD file exists. Flag any that don't exist yet — these are broken references that downstream authors will hit.

**Lore/narrative alignment:** If `design/gdd/game-concept.md` or any file in `design/narrative/` exists, read it. Note any mechanical choices in this GDD that contradict established world rules, tone, or design pillars. Pass this context to `game-designer` in Phase 3b.

**Prior review check:** Check whether `design/gdd/reviews/[doc-name]-review-log.md` exists. If it does, read the most recent entry — note what verdict was given and what blocking items were listed. This session is a re-review; track whether prior items were addressed.

---

## Phase 2: Completeness Check

Evaluate against the Design Document Standard checklist:

- [ ] Has Overview section (one-paragraph summary)
- [ ] Has Player Fantasy section (intended feeling)
- [ ] Has Detailed Rules section (unambiguous mechanics)
- [ ] Has Formulas section (all math defined with variables)
- [ ] Has Edge Cases section (unusual situations handled)
- [ ] Has Dependencies section (other systems listed)
- [ ] Has Tuning Knobs section (configurable values identified)
- [ ] Has Acceptance Criteria section (testable success conditions)

---

## Phase 3: Consistency and Implementability

**Internal consistency:**
- Do the formulas produce values that match the described behavior?
- Do edge cases contradict the main rules?
- Are dependencies bidirectional (does the other system know about this one)?

**Implementability:**
- Are the rules precise enough for a programmer to implement without guessing?
- Are there any "hand-wave" sections where details are missing?
- Are performance implications considered?

**Cross-system consistency:**
- Does this conflict with any existing mechanic?
- Does this create unintended interactions with other systems?
- Is this consistent with the game's established tone and pillars?

---

## Phase 3b: Adversarial Specialist Review (full mode only)

**Skip this phase in `lean` or `solo` mode.**

**This phase is MANDATORY in full mode.** Do not skip it.

**Before spawning any agents**, print this notice:
> "Full review: spawning specialist agents in parallel. This typically takes 8–15 minutes. Use `--review lean` for faster single-session analysis."

### Step 1 — Identify all domains the GDD touches

Read the GDD and identify every domain present. A GDD can touch multiple domains simultaneously — be thorough. Common signals:

| If the GDD contains... | Spawn these agents |
|------------------------|-------------------|
| Costs, prices, drops, rewards, economy | `economy-designer` |
| Combat stats, damage, health, DPS | `game-designer`, `systems-designer` |
| AI behaviour, pathfinding, targeting | `ai-programmer` |
| Level layout, spawning, wave structure | `level-designer` |
| Player progression, XP, unlocks | `economy-designer`, `game-designer` |
| UI, HUD, menus, player-facing displays | `ux-designer`, `ui-programmer` |
| Dialogue, quests, story, lore | `narrative-director` |
| Animation, feel, timing, juice | `gameplay-programmer` |
| Multiplayer, sync, replication | `network-programmer` |
| Audio cues, music triggers | `audio-director` |
| Performance, draw calls, memory | `performance-analyst` |
| Engine-specific patterns or APIs | Primary engine specialist (from `docs/technical-preferences.md`) |
| Acceptance criteria, test coverage | `qa-lead` |
| Data schema, resource structure | `systems-designer` |
| Any gameplay system | `game-designer` (always) |

Spawn `game-designer` for all GDDs that describe gameplay mechanics or player-facing rules.
Spawn `systems-designer` for all GDDs that contain formulas or system interaction rules.
These are the most common baselines — but not required for pure UI specs, audio specs, or lore documents. Use the domain table above to determine which specialists are truly relevant.

### Step 2 — Spawn all relevant specialists in parallel

**CRITICAL: `delegate_task` in this skill spawns a SUBAGENT — a separate independent
session with its own context window. It is NOT task tracking. Do NOT simulate specialist
perspectives internally. Do NOT reason through domain views yourself. You MUST issue
actual delegate_task calls. A simulated review is not a specialist review.**

Issue all delegate_task calls simultaneously. Do NOT spawn one at a time.

**Prompt each specialist adversarially:**
> "Here is the GDD for [system] and the main review's structural findings so far.
> Your job is NOT to validate this design — your job is to find problems.
> Challenge the design choices from your domain expertise. What is wrong,
> underspecified, likely to cause problems, or missing entirely?
> Be specific and critical. Disagreement with the main review is welcome."

**Additional instructions per agent type:**

- **`game-designer`**: Anchor your review to the Player Fantasy stated in Section B of this GDD. Does this design actually deliver that fantasy? Would a player feel the intended experience? Flag any rules that serve implementability but undermine the stated feeling.

- **`systems-designer`**: For every formula in the GDD, plug in boundary values (minimum and maximum plausible inputs). Report whether any outputs go degenerate — negative values, division by zero, infinity, or nonsensical results at the extremes.

- **`qa-lead`**: Review every acceptance criterion. Flag any that are not independently testable — phrases like "feels balanced", "works correctly", "performs well" are not ACs. Suggest concrete rewrites for any that fail this test.

### Step 3 — Senior lead review

After all specialists respond, spawn `creative-director` as the **senior reviewer**:
- Provide: the GDD, all specialist findings, any disagreements between them
- Ask: "Synthesise these findings. What are the most important issues? Do you agree with the specialists? What is your overall verdict on this design?"
- The creative-director's synthesis is the **scoring-pass verdict** in Phase 4. It is live document status only if Phase 5 does not write the GDD.

### Step 4 — Surface disagreements

If specialists disagree with each other or with the creative-director, do NOT silently pick one view. Present the disagreement explicitly in Phase 4 so the user can adjudicate.

Mark every finding with its source: `[game-designer]`, `[economy-designer]`, `[creative-director]` etc.

---

## Phase 4: Output Review

```
## Design Review: [Document Title]
Specialists consulted: [list agents spawned]
Re-review: [Yes — prior verdict was X on YYYY-MM-DD / No — first review]

### Completeness: [X/8 sections present]
[List missing sections]

### Dependency Graph
[List each declared dependency and whether its GDD file exists on disk]
- ✓ enemy-definition-data.md — exists
- ✗ loot-system.md — NOT FOUND (file does not exist yet)

### Required Before Implementation
[Numbered list — blocking issues only. Each item tagged with source agent.]

### Recommended Revisions
[Numbered list — important but not blocking. Source-tagged.]

### Specialist Disagreements
[Any cases where agents disagreed with each other or with the main review.
Present both sides — do not silently resolve.]

### Nice-to-Have
[Minor improvements, low priority.]

### Senior Verdict [creative-director]
[Creative director's synthesis and overall assessment.]

### Scope Signal
Estimate implementation scope based on: dependency count, formula count,
systems touched, and whether new ADRs are required.
- **S** — single system, no formulas, no new ADRs, <3 dependencies
- **M** — moderate complexity, 1-2 formulas, 3-6 dependencies
- **L** — multi-system integration, 3+ formulas, may require new ADR
- **XL** — cross-cutting concern, 5+ dependencies, multiple new ADRs likely
Label clearly: "Rough scope signal: M (producer should verify before sprint planning)"

### Verdict: [APPROVED / NEEDS REVISION / MAJOR REVISION NEEDED]
```

This skill is read-only — no files are written during Phase 4.

---

## Phase 5: Next Steps

`clarify` is for in-skill work only: the optional "revise now" path, and write
approvals for systems-index / review-log. Do not close the skill with a widget.

**If NEEDS REVISION or MAJOR REVISION NEEDED** — optional continuation of this
review (still in-skill):

- `[A] Revise the GDD now — address blocking items together`
- `[B] Leave the GDD as-is for now`

Do not offer "Stop here" or "Accept as-is" as a third menu. If the user wants to
accept advisory-only items, they can say so.

**If user selects [A] — Revise now:**

Work through all blocking items, asking for design decisions only where you cannot
resolve the issue from the GDD and existing docs alone. Group all design-decision
questions into a single multi-tab `clarify` before making any edits — do not
interrupt mid-revision for each blocker individually.

After all revisions are written:

1. Show a summary table (blocker → fix applied).
2. Re-read the patched GDD. For each Phase 4 blocking item, mark **Addressed** or
   **Still present** from the text only. This is edit-verification, not a new
   design verdict. Do not print APPROVED / NEEDS REVISION / MAJOR REVISION NEEDED
   from this check. Do not spawn specialists again in this session.
3. Continue to **Write approvals — GDD patched after Phase 4**. Do not use the
   unpatched closer.

No post-revision `clarify` menu.

**Write approvals — file not patched (Phase 4 score is still live):**

When the Phase 4 verdict is APPROVED, use a single `clarify` with `multiSelect: true` to
batch the two tracking updates:
- Prompt: "Verdict: APPROVED. I can update the tracking records now. Select any you'd like me to complete:"
- Options:
  - `Update systems-index.md status to 'Approved' for [system]`
  - `Append approval entry to design/gdd/reviews/[doc-name]-review-log.md`

If the review-log option is selected, append the same format as below.

When the Phase 4 verdict is NEEDS REVISION or MAJOR REVISION NEEDED and the GDD
was not written after Phase 4, use write-approval `clarify` (not a next-step menu):

- "May I update `design/gdd/systems-index.md` to mark [system] as [In Review / Approved]?"
  - `[A] Yes — update it` / `[B] No — leave it as-is`
- "May I append this review summary to `design/gdd/reviews/[doc-name]-review-log.md`?"
  - `[A] Yes — append to review log` / `[B] No — skip`

If yes, append an entry in this format:
```
## Review — [YYYY-MM-DD] — Verdict: [APPROVED / NEEDS REVISION / MAJOR REVISION NEEDED]
Scope signal: [S/M/L/XL]
Specialists: [list]
Blocking items: [count] | Recommended: [count]
Summary: [2-3 sentence summary of key findings from creative-director verdict]
Prior verdict resolved: [Yes / No / First review]
```

**Write approvals — GDD patched after Phase 4:**

The Phase 4 score is not live status. Do not mark systems-index Approved. Do not
stamp Needs Revision as if the patched file failed.

- systems-index: write-approval to set Status to `In Review` (waiting for re-score)
  only if it is not already `In Review`. Never `Approved`. Never `Needs Revision`
  from the pre-patch score.
- review-log: write-approval to append. If writing, label Phase 4 as a scoring-pass
  on pre-patch text:

```
## Review — [YYYY-MM-DD] — Scoring pass: [NEEDS REVISION / MAJOR REVISION NEEDED] (pre-patch)
Scope signal: [S/M/L/XL]
Specialists: [list]
Blocking items: [count] | Recommended: [count]
Patches applied: [N] blockers
Live verdict: unscored — specialists have not read the patched text
Summary: [2-3 sentence summary of key findings from creative-director verdict]
Prior verdict resolved: [Yes / No / First review]
```

---

**Done** — after writes (or declined writes) complete. Do not call `clarify`.

Print a done line, then follow-ups as a bullet list — only real items, with real names.

Before listing, read:
- `design/gdd/systems-index.md` — other systems still In Review or NEEDS REVISION
- Count `.md` files in `design/gdd/` (excluding game-concept.md, systems-index.md)
- Next system with Status: Not Started in design order

**If the GDD was not written after Phase 4:**

**Done line:** `Design review is done. Verdict: [APPROVED / NEEDS REVISION / MAJOR REVISION NEEDED].`

**If the GDD was patched after Phase 4:**

**Done line:** `Design review is done. Pre-patch score: [NEEDS REVISION / MAJOR REVISION NEEDED]. Patched [N] blockers. Live verdict: unscored.`

Do not put the Phase 4 score in a live `Verdict:` slot after a GDD write.

**Follow-ups** (omit any that do not apply):

- If patched: `Re-score the patched file (specialists have not read it): /design-review <doc-path>`
- `/design-review <other-gdd-path>` — real path, if another GDD is still In Review / NEEDS REVISION
- `/consistency-check` — if ≥1 other GDD exists
- `/review-all-gdds` — if ≥2 GDDs exist
- `/design-system <next-system>` — real name, next in design order

Do not offer "Stop here". Do not say "run /design-review again".
If context is above ~50% after a revision pass, add a plain note (not a menu): a
full re-review runs 5 agents and needs clean context.

## Pitfalls

- **Stale verdict after mutation:** Phase 4 scored the pre-patch text. After
  Revise now, that score is history, not live status. Headline `Live verdict:
  unscored` and point follow-up at re-scoring the patched file.
