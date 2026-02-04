---
name: plan
description: Turn a request into an executable implementation plan (scoped tasks + verification). Use for non-trivial, risky, cross-service, or ambiguous work before starting large edits.
---

# Plan

## Overview

Create a short plan that a developer (or agent) can execute end-to-end: ordered tasks, acceptance checks, and a concrete verification strategy.

## Workflow

1. Restate the goal and “done when” criteria (1–3 bullets).
2. Scope the change:
   - impacted components/services
   - impacted boundaries/contracts (HTTP/gRPC/events/WS/data model)
   - what is explicitly *out of scope*
3. Identify the primary risk(s) (pick 1–3): correctness, migration, partial failure, security/privacy, performance, operability.
4. Choose the minimum up-front artifacts:
   - if boundary semantics/contracts change → use `spec`
   - if cross-service/system pressure exists → use `architecture`
   - if in-process structure pressure exists → use `design`
   - if repeated boundary logic is likely → use `platform`
5. Produce an ordered task list:
   - tasks should be small, reversible, and verifiable
   - include “stop points” where you can re-check assumptions
6. Define verification:
   - exact commands (tests/lint/typecheck/build) if known
   - if unknown, list what you will run and ask once for preferred commands

## Guardrails

- Keep the plan short (usually 5–12 tasks). Avoid “spec theater” for tiny changes.
- Every task needs an observable acceptance check (test, command output, file diff, or demo step).
- Call out unknowns early; don’t pretend certainty.
- If you propose retries, also propose idempotency/dedupe and time budgets (`resilience`).

## Output Template

Return:

- **Goal**: 1–2 sentences.
- **Scope**: in/out.
- **Risks/assumptions**: 3–6 bullets.
- **Plan**: ordered checklist with acceptance per task.
- **Verification**: commands to run + what “good” looks like.
- **Open questions**: only if blocking.

