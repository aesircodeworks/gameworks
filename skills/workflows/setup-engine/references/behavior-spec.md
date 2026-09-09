> **Upstream:** Derived from Claude Code Game Studios by Donchitos (MIT). https://github.com/Donchitos/Claude-Code-Game-Studios — adapted for Hermes Agent / Aesir Gameworks.

# Skill Test Spec: /setup-engine

**Model tier:** Medium

## Skill Summary

`/setup-engine` pins the game engine and language by writing two **game-workspace**
files: `AGENTS.md` (Technology Stack + Engine Version Reference) and
`docs/technical-preferences.md` (naming, budgets, specialist routing). It never
writes the installed profile template
`skills/studio/gameworks/references/technical-preferences.md`. It never writes
`gameworksreferences/` or any concatenated skill-folder path.

Hermes does not expand `@` imports. The Engine Version Reference in `AGENTS.md`
must be a real paragraph pointing at `docs/engine-reference/<engine>/VERSION.md`,
not an `@` path.

If `docs/technical-preferences.md` is missing, copy the template via
`skill_view('gameworks', file_path='references/technical-preferences.md')` into
the game file, then fill it. If `AGENTS.md` is missing, copy
`skill_view('project-bootstrap', file_path='templates/AGENTS.md')` first, then fill Technology Stack.

An optional engine argument (e.g., `/setup-engine godot`) skips engine selection.
The skill has no director gates. The verdict is COMPLETE when both files are written.

---

## Scoped Authorization Checks

Apply [scoped authorization](../../../studio/gameworks/references/collaborative-design-principle.md) to the write examples below: ask only for missing target/changeset authorization or unresolved decisions, not for permission already supplied. Quoted write questions illustrate the missing-authorization branch, not mandatory wording or per-file prompt counts. An approved batch may cover multiple targets. Section-design approvals and later stage/release gates remain separate; a write request does not satisfy them. Children return missing decisions to the coordinator.

- [ ] With the same case's edits and targets explicitly approved, performs scoped writes and verification without another generic write question; retains required substantive gates.
- [ ] With only review requested, performs read-only discovery; asks before new targets, scope expansion, or unresolved material choices. Skeletons and checkpoints also require approved scope.

## Static Assertions (Structural)

Verified automatically by `/skill-test static` — no fixture needed.

- [ ] Has required frontmatter fields: `name`, `description`, `metadata.hermes`
- [ ] Has ≥2 phase headings
- [ ] Contains verdict keyword: COMPLETE
- [ ] Documents scoped write authorization: asks for missing scope or decisions, not repeated permission for approved edits
- [ ] Has a next-step handoff (e.g., `/brainstorm` or `/studio-start` depending on flow)

---

## Director Gate Checks

None. `/setup-engine` is a technical configuration skill. No director gates apply.

---

## Test Cases

### Case 1: Godot 4 + GDScript — Full engine configuration

**Fixture:**
- `AGENTS.md` Technology Stack still has `[CHOOSE]` placeholders
- `docs/technical-preferences.md` is missing (or contains only placeholders)
- Engine argument provided: `godot`

**Input:** `/setup-engine godot`

**Expected behavior:**
1. Skill skips engine-selection step (argument provided)
2. Skill presents language options for Godot: GDScript or C#
3. User selects GDScript
4. Skill shows proposed `AGENTS.md` Technology Stack (Engine/Language/Build/Asset Pipeline)
   and asks before writing `AGENTS.md`
5. If `docs/technical-preferences.md` is missing, skill copies the profile template
   into that game path, then drafts naming conventions, specialist routing, and
   remaining sections
6. Skill asks before writing `docs/technical-preferences.md`
7. Engine Version Reference in `AGENTS.md` is a real paragraph (no `@` import)
8. Both files are written after approval; verdict is COMPLETE

**Assertions:**
- [ ] `AGENTS.md` Technology Stack Engine/Language are filled (not `[CHOOSE]`)
- [ ] Language field is set to GDScript
- [ ] `AGENTS.md` Engine Version Reference is a real paragraph, not an `@` path
- [ ] Game file `docs/technical-preferences.md` is created or updated (profile template is not mutated; no `gameworksreferences/` path)
- [ ] Naming conventions are GDScript-appropriate (snake_case)
- [ ] Routing table includes `.gd`, `.gdshader`, and `.tscn` entries
- [ ] Specialists are assigned (not placeholders)
- [ ] "May I write" is asked before writing each of `AGENTS.md` and `docs/technical-preferences.md`
- [ ] Verdict is COMPLETE

