> **Upstream:** Derived from Claude Code Game Studios by Donchitos (MIT). https://github.com/Donchitos/Claude-Code-Game-Studios — adapted for Hermes Agent / Aesir Gameworks.

# Game Studio Agent Architecture -- Quick Start Guide

## What Is This?

This is a complete Hermes Agent agent architecture for game development. It
organizes 50 specialized AI agents into a studio hierarchy that mirrors
real game development teams, with defined responsibilities, delegation
rules, and coordination protocols. It includes engine-specialist agents
for Godot, Unity, Unreal, and Three.js. Godot, Unity, and Unreal have
dedicated sub-specialists; Three.js uses a single lead. All design agents and templates are grounded in
established game design theory (MDA Framework, Self-Determination Theory,
Flow State, Bartle Player Types). Use whichever engine set matches your project.

## How to Use

### 1. Understand the Hierarchy

There are three tiers of agents (roster labels, not runtime model wiring):

- **Tier 1 (Heavy)**: Directors who make high-level decisions
  - `creative-director` -- vision and creative conflict resolution
  - `technical-director` -- architecture and technology decisions
  - `producer` -- scheduling, coordination, and risk management

- **Tier 2 (Medium)**: Department leads who own their domain
  - `game-designer`, `lead-programmer`, `art-director`, `audio-director`,
    `narrative-director`, `qa-lead`, `release-manager`, `localization-lead`

- **Tier 3 (Medium/Light)**: Specialists who execute within their domain
  - Designers, programmers, artists, writers, testers, engineers

### 2. Pick the Right Agent for the Job

Ask yourself: "What department would handle this in a real studio?"

| I need to... | Use this agent | Model |
| ------------- | --------------- | ------- |
| Design a new mechanic | `game-designer` | Medium |
| Write combat code | `gameplay-programmer` | Medium |
| Create a shader | `technical-artist` | Medium |
| Write dialogue | `writer` | Medium |
| Plan the next sprint | `producer` | Heavy |
| Review code quality | `lead-programmer` | Medium |
| Write test cases | `qa-tester` | Light |
| Design a level | `level-designer` | Medium |
| Fix a performance problem | `performance-analyst` | Medium |
| Set up CI/CD | `devops-engineer` | Light |
| Design a loot table | `economy-designer` | Medium |
| Resolve a creative conflict | `creative-director` | Heavy |
| Make an architecture decision | `technical-director` | Heavy |
| Manage a release | `release-manager` | Medium |
| Prepare strings for translation | `localization-lead` | Medium |
| Test a mechanic idea quickly | `prototyper` | Medium |
| Review code for security issues | `security-engineer` | Medium |
| Check accessibility compliance | `accessibility-specialist` | Light |
| Get Unreal Engine advice | `unreal-specialist` | Medium |
| Get Unity advice | `unity-specialist` | Medium |
| Get Godot advice | `godot-specialist` | Medium |
| Get Three.js advice | `threejs-specialist` | Medium |
| Design GAS abilities/effects | `ue-gas-specialist` | Medium |
| Define BP/C++ boundaries | `ue-blueprint-specialist` | Medium |
| Implement UE replication | `ue-replication-specialist` | Medium |
| Build UMG/CommonUI widgets | `ue-umg-specialist` | Medium |
| Design DOTS/ECS architecture | `unity-dots-specialist` | Medium |
| Write Unity shaders/VFX | `unity-shader-specialist` | Medium |
| Manage Addressable assets | `unity-addressables-specialist` | Medium |
| Build UI Toolkit/UGUI screens | `unity-ui-specialist` | Medium |
| Write idiomatic GDScript | `godot-gdscript-specialist` | Medium |
| Write Godot C# code | `godot-csharp-specialist` | Medium |
| Create Godot shaders | `godot-shader-specialist` | Medium |
| Build GDExtension modules | `godot-gdextension-specialist` | Medium |
| Plan live events and seasons | `live-ops-designer` | Medium |
| Write patch notes for players | `community-manager` | Light |
| Brainstorm a new game idea | Use `/brainstorm` skill | Medium |

### 3. Use Slash Commands for Common Tasks

