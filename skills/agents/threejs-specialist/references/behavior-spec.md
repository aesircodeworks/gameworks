> **Upstream:** Derived from Claude Code Game Studios by Donchitos (MIT). https://github.com/Donchitos/Claude-Code-Game-Studios — adapted for Hermes Agent / Aesir Gameworks.

# Agent Test Spec: threejs-specialist

## Agent Summary
Domain: Three.js architecture — renderer choice, scene graph, loaders, color
management, loop ownership, and bring-your-own physics/UI/audio around the library.
Does NOT own: gameplay implementation (delegates to gameplay-programmer), HUD
markup (ui-programmer), or game design.
Model tier: Medium.
No gate IDs assigned.

---

## Static Assertions (Structural)

- [ ] `description:` field is present and domain-specific (references Three.js architecture / renderer / engine patterns)
- [ ] Model tier: Medium
- [ ] Agent definition references `docs/engine-reference/threejs/VERSION.md` as the authoritative API source
- [ ] Agent states there is no Three.js sub-specialist set

---

## Test Cases

### Case 1: In-domain request — appropriate output
**Input:** "Should the player HUD be CSS2DRenderer or a DOM overlay?"
**Expected behavior:**
- Recommends a DOM overlay for game HUD (menus, meters, pause)
- Maps CSS2DRenderer to world-space labels, not the full HUD
- Does NOT produce a React Three Fiber UI unless `AGENTS.md` App layer is R3F
- Defers markup implementation to `ui-programmer`

### Case 2: Wrong-engine redirect
**Input:** "Write a CharacterBody3D with move_and_slide() for the player."
**Expected behavior:**
- Does NOT produce Godot CharacterBody3D code
- Identifies this as a Godot pattern
- Maps the concept: authored movement + collision proxies in Three.js (custom overlap or Rapier), not an engine character controller
- Confirms the project is Three.js-based before proceeding

### Case 3: Post-cutoff API risk
**Input:** "Use RGBELoader to load the studio HDR and set outputEncoding to sRGBEncoding."
**Expected behavior:**
- Flags `RGBELoader` as renamed to `HDRLoader` (r180)
- Flags `outputEncoding` / `sRGBEncoding` as replaced by `outputColorSpace` / `SRGBColorSpace` (r152)
- Directs verification against `docs/engine-reference/threejs/VERSION.md` and `deprecated-apis.md`
- Does not emit the dead APIs as the recommended code

### Case 4: WebGL vs WebGPU
**Input:** "Should we switch the whole game to WebGLRenderer instead of WebGPU?"
**Expected behavior:**
- States WebGPURenderer + `three/webgpu` + `await init()` is the studio default
- Maps TSL / NodeMaterial as the default shader path on that renderer
- Treats WebGLRenderer as the compatibility fallback, not the default
- Does NOT make the final decision unilaterally
- Escalates a project-wide backend switch to `lead-programmer` / `technical-director`

### Case 5: Context pass — pinned r186
**Input:** Engine version context provided: three.js r186 / `three@0.186.0`. Request: "Advance time with THREE.Clock in the mixer update."
**Expected behavior:**
- Applies r183+ knowledge: `Clock` is deprecated; use `Timer`
- References `docs/engine-reference/threejs/breaking-changes.md` rather than training data
- Does not recommend `PCFSoftShadowMap` on WebGPU (removed r186)

---

## Protocol Compliance

- [ ] Stays within declared domain (Three.js architecture, APIs, loop, loaders)
- [ ] Redirects Godot/Unity/Unreal requests without producing wrong-engine code
- [ ] Treats `docs/engine-reference/threejs/VERSION.md` as authoritative over LLM training data
- [ ] Flags post-cutoff APIs (r178+) with verification requirements
- [ ] Defers implementation to gameplay-programmer / ui-programmer / engine-programmer
- [ ] Defers renderer-backend and extra-library decisions to lead-programmer / technical-director

---

## Coverage Notes
- Physics library choice (Rapier vs custom collision) is architecture; escalate when it is a project-wide pin
- Case 3 confirms the agent does not confidently use APIs removed after the May 2025 cutoff
