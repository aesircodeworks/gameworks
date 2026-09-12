> **Upstream:** Derived from Claude Code Game Studios by Donchitos (MIT). https://github.com/Donchitos/Claude-Code-Game-Studios — adapted for Hermes Agent / Aesir Gameworks.

# Three.js — Current Best Practices

Last verified: 2026-09-11 | Engine: r186

Practices that are **new or changed** since the model's training data (~r176).
This supplements (not replaces) the agent's built-in knowledge.

## Install and imports

```js
import * as THREE from 'three/webgpu';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

const renderer = new THREE.WebGPURenderer({ canvas, antialias: true, powerPreference: 'high-performance' });
await renderer.init();
```

Vite is the official recommended bundler. Pin `three` in `package.json` and
read that pin before suggesting APIs.

TSL lives in `'three/tsl'`. Do not mix `three` and `three/webgpu` default
exports in one app without a deliberate split.

WebGL (compatibility fallback only):

```js
import * as THREE from 'three';
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, powerPreference: 'high-performance' });
```

## Color and tone mapping

- `ColorManagement.enabled` is already true
- `renderer.outputColorSpace = THREE.SRGBColorSpace`
- Studio default: `renderer.toneMapping = THREE.ACESFilmicToneMapping`
- Color textures: `texture.colorSpace = SRGBColorSpace`
- HDR env: `LinearSRGBColorSpace` (often HalfFloat EXR/HDR via `HDRLoader`)
- Tone-map **once**. Bloom in HDR before tone map
- Default (WebGPU) post: `RenderPipeline` + TSL `pass()`, not EffectComposer
- WebGL fallback post: EffectComposer with `OutputPass` last

## Shadows and lights

- `renderer.shadowMap.enabled = true`; meshes opt in with `castShadow` / `receiveShadow`
- Use `PCFShadowMap`. Do not use `PCFSoftShadowMap` on WebGPU (r186)
- Point lights = six shadow passes — budget them
- AO is not a substitute for shadows

## Animation and time

- `AnimationMixer.update(delta)` with `Timer`, not `Clock`
- `Object3D.dispose()` exists in r186 — use it in subclass teardown
- Always dispose GPU resources on HMR and scene restart

## glTF pipeline

- `GLTFLoader` from addons
- Draco: `setDRACOLoader`; KTX2: `setKTX2Loader` + `detectSupport(renderer)` after init
- meshopt: `setMeshoptDecoder`
- Recommended format: `.glb`

## What not to treat as Three.js

- Physics, HUD toolkit, InputMap, navmesh, netcode, scene database, console SKUs
- cannon-es / ammo.js as "the" Three.js physics (docs: not maintained)
- R3F / drei as official three.js. R3F is an Aesir `/setup-engine` app-layer option wrapping the same `three` pin — not a second engine

## React Three Fiber (only when App layer is R3F)

- One `<Canvas>` owns the renderer. Do not construct a second `WebGPURenderer` beside it
- Pin `@react-three/fiber` to a release that supports the pinned `three`. Prefer WebGPU when that R3F version exposes it
- Reconcile R3F color/tone-mapping defaults with Aesir (`SRGBColorSpace`, ACES)
- HUD remains DOM. drei `Html` is for world labels
- Do not add `@react-three/drei` until a specific helper is used