| Command | Model | What it does |
| --------- | ------- | ------------- |
| `/studio-start` | Medium | First-time onboarding — asks where you are, guides you to the right workflow |
| `/studio-help` | Light | Context-aware "what do I do next?" — reads your current phase and artifacts |
| `/project-stage-detect` | Light | Analyze project state, detect stage, identify gaps |
| `/setup-engine` | Medium | Configure engine + version, populate reference docs |
| `/adopt` | Medium | Brownfield audit and migration plan for existing projects |
| `/brainstorm` | Medium | Guided game concept ideation from scratch |
| `/map-systems` | Medium | Decompose concept into systems, map dependencies, guide per-system GDDs |
| `/design-system` | Medium | Guided, section-by-section GDD authoring for a single game system |
| `/quick-design` | Medium | Lightweight spec for small changes — tuning, tweaks, minor additions |
| `/review-all-gdds` | Heavy | Cross-GDD consistency and game design theory review |
| `/propagate-design-change` | Medium | Find ADRs and stories affected by a GDD change |
| `/art-bible` | Medium | Guided, section-by-section Art Bible authoring — creates visual identity spec before asset production |
| `/asset-spec` | Medium | Generate per-asset visual specifications and AI generation prompts from GDDs or character profiles |
| `/ux-design` | Medium | Author UX specs (screen/flow, HUD, interaction patterns) |
| `/ux-review` | Medium | Validate UX specs for accessibility and GDD alignment |
| `/create-architecture` | Medium | Master architecture document for the game |
| `/architecture-decision` | Medium | Creates an ADR |
| `/architecture-review` | Heavy | Validate all ADRs, dependency ordering, GDD traceability |
| `/create-control-manifest` | Medium | Flat programmer rules sheet from Accepted ADRs |
| `/create-epics` | Medium | Translate GDDs + ADRs into epics (one per architectural module) |
| `/create-stories` | Medium | Break a single epic into implementable story files |
| `/dev-story` | Medium | Read a story and implement it — routes to the correct programmer agent |
| `/sprint-plan` | Medium | Creates or updates sprint plans |
| `/sprint-status` | Light | Quick 30-line sprint snapshot |
| `/story-readiness` | Light | Validate a story is implementation-ready before pickup |
| `/story-done` | Medium | End-of-story completion review — verifies acceptance criteria |
| `/estimate` | Medium | Produces structured effort estimates |
| `/design-review` | Medium | Reviews a design document |
| `/code-review` | Medium | Reviews code for quality and architecture |
| `/balance-check` | Medium | Analyzes game balance data |
| `/asset-audit` | Medium | Audits assets for compliance |
| `/content-audit` | Medium | GDD-specified content vs. implemented — find gaps |
| `/scope-check` | Light | Detect scope creep against plan |
| `/perf-profile` | Medium | Performance profiling and bottleneck ID |
| `/tech-debt` | Medium | Scan, track, and prioritize tech debt |
| `/gate-check` | Heavy | Validate phase readiness (PASS/CONCERNS/FAIL) |
| `/consistency-check` | Medium | Scan all GDDs for cross-document inconsistencies (conflicting stats, names, rules) |
| `/security-audit` | Medium | Audit for security vulnerabilities: save tampering, cheat vectors, network exploits, data exposure |
| `/reverse-document` | Medium | Generate design/architecture docs from existing code |
| `/milestone-review` | Medium | Reviews milestone progress |
| `/retrospective` | Medium | Runs sprint/milestone retrospective |
| `/bug-report` | Medium | Structured bug report creation |
| `/playtest-report` | Medium | Creates or analyzes playtest feedback |
| `/onboard` | Light | Generates onboarding docs for a role |
| `/release-checklist` | Medium | Validates pre-release checklist |
| `/launch-checklist` | Medium | Complete launch readiness validation |
| `/changelog` | Light | Generates changelog from git history |
| `/patch-notes` | Light | Generate player-facing patch notes |
| `/hotfix` | Medium | Emergency fix with audit trail |
| `/day-one-patch` | Medium | Prepare a focused day-one patch for known issues discovered after gold master |
| `/prototype` | Medium | Concept prototype — validate core idea before writing GDDs (Phase 1) |
| `/vertical-slice` | Medium | Production-quality end-to-end build — validate full game loop (Phase 4) |
| `/localize` | Medium | Localization scan, extract, validate |
| `/team-combat` | Medium | Orchestrate full combat team pipeline |
| `/team-narrative` | Medium | Orchestrate full narrative team pipeline |
| `/team-ui` | Medium | Orchestrate full UI team pipeline |
| `/team-release` | Medium | Orchestrate full release team pipeline |
| `/team-polish` | Medium | Orchestrate full polish team pipeline |
| `/team-audio` | Medium | Orchestrate full audio team pipeline |
| `/team-level` | Medium | Orchestrate full level creation pipeline |
| `/team-live-ops` | Medium | Orchestrate live-ops team for seasons, events, and post-launch content |
| `/team-qa` | Medium | Orchestrate full QA team cycle — test plan, test cases, smoke check, sign-off |
| `/qa-plan` | Medium | Generate a QA test plan for a sprint or feature |
| `/bug-triage` | Light | Re-prioritize open bugs, assign to sprints, surface systemic trends |
| `/smoke-check` | Medium | Run critical path smoke test gate before QA hand-off (PASS/FAIL) |
| `/soak-test` | Medium | Generate a soak test protocol for extended play sessions |
| `/regression-suite` | Medium | Map coverage to GDD critical paths, flag gaps, maintain regression suite |
| `/test-setup` | Medium | Scaffold test framework + CI pipeline for the project's engine (run once) |
| `/test-helpers` | Medium | Generate engine-specific test helper libraries and factory functions |
| `/test-flakiness` | Medium | Detect flaky tests from CI history, flag for quarantine or fix |
| `/test-evidence-review` | Medium | Quality review of test files and manual evidence — ADEQUATE/INCOMPLETE/MISSING |
| `/skill-test` | Medium | Validate skill files for compliance and correctness (static / spec / audit) |
| `/skill-improve` | Medium | Improve a skill using a test-fix-retest loop — diagnose, propose fix, rewrite, verify |

