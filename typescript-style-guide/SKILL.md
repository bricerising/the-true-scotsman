---
name: typescript-style-guide
description: Write, review, and refactor TypeScript code for readability, maintainability, and runtime safety. Use when creating or changing TypeScript modules (Node/React/shared libs), doing code reviews, establishing team conventions, modeling domain types, handling errors, validating external inputs, organizing modules/imports, or preventing cyclic dependencies.
---

# TypeScript Style Guide

## Overview

Produce TypeScript that is easy to read, easy to change, and safe at runtime—by treating the codebase as a *system*: explicit boundaries, explicit dependencies, explicit errors, and explicit lifetimes.

Most of the principles here translate to other languages; the TypeScript-specific parts are mainly about how to enforce them with TS tooling and types.

Default objectives:

- **Consistency**: prefer automated formatting and linting (Prettier + ESLint) to eliminate style drift.
- **Readability**: reduce cognitive load with clear naming, shallow control flow, and explicit types.
- **Maintainability**: keep modules cohesive and dependencies/lifetimes explicit so change stays local.

A note on scope: these guidelines are optimized for **systemic** TypeScript (long‑lived apps/services/libraries where ownership, I/O boundaries, and runtime behavior matter). For short‑lived scripts, you can relax some constraints (e.g. more `throw`, fewer abstractions) as long as the blast radius stays small.

Definitions:

- **Scriptic**: short‑lived scripts/one‑offs; optimize for speed and simplicity; `throw` is usually fine.
- **Systemic**: long‑lived apps/services/libraries; optimize for explicit boundaries, typed failures, and explicit lifetimes.

## Workflow (default)

1. Decide “scriptic vs systemic” and set policies (error strategy, boundary validation, ownership/lifetimes).
2. Separate pure logic from side effects (I/O, time, randomness, global state).
3. Identify boundaries (HTTP/DB/fs/env) and treat their inputs as `unknown`.
4. Model the domain with types (discriminated unions) and keep data as plain objects (serializable).
5. Apply the *Throwless Pact*: make known failures explicit in types; reserve `throw` for unknown/unrecoverable; catch and convert at boundaries.
6. Keep dependencies explicit via parameters/factories; centralize wiring in a composition root.
7. Keep the module graph acyclic; enforce a dependency direction; prefer `import type` for type-only imports.
8. Make lifetimes explicit (create/start/stop/dispose); don’t rely on GC or hidden ownership.
9. For long‑running work (pollers, consumers, schedulers), model explicit “agents” with typed inputs/state and explicit shutdown.
10. Test at seams (pure functions, decoders/validators, adapters).
11. At I/O boundaries, make timeouts/retries/idempotency explicit (`apply-resilience-patterns`) and keep telemetry consistent (`apply-observability-patterns`); if 2+ services need the same boundary primitive, extract it (see `shared-platform-library`).

## Guidelines

### Systemic constraints (avoid “complications”)

- **Types are erased at runtime**: validate external data; never “trust” `as X` on JSON/env/network input.
- **`throw` is untyped control flow**: don’t use it for expected failures; keep domain/application code effectively “throwless”.
- **Serialization is not bijective**: JSON/env/DB rows lose information (`Date`, `BigInt`, `undefined`, prototypes); decode/encode explicitly at boundaries.
- **Classes don’t serialize**: JSON round-trips strip prototypes; avoid using classes as data and avoid `JSON.parse(...) as MyClass`.
- **No deterministic destructors**: make cleanup explicit (`dispose()` / `close()`), and enforce it via `try/finally` (or `using` / `await using` where supported) at ownership boundaries.
- **Module initialization hides lifetimes**: avoid top-level side effects; create/start resources in a composition root so you can also stop them.
- **Cyclic dependencies break systems**: enforce an import direction and refactor cycles early.
- **Strings scale easily**: avoid representing large/structured data as long strings unless you’ve measured the cost.

### Naming

