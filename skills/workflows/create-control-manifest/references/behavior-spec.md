> **Upstream:** Derived from Claude Code Game Studios by Donchitos (MIT). https://github.com/Donchitos/Claude-Code-Game-Studios — adapted for Hermes Agent / Aesir Gameworks.

# Skill Test Spec: /create-control-manifest

**Model tier:** Medium

## Skill Summary

`/create-control-manifest` reads all Accepted ADRs from `docs/architecture/` and
generates a control manifest — a summary document that captures all architectural
constraints, required patterns, and forbidden patterns in one place. The manifest
is the reference document that story authors use when writing story files, ensuring
stories inherit the correct architectural rules without having to read all ADRs
individually.

The skill only includes Accepted ADRs; Proposed ADRs are excluded and noted.
In `full` review mode, **TD-MANIFEST** (`technical-director`) runs after the
rules summary and before writing `docs/architecture/control-manifest.md`. Parse
the first line for `[TD-MANIFEST]: TOKEN`. Lean and solo skip the gate. The skill
asks "May I write" before writing the manifest.

---

## Scoped Authorization Checks

Apply [scoped authorization](../../../studio/gameworks/references/collaborative-design-principle.md) to the write examples below: ask only for missing target/changeset authorization or unresolved decisions, not for permission already supplied. Quoted write questions illustrate the missing-authorization branch, not mandatory wording or per-file prompt counts. An approved batch may cover multiple targets. Section-design approvals and later stage/release gates remain separate; a write request does not satisfy them. Children return missing decisions to the coordinator.

- [ ] With the same case's edits and targets explicitly approved, performs scoped writes and verification without another generic write question; retains required substantive gates.
- [ ] With only review requested, performs read-only discovery; asks before new targets, scope expansion, or unresolved material choices. Skeletons and checkpoints also require approved scope.

## Static Assertions (Structural)

Verified automatically by `/skill-test static` — no fixture needed.

- [ ] Has required frontmatter fields: `name`, `description`, `metadata.hermes`
- [ ] Has ≥2 phase headings
- [ ] Contains verdict keywords: CREATED, BLOCKED
- [ ] Documents scoped write authorization: asks for missing scope or decisions, not repeated permission for approved edits
- [ ] Has a next-step handoff at the end (`/create-epics` or `/create-stories`)
- [ ] Documents that only Accepted ADRs are included (not Proposed)
- [ ] Documents gate behavior: TD-MANIFEST in full mode; skipped in lean/solo

---

## Director Gate Checks

In `full` mode: spawn `technical-director` with `delegate_task` using gate
**TD-MANIFEST** after the Control Manifest Preview and before writing the file.
Parse the first line for `[TD-MANIFEST]: TOKEN`. APPROVE proceeds to write;
CONCERNS surfaces via `clarify`; REJECT does not write the manifest.

In `lean` mode: skip. Note: "TD-MANIFEST skipped — Lean mode."

In `solo` mode: skip. Note: "TD-MANIFEST skipped — Solo mode."

---

## Test Cases

### Case 1: Happy Path — 4 Accepted ADRs create a correct manifest

**Fixture:**
- `docs/architecture/` contains 4 ADR files, all with `Status: Accepted`
- Each ADR has a "Required Patterns" and/or "Forbidden Patterns" section
- No existing `docs/architecture/control-manifest.md`

**Input:** `/create-control-manifest`

**Expected behavior:**
1. Skill reads all ADR files in `docs/architecture/`
2. Extracts Required Patterns, Forbidden Patterns, and key constraints from each
3. Drafts the manifest with correct section structure
4. Shows the draft manifest to the user
5. Asks "May I write `docs/architecture/control-manifest.md`?"
6. Writes the manifest after approval

**Assertions:**
- [ ] All 4 Accepted ADRs are represented in the manifest
- [ ] Manifest includes distinct sections for Required Patterns and Forbidden Patterns
- [ ] Manifest includes the source ADR number for each constraint
- [ ] "May I write" is asked before writing
- [ ] Skill does NOT write without approval
- [ ] Verdict is CREATED after writing

---

### Case 2: Failure Path — No ADRs found

**Fixture:**
- `docs/architecture/` directory exists but contains no ADR files

**Input:** `/create-control-manifest`

