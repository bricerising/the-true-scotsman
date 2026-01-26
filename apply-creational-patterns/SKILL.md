---
name: apply-creational-patterns
description: Apply creational GoF design patterns (Factory Method, Abstract Factory, Builder, Prototype, Singleton). Use when object construction is complex, varies by type/environment, must be decoupled from callers, needs consistent lifecycle, or you’re refactoring creation logic for testability.
---

# Apply Creational Patterns

## Overview

Create objects without hard-coding concrete classes into callers. Use these patterns to isolate construction, support multiple variants, and keep object creation testable.

## Workflow

1. Identify the creation pressure: variant explosion, complex setup, environment wiring, or lifecycle constraints.
2. Decide what must be stable for callers (interface and invariants), and what may vary (implementation, configuration, dependencies).
3. Pick the smallest creational pattern that matches the pressure (see chooser).
4. Implement with DI-friendly constructors; keep factories pure where possible.
5. Add tests that assert:
   - correct type selection for each variant
   - invariants validated during creation
   - callers depend only on interfaces/abstractions

## Chooser

- **Factory Method**: subclasses/modules decide which product to create for a common interface.
- **Abstract Factory**: select a “family” (e.g., platform/vendor) and create compatible products together.
- **Builder**: stepwise construction with validation; many optional parts or multiple representations.
- **Prototype**: clone existing instances to avoid complex constructors; preserve runtime types.
- **Singleton** (caution): one instance truly required; prefer passing dependencies explicitly or container-managed singletons.

## Implementation Checklist

- Make factories return interfaces/abstract types; hide concrete constructors in one place.
- Keep variant selection logic near configuration boundaries (composition root).
- Avoid “stringly-typed factories”; use enums/ADTs/typed keys where possible.
- Validate invariants at creation time; fail fast with actionable errors.
- Keep object graphs shallow in tests by injecting fakes/mocks (avoid global state).

## References

Read the relevant reference file before implementing or refactoring toward the pattern:

- `references/factory-method.md`
- `references/abstract-factory.md`
- `references/builder.md`
- `references/prototype.md`
- `references/singleton.md`

Each reference includes: selection cues, minimal structure, pitfalls, and test ideas.
