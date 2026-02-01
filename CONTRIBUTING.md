# Contributing

This repo is an opinionated system. Changes should preserve coherence and prompting compatibility.

## Start here

- Read `specs/000-index.md` and `specs/004-change-process.md`.
- Review taxonomy/workflow in `specs/003-taxonomy-and-workflow.md`.

## High-signal rules

- Treat skill names as API: don’t rename skill folders or `name:` values without a shim/migration (`specs/002-skill-contract.md`).
- For non-trivial changes, update the relevant spec and usually add an ADR in `specs/decisions/`.
- Keep `SKILL.md` lean; put depth in `references/` (progressive disclosure).
- Prefer cross-links between skills over duplicating content.

## Verification

- Validate changed skills: `python3 .system/skill-creator/scripts/quick_validate.py <skill-folder>`
- Keep `README.md` and `PROMPTS.md` aligned with the workflow-stage grouping (Define/Standardize/Harden/Verify/Mechanics).

