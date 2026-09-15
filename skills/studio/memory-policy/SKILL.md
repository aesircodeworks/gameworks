---
name: memory-policy
description: Classify durable Aesir memory or lessons.
version: 1.0.0
author: Donchitos; Hermes adaptation by Aesir Codeworks
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

# Aesir memory policy

- `USER.md` holds stable user facts that apply across projects.
- `MEMORY.md` holds compact cross-project environment facts only.
- Task procedures belong in skills, not memory.
- Project/sprint/stage state belongs in the **game workspace**, never in the profile memory files.
- Role-specific Claude memories belong in the corresponding agent skill (see `lead-programmer` `references/upstream-memory.md`).
- Never replace or bulk-seed the live profile's bounded `MEMORY.md` / `USER.md` during distribution installation.
