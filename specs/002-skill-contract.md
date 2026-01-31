# Spec 002: Skill Contract

## Overview

In this repo, a **skill** is a small, explicit playbook that can be invoked by name and applied procedurally.

Skill names and folder layout are treated as an API: prompts depend on them.

## Folder Contract

Each skill lives at:

```
<skill-name>/
  SKILL.md
  references/   (optional)
  scripts/      (optional)
  assets/       (optional)
```

Skill folders SHOULD NOT include extra docs like `README.md`, changelogs, or long essays. Keep `SKILL.md` lean; put depth in `references/`.

## `SKILL.md` Frontmatter Contract

`SKILL.md` MUST start with YAML frontmatter containing:

- `name`: MUST match the folder name.
- `description`: MUST be specific about when to use the skill (trigger precision matters).

## `SKILL.md` Body Contract (Minimum Shape)

Each skill SHOULD contain:

- **Overview**: what problem it solves and what success looks like.
- **Workflow**: a short numbered procedure that can be followed.
- **Guardrails**: what not to do / common pitfalls.
- **References**: pointers to `references/` files (progressive disclosure).
- **Output template**: what the agent should return (plan + verification + summary).

## Progressive Disclosure Rules

- `SKILL.md` SHOULD be under ~500 lines; move depth to `references/`.
- Avoid deep reference chains (keep references one level deep from `SKILL.md`).
- Prefer reusable templates/checklists over prose.

## Compatibility Rules (Skill Names Are API)

- Avoid renaming skill folders or `name:` values.
- If a rename is required, create a **shim skill** under the old name that clearly redirects to the new name and explains why.

## Validation + Packaging

- Skills MUST pass validation:
  - `python3 .system/skill-creator/scripts/quick_validate.py <skill-folder>`
- Skills MAY be packaged into `.skill` files for distribution:
  - `python3 .system/skill-creator/scripts/package_skill.py <skill-folder> ./dist`
- `dist/` is intentionally not committed; treat packaged artifacts as build output.

## Acceptance

This contract is satisfied when:

- Every skill folder matches the folder/frontmatter contract.
- Validation passes for every skill in the repo.
- Significant behavior changes come with spec updates under `specs/` and a migration story if skill APIs change.
