> **Upstream:** Derived from Claude Code Game Studios by Donchitos (MIT). https://github.com/Donchitos/Claude-Code-Game-Studios — adapted for Hermes Agent / Aesir Gameworks.

# Three.js — Breaking Changes

Last verified: 2026-09-11

Changes after the LLM cutoff (~r176). Source: https://github.com/mrdoob/three.js/wiki/Migration-Guide

## r185 → r186 (Sep 2026 — POST-CUTOFF, HIGH RISK)

| Subsystem | Change | Details |
|-----------|--------|---------|
| Core | `Object3D.dispose()` | Call `super.dispose()` in subclasses |
| Shadows | `PCFSoftShadowMap` removed on WebGPU | Use `PCFShadowMap` |
| Packaging | CJS `require('three')` deprecated | ESM only; shim warns `THREE_CJS_DEPRECATED` |
| Lights | `SunLight` (WebGL) | Cascaded sun shadows |
| Materials | MeshPhysical retroreflectivity | New physical property |

## r184 → r185 (Jul 2026 — POST-CUTOFF, HIGH RISK)

| Subsystem | Change | Details |
|-----------|--------|---------|
| WebGPU | Premultiplied-alpha default change | Check transparent materials |
| Loaders | `DRACOLoader.setDecoderConfig()` deprecated | WASM decoder going forward |

## r183 → r184 (Apr 2026 — POST-CUTOFF, HIGH RISK)

| Subsystem | Change | Details |
|-----------|--------|---------|
| Scene | Background/environment rotation | Aligned to object rotation |
| Loaders | FileLoader / ImageBitmapLoader | No longer return a value from `load` |

## r182 → r183 (Feb 2026 — POST-CUTOFF, HIGH RISK)

| Subsystem | Change | Details |
|-----------|--------|---------|
| WebGPU | `PostProcessing` → `RenderPipeline` | `outputNode = pass(scene, camera)` |
| Core | `Clock` deprecated | Use `Timer` (in core since r179) |
| IBL | RoomEnvironment lighting | Visual change with PMREM |

## r181 → r182 (Dec 2025 — POST-CUTOFF, HIGH RISK)

| Subsystem | Change | Details |
|-----------|--------|---------|
| Shadows | `PCFSoftShadowMap` deprecated on WebGLRenderer | Prefer `PCFShadowMap` |

## r180 → r181 (Oct 2025 — POST-CUTOFF, HIGH RISK)

| Subsystem | Change | Details |
|-----------|--------|---------|
| PBR | Energy/specular/PMREM | Materials look different |
| WebGPU | `renderAsync` / `computeAsync` deprecated | Sync methods after `init()`; `setAnimationLoop` inits for you |
| Docs | JSDoc English-only | New docs site |

## r179 → r180 (Sep 2025 — POST-CUTOFF, HIGH RISK)

| Subsystem | Change | Details |
|-----------|--------|---------|
| HDR | `RGBELoader` → `HDRLoader` | `three/addons/loaders/HDRLoader.js` |
| HDR | RGBMLoader removed | |

## r178 → r179 (Aug 2025 — POST-CUTOFF, HIGH RISK)

| Subsystem | Change | Details |
|-----------|--------|---------|
| Core | `Timer` moved to core | Replace `Clock` for mixer delta |
| Loaders | USDZLoader deprecated | |

## In-cutoff reminders (still commonly wrong)

| Version | Change |
|---------|--------|
| r165 | NodeMaterial only with WebGPURenderer |
| r163 | WebGL 1 dropped; `environmentIntensity` |
| r160 | UMD `three.js` / `three.min.js` removed |
| r155 | Physically correct lights default; EffectComposer needs `OutputPass` |
| r152 | `outputEncoding` → `outputColorSpace` |
| r148 | `examples/js` removed |
| r140 | `Geometry` removed; `BufferGeometry` only |
