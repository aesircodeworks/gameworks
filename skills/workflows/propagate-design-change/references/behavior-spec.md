> **Upstream:** Derived from Claude Code Game Studios by Donchitos (MIT). https://github.com/Donchitos/Claude-Code-Game-Studios — adapted for Hermes Agent / Aesir Gameworks.

# Skill Test Spec: /propagate-design-change

**Model tier:** Medium

## Skill Summary

`/propagate-design-change` handles GDD revision cascades. When a GDD is updated,
the skill traces all downstream artifacts that reference it: ADRs, TR-registry
entries, stories, and epics. It produces a structured impact report showing what
needs to change and why. The skill does NOT automatically apply changes — it
proposes edits for each affected artifact and asks "May I write" per artifact
before making any modification.

The skill is read-only during analysis and write-gated per artifact during the
update phase. In `full` review mode, **TD-CHANGE-IMPACT** (`technical-director`)
runs after the impact report and before ADR dispositions. Parse the first line
for `[TD-CHANGE-IMPACT]: TOKEN`. Lean and solo skip the gate.

---

## Scoped Authorization Checks

Apply [scoped authorization](../../../studio/gameworks/references/collaborative-design-principle.md) to the write examples below: ask only for missing target/changeset authorization or unresolved decisions, not for permission already supplied. Quoted write questions illustrate the missing-authorization branch, not mandatory wording or per-file prompt counts. An approved batch may cover multiple targets. Section-design approvals and later stage/release gates remain separate; a write request does not satisfy them. Children return missing decisions to the coordinator.

- [ ] With the same case's edits and targets explicitly approved, performs scoped writes and verification without another generic write question; retains required substantive gates.
- [ ] With only review requested, performs read-only discovery; asks before new targets, scope expansion, or unresolved material choices. Skeletons and checkpoints also require approved scope.

## Static Assertions (Structural)

Verified automatically by `/skill-test static` — no fixture needed.

- [ ] Has required frontmatter fields: `name`, `description`, `metadata.hermes`
- [ ] Has ≥2 phase headings
- [ ] Contains verdict keywords: COMPLETE, BLOCKED, NO IMPACT
- [ ] Documents scoped write authorization: asks for missing scope or decisions, not repeated permission for approved edits
- [ ] Has a next-step handoff at the end
- [ ] Documents that changes are proposed, not applied automatically
- [ ] Documents gate behavior: TD-CHANGE-IMPACT in full mode; skipped in lean/solo

---

## Director Gate Checks

In `full` mode: spawn `technical-director` with `delegate_task` using gate
**TD-CHANGE-IMPACT** after the Design Change Impact Report and before Phase 7
resolution. Parse the first line for `[TD-CHANGE-IMPACT]: TOKEN`. APPROVE proceeds;
CONCERNS surfaces via `clarify`; REJECT re-analyzes before ADR dispositions.

In `lean` mode: skip. Note: "TD-CHANGE-IMPACT skipped — Lean mode."

In `solo` mode: skip. Note: "TD-CHANGE-IMPACT skipped — Solo mode."

---

## Test Cases

### Case 1: Happy Path — GDD revision affects 2 stories and 1 epic

**Fixture:**
- `design/gdd/[system].md` exists and has been recently revised (git diff shows changes)
- `production/epics/[layer]/EPIC-[system].md` references this GDD
- 2 story files reference TR-IDs from this GDD
- The changed GDD section affects the acceptance criteria of both stories

**Input:** `/propagate-design-change design/gdd/[system].md`

**Expected behavior:**
1. Skill reads the revised GDD and identifies what changed (git diff or content comparison)
2. Skill scans ADRs, TR-registry, epics, and stories for references to this GDD
3. Skill produces an impact report: 1 epic affected, 2 stories affected
4. Skill shows the proposed change for each artifact
5. If the listed downstream edits are not authorized, asks for that changeset; accepts batch approval or individual selections
6. Applies only the individually or batch-approved changes

**Assertions:**
- [ ] Impact report identifies all 3 affected artifacts (1 epic + 2 stories)
- [ ] Each affected artifact's proposed change is shown before asking to write
- [ ] Authorization covers every selected artifact; an approved batch needs no per-artifact reapproval
- [ ] Skill does NOT apply changes outside the individually or batch-approved scope
- [ ] Verdict is COMPLETE after all approved changes are applied

---

### Case 2: No Impact — Changed GDD has no downstream references

