# Decision 007: LangChain CLI for Review Protocol Orchestration

**Date**: 2026-02-03
**Status**: Accepted

## Context

We want a repeatable, **multi-stage, multi-agent** code review workflow that can be executed outside a specific assistant runtime.

This repo already contains the `review-protocol` skill (critique → defense → rebuttal → verdict) and related deep-checklist skills (security/resilience/testing/etc), but running the workflow reliably is still manual.

## Decision

Add a small, self-contained **LangChain-based CLI** under `tools/langchain_clis/` that:

- Loads the `review-protocol` contract/prompt templates from the skill library.
- Uses additional skills as bounded “deep checklist” hints for specialist attacker passes.
- Enforces the protocol format contract by validating and retrying phases.
- Writes protocol artifacts into `.codex/review-protocol/<HEAD_SHA>/<REVIEW_TYPE>/` in the target repo.

This is implemented as a tool (not a new skill folder) to avoid expanding the skill taxonomy and to keep the skill library itself prompt-first.

## Consequences

- Positive: makes the review protocol easier to run consistently and produces comparable artifacts across runs.
- Trade-off: introduces a small Python packaging surface (dependencies, versioning) inside the repo.
- Compatibility: no changes to existing skill names or prompting compatibility; the tool reads skill content without requiring renames/migrations.
