---
name: memory-policy
description: Use when classifying durable Aesir memory or lessons.
version: 1.0.0
author: Donchitos; Hermes adaptation by Aesir Gameworks
license: MIT
metadata:
  hermes:
    tags:
    - aesir-gameworks
    - game-development
    - memory
    related_skills:
    - gameworks
---

> **Upstream:** Derived from Claude Code Game Studios by Donchitos (MIT). https://github.com/Donchitos/Claude-Code-Game-Studios

# Aesir memory policy

- `USER.md` holds stable user facts that apply across projects.
- `MEMORY.md` holds compact cross-project environment facts only.
- Task procedures belong in skills, not memory.
- Project/sprint/stage state belongs in the **game workspace**, never in the profile memory files.
- Role-specific Claude memories belong in the corresponding agent skill (see `lead-programmer` `references/upstream-memory.md`).
- Never replace or bulk-seed the live profile's bounded `MEMORY.md` / `USER.md` during distribution installation.