### 4. Use Templates for New Documents

Templates are in `skill_view('project-templates', file_path='templates/')`:

- `game-design-document.md` -- for new mechanics and systems
- `architecture-decision-record.md` -- for technical decisions
- `architecture-traceability.md` -- maps GDD requirements to ADRs to story IDs
- `risk-register-entry.md` -- for new risks
- `narrative-character-sheet.md` -- for new characters
- `test-plan.md` -- for feature test plans
- `sprint-plan.md` -- for sprint planning
- `milestone-definition.md` -- for new milestones
- `level-design-document.md` -- for new levels
- `game-pillars.md` -- for core design pillars
- `art-bible.md` -- for visual style reference
- `technical-design-document.md` -- for per-system technical designs
- `post-mortem.md` -- for project/milestone retrospectives
- `sound-bible.md` -- for audio style reference
- `release-checklist-template.md` -- for platform release checklists
- `changelog-template.md` -- for player-facing patch notes
- `release-notes.md` -- for player-facing release notes
- `incident-response.md` -- for live incident response playbooks
- `game-concept.md` -- for initial game concepts (MDA, SDT, Flow, Bartle)
- `pitch-document.md` -- for pitching the game to stakeholders
- `economy-model.md` -- for virtual economy design (sink/faucet model)
- `faction-design.md` -- for faction identity, lore, and gameplay role
- `systems-index.md` -- for systems decomposition and dependency mapping
- `project-stage-report.md` -- for project stage detection output
- `design-doc-from-implementation.md` -- for reverse-documenting existing code into GDDs
- `architecture-doc-from-code.md` -- for reverse-documenting code into architecture docs
- `concept-doc-from-prototype.md` -- for reverse-documenting prototypes into concept docs
- `ux-spec.md` -- for per-screen UX specifications (layout zones, states, events)
- `hud-design.md` -- for whole-game HUD philosophy, zones, and element specs
- `accessibility-requirements.md` -- for project-wide accessibility tier and feature matrix
- `interaction-pattern-library.md` -- for standard UI controls and game-specific patterns
- `player-journey.md` -- for 6-phase emotional arc and retention hooks by time scale
- `difficulty-curve.md` -- for difficulty axes, onboarding ramp, and cross-system interactions
- `test-evidence.md` -- template for recording manual test evidence (screenshots, walkthrough notes)

Also in `skill_view('project-templates', file_path='templates/collaborative-protocols/')` (used by agents, not typically edited directly):

- `design-agent-protocol.md` -- question-options-draft-approval cycle for design agents
- `implementation-agent-protocol.md` -- story pickup through /story-done cycle for programming agents
- `leadership-agent-protocol.md` -- cross-department delegation and escalation for director-tier agents

