> **Upstream:** Derived from Claude Code Game Studios by Donchitos (MIT). https://github.com/Donchitos/Claude-Code-Game-Studios — adapted for Hermes Agent / Aesir Gameworks.

# Three.js Physics — Quick Reference

Last verified: 2026-09-11 | Engine: r186

Three.js has **no physics engine**. Official manual: parallel world, copy
transforms onto meshes, usually a fixed timestep.
https://threejs.org/manual/pages/physics.html

## Ladder

1. **Custom collision** — arcade overlaps, pickups, rails, bullets
2. **Rapier** — default when real rigid-body simulation is needed (`@dimforge/rapier3d-compat`)
3. **Jolt** — only if that behavior is specifically wanted
4. **cannon-es / ammo.js** — only if the project already depends on them (docs: not maintained)

Official wrappers live in `three/addons` physics examples. They wrap engines;
they are not engines.

## Rapier pattern

```ts
await RAPIER.init();
const world = new RAPIER.World({ x: 0, y: -9.81, z: 0 });
const fixedDt = 1 / 60;
// clamp accumulator (tab-switch) then world.step()
```

Sync body → mesh in **one** system. Primitive / compound / hull colliders —
never the visual glTF mesh. Sensors need `ActiveEvents.COLLISION_EVENTS`.
CCD only on fast bodies.

Update order: input → fixed physics → game state → VFX/camera/UI → render.

## Common Mistakes

- Treating Cannon as part of three.js
- Variable-delta `world.step`
- Syncing transforms in two places
- Leaving bodies alive across restart
