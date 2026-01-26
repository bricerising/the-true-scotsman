---
name: apply-behavioral-patterns
description: Apply behavioral GoF design patterns (Chain of Responsibility, Command, Iterator, Mediator, Memento, Observer, State, Strategy, Template Method, Visitor). Use when you need pluggable algorithms, event-driven updates, request pipelines, undo/redo, decoupled collaboration, state-dependent behavior, or stable iteration over collections.
---

# Apply Behavioral Patterns

## Overview

Manage algorithms and collaboration without turning your code into nested conditionals and tight coupling. Behavioral patterns help you route requests, encapsulate actions, and swap behavior safely.

## Workflow

1. Identify the interaction pressure: pipelines, events, undo, state machines, or algorithm selection.
2. Draw a quick responsibility map: who triggers actions, who owns state, who receives outcomes?
3. Pick a pattern that makes responsibilities explicit (interfaces + concrete behaviors).
4. Implement with clear contracts and tests for ordering, error handling, and invariants.

## Chooser

- **Chain of Responsibility**: configurable pipeline; each handler may handle or pass along.
- **Command**: represent actions as objects; queue/schedule/undo/retry.
- **Iterator**: traverse collections/graphs without exposing representation.
- **Mediator**: central coordinator to reduce many-to-many coupling.
- **Memento**: snapshot/restore object state; undo/redo without leaking internals.
- **Observer**: pub/sub updates; multiple listeners react to events.
- **State**: state machine; behavior varies by state; transitions are explicit.
- **Strategy**: swap algorithms behind a stable interface (runtime/config selection).
- **Template Method**: inheritance-based algorithm skeleton; override steps.
- **Visitor**: add new operations across a stable object structure without changing element classes.

## Implementation Checklist

- Make ordering explicit for pipelines and observers; define error propagation/retry rules.
- Keep strategies/states small and pure when possible; inject dependencies via context.
- Prefer composition for Strategy/State; reserve Template Method for cases where inheritance is already a fit.
- For Command/Memento: define serialization and persistence needs early (in-memory vs durable).

## Snippets (optional)

- TypeScript: `references/snippets/typescript.md`
- React: `references/snippets/react.md`

## References

Read the relevant reference file before implementing or refactoring toward the pattern:

- `references/chain-of-responsibility.md`
- `references/command.md`
- `references/iterator.md`
- `references/mediator.md`
- `references/memento.md`
- `references/observer.md`
- `references/state.md`
- `references/strategy.md`
- `references/template-method.md`
- `references/visitor.md`

Each reference includes: selection cues, minimal structure, pitfalls, and test ideas.
