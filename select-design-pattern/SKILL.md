---
name: select-design-pattern
description: Choose an appropriate GoF design pattern (creational/structural/behavioral) from a problem statement. Use when the user asks which pattern to use, compares patterns, or you need a quick decision workflow to refactor for extensibility, decoupling, composability, or testability.
---

# Select Design Pattern

## Overview

Pick the simplest design that fits, then map it to a GoF pattern only if it buys you clear leverage (change isolation, testability, reuse, or performance).

## Workflow

1. Restate the problem as: **what varies** and **what must stay stable** (API, data model, timing, performance).
2. Identify the main pressure:
   - **Creation** pressure: hard-to-test construction, many variants, environment-specific families.
   - **Structure** pressure: wrapping/combining objects, incompatible interfaces, indirection, memory sharing.
   - **Behavior** pressure: pluggable algorithms, eventing, pipelines, undo, state-dependent behavior.
3. Pick 1 primary pattern (avoid “pattern soup”). Add a 2nd only if it addresses a different pressure.
4. Validate with 2 examples: a “happy path” and a likely future change.
5. Confirm the choice reduces coupling and increases testability (or has a clear perf win).

## Clarifying Questions

- What is the stable API/contract we must preserve?
- What changes most often: **implementations**, **algorithms**, **steps**, **object graphs**, **external systems**?
- Do we need runtime selection, configuration-based selection, or compile-time wiring?
- Do we need undo/redo, queuing, retries, caching, auth, logging, or other cross-cutting concerns?
- Are there many similar objects (memory pressure) or many collaborators (dependency explosion)?

## Pattern Chooser (Cheat Sheet)

### Creational

- **Factory Method**: callers want an interface; subclasses/modules choose which concrete product to create.
- **Abstract Factory**: pick an “environment” (e.g., OS/vendor) and create a *compatible family* of products.
- **Builder**: object has many optional parts or multiple representations; construction must be stepwise/validated.
- **Prototype**: cloning is cheaper/cleaner than constructing; you must preserve runtime types without `new` logic.
- **Singleton** (use sparingly): exactly one instance is required; prefer DI/container-managed lifetimes instead.

### Structural

- **Adapter**: translate one interface to another to integrate a legacy/third-party API.
- **Bridge**: split abstraction from implementation so each can vary independently (two axes of change).
- **Composite**: treat individual objects and object trees uniformly.
- **Decorator**: add optional behavior by wrapping (stackable features).
- **Facade**: hide a complex subsystem behind a small, stable API.
- **Flyweight**: lots of similar objects; separate intrinsic vs extrinsic state to reduce memory.
- **Proxy**: stand-in that controls access (lazy load, cache, auth, remote boundary, rate limit).

### Behavioral

- **Chain of Responsibility**: request flows through a configurable pipeline of handlers.
- **Command**: represent an action/request as an object (queue, schedule, undo).
- **Iterator**: traverse a structure without exposing representation; support multiple traversal strategies.
- **Mediator**: reduce many-to-many coupling; centralize coordination rules.
- **Memento**: snapshot/restore state (undo/redo) without exposing internals.
- **Observer**: publish/subscribe updates; multiple listeners react to events.
- **State**: behavior changes as state changes; states own transitions/behaviors.
- **Strategy**: swap algorithms behind a stable interface; choose at runtime/config.
- **Template Method**: stable algorithm skeleton with overridable steps (inheritance-based).
- **Visitor**: add new operations over a stable object structure without changing the element classes.

## Common Confusions

- **Decorator vs Proxy vs Adapter vs Facade**:
  - Decorator adds behavior; Proxy controls access; Adapter converts interface; Facade simplifies a subsystem.
- **Strategy vs State vs Template Method**:
  - Strategy chooses an algorithm; State changes behavior based on internal state; Template Method fixes skeleton + overrides steps.
- **Factory Method vs Abstract Factory vs Builder**:
  - Factory Method picks a product; Abstract Factory picks a compatible family; Builder controls stepwise construction.

## Guardrails

- Prefer simpler refactors first: extract functions, introduce interfaces, compose objects, use DI.
- Avoid patterns that force inheritance when composition would do (especially Template Method/Singleton).
- Keep “pattern seams” small: a tiny interface plus focused implementations.
- If the change axis is unclear, prototype with a simple interface + two implementations before formalizing.

## Output Template

When recommending a pattern, return:

- 1–2 sentences: pattern + why it fits this problem (what changes, what stays stable).
- Trade-offs and 1 alternative (“no pattern” option included).
- A minimal implementation plan (roles/interfaces, wiring point, tests).
- If implementing: small skeleton + one example call site.
