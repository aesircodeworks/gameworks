> **Upstream:** Derived from Claude Code Game Studios by Donchitos (MIT). https://github.com/Donchitos/Claude-Code-Game-Studios — adapted for Hermes Agent / Aesir Gameworks.

# Available Skills (Slash Commands)

73 slash commands organized by phase. Type `/` in Hermes Agent to access any of them.

## Onboarding & Navigation

| Command | Purpose |
|---------|---------|
| `/aesir-start` | First-time onboarding — asks where you are, then guides you to the right workflow |
| `/aesir-help` | Context-aware "what do I do next?" — reads current stage and surfaces the required next step |
| `/aesir-project-stage-detect` | Full project audit — detect phase, identify existence gaps, recommend next steps |
| `/aesir-setup-engine` | Configure engine + version, detect knowledge gaps, populate version-aware reference docs |
| `/aesir-adopt` | Brownfield format audit — checks internal structure of existing GDDs/ADRs/stories, produces migration plan |

## Game Design

| Command | Purpose |
|---------|---------|
| `/aesir-brainstorm` | Guided ideation using professional studio methods (MDA, SDT, Bartle, verb-first) |
| `/aesir-map-systems` | Decompose game concept into systems, map dependencies, prioritize design order |
| `/aesir-design-system` | Guided, section-by-section GDD authoring for a single game system |
| `/aesir-quick-design` | Lightweight design spec for small changes — tuning, tweaks, minor additions |
| `/aesir-review-all-gdds` | Cross-GDD consistency and game design holism review across all design docs |
| `/aesir-propagate-design-change` | When a GDD is revised, find affected ADRs and produce an impact report |

## Art & Assets

| Command | Purpose |
|---------|---------|
| `/aesir-art-bible` | Guided, section-by-section Art Bible authoring — creates visual identity spec before asset production begins |
| `/aesir-asset-spec` | Generate per-asset visual specifications and AI generation prompts from GDDs, level docs, or character profiles |
| `/aesir-asset-audit` | Audit assets for naming conventions, file size budgets, and pipeline compliance |

## UX & Interface Design

| Command | Purpose |
|---------|---------|
| `/aesir-ux-design` | Guided section-by-section UX spec authoring (screen/flow, HUD, or pattern library) |
| `/aesir-ux-review` | Validate UX specs for GDD alignment, accessibility, and pattern compliance |

## Architecture

| Command | Purpose |
|---------|---------|
| `/aesir-create-architecture` | Guided authoring of the master architecture document |
| `/aesir-architecture-decision` | Create an Architecture Decision Record (ADR) |
| `/aesir-architecture-review` | Validate all ADRs for completeness, dependency ordering, and GDD coverage |
| `/aesir-create-control-manifest` | Generate flat programmer rules sheet from accepted ADRs |

## Stories & Sprints

| Command | Purpose |
|---------|---------|
| `/aesir-create-epics` | Translate GDDs + ADRs into epics — one per architectural module |
| `/aesir-create-stories` | Break a single epic into implementable story files |
| `/aesir-dev-story` | Read a story and implement it — routes to the correct programmer agent |
| `/aesir-sprint-plan` | Generate or update a sprint plan; initializes sprint-status.yaml |
| `/aesir-sprint-status` | Fast 30-line sprint snapshot (reads sprint-status.yaml) |
| `/aesir-story-readiness` | Validate a story is implementation-ready before pickup (READY/NEEDS WORK/BLOCKED) |
| `/aesir-story-done` | 8-phase completion review after implementation; updates story file, surfaces next story |
| `/aesir-estimate` | Structured effort estimate with complexity, dependencies, and risk breakdown |

## Reviews & Analysis

| Command | Purpose |
|---------|---------|
| `/aesir-design-review` | Review a game design document for completeness and consistency |
| `/aesir-code-review` | Architectural code review for a file or changeset |
| `/aesir-balance-check` | Analyze game balance data, formulas, and config — flag outliers |
| `/aesir-content-audit` | Audit GDD-specified content counts against implemented content |
| `/aesir-scope-check` | Analyze feature or sprint scope against original plan, flag scope creep |
| `/aesir-perf-profile` | Structured performance profiling with bottleneck identification |
| `/aesir-tech-debt` | Scan, track, prioritize, and report on technical debt |
| `/aesir-gate-check` | Validate readiness to advance between development phases (PASS/CONCERNS/FAIL) |
| `/aesir-consistency-check` | Scan all GDDs against the entity registry to detect cross-document inconsistencies (stats, names, rules that contradict each other) |
| `/aesir-security-audit` | Audit the game for security vulnerabilities: save tampering, cheat vectors, network exploits, data exposure, and input validation gaps |

