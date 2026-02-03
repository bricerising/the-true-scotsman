# PROMPTS (Prompt Recipes)

Copy/paste prompts for using **enterprise-software-playbook** with an AI coding assistant.

If your assistant supports “skills”, name them explicitly (e.g., `enterprise-web-app-workflow`). If not, point it at the referenced `SKILL.md` files.

## Conversational bootstrap (auto-route)

Use this to start most sessions:

```text
Use enterprise-web-app-workflow (read enterprise-web-app-workflow/SKILL.md).

Follow the default loop: Define → Standardize → Harden → Verify → Mechanics.
Keep overhead proportional (tiny changes stay lightweight).

If you change a boundary contract/semantics (HTTP/gRPC/events/WS), update specs/contracts first and pin behavior with tests.

When you finish, report: skills applied, what changed, verification, follow-ups.

Task: <describe what you want>
```

## Define (what are we building?)

### Write/update a spec bundle

```text
Use spec-driven-development.

Goal: <feature/bug/refactor intent>

Before implementing, write or update the relevant spec bundle:
- System-level: specs/*.md and/or specs/decisions/*.md (if cross-service or significant)
- Service-level: apps/<service>/spec/ (spec.md, contracts/, plan.md, tasks.md, quickstart.md)

Include: acceptance scenarios, edge cases, failure-mode expectations, and a verification plan.
```

### Choose a system/architecture pattern

```text
Use select-architecture-pattern.

Context: <system pressure(s): partial failures, consistency, cross-service workflows, integration seams>
Constraints: <latency/SLOs, scalability, team boundaries, compliance>

Recommend the smallest viable pattern(s), risks/anti-patterns, and a validation plan.
```

### Choose an in-process/design pattern

```text
Use select-design-pattern.

Context: <construction/structure/behavior pressure>
Constraints: <testability, extensibility, performance, simplicity>

Recommend the smallest viable pattern and show how it fits this codebase.
```

## Standardize (make it consistent)

### Extract a shared “golden path” primitive

```text
Use shared-platform-library.

Problem: We have repeated boundary logic across services (timeouts/retries/error mapping/telemetry fields/etc.).
Goal: Propose a small shared primitive (two-consumer rule) that removes copy/paste drift.

Include: API shape, error envelope, time budget policy, telemetry field contract, and adoption steps.
```

### TypeScript safety/refactor pass

```text
Use typescript-style-guide.

Goal: Improve maintainability and runtime safety without changing behavior.
Focus: typed boundaries, explicit lifetimes, safe module structure, and predictable error handling.
```

## Harden (make it survive reality)

### Resilience hardening for I/O boundaries

```text
Use apply-resilience-patterns.

Boundary: <HTTP/gRPC/DB/cache/queue/external API>
Risk: <timeouts, retries, at-least-once delivery, partial failure>

Add explicit time budgets + cancellation propagation. Only add retries when safe and idempotent.
```

### Security hardening for boundaries

```text
Use apply-security-patterns.

Boundary: <HTTP/gRPC/WS/events/outbound HTTP/DB/etc>
Risk: <authn/authz, injection, SSRF, secrets/PII, multi-tenant isolation>

Add authn/authz checks, strict input validation, safe logging/telemetry, and SSRF/injection guardrails where applicable.
```

### Observability instrumentation + verification

```text
Use apply-observability-patterns.

Boundary: <HTTP/gRPC/events/jobs>
Goal: Add correlated logs/traces/metrics and local verification steps (log → trace → metrics).

Define a stable telemetry field contract (IDs, names) and avoid high-cardinality metrics labels.
```

### Triage an incident / regression (log → trace → metrics)

```text
Use observability-triage.

Symptom: <what is broken/slow?>
Environment: <local/dev/staging/prod>
Time window: <start/end>
Exemplar: <traceId/requestId/log line timestamp/etc>

Guide a systematic investigation and end with: evidence, hypothesis, mitigation, and a fix/follow-up plan.
```

## Verify (prove behavior)

### Add consumer-centric tests

```text
Use consumer-test-coverage.

Goal: Pin consumer-visible behavior for <feature/bug/refactor>.
Approach: characterization tests before refactors; avoid asserting implementation details.
```

### Run an adversarial code review debate

```text
Use review-protocol (read review-protocol/SKILL.md).

Review type: general
Scope: <PR link / diff / commit range / file list>
Output dir: <where to write 1-critique.txt ... 4-verdict.txt>

Run the 4-phase protocol and finish with the skill’s output template.
```

## Mechanics (in-process building blocks)

### Apply a concrete GoF pattern

```text
Use apply-<creational|structural|behavioral>-patterns.

Problem: <what needs structure?>
Goal: Introduce a pattern seam that improves readability/testability without over-engineering.
```
