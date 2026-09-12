> **Upstream:** Derived from Claude Code Game Studios by Donchitos (MIT). https://github.com/Donchitos/Claude-Code-Game-Studios — adapted for Hermes Agent / Aesir Gameworks.

# Three.js — Deprecated APIs

Last verified: 2026-09-11

If an agent suggests any API in the "Deprecated" column, replace it.

## Packaging and loaders

| Deprecated | Use Instead | Since | Notes |
|------------|-------------|-------|-------|
| `new THREE.Geometry()` | `BufferGeometry` / `BoxGeometry` | r140 | Removed |
| `BoxBufferGeometry` alias | `BoxGeometry` | r145 | |
| `examples/js/controls/OrbitControls.js` | `three/addons/controls/OrbitControls.js` | r148 | |
| `<script src="three.min.js">` + global `THREE` | ESM `import * as THREE from 'three'` | r160 | |
| `require('three')` | ESM import | r186 | Deprecated shim |
| `RGBELoader` | `HDRLoader` | r180 | |
| `DRACOLoader.setDecoderConfig()` | WASM decoder defaults | r185 | |
| `GLTFLoader` WebP/AVIF runtime detect | Browser decode | r176 | Files still work if the browser can decode them |

## Color, lights, renderer

| Deprecated | Use Instead | Since | Notes |
|------------|-------------|-------|-------|
| `renderer.outputEncoding` / `setEncoding` | `renderer.outputColorSpace = SRGBColorSpace` | r152 | |
| `texture.encoding` / `sRGBEncoding` | `texture.colorSpace = SRGBColorSpace` | r152 | |
| `LinearEncoding` | `LinearSRGBColorSpace` | r152 | |
| `ColorManagement.legacyMode` | `ColorManagement.enabled` (default true) | r152 | |
| `physicallyCorrectLights` / `useLegacyLights` | delete; physical is default | r155 | |
| EffectComposer without `OutputPass` | `OutputPass` last | r155 | Tone map + color space apply when drawing to screen |
| `PCFSoftShadowMap` | `PCFShadowMap` | r182 / r186 | Removed on WebGPU in r186 |
| `PostProcessing` (WebGPU) | `RenderPipeline` | r183 | |
| `renderAsync` / `computeAsync` | sync after `renderer.init()` | r181 | |
| NodeMaterial on `import from 'three'` | `three/webgpu` + WebGPURenderer | r165 | Studio default is WebGPU |
| New-project `WebGLRenderer` | `WebGPURenderer` from `three/webgpu` | Aesir | Compatibility fallback only |
| `Clock` | `Timer` | r183 | Timer in core since r179 |

## Patterns

| Deprecated Pattern | Use Instead | Why |
|--------------------|-------------|-----|
| `Object3D.clone()` of a skinned glTF | `SkeletonUtils.clone` | Skeleton shared incorrectly |
| Raw `requestAnimationFrame` plus a second loop | One owner; prefer `setAnimationLoop` | Double render / leaked rAF |
| Visual mesh as Rapier collider | Primitive / compound / hull proxies | Cost and wrong contacts |
| `Math.random` in gameplay | Seeded RNG | Breaks deterministic tests |
| R3F defaults assumed on vanilla three | Set color space and tone mapping yourself | Different ecosystem defaults |