**Fixture:**
- `design/gdd/[system].md` exists and has been revised
- No ADRs, stories, or epics reference this GDD's TR-IDs or GDD path

**Input:** `/propagate-design-change design/gdd/[system].md`

**Expected behavior:**
1. Skill reads the revised GDD
2. Skill scans all ADRs, stories, and epics for references
3. No references found
4. Skill outputs: "No downstream impact found for [system].md — no artifacts reference this GDD."
5. No write operations are performed

**Assertions:**
- [ ] Skill outputs the "No downstream impact found" message
- [ ] Verdict is NO IMPACT
- [ ] No "May I write" asks are issued (nothing to update)
- [ ] Skill does NOT error or crash when no references are found

---

### Case 3: In-Progress Story Warning — Referenced story is currently being developed

**Fixture:**
- A story referencing this GDD has `Status: In Progress`
- The developer has already started implementing this story

**Input:** `/propagate-design-change design/gdd/[system].md`

**Expected behavior:**
1. Skill identifies the In Progress story as an affected artifact
2. Skill outputs an elevated warning: "CAUTION: [story-file] is currently In Progress — a developer may be working on this. Coordinate before updating."
3. The warning appears in the impact report before the "May I write" ask for that story
4. User can still approve or skip the update for that story

**Assertions:**
- [ ] In Progress story is flagged with an elevated warning (distinct from regular affected-artifact entries)
- [ ] Warning appears before the "May I write" ask for that story
- [ ] Skill still offers to update the story — the warning does not block the option
- [ ] Other (non-In-Progress) artifacts are not affected by this warning

---

### Case 4: Edge Case — No argument provided

**Fixture:**
- Multiple GDDs exist in `design/gdd/`

**Input:** `/propagate-design-change` (no argument)

**Expected behavior:**
1. Skill detects no argument is provided
2. Skill outputs a usage error: "No GDD specified. Usage: /propagate-design-change design/gdd/[system].md"
3. Skill lists recently modified GDDs as suggestions (git log)
4. No analysis is performed

**Assertions:**
- [ ] Skill outputs a usage error when no argument is given
- [ ] Usage example is shown with the correct path format
- [ ] No impact analysis is performed without a target GDD
- [ ] Skill does NOT silently pick a GDD without user input

---

### Case 5: Director Gate — TD-CHANGE-IMPACT in full mode; skipped in lean/solo

**Fixture:**
- A GDD has been revised with downstream ADR references
- `production/review-mode.txt` exists with `full`

**Input:** `/propagate-design-change design/gdd/[system].md`

**Expected behavior:**
1. Skill reads the GDD, traces affected ADRs, and presents the impact report
2. Skill reads `production/review-mode.txt` — determines `full`
3. Skill spawns `technical-director` with `delegate_task` using gate **TD-CHANGE-IMPACT**
4. Skill parses the first line for `[TD-CHANGE-IMPACT]: TOKEN`
5. APPROVE → Phase 7 resolution; CONCERNS → `clarify`; REJECT → re-analyze, no ADR dispositions
6. In lean/solo: skip with "TD-CHANGE-IMPACT skipped — Lean/Solo mode" and proceed to Phase 7

**Assertions:**
- [ ] TD-CHANGE-IMPACT is spawned in full mode (not during analysis, after the impact report)
- [ ] First-line gate token `[TD-CHANGE-IMPACT]: TOKEN` is parsed
- [ ] REJECT blocks ADR disposition until re-analysis
- [ ] Lean and solo skip the gate with an explicit skip note

---

## Protocol Compliance

- [ ] Reads revised GDD and all potentially affected artifacts before producing impact report
- [ ] Impact report shown in full before any "May I write" ask
- [ ] Accepts authorization for the stated downstream changeset without repeated per-artifact questions
- [ ] In Progress stories flagged with elevated warning before their approval ask
- [ ] TD-CHANGE-IMPACT runs in full mode; skipped and noted in lean/solo
- [ ] Ends with next-step handoff appropriate to verdict (COMPLETE or NO IMPACT)

---

## Coverage Notes

- ADR impact (when a GDD change requires an ADR update or new ADR) follows the
  same per-artifact approval pattern as story/epic updates — not independently
  fixture-tested.
- TR-registry impact (when changed GDD requires new or updated TR-IDs) is part
  of the analysis phase but not independently fixture-tested.
- The git diff comparison method (detecting what changed in the GDD) is a runtime
  concern — fixtures use pre-arranged content differences.