### 5. Follow the Coordination Rules

1. Work flows down the hierarchy: Directors -> Leads -> Specialists
2. Conflicts escalate up the hierarchy
3. Cross-department work is coordinated by the `producer`
4. Agents do not modify files outside their domain without delegation
5. All decisions are documented

## First Steps for a New Project

**Don't know where to begin?** Run `/studio-start`. It asks where you are and routes
you to the right workflow. No assumptions about your game, engine, or experience level.

If you already know what you need, jump directly to the relevant path:

### Path A: "I have no idea what to build"

1. **Run `/studio-start`** (or `/brainstorm open`) — guided creative exploration:
   what excites you, what you've played, your constraints
   - Generates 3 concepts, helps you pick one, defines core loop and pillars
   - Produces a game concept document and recommends an engine
2. **Set up the engine** — Run `/setup-engine` (uses the brainstorm recommendation)
   - Configures AGENTS.md, detects knowledge gaps, populates reference docs
   - Creates `docs/technical-preferences.md` with naming conventions,
     performance budgets, and engine-specific defaults
   - If the engine version is newer than the LLM's training data, it fetches
     current docs from the web so agents suggest correct APIs
3. **Validate the concept** — Run `/design-review design/gdd/game-concept.md`
4. **Decompose into systems** — Run `/map-systems` to map all systems and dependencies
5. **Design each system** — Run `/design-system [system-name]` (or `/map-systems next`)
   to write GDDs in dependency order
6. **Prototype the mechanic** — Run `/prototype [core-mechanic]` (1–3 days — before writing GDDs)
7. **Design each system** — Run `/design-system [system-name]` to write GDDs, informed by prototype findings
8. **Plan the first sprint** — After architecture and `/vertical-slice`, run `/sprint-plan new`
9. Start building

### Path B: "I know what I want to build"

If you already have a game concept and engine choice:

1. **Set up the engine** — Run `/setup-engine [engine] [version]`
   (e.g., `/setup-engine godot 4.6` or `/setup-engine threejs 0.186.0`) — also creates `docs/technical-preferences.md`
2. **Write the Game Pillars** — delegate to `creative-director`
3. **Decompose into systems** — Run `/map-systems` to enumerate systems and dependencies
4. **Design each system** — Run `/design-system [system-name]` for GDDs in dependency order
5. **Create the initial ADR** — Run `/architecture-decision`
6. **Create the first milestone** in `production/milestones/`
7. **Plan the first sprint** — Run `/sprint-plan new`
8. Start building

### Path C: "I know the game but not the engine"

If you have a concept but don't know which engine fits:

1. **Run `/setup-engine`** with no arguments — it will ask about your game's
   needs (2D/3D, platforms, team size, language preferences) and recommend
   an engine based on your answers
2. Follow Path B from step 2 onward

### Path D: "I have an existing project"

If you have design docs, prototypes, or code already:

1. **Run `/studio-start`** (or `/project-stage-detect`) — analyzes what exists,
   identifies gaps, and recommends next steps
2. **Run `/adopt`** if you have existing GDDs, ADRs, or stories — audits
   internal format compliance and builds a numbered migration plan to fill gaps
   without overwriting your existing work
3. **Configure engine if needed** — Run `/setup-engine` if not yet configured
4. **Validate phase readiness** — Run `/gate-check` to see where you stand
5. **Plan the next sprint** — Run `/sprint-plan new`

## File Structure Reference

```
Hermes profile (installed separately from the game workspace):
SOUL.md                            -- Aesir Gameworks identity and operating posture
config.yaml                        -- Hermes hook and profile settings
skills/
  studio/                          -- Studio routing and operating references
  workflows/                       -- 73 slash-command workflows
  agents/                          -- 50 specialist role definitions
  rules/                           -- 11 path-specific rule skills
  support/                         -- Bootstrap and templates
  engines/                         -- Version-pinned engine references
  quality/                         -- Framework QA specifications

Game workspace:
AGENTS.md                          -- Hermes workspace context (engine pin; no @ imports)
docs/technical-preferences.md      -- Live engine, language, naming, budgets, specialist routing
src/  assets/  design/  docs/      -- Game implementation and documentation
tests/  prototypes/  production/   -- Validation, experiments, and delivery records
```
