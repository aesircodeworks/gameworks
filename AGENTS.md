# Aesir Gameworks — profile development

This repository is a Hermes profile distribution, not a game.
Do not write GDDs, ADRs, or game code here.

Read `CONTRIBUTING.md` before editing skills or hooks.

## Release hygiene

On any behavior, skill, hook, or packaging change, note it under `CHANGELOG.md` **Unreleased**. Do not bump `distribution.yaml` until a release.

When the user says **release**, **ship**, **create a release**, or **bump the version**: follow `CONTRIBUTING.md` ## Release. That includes a `vX.Y.Z` git tag and a GitHub Release. Do not invent a CI job. Do not wait for a second design discussion if Unreleased has items.

Shipped means: `distribution.yaml` version bumped, Unreleased folded into that heading, commit on `main`, pushed, tagged, GitHub Release published, `gameworks` updated from this tree.