## QA & Testing

| Command | Purpose |
|---------|---------|
| `/aesir-qa-plan` | Generate a QA test plan for a sprint or feature |
| `/aesir-smoke-check` | Run critical path smoke test gate before QA hand-off |
| `/aesir-soak-test` | Generate a soak test protocol for extended play sessions |
| `/aesir-regression-suite` | Map test coverage to GDD critical paths, identify fixed bugs without regression tests |
| `/aesir-test-setup` | Scaffold the test framework and CI/CD pipeline for the project's engine |
| `/aesir-test-helpers` | Generate engine-specific test helper libraries for the test suite |
| `/aesir-test-evidence-review` | Quality review of test files and manual evidence documents |
| `/aesir-test-flakiness` | Detect non-deterministic (flaky) tests from CI run logs |
| `/aesir-skill-test` | Validate skill files for structural compliance and behavioral correctness |
| `/aesir-skill-improve` | Improve a skill using a test-fix-retest loop — diagnose, propose fix, rewrite, verify |

## Production

| Command | Purpose |
|---------|---------|
| `/aesir-milestone-review` | Review milestone progress and generate status report |
| `/aesir-retrospective` | Run a structured sprint or milestone retrospective |
| `/aesir-bug-report` | Create a structured bug report |
| `/aesir-bug-triage` | Read all open bugs, re-evaluate priority vs. severity, assign owner and label |
| `/aesir-reverse-document` | Generate design or architecture docs from existing implementation |
| `/aesir-playtest-report` | Generate a structured playtest report or analyze existing playtest notes |

## Release

| Command | Purpose |
|---------|---------|
| `/aesir-release-checklist` | Generate and validate a pre-release checklist for the current build |
| `/aesir-launch-checklist` | Complete launch readiness validation across all departments |
| `/aesir-changelog` | Auto-generate changelog from git commits and sprint data |
| `/aesir-patch-notes` | Generate player-facing patch notes from git history and internal data |
| `/aesir-hotfix` | Emergency fix workflow with audit trail, bypassing normal sprint process |
| `/aesir-day-one-patch` | Prepare a focused day-one patch for known issues discovered after gold master but before or at public launch |

## Creative & Content

| Command | Purpose |
|---------|---------|
| `/aesir-prototype` | Concept prototype — throwaway build right after brainstorm to validate core idea (Phase 1) |
| `/aesir-vertical-slice` | Pre-Production validation — production-quality end-to-end build before committing to Production (Phase 4) |
| `/aesir-onboard` | Generate contextual onboarding document for a new contributor or agent |
| `/aesir-localize` | Localization workflow: string extraction, validation, translation readiness |

## Team Orchestration

Coordinate multiple agents on a single feature area:

| Command | Coordinates |
|---------|-------------|
| `/aesir-team-combat` | game-designer + gameplay-programmer + ai-programmer + technical-artist + sound-designer + qa-tester |
| `/aesir-team-narrative` | narrative-director + writer + world-builder + level-designer |
| `/aesir-team-ui` | ux-designer + ui-programmer + art-director + accessibility-specialist |
| `/aesir-team-release` | release-manager + qa-lead + devops-engineer + producer |
| `/aesir-team-polish` | performance-analyst + technical-artist + sound-designer + qa-tester |
| `/aesir-team-audio` | audio-director + sound-designer + technical-artist + gameplay-programmer |
| `/aesir-team-level` | level-designer + narrative-director + world-builder + art-director + systems-designer + qa-tester |
| `/aesir-team-live-ops` | live-ops-designer + economy-designer + community-manager + analytics-engineer |
| `/aesir-team-qa` | qa-lead + qa-tester + gameplay-programmer + producer |
