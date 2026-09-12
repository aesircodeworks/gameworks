> **Upstream:** Derived from Claude Code Game Studios by Donchitos (MIT). https://github.com/Donchitos/Claude-Code-Game-Studios — adapted for Hermes Agent / Aesir Gameworks.

# Three.js Animation — Quick Reference

Last verified: 2026-09-11 | Engine: r186

https://threejs.org/manual/pages/animation-system.html

## Current API

- glTF `gltf.animations` → `AnimationClip[]`
- `new THREE.AnimationMixer(root); mixer.clipAction(clip).play(); mixer.update(delta)`
- Delta from **`Timer`**, not deprecated `Clock` (r183)
- Morphs: `mesh.morphTargetInfluences`
- Skinned clones: `import * as SkeletonUtils from 'three/addons/utils/SkeletonUtils.js'`

r186: `Object3D.dispose()` — call `super.dispose()` in subclasses.

## Common Mistakes

- `Object3D.clone()` on a skinned character
- Mixing animation delta units (ms vs seconds)
- Updating the mixer while a screenshot freeze is supposed to pause **gameplay** only — freeze sim, keep rendering