- Prefer precise, searchable names; avoid abbreviations and “mental mapping”.
- Avoid redundant context in names; let modules and types provide the scope.
- Use `verbNoun` for functions (`parseUser`, `loadConfig`); use `is/has/can/should` for booleans (`isReady`, `shouldRetry`).
- Use a consistent vocabulary; don’t alternate synonyms (`fetch/get/load`) unless you mean different semantics.
- Avoid vague names like `data`, `value`, `handle`, `handler`; prefer names with domain meaning.
- Avoid prefixing interfaces with `I` (prefer `User`, not `IUser`) and avoid leading/trailing underscores (use access modifiers instead).
- Avoid Hungarian notation and redundant suffixes/prefixes (`FooClass`, `UserInterface`); types and scope already communicate that.
- Avoid single-letter names outside small scopes (trivial lambdas, simple indices).
- Use consistent casing:
  - `camelCase` for values, variables, and functions
  - `PascalCase` for types and exported components
  - `UPPER_SNAKE_CASE` for hard constants
- Prefer stable file/module names; avoid deeply nested folder trees.

### Variables

- Use `const` by default; use `let` only when reassigned; avoid `var`.
- Avoid magic numbers/strings and sentinel values; introduce named constants.
- Keep scopes tight; declare variables close to where they’re used.
- Use explanatory variables for complex conditions instead of repeating deep property access.

### Types and data

- Prefer `unknown` over `any`; narrow with type guards or runtime validators.
- Avoid unchecked assertions (`as X`) for untrusted data (JSON, env, network); decode/validate at the boundary.
- Prefer discriminated unions over boolean flags or “stringly-typed” states.
- For discriminated unions, enforce exhaustiveness (`never` checks) instead of a catch‑all `default` that hides missing variants.
- Keep “data” serializable and prototype-free (plain objects); don’t rely on class instances surviving JSON.
- Keep “wire” shapes (JSON/env/DB rows) separate from domain types; decode/encode explicitly so round-trips don’t silently lose meaning.
- Use the narrowest useful types (`'asc' | 'desc'`, `UserId` brand) to reduce invalid states.
- Default to immutability (`readonly`, `ReadonlyArray`) unless mutation is a measured need.
- For “closed sets”, prefer literal unions or `as const` objects; use `enum` only when you explicitly want a runtime object.
- Prefer `satisfies` to validate object literals without widening inference.
- Prefer built-in utility types (`Pick`, `Omit`, `Partial`, `Required`, `ReturnType`, `Parameters`, `Awaited`) over duplicating shapes by hand.
- Keep advanced types readable: split complex conditional/mapped types into named parts; avoid “type gymnastics” that obscures intent.

### Functions

- Keep functions small (ideally one screen / ~20–30 lines) and do one thing; name them after their single responsibility.
- Minimize parameters; group related parameters into an options object; avoid boolean flags.
- Prefer object parameters + destructuring for “named parameters” at the callsite.
- Prefer default parameters or nullish coalescing (`x ?? default`) over “falsy” fallbacks (`x || default`) when `0`, `''`, or `false` are valid.
- Prefer optional chaining (`?.`) over manual `&&` chains or deep `if` ladders when values may be missing.
- Avoid hidden dependencies (global singletons, module state); pass dependencies in.
- Prefer early returns; keep indentation shallow; extract helpers instead of nesting.
- Avoid side effects in domain logic; isolate them in adapters (DB/HTTP/fs/clock).

### Readability

- Avoid deep nesting (>2–3 levels); prefer guard clauses (`return` / `continue`) and helper functions to flatten.
- Prefer one statement per line; avoid comma operators and “packed” multi-statement lines.
- Use ternaries only for simple expressions; avoid nested ternaries and avoid side effects in ternaries.
- Use blank lines to separate logical phases (setup → core logic → return); avoid excessive blank lines.
- Keep complexity low; if a function has many branches/paths, split it or model cases as a discriminated union.
- Remove obvious duplication (DRY), but don’t over-abstract; optimize for clarity and allow divergence when semantics differ.

### Errors (known vs unknown)

- Treat expected failures as values, not exceptions (*Throwless Pact*):
  - **Known errors**: return a typed `Result<T, E>` / tagged union with stable **signifiers** (e.g. `{ type: 'NotFound'; ... }`).
  - **Unknown errors**: `throw` `Error` and catch at the boundary to log/convert to a known error.
