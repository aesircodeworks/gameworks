---
name: design-system
description: Author a GDD for one game system.
version: 1.1.0
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

# Design System

**Model tier:** Medium

Authors one system GDD section by section: gather context, create the file
skeleton, walk the 8 required sections through
Question → Options → Decision → Draft → Approval → Write, then validate and
update tracking. The GDD is complete only when every unresolved design
decision has been put to the user — nothing is parked silently.

## 1. Parse Arguments & Validate

Resolve the review mode (once, store for all gate spawns this run):
1. `--review [full|lean|solo]` if passed
2. else `production/review-mode.txt`
3. else `lean`

See `skill_view('gameworks', file_path='references/director-gates.md')` for
the gate check pattern.

A system name or retrofit path is **required**. If missing: check
`design/gdd/systems-index.md` — if present, offer the highest-priority
Not Started system via `clarify` ("Start designing [system]? / Pick another /
Stop here"); if absent, fail with the `/map-systems` pointer.

**Retrofit mode** (argument starts with `retrofit` or is a path to an existing
GDD): read the file, identify present vs. missing/placeholder sections of the
8-section standard, show the split (✓ kept untouched / ✗ will be authored),
and ask before writing anything. Never overwrite existing section content —
`patch` only `[To be designed]` placeholders or empty bodies.

Otherwise normalize the system name to kebab-case for the filename.

## 2. Gather Context

Read everything relevant **before** asking the user anything.

**Required:** `design/gdd/game-concept.md` (fail: "Run `/brainstorm` first"),
`design/gdd/systems-index.md` (fail: "Run `/map-systems` first"), the system's
index row (warn if unlisted), and `design/registry/entities.yaml` if present —
hold entries referenced by this system as **known facts** this GDD must not
contradict. Read `docs/consistency-failures.md` if present and surface
matching domain entries as "Past failure patterns".

**Dependencies:** from the index, read upstream dependency GDDs (decisions to
respect) and downstream dependent GDDs (expectations to satisfy). Extract
interfaces, formulas referencing this system, and constraining edge cases.

**Optional:** `design/gdd/game-pillars.md`, an existing GDD (resume, don't
restart), thematically related GDDs.

**Present the context summary:** system, priority/layer, dependencies (with
GDD-yes/no), pillar alignment, and the locked registry facts. Warn about
undesigned upstream dependencies and offer to design them first or mark the
contract provisional.

**Technical feasibility pre-check:** map the system category to an engine
domain (physics/rendering/UI/audio/navigation/animation/networking/input/
core/scripting). If `docs/technical-preferences.md` configures an engine, read
`docs/engine-reference/[engine]/` (VERSION, domain module, breaking changes)
and matching ADRs, then present the Feasibility Brief: known capabilities,
constraints shaping the design, knowledge gaps with risk, constraining ADRs.
If no engine is configured, note it and move on.

Use one `clarify`: "Any constraints to add before we begin?" (Proceed / Add a
constraint / Pause to check engine docs).

## 3. Create File Skeleton

Use the structure from
`skill_view('project-templates', file_path='templates/game-design-document.md')`:
Status/Author/Last Updated/Implements Pillar header, then the 8 required
sections (Overview, Player Fantasy, Detailed Design, Formulas, Edge Cases,
Dependencies, Tuning Knobs, Acceptance Criteria) plus Visual/Audio
Requirements, UI Requirements, and Open Questions — each `[To be designed]`.

In one `clarify` call, request the skeleton write at
`design/gdd/[system-name].md` and offer an independent optional completion
update: link the GDD, set the index row to `Designed`, and recalculate
progress counts in `design/gdd/systems-index.md` once the GDD is complete.
Show the exact row and path first. Skip missing/no-op rows; if declined, do
not re-offer in Phase 5. This does not approve section designs or bypass
CD-GDD-ALIGN. If the skeleton itself is declined, stop:
> "Verdict: **BLOCKED** — skeleton declined. Re-run `/design-system [system]`
> when ready to create the file."

## 4. Section-by-Section Design

For **each section**, run the cycle:

```
Context → Questions → Options → Decision → Draft → Approval → Write
```

1. **Context**: what the section must contain; constraining decisions from
   dependency GDDs.
2. **Questions**: section-specific; `clarify` for constrained questions,
   conversation for open exploration.
3. **Options**: 2–4 approaches with pros/cons for genuine design choices.
4. **Decision**: user picks or redirects.
5. **Draft**: in conversation, flagging provisional assumptions about
   undesigned dependencies.
6. **Approval**: in the SAME response, `clarify`: "Approve the [Section]
   section?" (`Approve — write` / `Make changes` / `Start over`). A draft
   without its approval widget is a protocol violation.
7. **Write**: `patch` with the heading in `old_string` (`"## [Section]\n\n[To
   be designed]"`) — never match the bare placeholder. Confirm the write.
8. **Registry conflict check** (Detailed Design and Formulas): compare newly
   written entity/item/formula/constant values against the registry. Any
   mismatch stops the session until resolved; new names are registration
   candidates for Phase 5.

**Delegation and review mode (applies to every section — read once):**

- `solo` → no agent spawns anywhere. Note: "Specialists not consulted — Solo
  mode. Review manually before production."
- `lean` (default) → spawn only for **high implementation-risk sections**:
  Formulas (D) and Acceptance Criteria (H), plus the CD-GDD-ALIGN gate skip
  rule in 5a-bis. Other sections draft without agents.
- `full` → spawn as described per section below.
- Agents return analysis to the main session; the user decides via `clarify`;
  the main session owns all file writes. Never draft a delegated section
  before the agent responds, and never invent formula/balance values without
  specialist input.

### Section A: Overview

One paragraph a stranger could understand. Derive recommended options from
layer/category (Foundation → technical framing `[A]`; player-facing → `[C]
Both`), from ADR search results (cite an ADR only if one exists), and layer
(player-facing → state a Player Fantasy). Ask the three framing tabs via one
multi-tab `clarify` (Framing / ADR ref / Fantasy), then draft. Keep questions
at behavior level — implementation questions become "→ ADR" notes, not GDD
content. Cross-check against the systems index description.

### Section B: Player Fantasy

The emotional target. Ask direct/indirect/both (recommend from category), then
in `full` mode spawn `creative-director` for 2–3 candidate framings (anchor to
the stated pillars and any reference games). Must quote the pillar it serves.

### Section C: Detailed Design

Unambiguous specification a programmer could implement without questions:
numbered Core Rules, a States-and-Transitions table, and per-dependency
interface specs (data in, data out, owner). Ask for a typical use walkthrough,
player decision points, and what the player **cannot** do. In `full` mode
spawn the category's Primary + Supporting agents (routing table below) in
parallel; surface disagreements to the user. Cross-check every interaction
against dependency GDDs.

### Section D: Formulas

Every formula in this exact structure:

```
`[formula_name] = [expression]`
**Variables:** | Variable | Symbol | Type | Range | Description |
**Output Range:** [min] to [max]; [behavior at extremes]
**Example:** [worked example with real numbers]
```

No prose-only formulas, no `[TBD]`. In `lean` and `full`, spawn
`systems-designer` (propose formulas with variable tables from Core Rules and
tuning goals); for economy/cost systems also `economy-designer` (cost curves,
ratios). Present proposals for the user's decision. Connect to dependency
formulas — don't reinvent.

### Section E: Edge Cases

Each edge case as `**If [condition]**: [exact outcome]`. No "handle
appropriately" — an edge case without a resolution is an unresolved design
decision, not a specification. Cover zero, maximum, out-of-range, simultaneous
triggers, and known degenerate strategies. In `full` mode spawn
`systems-designer` to sweep the formula/rule space for missed cases (plus
`narrative-director` for narrative systems); the user picks which to include.

### Section F: Dependencies

Pre-fill from context; ask what's missing, the specific data interface per
dependency, and hard vs. soft. Must be bidirectionally consistent with other
GDDs — flag one-directional edges.

### Section G: Tuning Knobs

Every designer-adjustable value with safe ranges and too-high/too-low
behavior. Note knob interactions. Delegate derivation to `systems-designer`
when formulas are complex. Reference dependency GDD knobs — no duplicates.

### Section H: Acceptance Criteria

Each criterion as GIVEN/WHEN/THEN, independently verifiable by a QA tester
without reading the GDD. Minimum coverage: one per Core Rule, one per formula,
plus cross-system interactions. In `lean` and `full`, spawn `qa-lead` to
validate testability and coverage; surface gaps to the user.

### Optional Sections: Visual/Audio, UI Requirements, Open Questions

Visual/Audio is **required (do not offer to skip)** for combat, UI,
animation/movement, VFX, character, dialogue/quest, and level/world systems —
in `full` mode spawn `art-director` for VFX/animation/style requirements
first. For other categories, offer all three optional sections in one
`clarify`.

After Visual/Audio gets real content, print the Asset Spec flag (run
`/asset-spec system:[name]` after the art bible is approved). After UI
Requirements gets real content, print the UX flag (run `/ux-design` before
epics; stories cite `design/ux/[screen].md`, not the GDD).

**Open Questions — consent rule:** every entry must have been put to the user
before the GDD is declared complete: present it in a `clarify` with a proposed
default (decide now with the default / decide differently / park as an Open
Question with owner and target). A question the user parked is recorded with
its owner; a question the user never saw is a violation — do not write it into
the GDD silently.

## 5. Post-Design Validation

### 5a: Self-Check

Read the GDD back **from file**. Verify: all 8 required sections have real
content, formulas reference defined variables, edge cases have resolutions,
dependencies list interfaces, acceptance criteria are testable.

### 5a-bis: Creative Director Pillar Review

- `solo` → skip: "CD-GDD-ALIGN skipped — Solo mode."
- `lean` → skip: "CD-GDD-ALIGN skipped — Lean mode."
- `full` → spawn `creative-director` with gate **CD-GDD-ALIGN**
  (`skill_view('gameworks', file_path='references/director-gates.md')`),
  passing the GDD path, pillars, and MDA target. Handle the verdict per the
  standard gate rules, then record in the GDD header:
  `> **Creative Director Review (CD-GDD-ALIGN)**: APPROVED [date] / CONCERNS (accepted) [date] / REVISED [date]`

### 5b: Registry and Index

Scan the GDD for cross-system facts (named entities with stats, items with
values, formulas with variables and ranges, shared constants). Show the
registry candidates (NEW vs. already registered) and the systems-index row
changes together, then one `clarify` with independent choices for
`design/registry/entities.yaml` and `design/gdd/systems-index.md` — only
writes not already authorized; omit no-ops; honor declines without
re-offering. Value conflicts with existing entries need a separate design
decision, not routine bookkeeping.

### 5c: Completion Summary and Independent Review

Present: sections written, provisional assumptions, cross-system conflicts
found or "none". Direct the user to run
`/design-review design/gdd/[system-name].md` in a **fresh session** — never
inline; the reviewing context must be independent of the authoring history.

### 5d: Apply Authorized Tracking Writes

Apply and verify the registry/index writes authorized in Phase 3 or 5b. If
neither approval included them, leave them unchanged and say so. Report GDD,
registry, and index individually as written, skipped, or failed; never claim
synchronization from a partial state or undo the completed GDD.

### 5f: Done

`/design-system` is finished. Do not call `clarify`.

**Done line:** `GDD is written: design/gdd/[system-name].md. /design-system is done.`

**Follow-ups** (omit any that do not apply):
- `/consistency-check` — verify this GDD's values against existing GDDs
- `/design-review design/gdd/[system-name].md` — in a fresh session
- Next undesigned system — `/design-system <real name>`
- `/gate-check systems-design` — only if enough MVP systems are designed

## 6. Specialist Agent Routing

| System Category | Primary Agent | Supporting Agent(s) |
|----------------|---------------|---------------------|
| **Foundation/Infrastructure** (event bus, save/load, scene mgmt) | `systems-designer` | `gameplay-programmer`, `engine-programmer` |
| Combat, damage, health | `game-designer` | `systems-designer`, `ai-programmer`, `art-director` (hit feedback, VFX intent) |
| Economy, loot, crafting | `economy-designer` | `systems-designer`, `game-designer` |
| Progression, XP, skills | `game-designer` | `systems-designer`, `economy-designer` (sinks) |
| Dialogue, quests, lore | `game-designer` | `narrative-director`, `writer`, `art-director` |
| UI systems (HUD, menus) | `game-designer` | `ux-designer`, `ui-programmer`, `art-director`, `technical-artist` |
| Audio systems | `game-designer` | `audio-director`, `sound-designer` |
| AI, pathfinding, behavior | `game-designer` | `ai-programmer`, `systems-designer` |
| Level/world systems | `game-designer` | `level-designer`, `world-builder` |
| Camera, input, controls | `game-designer` | `ux-designer`, `gameplay-programmer` |
| Animation, character movement | `game-designer` | `art-director`, `technical-artist`, `gameplay-programmer` |
| Visual effects, particles, shaders | `game-designer` | `art-director`, `technical-artist`, `systems-designer` |
| Character systems (stats, archetypes) | `game-designer` | `art-director`, `narrative-director`, `systems-designer` |

## 7. Recovery & Resume

If interrupted: read `production/session-state/active.md` (if an authorized
checkpoint exists) and the GDD file — sections with real content are done.
Resume from the next `[To be designed]` section without re-discussing
completed ones. Session checkpoints are a separate target: skeleton, section,
registry, and index approvals never authorize
`production/session-state/active.md`; record progress there only if that
target was explicitly authorized, otherwise report progress in the response.

## Never

- Auto-generate the full GDD as a fait accompli.
- Write a section without its approval widget.
- Contradict an approved GDD or registry fact without flagging the conflict.
- Park an unresolved design decision in Open Questions without the user's
  explicit decision to park it.
- Run `/design-review` inline in the authoring session.

## Context Window Awareness

After each section, if context is at or above 70%, append: progress is saved
in the GDD file; continue in a fresh session with
`/design-system [system-name]` — it resumes from the next incomplete section.
