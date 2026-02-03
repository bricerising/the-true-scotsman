# Decision 008: Additional LangChain CLIs (Ideation, Progress, Spec Alignment)

**Date**: 2026-02-03  
**Status**: Accepted

## Context

We already have a LangChain-based CLI under `tools/langchain_clis/` for running `review-protocol` end-to-end from a git diff.

We also want repeatable, format-enforced workflows for:

- ideating next feature work in a way that stays spec-aware
- communicating progress on a feature (from evidence in diffs)
- judging whether implementation changes align with a project’s `specs/` folder

These workflows should reuse **enterprise-software-playbook** skill prompts as bounded “hints”, and produce shareable artifacts in `.codex/` in the target repo.

## Decision

Extend `tools/langchain_clis/` with three additional console commands:

- `feature-ideate`: generates `1-ideas.md` under `.codex/feature-ideation/<HEAD_SHA>/`
- `feature-progress`: generates `1-update.md` under `.codex/feature-progress/<HEAD_SHA>/`
- `spec-align`: generates `1-alignment.md` under `.codex/spec-alignment/<HEAD_SHA>/`

Each command:

- builds a bounded context (diff + optional line-numbered excerpts; plus optional `specs/` excerpts)
- treats all repo text as untrusted (prompt injection guardrail)
- enforces an output contract with lightweight validation + retries

## Consequences

- Positive: makes “idea → work → comms → spec alignment” loops more repeatable and comparable across runs.
- Trade-off: adds more surface area to maintain inside the Python tool package.
- Compatibility: keeps the existing `code-review` command and folder layout intact; the new commands are additive.
