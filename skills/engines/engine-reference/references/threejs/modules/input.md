> **Upstream:** Derived from Claude Code Game Studios by Donchitos (MIT). https://github.com/Donchitos/Claude-Code-Game-Studios — adapted for Hermes Agent / Aesir Gameworks.

# Three.js Input — Quick Reference

Last verified: 2026-09-11 | Engine: r186

Three.js has no InputMap. Keyboard, pointer, touch, and gamepad are DOM events.
Addons: `OrbitControls`, `PointerLockControls` (`three/addons/controls/...`).
Picking: `Raycaster`.

## Patterns

- Translate hardware to **intents** (move, look, dash) in one controller
- Pointer Lock for FPS; Orbit for editor/debug; don't mix without a mode switch
- `setPointerCapture` for on-canvas sticks; clear on `pointerup` / `pointercancel`
- Touch is required only when mobile is a target
- `touch-action: none` on the game canvas to stop browser pan/zoom

## Common Mistakes

- Polling `keydown` in the render loop without a key set
- Leaving Pointer Lock listeners after scene dispose
- Using OrbitControls in a production FPS
- Raycasting every frame against unindexed dense meshes
