> **Upstream:** Derived from Claude Code Game Studios by Donchitos (MIT). https://github.com/Donchitos/Claude-Code-Game-Studios — adapted for Hermes Agent / Aesir Gameworks.

# Framework QA

Quality assurance infrastructure for the framework.
Tests the skills and role skills themselves — not any game built with them.

> **This folder is self-contained and optional.**
> Game developers using the framework don't need it. Specs live next to each
> skill; this folder holds the catalog, rubric, templates, and saved results.

---

## What's in here

```
skills/quality/framework-qa/
├── SKILL.md
├── references/
│   ├── README.md              ← you are here
│   ├── authoring-policy.md    ← how to run tests and where files live
│   ├── catalog.yaml           ← master registry: 73 workflow skills + 49 role skills
│   ├── quality-rubric.md      ← category-specific pass/fail metrics for /skill-test category
│   └── results/               ← test run outputs (written by /skill-test spec, gitignored)
└── templates/
    ├── skill-test-spec.md     ← template for skill behavioral specs
    └── agent-test-spec.md     ← template for role-skill behavioral specs
```

Behavior specs are **not** nested here. Each skill keeps its spec at:

`skills/<category>/<name>/references/behavior-spec.md`

Role skills live at `skills/agents/<name>/SKILL.md` with the same spec layout.
Catalog `spec:` fields point at those paths.

---

## How to use it

Run `/skill-test` and `/skill-improve` from the distribution or installed
profile (a root that contains `skills/studio`). They test this skill tree, not
a game workspace. Game workspaces have no `skills/` tree.

### Check structural compliance

```
/skill-test static [skill-name]     # Check one skill (7 checks)
/skill-test static all              # Check the live tree (skills/*/*/SKILL.md)
```

### Run a behavioral spec test

```
/skill-test spec gate-check         # Evaluate a skill against its written spec
/skill-test spec design-review
```

### Check against category rubric

```
/skill-test category gate-check     # Evaluate one skill against its category metrics
/skill-test category all            # Run rubric checks across all categorized skills
```

### See full coverage picture

```
/skill-test audit                   # 73 workflow + 49 role: has-spec, last tested, result
```

### Improve a failing skill

```
/skill-improve gate-check           # Test → diagnose → propose fix → retest loop
```

---

## Skill categories

| Category | Skills | Key metrics |
|----------|--------|-------------|
| `gate` | gate-check | Review mode read, full/lean/solo director panel, no auto-advance |
| `review` | design-review, architecture-review, review-all-gdds | Read-only, 8-section check, correct verdicts |
| `authoring` | design-system, quick-design, art-bible, create-architecture, … | Section-by-section write authorization, skeleton-first |
| `readiness` | story-readiness, story-done | Blockers surfaced, director gate in full mode |
| `pipeline` | create-epics, create-stories, dev-story, map-systems, … | Upstream dependency check, handoff path clear |
| `analysis` | consistency-check, balance-check, code-review, tech-debt, … | Read-only report (`read_file`/`search_files`), verdict keyword, no writes |
| `team` | team-combat, team-narrative, team-audio, … | All required agents spawned via parallel `delegate_task`, blocked surfaced |
| `sprint` | sprint-plan, sprint-status, milestone-review, … | Reads sprint data, status keywords present |
| `utility` | studio-start, adopt, hotfix, localize, setup-engine, … | Passes static checks |

---

## Agent tiers

| Tier | Agents |
|------|--------|
| `directors` | creative-director, technical-director, producer, art-director |
| `leads` | lead-programmer, narrative-director, audio-director, ux-designer, qa-lead, release-manager, localization-lead |
| `specialists` | gameplay-programmer, engine-programmer, ui-programmer, tools-programmer, network-programmer, ai-programmer, level-designer, sound-designer, technical-artist |
| `godot` | godot-specialist, godot-gdscript-specialist, godot-csharp-specialist, godot-shader-specialist, godot-gdextension-specialist |
| `unity` | unity-specialist, unity-ui-specialist, unity-shader-specialist, unity-dots-specialist, unity-addressables-specialist |
| `unreal` | unreal-specialist, ue-gas-specialist, ue-replication-specialist, ue-umg-specialist, ue-blueprint-specialist |
| `operations` | devops-engineer, security-engineer, performance-analyst, analytics-engineer, community-manager |
| `creative` | writer, world-builder, game-designer, economy-designer, systems-designer, prototyper |

---

## Updating the catalog

`catalog.yaml` tracks test coverage for every workflow skill and role skill. After running a test:

- `/skill-test spec [name]` will offer to update `last_spec` and `last_spec_result`
- `/skill-test category [name]` will offer to update `last_category` and `last_category_result`
- `last_static` and `last_static_result` are updated manually or via `/skill-improve`

Results are written to `skill_view('framework-qa', file_path='references/results/')` (skill_view path).

---

## Writing a new spec

1. Find the spec template at `templates/skill-test-spec.md` (or `templates/agent-test-spec.md` for a role)
2. Copy it to `skills/<category>/<name>/references/behavior-spec.md`
3. Update the `spec:` field in `catalog.yaml` to point to the new file
4. Run `/skill-test spec [skill-name]` to validate it

---

## Removing this QA layer

This folder has no hooks into a game workspace. To remove:

```bash
rm -rf skills/quality/framework-qa
```

The skills `/skill-test` and `/skill-improve` will still function — they'll
report that `catalog.yaml` is missing and suggest running `/skill-test audit` to
initialize it.
