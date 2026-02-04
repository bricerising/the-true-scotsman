# Decision 004: Add Triage + Boundary Wrapper Guidance + System Decision Tree

**Date**: 2026-02-01
**Status**: Accepted

## Context

This repo focuses on day-1 behaviors (specs, implementation patterns, tests, instrumentation), but teams also need day-2 operational help:

- A consistent **debug loop** for incidents and regressions (log → trace → metrics).
- A repeatable way to build shared “golden path” **boundary wrappers** (HTTP/gRPC/jobs/consumers) that standardize error semantics, time budgets, retries/idempotency, and telemetry.
- More procedural guidance for selecting **system patterns** (pressure → candidate patterns → risks), with explicit anti-pattern guardrails.

These capabilities are already captured as backlog tasks (T003/T004/T005) and fit the existing workflow-stage taxonomy.

## Decision

Implement three additions:

1. Add a new skill `debug/` focused on triage workflows (not instrumentation).
2. Extend `platform/` with explicit guidance + templates for boundary wrappers, keeping depth in `references/`.
3. Extend `architecture/` with a compact decision tree in `references/`, including common anti-pattern guardrails.

## Consequences

- Positive: Improves operational usefulness (day-2), reduces “what do I do next?” friction, and makes recommendations more procedural and auditable.
- Trade-off: Slightly more surface area to maintain; mitigated by keeping deep detail in `references/`.
- Compatibility: Additive only (new skill + references); no renames or breaking prompt contracts.
