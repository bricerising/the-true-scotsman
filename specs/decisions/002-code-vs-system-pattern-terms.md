# Decision 002: Use “Code Patterns” vs “System Patterns”

**Date**: 2026-01-31
**Status**: Accepted

## Context

The repo initially used “GoF” frequently. While accurate historically, it is too narrow for an opinionated enterprise-app system that also covers cross-service patterns and operational workflows.

We want terminology that:

- scales beyond classic GoF patterns
- cleanly separates in-process vs cross-process pressures
- remains short and prompt-friendly

## Decision

Use:

- **Code patterns** for in-process patterns (classic creational/structural/behavioral; mostly GoF)
- **System patterns** for cross-process patterns (architecture/distributed systems/ops)

## Consequences

- Skills can evolve beyond GoF without renaming whole categories.
- Skill descriptions and prompt recipes become more consistent.
- “GoF” can still be referenced for historical clarity, but it is no longer the primary label.
