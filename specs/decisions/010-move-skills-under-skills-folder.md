# Decision 010: Move Skill Folders Under `skills/`

**Date**: 2026-02-04  
**Status**: Accepted

## Context

We want the repo to be easier to share and install (clone anywhere, then symlink/copy skills into a tool’s skills directory).

Keeping skill folders at the repo root makes the repository double as an “installed skills directory”, but it also:

- mixes library docs/specs with installable skill content
- makes it harder to share simple install instructions that point at a single `skills/` folder
- encourages accidental coupling between “repo layout” and “assistant runtime layout”

## Decision

Move all skill folders into a dedicated `skills/` directory:

- `skills/<skill-name>/SKILL.md`

Repo-level documentation and specs remain at the repo root (`README.md`, `PROMPTS.md`, `specs/`, etc.).

This is a breaking change for any consumer that assumes skill folders live at the repo root.

## Consequences

- **Positive**: Cleaner repo layout; simpler install guidance (symlink/copy from `skills/*`).
- **Positive**: Reduces drift risk between docs/specs and skills.
- **Trade-off**: The repo can no longer be used directly as a skills directory without symlinking/copying `skills/*` into the assistant’s skill directory.

