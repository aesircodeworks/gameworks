---
name: team-polish
description: Use when coordinating feature polish for release.
version: 1.0.0
author: Donchitos; Hermes adaptation by Aesir Gameworks
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

**Model tier:** Medium

If no argument is provided, output usage guidance and exit without spawning any agents:
> Usage: `/team-polish [feature or area]` — specify the feature or area to polish (e.g., `combat`, `main menu`, `inventory system`, `level-1`). Do not use `clarify` here; output the guidance directly.

When this skill is invoked with an argument, orchestrate the polish team through a structured pipeline.

**Decision Points:** At each phase transition, use `clarify` to present
the user with the subagent's proposals as selectable options. Write the agent's
full analysis in conversation, then capture the decision with concise labels.
The user must approve before moving to the next phase.

## Phase 0: Resolve Review Mode

1. If `--review [mode]` was passed as an argument, use that mode.
2. Else read `production/review-mode.txt` — use whatever is written there.
3. Else default to `lean`.

Modes:
- `full` — spawn all director and lead gates as described
- `lean` — skip director gates unless they are PHASE-GATE type (CD-PHASE-GATE, TD-PHASE-GATE, PR-PHASE-GATE, AD-PHASE-GATE)
- `solo` — skip all director gate spawning entirely; run the skill without any agent gates

Store the resolved mode for use in all subsequent phases.

**Director gate skip rule**: Before spawning any Tier 1 director or lead for review (outside of PHASE-GATE triggers), apply the resolved mode: skip if solo mode; skip if lean mode and this is not a PHASE-GATE.

## Team Composition
- **performance-analyst** — Profiling, optimization, memory analysis, frame budget
- **engine-programmer** — Engine-level bottlenecks: rendering pipeline, memory, resource loading (invoke when performance-analyst identifies low-level root causes)
- **technical-artist** — VFX polish, shader optimization, visual quality
- **sound-designer** — Audio polish, mixing, ambient layers, feedback sounds
- **tools-programmer** — Content pipeline tool verification, editor tool stability, automation fixes (invoke when content authoring tools are involved in the polished area)
- **qa-tester** — Edge case testing, regression testing, soak testing

## How to Delegate

Use the delegate_task tool to spawn each team member as a subagent:
- Spawn `performance-analyst` with `delegate_task` — Profiling, optimization, memory analysis
- Spawn `engine-programmer` with `delegate_task` — Engine-level fixes for rendering, memory, resource loading
- Spawn `technical-artist` with `delegate_task` — VFX polish, shader optimization, visual quality
- Spawn `sound-designer` with `delegate_task` — Audio polish, mixing, ambient layers
- Spawn `tools-programmer` with `delegate_task` — Content pipeline and editor tool verification
- Spawn `qa-tester` with `delegate_task` — Edge case testing, regression testing, soak testing

Always provide full context in each agent's prompt (target feature/area, performance budgets, known issues). Launch independent agents in parallel where the pipeline allows it (e.g., Phases 3 and 4 can run simultaneously).

## Pipeline

### Phase 1: Assessment
Delegate to **performance-analyst**:
- Profile the target feature/area using `/perf-profile`
- Identify performance bottlenecks and frame budget violations
- Measure memory usage and check for leaks
- Benchmark against target hardware specs
- Output: performance report with prioritized optimization list

### Phase 2: Optimization
Delegate to **performance-analyst** (with relevant programmers as needed):
- Fix performance hotspots identified in Phase 1
- Optimize draw calls, reduce overdraw
- Fix memory leaks and reduce allocation pressure
- Verify optimizations don't change gameplay behavior
- Output: optimized code with before/after metrics

If Phase 1 identified engine-level root causes (rendering pipeline, resource loading, memory allocator), delegate those fixes to **engine-programmer** in parallel:
- Optimize hot paths in engine systems
- Fix allocation pressure in core loops
- Output: engine-level fixes with profiler validation

### Phase 3: Visual Polish (parallel with Phase 2)
Delegate to **technical-artist**:
- Review VFX for quality and consistency with art bible
- Optimize particle systems and shader effects
- Add screen shake, camera effects, and visual juice where appropriate
- Ensure effects degrade gracefully on lower settings
- Output: polished visual effects

### Phase 4: Audio Polish (parallel with Phase 2)
Delegate to **sound-designer**:
- Review audio events for completeness (are any actions missing sound feedback?)
- Check audio mix levels — nothing too loud or too quiet relative to the mix
- Add ambient audio layers for atmosphere
- Verify audio plays correctly with spatial positioning
- Output: audio polish list and mixing notes

### Phase 5: Hardening
Delegate to **qa-tester**:
- Test all edge cases: boundary conditions, rapid inputs, unusual sequences
- Soak test: run the feature for extended periods checking for degradation
- Stress test: maximum entities, worst-case scenarios
- Regression test: verify polish changes haven't broken existing functionality
- Test on minimum spec hardware (if available)
- Output: test results with any remaining issues

### Phase 6: Sign-off
- Collect results from all team members
- Compare performance metrics against budgets
- Report: READY FOR RELEASE / NEEDS MORE WORK
- List any remaining issues with severity and recommendations

## Error Recovery Protocol

If any spawned agent (with delegate_task) returns BLOCKED, errors, or cannot complete:

1. **Surface immediately**: Report "[AgentName]: BLOCKED — [reason]" to the user before continuing to dependent phases
2. **Assess dependencies**: Check whether the blocked agent's output is required by subsequent phases. If yes, do not proceed past that dependency point without user input.
3. **Offer options** via clarify with choices:
   - Skip this agent and note the gap in the final report
   - Retry with narrower scope
   - Stop here and resolve the blocker first
4. **Always produce a partial report** — output whatever was completed. Never discard work because one agent blocked.

Common blockers:
- Input file missing (story not found, GDD absent) → redirect to the skill that creates it
- ADR status is Proposed → do not implement; run `/architecture-decision` first
- Scope too large → split into two stories via `/create-stories`
- Conflicting instructions between ADR and story → surface the conflict, do not guess

## File Write Protocol

All file writes (performance reports, test results, evidence docs) are delegated to
sub-agents spawned with delegate_task. The coordinator obtains any missing write approval and passes the approved scope to each child. Children return new scope decisions to the coordinator; they do not ask the user directly or repeat approval already supplied. Load `skill_view('gameworks', file_path='references/collaborative-design-principle.md')` when resolving authorization. This orchestrator does not write files directly.

## Output

A summary report covering: performance before/after metrics, visual polish changes, audio polish changes, test results, and release readiness assessment.

## Next Steps

- If READY FOR RELEASE: run `/release-checklist` for the final pre-release validation.
- If NEEDS MORE WORK: schedule remaining issues in `/sprint-plan update` and re-run `/team-polish` after fixes.
- Run `/gate-check` for a formal phase gate verdict before handing off to release.
