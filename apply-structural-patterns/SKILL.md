---
name: apply-structural-patterns
description: Apply structural GoF design patterns (Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy). Use when you need to wrap/compose objects, translate interfaces, split abstraction from implementation, simplify a subsystem, share memory, or add indirection (caching, access control, lazy loading).
---

# Apply Structural Patterns

## Overview

Shape object relationships to reduce coupling without rewriting everything. Use structural patterns to compose behavior, hide complexity, and add indirection at boundaries.

## Workflow

1. Identify the boundary: what do callers want to depend on, and what do you want to hide?
2. Decide if you’re changing:
   - **interface** (Adapter)
   - **abstraction vs implementation axes** (Bridge)
   - **object graph shape** (Composite)
   - **optional behavior stacking** (Decorator)
   - **subsystem surface area** (Facade)
   - **memory footprint** (Flyweight)
   - **access policy/indirection** (Proxy)
3. Keep the public surface small: one interface + a few implementations/wrappers.
4. Add tests around the boundary (callers see stable behavior even as internals change).

## Chooser

- **Adapter**: make incompatible APIs work together (often at third-party/legacy boundaries).
- **Bridge**: two axes vary independently (e.g., “shape” x “renderer”, “transport” x “codec”).
- **Composite**: treat leaf and container uniformly; tree recursion + operations over nodes.
- **Decorator**: add optional responsibilities without subclass explosion; wrappers are stackable.
- **Facade**: shrink a subsystem to a simple, stable API; hide orchestration.
- **Flyweight**: many similar objects; split intrinsic state (shared) vs extrinsic (supplied).
- **Proxy**: control access (lazy init, cache, auth, throttling, remote boundary, logging).

## Implementation Checklist

- Prefer composition; wrappers should delegate almost everything and add one focused concern.
- Make wrappers transparent where appropriate (don’t leak internals via type checks).
- Put facades and adapters at module boundaries; keep core domain clean.
- For proxies: define clear caching/invalidations, error propagation, and concurrency semantics.
- For flyweights: prove the memory win and define ownership/lifetime of shared state.

## References

Read the relevant reference file before implementing or refactoring toward the pattern:

- `references/adapter.md`
- `references/bridge.md`
- `references/composite.md`
- `references/decorator.md`
- `references/facade.md`
- `references/flyweight.md`
- `references/proxy.md`

Each reference includes: selection cues, minimal structure, pitfalls, and test ideas.
