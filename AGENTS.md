# Agent Instructions (the-true-scotsman)

This repo is itself an opinionated system for writing agent skills. To prevent drift, follow the repo specs.

## Start Here

- Read `specs/000-index.md` (index) and `specs/004-change-process.md` (how to make changes).
- Taxonomy and default workflow live in `specs/003-taxonomy-and-workflow.md`.

## Change Rules (High Signal)

- Treat skill names as API: avoid renaming skill folders or `name:` values without a migration/shim (`specs/002-skill-contract.md`).
- For non-trivial changes, add/update a decision record in `specs/decisions/`.
- Keep skills concise; put depth in `references/` (progressive disclosure).
- Prefer cross-links between skills over duplicating content.

## Verification

- Validate changed skills: `python3 .system/skill-creator/scripts/quick_validate.py <skill-folder>`
- Keep `README.md` and `PROMPTS.md` aligned with the workflow-stage grouping (Define/Standardize/Harden/Verify/Mechanics).

## Packaging (Optional)

- Package skills to `dist/` (build output): `python3 .system/skill-creator/scripts/package_skill.py <skill-folder> ./dist`