**Expected behavior:**
1. Skill reads `docs/architecture/` and finds no ADR files
2. Skill outputs: "No ADRs found. Run `/architecture-decision` to create ADRs before generating the control manifest."
3. Skill exits without creating any file
4. Verdict is BLOCKED

**Assertions:**
- [ ] Skill outputs a clear error when no ADRs are found
- [ ] No control manifest file is written
- [ ] Skill recommends `/architecture-decision` as the next action
- [ ] Verdict is BLOCKED (not an error crash)

---

### Case 3: Mixed ADR Statuses — Only Accepted ADRs included

**Fixture:**
- `docs/architecture/` contains 3 Accepted ADRs and 2 Proposed ADRs

**Input:** `/create-control-manifest`

**Expected behavior:**
1. Skill reads all ADR files and filters by Status: Accepted
2. Manifest is drafted from the 3 Accepted ADRs only
3. Output notes: "2 Proposed ADRs were excluded: [adr-NNN-name, adr-NNN-name]"
4. User sees which ADRs were excluded before approving the write
5. Asks "May I write `docs/architecture/control-manifest.md`?"

**Assertions:**
- [ ] Only the 3 Accepted ADRs appear in the manifest content
- [ ] Excluded Proposed ADRs are listed by name in the output
- [ ] User sees the exclusion list before approving the write
- [ ] Skill does NOT silently omit Proposed ADRs without noting them

---

### Case 4: Edge Case — Manifest already exists

**Fixture:**
- `docs/architecture/control-manifest.md` already exists (version 1, dated last week)
- `docs/architecture/` contains Accepted ADRs (some new since last manifest)

**Input:** `/create-control-manifest`

**Expected behavior:**
1. Skill detects existing manifest and reads its version number / date
2. Skill offers to regenerate: "control-manifest.md already exists (v1, [date]). Regenerate with current ADRs?"
3. If user confirms: skill drafts updated manifest, increments version number
4. Asks "May I write `docs/architecture/control-manifest.md`?" (overwrite)
5. Writes updated manifest after approval

**Assertions:**
- [ ] Skill reads and reports the existing manifest version before offering to regenerate
- [ ] User is offered a regenerate/skip choice — not auto-overwritten
- [ ] Updated manifest has an incremented version number
- [ ] "May I write" is asked before overwriting the existing file

---

### Case 5: Director Gate — TD-MANIFEST in full mode; skipped in lean/solo

**Fixture:**
- 4 Accepted ADRs exist
- `production/review-mode.txt` exists with `full`

**Input:** `/create-control-manifest`

**Expected behavior:**
1. Skill reads ADRs and presents the Control Manifest Preview
2. Skill reads `production/review-mode.txt` — determines `full`
3. Skill spawns `technical-director` with `delegate_task` using gate **TD-MANIFEST**
4. Skill parses the first line for `[TD-MANIFEST]: TOKEN`
5. APPROVE → write the manifest; CONCERNS → `clarify`; REJECT → do not write
6. In lean/solo: skip with "TD-MANIFEST skipped — Lean/Solo mode" and proceed to write approval

**Assertions:**
- [ ] TD-MANIFEST is spawned in full mode after the preview, before the write
- [ ] First-line gate token `[TD-MANIFEST]: TOKEN` is parsed
- [ ] Manifest is not written on REJECT
- [ ] Lean and solo skip the gate with an explicit skip note

---

## Protocol Compliance

- [ ] Reads all ADR files before drafting manifest
- [ ] Only Accepted ADRs included — Proposed ones noted as excluded
- [ ] Manifest draft shown to user before "May I write" ask
- [ ] "May I write `docs/architecture/control-manifest.md`?" asked before writing
- [ ] TD-MANIFEST runs in full mode; skipped and noted in lean/solo
- [ ] Ends with next-step handoff: `/create-epics` or `/create-stories`

---

## Coverage Notes

- The exact section structure of the generated manifest (constraint tables, pattern
  lists) is defined by the skill body and not re-enumerated in test assertions.
- The `version` field incrementing logic (v1 → v2) is tested via Case 4 but exact
  version numbering format is not fixture-locked.
- ADR parsing (extracting Required/Forbidden Patterns) depends on consistent ADR
  structure — tested implicitly via Case 1's fixture.
