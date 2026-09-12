> **Upstream:** Derived from Claude Code Game Studios by Donchitos (MIT). https://github.com/Donchitos/Claude-Code-Game-Studios — adapted for Hermes Agent / Aesir Gameworks.

# Three.js Audio — Quick Reference

Last verified: 2026-09-11 | Engine: r186

Partial: `AudioListener` on the camera, `Audio` / `PositionalAudio`, `AudioLoader`.
This is the Web Audio API, not FMOD. Autoplay is blocked until a user gesture.

## Patterns

- One listener. Unlock `AudioContext` on first pointer/key
- Gameplay emits **events**; a small audio system plays buffers
- Pause/mute must stop loops and resume without stacking
- Do not ship API keys in the client

## Common Mistakes

- Creating a new `AudioContext` per SFX
- Spatial audio without attaching the listener to the camera
- Ignoring the gesture-unlock requirement
