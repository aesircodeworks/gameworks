> **Upstream:** Derived from Claude Code Game Studios by Donchitos (MIT). https://github.com/Donchitos/Claude-Code-Game-Studios — adapted for Hermes Agent / Aesir Gameworks.

# Three.js Rendering — Quick Reference

Last verified: 2026-09-11 | Engine: r186

## What Changed Since ~r176

- r183: WebGPU `PostProcessing` renamed `RenderPipeline`
- r182–r186: `PCFSoftShadowMap` deprecated then removed on WebGPU
- r181: PBR/PMREM appearance change; `renderAsync` deprecated
- r165 (in-cutoff but still missed): NodeMaterial is WebGPURenderer-only

## Current API Patterns

### Default (WebGPU / TSL)

```js
import * as THREE from 'three/webgpu';
const renderer = new THREE.WebGPURenderer({ canvas, antialias: true, powerPreference: 'high-performance' });
await renderer.init();
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFShadowMap;
```

TSL: `'three/tsl'`. Node materials are not the `import from 'three'` path.
Post: `RenderPipeline` + TSL `pass()`, not EffectComposer.

`WebGPURenderer` can fall back to WebGL 2 when WebGPU is missing — still import
from `'three/webgpu'`. Do not silently rewrite a new project onto `WebGLRenderer`.

### Compatibility fallback (WebGL)

```js
import * as THREE from 'three';
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, powerPreference: 'high-performance' });
```

Materials: `MeshStandardMaterial` / `MeshPhysicalMaterial`. Always give PBR an
environment map (`scene.environment` from HDR + `PMREMGenerator`, or `RoomEnvironment`).

WebGL post: `EffectComposer` from addons, **`OutputPass` last**.

### Resize

Match drawing buffer to CSS size. Cap DPR (studio: 2 desktop, 1.5–2 mobile).
`setSize(width, height, false)` when the canvas is CSS-sized.

## Common Mistakes

- `outputEncoding` instead of `outputColorSpace`
- Assuming TSL works on WebGLRenderer
- Defaulting a new project to `WebGLRenderer`
- Mixing EffectComposer (WebGL) with RenderPipeline (WebGPU)
- Uncapped DPR on mobile
- Two `requestAnimationFrame` loops
