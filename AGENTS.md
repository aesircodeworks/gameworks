# Aesir Gameworks — profile development

This repository is a Hermes profile distribution, not a game.
Do not write GDDs, ADRs, or game code here.

Read `CONTRIBUTING.md` before editing skills or hooks.

## Release hygiene

On any behavior, skill, hook, or packaging change, note it under `CHANGELOG.md` **Unreleased**. Do not bump `distribution.yaml` until a release.

When the user says **release**, **ship**, **create a release**, or **bump the version**: follow `CONTRIBUTING.md` ## Release. Do not invent a GitHub release, git tag, or CI job. Do not wait for a second design discussion if Unreleased has items.

Shipped means: `distribution.yaml` version bumped, Unreleased folded into that heading, commit on `main`, `gamedev` updated from this tree.
