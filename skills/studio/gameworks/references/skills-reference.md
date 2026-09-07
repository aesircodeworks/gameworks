> **Upstream:** Derived from Claude Code Game Studios by Donchitos (MIT). https://github.com/Donchitos/Claude-Code-Game-Studios — adapted for Hermes Agent / Aesir Gameworks.

# Available Skills (Slash Commands)

73 slash commands organized by phase. Type `/` in Hermes Agent to access any of them.

## Onboarding & Navigation

| Command | Model | Purpose |
| --------- | ------- | --------- |
| `/studio-start` | Medium | First-time onboarding — asks where you are, then guides you to the right workflow |
| `/studio-help` | Light | Context-aware "what do I do next?" — reads current stage and surfaces the required next step |
| `/project-stage-detect` | Light | Full project audit — detect phase, identify existence gaps, recommend next steps |
| `/setup-engine` | Medium | Configure engine + version, detect knowledge gaps, populate version-aware reference docs |
| `/adopt` | Medium | Brownfield format audit — checks internal structure of existing GDDs/ADRs/stories, produces migration plan |

## Game Design

| Command | Model | Purpose |
| --------- | ------- | --------- |
| `/brainstorm` | Medium | Guided ideation using professional studio methods (MDA, SDT, Bartle, verb-first) |
| `/map-systems` | Medium | Decompose game concept into systems, map dependencies, prioritize design order |
| `/design-system` | Medium | Guided, section-by-section GDD authoring for a single game system |
| `/quick-design` | Medium | Lightweight design spec for small changes — tuning, tweaks, minor additions |
| `/review-all-gdds` | Heavy | Cross-GDD consistency and game design holism review across all design docs |
| `/propagate-design-change` | Medium | When a GDD is revised, find affected ADRs and produce an impact report |

## Art & Assets

| Command | Model | Purpose |
| --------- | ------- | --------- |
| `/art-bible` | Medium | Guided, section-by-section Art Bible authoring — creates visual identity spec before asset production begins |
| `/asset-spec` | Medium | Generate per-asset visual specifications and AI generation prompts from GDDs, level docs, or character profiles |
| `/asset-audit` | Medium | Audit assets for naming conventions, file size budgets, and pipeline compliance |

## UX & Interface Design

| Command | Model | Purpose |
| --------- | ------- | --------- |
| `/ux-design` | Medium | Guided section-by-section UX spec authoring (screen/flow, HUD, or pattern library) |
| `/ux-review` | Medium | Validate UX specs for GDD alignment, accessibility, and pattern compliance |

## Architecture

| Command | Model | Purpose |
| --------- | ------- | --------- |
| `/create-architecture` | Medium | Guided authoring of the master architecture document |
| `/architecture-decision` | Medium | Create an Architecture Decision Record (ADR) |
| `/architecture-review` | Heavy | Validate all ADRs for completeness, dependency ordering, and GDD coverage |
| `/create-control-manifest` | Medium | Generate flat programmer rules sheet from accepted ADRs |

## Stories & Sprints

| Command | Model | Purpose |
| --------- | ------- | --------- |
| `/create-epics` | Medium | Translate GDDs + ADRs into epics — one per architectural module |
| `/create-stories` | Medium | Break a single epic into implementable story files |
| `/dev-story` | Medium | Read a story and implement it — routes to the correct programmer agent |
| `/sprint-plan` | Medium | Generate or update a sprint plan; initializes sprint-status.yaml |
| `/sprint-status` | Light | Fast 30-line sprint snapshot (reads sprint-status.yaml) |
| `/story-readiness` | Light | Validate a story is implementation-ready before pickup (READY/NEEDS WORK/BLOCKED) |
| `/story-done` | Medium | 8-phase completion review after implementation; updates story file, surfaces next story |
| `/estimate` | Medium | Structured effort estimate with complexity, dependencies, and risk breakdown |

## Reviews & Analysis

