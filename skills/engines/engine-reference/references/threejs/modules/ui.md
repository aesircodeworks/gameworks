> **Upstream:** Derived from Claude Code Game Studios by Donchitos (MIT). https://github.com/Donchitos/Claude-Code-Game-Studios — adapted for Hermes Agent / Aesir Gameworks.

# Three.js UI — Quick Reference

Last verified: 2026-09-11 | Engine: r186

Three.js has no HUD toolkit. Official easiest path: **DOM + CSS overlay**.
https://threejs.org/manual/pages/creating-text.html

## Ladder

1. **DOM overlay** — HUD, menus, pause, settings (studio default)
2. **CSS2DRenderer** — labels that follow world positions
3. **CSS3DRenderer** — HTML in 3D space (not materials/meshes)
4. **troika-three-text** — in-world TTF if you must
5. **R3F `Html` / drei** — world labels only, and only when App layer is R3F

UI reads game state and dispatches intents. It does not own simulation.

Use `env(safe-area-inset-*)`, stable text-fit, and touch targets when mobile
is in scope. `lil-gui` is debug-only (`?debug`), not the player HUD.

## Common Mistakes

- Building the whole HUD in CSS2D
- Stat-card DOM covering the next player decision
- Duplicating game rules inside UI code
- Assuming R3F Html is the HUD on a Vanilla project
- Building the player HUD in drei `Html` on an R3F project (DOM overlay stays default)
