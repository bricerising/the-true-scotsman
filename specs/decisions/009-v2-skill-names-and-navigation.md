# Decision 009: V2 Skill Names and Command-Oriented Navigation

**Date**: 2026-02-04  
**Status**: Accepted

## Context

This repo is early, has few users, and we want to optimize for:

- lower prompting friction (shorter, more memorable names)
- a more “command-like” workflow (bootstrap → plan/spec → implement → verify → finish)
- less taxonomy noise in names (e.g., `apply-*`, `select-*`)
- fewer places where docs drift (README/PROMPTS/templates all referencing legacy names)

The existing skill set is solid, but many names encode *implementation intent* (“apply/select”) rather than *user intent* (“review/debug/test”), and the prefixes create unnecessary cognitive overhead.

## Decision

### 1) Rename skills to short, intent-based names (breaking change)

We will rename skill folders and `SKILL.md` `name:` values to a simpler, command-like naming scheme.

This is a **breaking change** and we will **not** provide shim skills.

### 2) Add two workflow “glue” skills

- Add `plan`: produce an executable plan (tasks + verification) before large changes.
- Add `finish`: a “definition of done” checklist and reporting format for shipping-quality output.

### 3) Keep the workflow-stage taxonomy

The navigation and default loop remains:

**Define → Standardize → Harden → Verify → Mechanics**

Skill names are simplified; the workflow staging remains the primary organization.

## Migration (Rename Map)

| Old skill | New skill |
| --- | --- |
| `enterprise-web-app-workflow` | `workflow` |
| `spec-driven-development` | `spec` |
| `select-architecture-pattern` | `architecture` |
| `select-design-pattern` | `design` |
| `shared-platform-library` | `platform` |
| `typescript-style-guide` | `typescript` |
| `apply-resilience-patterns` | `resilience` |
| `apply-security-patterns` | `security` |
| `apply-observability-patterns` | `observability` |
| `observability-triage` | `debug` |
| `consumer-test-coverage` | `testing` |
| `review-protocol` | `review` |
| `apply-creational-patterns` | `patterns-creational` |
| `apply-structural-patterns` | `patterns-structural` |
| `apply-behavioral-patterns` | `patterns-behavioral` |

New skills:

- `plan`
- `finish`

## Consequences

- **Positive**: Prompts become shorter and more memorable; skills read more like “commands”.
- **Positive**: Improves default workflow cohesion via explicit `plan` and `finish` steps.
- **Trade-off**: This breaks any external prompts and app-repo instructions referencing old skill names.
- **Mitigation**: Update `specs/`, `README.md`, `PROMPTS.md`, and templates in the same change; include the rename map in this decision record.