| Command | Model | Purpose |
| --------- | ------- | --------- |
| `/design-review` | Medium | Review a game design document for completeness and consistency |
| `/code-review` | Medium | Architectural code review for a file or changeset |
| `/balance-check` | Medium | Analyze game balance data, formulas, and config — flag outliers |
| `/content-audit` | Medium | Audit GDD-specified content counts against implemented content |
| `/scope-check` | Light | Analyze feature or sprint scope against original plan, flag scope creep |
| `/perf-profile` | Medium | Structured performance profiling with bottleneck identification |
| `/tech-debt` | Medium | Scan, track, prioritize, and report on technical debt |
| `/gate-check` | Heavy | Validate readiness to advance between development phases (PASS/CONCERNS/FAIL) |
| `/consistency-check` | Medium | Scan all GDDs against the entity registry to detect cross-document inconsistencies (stats, names, rules that contradict each other) |
| `/security-audit` | Medium | Audit the game for security vulnerabilities: save tampering, cheat vectors, network exploits, data exposure, and input validation gaps |

## QA & Testing

| Command | Model | Purpose |
| --------- | ------- | --------- |
| `/qa-plan` | Medium | Generate a QA test plan for a sprint or feature |
| `/smoke-check` | Medium | Run critical path smoke test gate before QA hand-off |
| `/soak-test` | Medium | Generate a soak test protocol for extended play sessions |
| `/regression-suite` | Medium | Map test coverage to GDD critical paths, identify fixed bugs without regression tests |
| `/test-setup` | Medium | Scaffold the test framework and CI/CD pipeline for the project's engine |
| `/test-helpers` | Medium | Generate engine-specific test helper libraries for the test suite |
| `/test-evidence-review` | Medium | Quality review of test files and manual evidence documents |
| `/test-flakiness` | Medium | Detect non-deterministic (flaky) tests from CI run logs |
| `/skill-test` | Medium | Validate skill files for structural compliance and behavioral correctness |
| `/skill-improve` | Medium | Improve a skill using a test-fix-retest loop — diagnose, propose fix, rewrite, verify |

## Production

| Command | Model | Purpose |
| --------- | ------- | --------- |
| `/milestone-review` | Medium | Review milestone progress and generate status report |
| `/retrospective` | Medium | Run a structured sprint or milestone retrospective |
| `/bug-report` | Medium | Create a structured bug report |
| `/bug-triage` | Light | Read all open bugs, re-evaluate priority vs. severity, assign owner and label |
| `/reverse-document` | Medium | Generate design or architecture docs from existing implementation |
| `/playtest-report` | Medium | Generate a structured playtest report or analyze existing playtest notes |

## Release

| Command | Model | Purpose |
| --------- | ------- | --------- |
| `/release-checklist` | Medium | Generate and validate a pre-release checklist for the current build |
| `/launch-checklist` | Medium | Complete launch readiness validation across all departments |
| `/changelog` | Light | Auto-generate changelog from git commits and sprint data |
| `/patch-notes` | Light | Generate player-facing patch notes from git history and internal data |
| `/hotfix` | Medium | Emergency fix workflow with audit trail, bypassing normal sprint process |
| `/day-one-patch` | Medium | Prepare a focused day-one patch for known issues discovered after gold master but before or at public launch |

## Creative & Content

| Command | Model | Purpose |
| --------- | ------- | --------- |
| `/prototype` | Medium | Concept prototype — throwaway build right after brainstorm to validate core idea (Phase 1) |
| `/vertical-slice` | Medium | Pre-Production validation — production-quality end-to-end build before committing to Production (Phase 4) |
| `/onboard` | Light | Generate contextual onboarding document for a new contributor or agent |
| `/localize` | Medium | Localization workflow: string extraction, validation, translation readiness |

## Team Orchestration

Coordinate multiple agents on a single feature area:

| Command | Model | Coordinates |
| --------- | ------- | ------------- |
| `/team-combat` | Medium | game-designer + gameplay-programmer + ai-programmer + technical-artist + sound-designer + qa-tester |
| `/team-narrative` | Medium | narrative-director + writer + world-builder + level-designer |
| `/team-ui` | Medium | ux-designer + ui-programmer + art-director + accessibility-specialist |
| `/team-release` | Medium | release-manager + qa-lead + devops-engineer + producer |
| `/team-polish` | Medium | performance-analyst + technical-artist + sound-designer + qa-tester |
| `/team-audio` | Medium | audio-director + sound-designer + technical-artist + gameplay-programmer |
| `/team-level` | Medium | level-designer + narrative-director + world-builder + art-director + systems-designer + qa-tester |
| `/team-live-ops` | Medium | live-ops-designer + economy-designer + community-manager + analytics-engineer |
| `/team-qa` | Medium | qa-lead + qa-tester + gameplay-programmer + producer |
