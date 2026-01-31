# Tasks (Skill Library Backlog)

This is the repo’s backlog of work to improve agent effectiveness.

Keep tasks small, orderable, and testable. Prefer “acceptance” that is observable (commands, file outputs, prompt success criteria).

## T001: Add `specs/` system spec bundle

- **Status**: Done (2026-01-31)
- **Acceptance**:
  - `specs/000-index.md` exists and links to the key specs.
  - Specs define taxonomy, skill contract, and change process.
  - `README.md` and `PROMPTS.md` remain aligned with the taxonomy spec.

## T002: Add a “decision record” template to `spec-driven-development`

- **Status**: Done (2026-01-31)
- **Acceptance**:
  - `spec-driven-development` references decision records as a first-class artifact (system-level).
  - A reusable ADR template exists and is referenced from the skill.

## T006: Add conversational auto-skill routing (adoption path)

- **Status**: Done (2026-01-31)
- **Acceptance**:
  - Router skill exists (`enterprise-web-app-workflow`).
  - `PROMPTS.md` includes a conversational bootstrap prompt.
  - An app-repo `AGENTS.md` template exists under `specs/templates/`.
  - `specs/005-application-integration.md` documents adoption.

## T003: Add an “observability triage” skill (debug loop)

- **Acceptance**:
  - New skill focuses on production/local triage workflows (log → trace → metrics), not instrumentation.
  - Includes copy/paste commands/checklists for common enterprise web app stacks (HTTP + gRPC + async consumers).

## T004: Add a “boundary wrapper” shared-primitive guide

- **Acceptance**:
  - Either extend `shared-platform-library` or create a dedicated skill for “golden path” boundary wrappers (HTTP/gRPC/job/consumer).
  - Includes required contracts: error envelope, retry/idempotency policy, telemetry field contract.

## T005: Add a system-pattern decision tree

- **Acceptance**:
  - Extend `select-architecture-pattern` with a compact decision tree (pressure → candidate patterns → risks).
  - Includes anti-pattern guardrails (e.g., saga misuse, event sourcing misuse, retries without idempotency).
