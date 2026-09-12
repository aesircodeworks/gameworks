> **Upstream:** Derived from Claude Code Game Studios by Donchitos (MIT). https://github.com/Donchitos/Claude-Code-Game-Studios — adapted for Hermes Agent / Aesir Gameworks.

# Three.js Networking — Quick Reference

Last verified: 2026-09-11 | Engine: r186

**Bring your own.** three.js has no replication, RPC, or matchmaking.
Use a dedicated netcode library and keep the renderer as a view of replicated
state. Escalate library choice to `network-programmer` / `technical-director`.
