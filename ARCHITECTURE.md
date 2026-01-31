# Architecture

This repo is a small library of **agent skills**: self-contained playbooks stored in `*/SKILL.md` files.
It’s designed around **progressive disclosure**: load only the skill(s) needed for the current task.

## Repository layout

- `*/SKILL.md`: Skill entrypoint (workflow + checklists + minimal examples). Required YAML frontmatter:
  - `name`: must match the directory name
  - `description`: 1–2 sentence summary
- `*/references/`: Optional deeper guidance and copy/pasteable snippets. Keep `SKILL.md` short.
- `scripts/`: Tooling to install/validate skills and generate project instruction files.
- `skills-config.json`: Skill ordering and lightweight detectors used by tooling.
- `.github/workflows/`: CI checks (structure validation + theme coherence review).

## How skills get used (progressive disclosure)

There are two “layers”:

1. **Index/rules layer**: a small instruction file in the project being edited that tells the agent how to pick skills and where to find them.
2. **Skill layer**: the selected `*/SKILL.md` (and only the relevant `references/` files when needed).

This keeps the default context small while still making deeper guidance available on demand.

## Tooling

### `scripts/validate-skills.sh`

Validates repo invariants:

- every skill directory has `SKILL.md` with required frontmatter
- `README.md` mentions every skill directory
- `skills-config.json` stays consistent with the repo
- scripts smoke tests (basic “runs + outputs exist” checks)

### `scripts/generate-project-rules.py`

Generates tool-specific “project rules” files that point at the skills in this repo:

- `.codex/AGENTS.md`
- `.claude/AGENTS.md`
- `.cursorrules`
- `.github/copilot-instructions.md`

The generated files:

- instruct the agent not to load everything at once
- provide a quick picker + a full skill index
- include a repo version stamp (git short SHA when available)

### `scripts/recommend-skills.py`

Given a project directory + a prompt, recommends a small ordered set of skills using:

- `skills-config.json` `projectDetectors` (repo markers/deps)
- `skills-config.json` `promptDetectors` (keywords)

It’s intentionally simple and deterministic.

## Design constraints

- Skills should be useful across repos and teams: prefer timeless principles over “my stack only” advice.
- Keep diffs reviewable: when adding guidance, avoid sprawling rewrites.
- Preserve cross-skill consistency via `.github/theme-coherence.theme.md`.

