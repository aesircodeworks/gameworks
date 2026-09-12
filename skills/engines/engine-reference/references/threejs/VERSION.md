> **Upstream:** Derived from Claude Code Game Studios by Donchitos (MIT). https://github.com/Donchitos/Claude-Code-Game-Studios — adapted for Hermes Agent / Aesir Gameworks.

# Three.js — Version Reference

| Field | Value |
|-------|-------|
| **Engine Version** | three.js r186 / npm `three@0.186.0` |
| **Release Date** | 2026-09-08 |
| **Project Pinned** | 2026-09-11 |
| **Last Docs Verified** | 2026-09-11 |
| **LLM Knowledge Cutoff** | May 2025 |

## Knowledge Gap Warning

The LLM's training data likely covers three.js through ~r176 / early r177.
r178–r186 changed WebGPU imports, post-processing names, HDR loaders, Timer/Clock,
shadows, CJS, and PBR appearance. Always cross-reference this directory before
suggesting Three.js API calls. Inspect the game's installed `three` if it differs.

## Post-Cutoff Version Timeline

| Version | Release | Risk Level | Key Theme |
|---------|---------|------------|-----------|
| r177 | 2025-05-30 | MEDIUM | ColorManagement method names |
| r178 | 2025-06-30 | HIGH | Premultiplied blending |
| r179 | 2025-08-02 | HIGH | `Timer` in core |
| r180 | 2025-09-03 | HIGH | `RGBELoader` → `HDRLoader` |
| r181 | 2025-10-31 | HIGH | PBR/PMREM look; async renderer APIs deprecated; JSDoc docs |
| r182 | 2025-12-10 | HIGH | `PCFSoftShadowMap` deprecated on WebGLRenderer |
| r183 | 2026-02-25 | HIGH | `PostProcessing` → `RenderPipeline`; `Clock` deprecated |
| r184 | 2026-04-16 | HIGH | Background/env rotation; loader return values |
| r185 | 2026-07-01 | HIGH | WebGPU premultiplied alpha; Draco config |
| r186 | 2026-09-08 | HIGH | `Object3D.dispose()`; `PCFSoftShadowMap` removed on WebGPU; CJS deprecated |

r187 existed only as unreleased wiki notes as of 2026-09-11. Do not pin it.

## Studio defaults (Aesir)

- Language: TypeScript
- Bundler: Vite (`npm install --save three` + `vite`)
- Renderer: **WebGPURenderer** (`import from 'three/webgpu'`, `await init()`, ACES Filmic, `SRGBColorSpace`)
- Shaders: TSL / NodeMaterial (`'three/tsl'`); post: `RenderPipeline`
- Imports: `three/webgpu` and `three/addons/...`
- Assets: glTF/GLB
- HUD: DOM overlay
- Physics: none until needed; Rapier when simulation is real
- App layer: **Vanilla** unless `/setup-engine` chose React Three Fiber
- WebGLRenderer is the compatibility fallback
- R3F (`@react-three/fiber`) is a `/setup-engine` app-layer option wrapping the same pinned `three`. `@react-three/drei` is added only when a helper is used

## Verified Sources

- Docs: https://threejs.org/docs/
- LLM sheet (pins 0.186.0): https://threejs.org/docs/llms.txt
- Manual / install: https://threejs.org/manual/pages/installation.html
- Color management: https://threejs.org/manual/pages/color-management.html
- Migration wiki: https://github.com/mrdoob/three.js/wiki/Migration-Guide
- r186 release: https://github.com/mrdoob/three.js/releases/tag/r186
- npm: https://www.npmjs.com/package/three
