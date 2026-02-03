# Spec 003: Taxonomy and Default Workflow

## Overview

Skills are grouped by **how agents execute work** (workflow stage), not by whether a pattern is “code” vs “system”.

This reduces decision friction: an agent can follow a reliable loop without debating taxonomy.

## Workflow-Stage Taxonomy

### Define (what are we building?)

Intent and boundaries:

- Auto-routing across this library in conversational mode (`enterprise-web-app-workflow`)
- Specs and contracts (`spec-driven-development`)
- System-pattern selection for cross-service pressures (`select-architecture-pattern`)
- Code-pattern selection for in-process pressures (`select-design-pattern`)

### Standardize (make it consistent)

Make the “golden path” boring and reusable:

- Shared platform primitives (`shared-platform-library`)
- Language conventions for safety and maintainability (`typescript-style-guide`)

### Harden (make it survive reality)

Make partial failure and production debugging predictable:

- Timeouts, retries, idempotency, breakers, bulkheads (`apply-resilience-patterns`)
- Practical security guardrails (authn/authz, input validation, injection safety, secrets, SSRF) (`apply-security-patterns`)
- Logs/metrics/traces correlation + verification steps (`apply-observability-patterns`)
- Debug loop (log → trace → metrics) triage workflows (`observability-triage`)

### Verify (prove behavior)

Pin behavior at the boundary:

- Consumer-centric tests and characterization (`consumer-test-coverage`)
- Adversarial code review debate for provable findings (`review-protocol`)

### Mechanics (in-process building blocks)

Apply classic in-process patterns when implementation needs structure:

- Creation (`apply-creational-patterns`)
- Wrapping/indirection (`apply-structural-patterns`)
- Pipelines/eventing/state machines (`apply-behavioral-patterns`)

## Terminology (Scope Words, Not Navigation)

- **Code patterns**: in-process patterns (classic GoF + adjacent).
- **System patterns**: cross-process patterns (architecture/distributed-systems).
- **Operational patterns**: repeatable workflows/policies that make delivery + operations predictable.

These terms describe *scope*, but the repo groups skills by *workflow stage*.

## Default Sequence (Enterprise Web Apps)

Unless you have a strong reason to deviate:

1. `spec-driven-development`
2. `select-architecture-pattern` (if cross-service/system pressure exists)
3. `shared-platform-library` (if multiple services need the same boundary behavior)
4. `typescript-style-guide` (or the relevant language style guide)
5. `apply-resilience-patterns`
6. `apply-security-patterns`
7. `apply-observability-patterns`
8. `consumer-test-coverage`

In-process pattern application (`apply-*-patterns`) is usually a supporting step during implementation, not the starting point.

## Acceptance

This taxonomy is applied when:

- `README.md` and `PROMPTS.md` list skills under Define/Standardize/Harden/Verify/Mechanics.
- Prompt recipes use the default sequence for enterprise web apps.
- New skills are assigned a workflow stage and documented accordingly.
