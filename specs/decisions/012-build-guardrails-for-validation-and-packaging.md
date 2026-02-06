# Decision 012: Add Build Guardrails for Validation, Docs Drift, and Packaging

**Date**: 2026-02-06  
**Status**: Accepted

## Context

The repo requires stable skill APIs and aligned docs/specs, but enforcement was incomplete:

- `PROMPTS.md` had contradictory workflow guidance (`finish` sequencing).
- Packaging docs referenced `package_skill.py`, but the script did not exist.
- Validation did not enforce `SKILL.md` `name` matching the skill folder.
- Validation accepted empty required frontmatter fields and did not enforce required section headings.
- CI did not gate on skill validation or README/PROMPTS consistency.

Goal: restore executable build/verification commands and prevent silent drift.

## Options considered

| Option | Optimizes for | Knowingly worsens | Reversibility |
| --- | --- | --- | --- |
| A) Documentation-only fixes | Fastest patch | Drift can reappear silently; no automated gate | High |
| B) Add repo guardrails + CI checks (chosen) | Ongoing consistency and early failure | Slightly more maintenance and CI time | High |
| C) Heavyweight schema/lint framework | Strongest policy enforcement | Added complexity and tooling burden | Medium |

## Decision

Adopt Option B:

1. Restore packaging command compatibility by adding `.system/skill-creator/scripts/package_skill.py`.
2. Strengthen `quick_validate.py` to enforce:
   - non-empty required frontmatter fields (`name`, `description`)
   - `frontmatter.name == folder name`
   - required `SKILL.md` sections (`Workflow`, `Output Template`)
3. Add `.system/skill-creator/scripts/check_repo_consistency.py` for workflow-stage/doc prompt drift checks.
4. Add CI workflow `.github/workflows/skill-validation.yml` to run:
   - all-skill validation
   - repo consistency checks
   - packaging checks for all skill folders
5. Update prompts/spec docs to align with the default workflow (`finish` at end) and publish new validation command in contributor docs.

## Kill criteria / reversal trigger

Revisit if either:

- the consistency checks produce repeated high-noise false failures, or
- packaging format requirements change and `.skill` ZIP output becomes incompatible.

## Measurement + review ritual

- **Leading indicators (early)**: CI failure catches drift before merge; no broken documented commands.
- **Lagging outcomes**: fewer regressions in skill naming/docs alignment and packaging support.
- **Instrumentation source**: GitHub Actions history for `Skill Validation`.
- **Owner + cadence + action trigger**: repo maintainers; review on every failing PR; tighten/adjust checks when two consecutive failures indicate the same false-positive pattern.

## Consequences

- Positive:
  - Documented quickstart/change-process commands are executable again.
  - CI now enforces core repo contracts instead of relying on reviewer memory.
  - Reduced chance of prompt/workflow drift across README/PROMPTS/skills.
- Trade-offs:
  - Additional script surface to maintain.
  - Slightly longer CI runtime.
- Compatibility/migration impact:
  - Additive; no skill renames or taxonomy changes.
