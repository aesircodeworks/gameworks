# Skill Test Spec: /aesir-vertical-slice

> **Upstream:** Derived from Claude Code Game Studios by Donchitos (MIT). https://github.com/Donchitos/Claude-Code-Game-Studios

## Skill Summary

`/aesir-vertical-slice` validates a playable slice against design, UX, and production evidence. It never advances `production/stage.txt` automatically.

## Protocol

- Approval before write.
- No automatic production-stage advance.
- Verdicts must be evidence-backed.

## Test Cases

### Case 1: complete prerequisites → PROCEED

**Fixture:** GDD, architecture, and UX spec exist with acceptance criteria.

**Expected:** PROCEED.

### Case 2: missing GDD/architecture/UX prerequisite → BLOCKED

**Fixture:** one of GDD, architecture, or UX spec is missing.

**Expected:** BLOCKED.

### Case 3: failed playtest acceptance criterion → PIVOT

**Fixture:** playtest report fails a stated acceptance criterion.

**Expected:** PIVOT.

### Case 4: infeasible production estimate → KILL

**Fixture:** estimate shows the slice cannot ship in the remaining schedule.

**Expected:** KILL.

### Case 5: full/lean/solo review-mode routing

**Fixture:** `production/review-mode.txt` is `full`, `lean`, or `solo`.

**Expected:** full runs directors; lean runs directors for the slice gate; solo skips director `delegate_task` calls and uses artifact checks.
