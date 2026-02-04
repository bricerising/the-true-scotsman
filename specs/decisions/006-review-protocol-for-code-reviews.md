# Decision 006: Review Protocol for Code Reviews

**Date**: 2026-02-03
**Status**: Accepted

## Context

The repo includes a `review` skill, but it was missing “default code review” guidance and wasn’t listed alongside other skills in the workflow-stage navigation (`README.md`, `PROMPTS.md`, Spec 003).

For real code reviews (especially PR/diff reviews), reviewers also need:

- A “general” mode (not a single-axis audit like security-only)
- A way to make findings easy to locate even when line numbers drift (e.g., rebases)
- Clearer severity calibration so non-security findings aren’t over/under-weighted

## Decision

- Treat `review` as a code review skill and list it under **Verify** in `README.md`, `PROMPTS.md`, and Spec 003.
- Add `general` and `correctness` review types.
- Recommend an “Anchor” field (symbol/snippet) alongside file+line evidence to keep findings locatable across diffs.
- Add brief severity calibration guidance tuned for code review usage.
- Cross-link review types to existing skills for deeper checklists (avoid duplicating guidance).

## Consequences

- Easier discovery and consistent taxonomy/navigation across repo docs.
- More useful defaults for everyday PR reviews (`general`) while preserving focused audits.
- Slight format expansion (recommended `Anchor` line) that reviewers should enforce consistently if they choose to use it.
