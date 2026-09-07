> **Upstream:** Derived from Claude Code Game Studios by Donchitos (MIT). https://github.com/Donchitos/Claude-Code-Game-Studios — adapted for Hermes Agent / Aesir Gameworks.

# Agent Roster

The following agents are available. Each has a role skill at
`skills/agents/<name>/SKILL.md` in the installed profile. Use the agent best suited to the task at hand. When a task
spans multiple domains, the coordinating agent (usually `producer` or the
domain lead) should delegate to specialists.

## Tier 1 -- Leadership Agents (Heavy)
| Agent | Domain | Model | When to Use |
|-------|--------|-------|-------------|
| `creative-director` | High-level vision | Heavy | Major creative decisions, pillar conflicts, tone/direction |
| `technical-director` | Technical vision | Heavy | Architecture decisions, tech stack choices, performance strategy |
| `producer` | Production management | Heavy | Sprint planning, milestone tracking, risk management, coordination |

## Tier 2 -- Department Lead Agents (Medium)
| Agent | Domain | Model | When to Use |
|-------|--------|-------|-------------|
| `game-designer` | Game design | Medium | Mechanics, systems, progression, economy, balancing |
| `lead-programmer` | Code architecture | Medium | System design, code review, API design, refactoring |
| `art-director` | Visual direction | Medium | Style guides, art bible, asset standards, UI/UX direction |
| `audio-director` | Audio direction | Medium | Music direction, sound palette, audio implementation strategy |
| `narrative-director` | Story and writing | Medium | Story arcs, world-building, character design, dialogue strategy |
| `qa-lead` | Quality assurance | Medium | Test strategy, bug triage, release readiness, regression planning |
| `release-manager` | Release pipeline | Medium | Build management, versioning, changelogs, deployment, rollbacks |
| `localization-lead` | Internationalization | Medium | String externalization, translation pipeline, locale testing |

## Tier 3 -- Specialist Agents (Medium or Light)
| Agent | Domain | Model | When to Use |
|-------|--------|-------|-------------|
| `systems-designer` | Systems design | Medium | Specific mechanic implementation, formula design, loops |
| `level-designer` | Level design | Medium | Level layouts, pacing, encounter design, flow |
| `economy-designer` | Economy/balance | Medium | Resource economies, loot tables, progression curves |
| `gameplay-programmer` | Gameplay code | Medium | Feature implementation, gameplay systems code |
| `engine-programmer` | Engine systems | Medium | Core engine, rendering, physics, memory management |
| `ai-programmer` | AI systems | Medium | Behavior trees, pathfinding, NPC logic, state machines |
| `network-programmer` | Networking | Medium | Netcode, replication, lag compensation, matchmaking |
| `tools-programmer` | Dev tools | Medium | Editor extensions, pipeline tools, debug utilities |
| `ui-programmer` | UI implementation | Medium | UI framework, screens, widgets, data binding |
| `technical-artist` | Tech art | Medium | Shaders, VFX, optimization, art pipeline tools |
| `sound-designer` | Sound design | Medium | SFX design docs, audio event lists, mixing notes |
| `writer` | Dialogue/lore | Medium | Dialogue writing, lore entries, item descriptions |
| `world-builder` | World/lore design | Medium | World rules, faction design, history, geography |
| `qa-tester` | Test execution | Light | Writing test cases, bug reports, test checklists |
| `performance-analyst` | Performance | Medium | Profiling, optimization recs, memory analysis |
| `devops-engineer` | Build/deploy | Light | CI/CD, build scripts, version control workflow |
| `analytics-engineer` | Telemetry | Medium | Event tracking, dashboards, A/B test design |
| `ux-designer` | UX flows | Medium | User flows, wireframes, accessibility, input handling |
| `prototyper` | Rapid prototyping | Medium | Throwaway prototypes, mechanic testing, feasibility validation |
| `security-engineer` | Security | Medium | Anti-cheat, exploit prevention, save encryption, network security |
| `accessibility-specialist` | Accessibility | Light | WCAG compliance, colorblind modes, remapping, text scaling |
| `live-ops-designer` | Live operations | Medium | Seasons, events, battle passes, retention, live economy |
| `community-manager` | Community | Light | Patch notes, player feedback, crisis comms, community health |

## Engine-Specific Agents (use the set matching your engine)

### Engine Leads

| Agent | Engine | Model | When to Use |
| ---- | ---- | ---- | ---- |
| `unreal-specialist` | Unreal Engine 5 | Medium | Blueprint vs C++, GAS overview, UE subsystems, Unreal optimization |
| `unity-specialist` | Unity | Medium | MonoBehaviour vs DOTS, Addressables, URP/HDRP, Unity optimization |
| `godot-specialist` | Godot 4 | Medium | GDScript patterns, node/scene architecture, signals, Godot optimization |

### Unreal Engine Sub-Specialists

| Agent | Subsystem | Model | When to Use |
| ---- | ---- | ---- | ---- |
| `ue-gas-specialist` | Gameplay Ability System | Medium | Abilities, gameplay effects, attribute sets, tags, prediction |
| `ue-blueprint-specialist` | Blueprint Architecture | Medium | BP/C++ boundary, graph standards, naming, BP optimization |
| `ue-replication-specialist` | Networking/Replication | Medium | Property replication, RPCs, prediction, relevancy, bandwidth |
| `ue-umg-specialist` | UMG/CommonUI | Medium | Widget hierarchy, data binding, CommonUI input, UI performance |

### Unity Sub-Specialists

| Agent | Subsystem | Model | When to Use |
| ---- | ---- | ---- | ---- |
| `unity-dots-specialist` | DOTS/ECS | Medium | Entity Component System, Jobs, Burst compiler, hybrid renderer |
| `unity-shader-specialist` | Shaders/VFX | Medium | Shader Graph, VFX Graph, URP/HDRP customization, post-processing |
| `unity-addressables-specialist` | Asset Management | Medium | Addressable groups, async loading, memory, content delivery |
| `unity-ui-specialist` | UI Toolkit/UGUI | Medium | UI Toolkit, UXML/USS, UGUI Canvas, data binding, cross-platform input |

### Godot Sub-Specialists

| Agent | Subsystem | Model | When to Use |
| ---- | ---- | ---- | ---- |
| `godot-gdscript-specialist` | GDScript | Medium | Static typing, design patterns, signals, coroutines, GDScript performance |
| `godot-csharp-specialist` | C# / .NET | Medium | .NET patterns, [Signal] delegates, async, nullable types, type-safe node access |
| `godot-shader-specialist` | Shaders/Rendering | Medium | Godot shading language, visual shaders, particles, post-processing |
| `godot-gdextension-specialist` | GDExtension | Medium | C++/Rust bindings, native performance, custom nodes, build systems |