- Avoid “sentinel” error signals (`null`, `false`, `-1`) and avoid using free-form strings as program logic; prefer structured error variants with context fields.
- Never `throw` strings; throw `Error` (or subclasses) and attach context (use `cause` when wrapping).
- Don’t swallow errors; handle, transform, or rethrow with context.
- Log and translate errors at boundaries; avoid logging the same error repeatedly across layers (log once, then propagate as typed failure).
- In `catch`, treat the value as `unknown` and narrow before reading `message/stack`.

Minimal `Result` pattern:

```ts
export type Ok<T> = { ok: true; value: T };
export type Err<E> = { ok: false; error: E };
export type Result<T, E> = Ok<T> | Err<E>;

export const ok = <T>(value: T): Ok<T> => ({ ok: true, value });
export const err = <E>(error: E): Err<E> => ({ ok: false, error });
```

Example known-error union (signified variants):

```ts
export type GetUserError =
  | { type: 'NotFound'; userId: string }
  | { type: 'DbUnavailable' };

export async function getUser(
  userId: string,
): Promise<Result<{ id: string; name: string }, GetUserError>> {
  /* ... */
}
```

### Boundaries and validation

- Treat all external inputs as `unknown` (HTTP, DB rows, env vars, JSON files).
- Validate/parse once at the boundary; after that, internal code should accept well-typed values.
- Keep parsing separate from effects: `decode(input) -> Result<Domain, DecodeError>`, then `apply(domain)`.
- Treat `JSON.parse` output as `unknown` (TS types it as `any`); validate before use.
- Prefer paired **decoders/encoders** at system edges so “wire” shapes and domain types don’t drift (especially around `Date`, `BigInt`, and optional fields).
- Prefer a schema/decoder library (or hand‑rolled decoders) for boundary validation; keep decoders pure and test them directly.

### Async, resources, and lifetimes

- Avoid doing real work in constructors; prefer `createX()` factories for async setup.
- Make lifetimes explicit (start/stop, connect/disconnect); don’t hide resource ownership.
- Ensure cleanup is guaranteed where ownership lives (typically via `try/finally`).
- Prefer explicit parent → child ownership: whoever creates a resource/agent is responsible for stopping it (and awaiting its termination).
- Prefer `AbortSignal` for cancellation and timeouts at boundaries.
- Avoid “detached” promises and background loops without an owner (they’re leaks with no shutdown path).

### Concurrency and agents

Use explicit “agents” for long-running work (pollers, consumers, schedulers) instead of ad-hoc module state.

- Give each agent a single entrypoint that takes an `AbortSignal`.
- Keep state private to the agent; communicate via typed messages or function calls at boundaries.
- Supervise agents from a parent that can stop them and await completion.

A minimal shape:

```ts
export type Agent = {
  run(signal: AbortSignal): Promise<void>;
};
```

### Classes vs factory functions

- Prefer factory functions/closures for most modules; they avoid `this`/unbound-method pitfalls, make dependencies explicit, and fit async setup/lifetimes cleanly.
- Use classes when you need framework integration, `instanceof`, or polymorphism; if you do:
  - avoid inheritance; prefer composition
  - avoid passing unbound instance methods as callbacks
  - don’t use classes as DTOs; keep boundary data as plain objects

### Modules and dependencies

- Prevent cyclic imports; refactor toward a clear dependency direction (domain → application → infrastructure).
- Keep composition/wiring in one place (composition root); avoid cross-cutting “magic” imports.
- Prefer one feature/module per file; avoid catch‑all `utils.ts` that mixes unrelated responsibilities.
- Keep files small and cohesive (a few hundred lines max); split when responsibilities diverge or the file stops fitting in your head.
- Separate concerns by layer (data access vs domain logic vs presentation) and depend on contracts (types/interfaces) rather than concrete implementations.
- Prefer readable imports (path aliases) over deep relative paths.
- If you hit a cycle, break it by extracting shared *types* to a leaf module, inverting a dependency, or moving wiring to the composition root.
- Be cautious with barrel exports (`index.ts`) across layers; they can hide dependencies and make cycles harder to spot.

### Tooling defaults (if you control config)

