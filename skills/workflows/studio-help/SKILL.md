---
name: studio-help
description: Choose the next game development step.
version: 1.1.0
author: Donchitos; Hermes adaptation by Aesir Codeworks
license: MIT
metadata:
  hermes:
    tags:
    - aesir-gameworks
    - game-development
    - workflow
    related_skills:
    - gameworks
---

# Studio Help — What Do I Do Next?

**Model tier:** Light

Read-only. Lightweight orientation, not a full audit. For a gap analysis, `/project-stage-detect`. Structural keyword COMPLETE is internal — do not print it. The printed done line is `studio-help done.`

---

## Step 1: Read the Catalog

Read `skill_view('gameworks', file_path='references/workflow-catalog.yaml')`. That list is authoritative for phases, step order, required vs optional, and artifact globs.

Do not glob `(game-workspace)/skills/*/SKILL.md`. Do not collect uncataloged skills. There is no "Also installed" footer.

---

## Step 2: Determine Current Phase

Check in this order:

1. **Read `production/stage.txt`** — if it has content, that is the phase. Map it:
   - "Concept" → `concept`
   - "Systems Design" → `systems-design`
   - "Technical Setup" → `technical-setup`
   - "Pre-Production" → `pre-production`
   - "Production" → `production`
   - "Polish" → `polish`
   - "Release" → `release`

2. **If stage.txt is missing**, infer from artifacts (most-advanced match wins):
   - `src/` has 10+ source files → `production`
   - `production/epics/` has files (EPIC.md or `story-*.md`) → `pre-production`
   - `docs/architecture/adr-*.md` exists → `technical-setup`
   - `design/gdd/systems-index.md` exists → `systems-design`
   - `design/gdd/game-concept.md` exists → `concept`
   - Nothing → `concept` (fresh project)

---

## Step 3: Read Session Context

Read `production/session-state/active.md` if it exists. Extract the current artifact, in-progress task, and STATUS block. Use this for the Focus row and to name the Next target. Do not quote it as a paragraph.

---

## Step 4: Check Step Completion for the Current Phase

For each step in the current phase (from the catalog):

### Artifact-based checks

If the step has `artifact.glob`:
- Use `search_files` with `file_glob` set to the catalog glob (game-workspace relative)
- If `min_count` is specified, verify at least that many files match
- If `artifact.pattern` is specified, search that pattern on the matched file
- **Complete** = artifact condition is met
- **Incomplete** = artifact is missing or pattern not found

If the step has `artifact.note` (no glob): read the file the note names when it is a path. Count statuses. Do not mark MANUAL if that file yields counts.

If the step has no `artifact` field: infer from the same counts when a later/earlier step in this phase already produced them (e.g. Designed vs Approved GDDs). Otherwise mark **UNKNOWN**.

Mark **MANUAL** only when there is no file or count to read.

### Production: `sprint-status.yaml`

When the phase is `production` and `production/sprint-status.yaml` exists, read it before globbing stories.

- `in-progress` → active work (Focus / Next target)
- `ready-for-dev` → Next if nothing is in-progress
- `done` → complete
- `blocked` → include the `blocker` field in the fact line

Skip glob checks for `implement` and `story-done` when the YAML exists.

### Repeatable required steps

Counts go on the fact line. Next is this step only while it still has a named item to *create*. Items that exist and wait on a later required step (review, approve) do not keep this step as Next.

Systems Design: read `design/gdd/systems-index.md` and the GDD files. Missing GDD → `Next: /design-system  [system]`. GDD exists but not Approved → `Next: /design-review  [path]`. All MVP Approved → advance to `/review-all-gdds`.

---

## Step 5: Pick Next and Optional

From the completion data:

1. **Next** — the first incomplete *required* step. Exactly one.
2. **Optional** — at most one incomplete *optional* catalog step that can run now and does not replace Next.

If catalog text says the optional runs after a still-incomplete required step, omit it — unless session state queued it now; then keep it and append `(does not replace /command)`.

If the user named a just-finished step (e.g. "just finished design-review"), advance past that step when the artifact check is ambiguous.

`clarify` only when Next would be **MANUAL** and there is no count or file evidence. Do not `clarify` after the report.

If the user passed a topic (`/studio-help testing`): facts stay. Next is the topic skill only when it can run now; otherwise Next stays the required step and the topic skill may appear as Optional under the same Optional rules. Do not list multiple topic skills.

Do not print upcoming required steps. `/gate-check` appears only when it *is* Next.

---

## Step 6: Present Output

Print only this shape. No headings, no Done list, no Coming up, no gate warning, no "fresh session", no skill catalog.

```
Phase  [Phase Label]
[Noun] [counts or named status — 1–2 lines, current phase only]
Focus  [path] — [short status]

Next: /command  [named target]

Optional: /command (does not replace /next-command)

studio-help done.
```

**Rows**

- `Phase` always.
- 1–2 fact lines after it: counts or named artifacts for this phase only (`GDDs  8 written · 1 approved (Economy) · 7 Designed`, `Sprint  4 · 3 in-progress · 1 blocked`, `Concept  missing`). Never a completed-step list.
- `Focus` only when `active.md` or an in-progress artifact exists. Omit the row otherwise.
- `Next:` exactly one row, always prefixed `Next:`. If the catalog step has `command:`, print `Next: /command  [named target]`. If it has no command (e.g. `accessibility-doc`), print `Next: [imperative]  [named path]` — still that one row, never a paragraph or a second recommendation.
- `Optional:` at most one line. Omit the row when nothing qualifies.
- Done line last, exactly: `studio-help done.` Print nothing after it.

Never auto-run the next skill.

If nothing exists to infer (no stage.txt, no concept, no engine pin): `Phase  Concept`, fact `Concept  missing`, `Next: /studio-start`. Do not print a full workflow map.
