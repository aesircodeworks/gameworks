> **Upstream:** Derived from Claude Code Game Studios by Donchitos (MIT). https://github.com/Donchitos/Claude-Code-Game-Studios — adapted for Hermes Agent / Aesir Gameworks.

# Agent Coordination Rules

When assigning write scope or handling a new decision, load
`collaborative-design-principle.md`. Delegated children inherit only the user's
approved scope and supplied decisions; they return new decisions or blockers to
the coordinator instead of asking the user directly. Consultation and delegation
do not grant new authority or bypass later design, stage, or release gates.

1. **Vertical Delegation**: Leadership agents delegate to department leads, who
   delegate to specialists. Never skip a tier for complex decisions.
2. **Horizontal Consultation**: Agents at the same tier may consult each other
   but must not make binding decisions outside their domain.
3. **Conflict Resolution**: When two agents disagree, escalate to the shared
   parent. If no shared parent, escalate to `creative-director` for design
   conflicts or `technical-director` for technical conflicts.
4. **Change Propagation**: When a design change affects multiple domains, the
   `producer` agent coordinates the propagation.
5. **No Unilateral Cross-Domain Changes**: An agent must never modify files
   outside its designated directories without explicit delegation.

## Model Tier Assignment

Skills and agents are assigned a model tier by task complexity. Use these names
everywhere a model tier is stated:

| Model tier | When to use |
|------------|-------------|
| **Light** | Read-only status checks, formatting, simple lookups — no creative judgment needed |
| **Medium** | Implementation, design authoring, analysis of individual systems — most work |
| **Heavy** | Multi-document synthesis, high-stakes phase gate verdicts, cross-system holistic review |

Model tier Light: `/studio-help`, `/sprint-status`, `/story-readiness`, `/scope-check`,
`/project-stage-detect`, `/changelog`, `/patch-notes`, `/onboard`, `/bug-triage`

Model tier Heavy: `/review-all-gdds`, `/architecture-review`, `/gate-check`

All other skills: Medium. When creating new skills, assign Light if the skill only
reads and formats; assign Heavy if it must synthesize 5+ documents with high-stakes
output; otherwise Medium.

Role model tiers are in `agent-roster.md`. Directors (`creative-director`,
`technical-director`, `producer`) are Heavy. `art-director` and other leads are
Medium. Specialists are Medium except Light for `qa-tester`, `devops-engineer`,
`accessibility-specialist`, and `community-manager`.

## Subagents

Spawned via `delegate_task` within a single Hermes Agent session. Used by all `team-*` skills
and orchestration skills. Subagents share the session's permission context, run
sequentially or in parallel within the session, and return results to the parent.

**When to spawn in parallel**: If two subagents' inputs are independent (neither
needs the other's output to begin), spawn both `delegate_task` calls simultaneously rather
than waiting. Example: `/review-all-gdds` Phase 1 (consistency) and Phase 2
(design theory) are independent — spawn both at the same time.

## Parallel Task Protocol

When an orchestration skill spawns multiple independent agents:

1. Issue all independent delegate_task calls before waiting for any result
2. Collect all results before proceeding to dependent phases
3. If any agent is BLOCKED, surface it immediately — do not silently skip
4. Always produce a partial report if some agents complete and others block