- Enforce consistency with tooling: Prettier for formatting; ESLint (+ typescript-eslint) for correctness/style; run them in CI.
- Turn on TS strictness (`strict`); if you can’t yet, at least enable `noImplicitAny` and `strictNullChecks` and migrate incrementally.
- Add `@typescript-eslint/no-explicit-any` (with a small allowlist) so `any` stays a last resort.
- Turn on additional correctness flags like `noUnusedLocals`, `noUnusedParameters`, `noImplicitReturns`, and `noFallthroughCasesInSwitch` to keep the codebase honest.
- Prefer type-only imports via config (`verbatimModuleSyntax`) + linting (`consistent-type-imports`) to keep runtime dependencies explicit.
- Add lint rules that prevent async footguns (`no-floating-promises`, `no-misused-promises`) and add cycle detection in larger repos.

### Formatting

- Follow the project’s formatter/linter (often Prettier + ESLint); prefer automation over “style debates”.
- If there’s no established house style, default to: 2-space indentation (no tabs), 1TBS braces for all control flow (even single statements), semicolons (avoid ASI surprises), trailing commas in multiline (clean diffs), and a ~100–120 character line limit (or the project’s formatter `printWidth`).
- Default to single quotes in TS and double quotes in JSON (unless the project’s formatter says otherwise).
- Keep imports grouped and sorted: built-ins → third-party → internal; blank lines between groups; alphabetize within groups; prefer named imports and avoid `import * as X` unless the library expects it.
- Use consistent whitespace (space after commas, around operators, and after `:` in types/object entries); avoid trailing spaces.
- Keep related code close: group by feature, keep callers/callees near, and keep files focused.
- Keep type-only imports explicit via `import type` when configured.

### Comments and documentation

- Comment the “why” (constraints, trade-offs), not the “what”.
- Avoid redundant comments; delete/update comments when code changes.
- Keep public APIs self-documenting via naming/types; use JSDoc/TSDoc only where it improves usage (constraints, examples, edge cases).

## References

- Glossary for common terms: [`GLOSSARY.md`](../GLOSSARY.md)
- Specs/contracts as sources of truth: [`spec-driven-development`](../spec-driven-development/SKILL.md)
- Boundary time budgets and idempotency: [`apply-resilience-patterns`](../apply-resilience-patterns/SKILL.md)
- Telemetry consistency: [`apply-observability-patterns`](../apply-observability-patterns/SKILL.md)
- Shared “golden path” primitives: [`shared-platform-library`](../shared-platform-library/SKILL.md)

## Review checklist

Use this list when reviewing/refactoring TypeScript:

- Names are precise; no mystery abbreviations or misleading types.
- Formatting/imports follow the formatter (Prettier/ESLint); import order is stable.
- Functions are small, single-purpose, and mostly pure; few parameters; no boolean flags.
- Control flow is readable: shallow indentation, no nested ternaries, and no “clever” one-liners.
- Discriminated unions are handled exhaustively; missing variants fail fast at compile time.
- No accidental `any`; `unknown` is narrowed/decoded before use.
- External input is validated/decoded at boundaries; no unsafe `as` casts from JSON/env/network input.
- JSON/env/DB “wire” shapes are kept separate from domain types; round-trips don’t silently lose meaning.
- Expected failures are signified (tagged unions / `Result`); no sentinel returns; internal code is effectively “throwless”.
- Boundary code catches unknown throws and converts them to known error variants.
- Errors aren’t logged repeatedly across layers; logging happens at boundaries with enough context.
- Side effects are isolated; module dependencies are explicit and acyclic.
- No top-level side effects; composition root owns startup/shutdown.
- Resource ownership/cleanup is explicit; no “leaky” lifetimes; cancellation is threaded via `AbortSignal`.
- Long-running loops are explicit agents with shutdown/await paths.
- Tests cover pure logic and boundary adapters (decoders, repositories, clients).

## Output template

When asked to apply this guide, respond with:

- Start with the highest-leverage changes (usually around boundaries, error signifiers, and lifetimes/ownership).
- Concrete refactors (diffs or patch-sized snippets).
- Any trade-offs and clarifying questions (scriptic vs systemic scope, domain boundaries, lifetime/agent ownership, error policy).