---

### Case 2: Unity + C# — Unity-specific configuration

**Fixture:**
- `docs/technical-preferences.md` contains only placeholders (or is missing)
- Engine argument provided: `unity`

**Input:** `/setup-engine unity`

**Expected behavior:**
1. Skill sets `AGENTS.md` Technology Stack to Unity + C#
2. Naming conventions in `docs/technical-preferences.md` are C#-appropriate (PascalCase for classes, camelCase for fields)
3. Specialist assignments reference unity-specialist (C# review is covered by primary)
4. Routing table: `.cs` → unity-specialist, `.unity` (scene) → unity-specialist
5. Skill asks before writing `AGENTS.md` and `docs/technical-preferences.md` and writes on approval

**Assertions:**
- [ ] Engine field is set to Unity (not Godot or Unreal)
- [ ] Language field is set to C#
- [ ] Naming conventions reflect C# conventions
- [ ] Routing table includes `.cs` and `.unity` entries
- [ ] Verdict is COMPLETE

---

### Case 3: Unreal + Blueprint — Unreal-specific configuration

**Fixture:**
- `docs/technical-preferences.md` contains only placeholders (or is missing)
- Engine argument provided: `unreal`

**Input:** `/setup-engine unreal`

**Expected behavior:**
1. Skill sets engine to Unreal Engine 5, primary language to Blueprint (Visual Scripting)
2. Specialist assignments reference unreal-specialist, blueprint-specialist
3. Routing table: `.uasset` → blueprint-specialist or unreal-specialist,
   `.umap` → unreal-specialist
4. Performance budgets are pre-set with Unreal defaults (e.g., higher draw call budget)
5. Skill asks "May I write" and writes on approval; verdict is COMPLETE

**Assertions:**
- [ ] Engine field is set to Unreal Engine 5
- [ ] Routing table includes `.uasset` and `.umap` entries
- [ ] Blueprint specialist is assigned
- [ ] Verdict is COMPLETE

---

### Case 4: Engine Already Configured — Offers to reconfigure specific sections

**Fixture:**
- `docs/technical-preferences.md` has engine set to Godot 4 with all fields populated
- `AGENTS.md` Technology Stack is already filled (not `[CHOOSE]`)
- No engine argument provided

**Input:** `/setup-engine`

**Expected behavior:**
1. Skill reads game-workspace `docs/technical-preferences.md` (not the profile template) and detects fully configured engine (Godot 4)
2. Skill reports: "Engine already configured as Godot 4 + GDScript"
3. Skill presents options: reconfigure all, reconfigure specific section only
   (Engine/Language, Naming Conventions, Specialists, Performance Budgets)
4. User selects "Reconfigure Performance Budgets only"
5. Only the performance budget section is updated; all other fields unchanged
6. Skill asks before writing `docs/technical-preferences.md` and writes on approval

**Assertions:**
- [ ] Skill does NOT overwrite all fields when only a section update was requested
- [ ] User is offered section-specific reconfiguration
- [ ] Only the selected section is modified in the written file
- [ ] Verdict is COMPLETE

---

### Case 5: Director Gate Check — No gate; setup-engine is a utility skill

**Fixture:**
- Fresh project with no engine configured

**Input:** `/setup-engine godot`

**Expected behavior:**
1. Skill completes full engine configuration
2. No director agents are spawned at any point
3. No gate IDs appear in output

**Assertions:**
- [ ] No director gate is invoked
- [ ] No gate skip messages appear
- [ ] Verdict is COMPLETE without any gate check

---

## Protocol Compliance

- [ ] Presents draft configuration before asking to write
- [ ] Asks before writing `AGENTS.md` and `docs/technical-preferences.md`
- [ ] Does not write `@` imports into `AGENTS.md`
- [ ] Copies the profile template into `docs/technical-preferences.md` only when that game file is missing
- [ ] Respects engine argument when provided (skips selection step)
- [ ] Detects existing config and offers partial reconfigure
- [ ] Routing table is populated for all key file types for the chosen engine
- [ ] Verdict is COMPLETE after both files are written

---

## Coverage Notes

- Godot 4 + C# (instead of GDScript) follows the same flow as Case 1 with
  different naming conventions and the godot-csharp-specialist assignment.
  This variant is not separately tested.
- The engine-version-specific guidance (e.g., Godot 4.6 knowledge gap warning
  from VERSION.md) is surfaced by the skill but not assertion-tested here.
- Performance budget defaults per engine are noted as engine-specific but
  exact default values are not assertion-tested.
