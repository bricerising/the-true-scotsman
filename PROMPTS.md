# Prompt Library

These are copy/paste **prompt sequences** that work well across most software projects (apps, services, CLIs, libraries, monorepos).

They work best because they:

- Front-load **scope** + **constraints** + **verification**
- Force an **iteration loop** (“run it until green”)
- Anchor work to **consumer-visible behavior** (specs/tests), not internals

Replace placeholders like `<service>`, `<spec-path>`, `<commands>`, etc.

## Make agents effective

The fastest way to get high-quality results is to include the information that lets an agent **act** rather than guess:

- **One-line goal**: what “done” looks like in plain English.
- **Scope**: exact folders/modules that are in-scope, and what is explicitly out-of-scope.
- **Invariants**: what must not change (public API, behavior, error semantics, data model, UX, perf budgets).
- **Verification commands**: the exact commands to run (unit/integration/e2e/lint/build) and any required setup.
- **Production-like runtime**: how you want it verified locally (containers, dev server, seeds, localstack, etc.).
- **Entry points**: the main files/services/routes/jobs involved (or where to start looking).
- **Repro steps + inputs**: steps, payloads, env vars, feature flags, and test data to reproduce.
- **Expected vs actual**: observable behavior (status codes, responses, UI state), not internal implementation.
- **Constraints on change**: “small diff”, “no new deps”, “no schema changes”, “no breaking changes”, etc.
- **Stop condition**: when the agent should stop iterating and report back (tests green + specific behavior).

## Prompt skeleton

```text
Skills (in order): <skill-1>, <skill-2>, <skill-3> (optional)
Goal: <what you want, in one sentence>
Requirements: <bullets of behavior>
Non-goals: <explicitly what not to do>
Constraints: <what must not change>
Scope: <in-scope paths/modules> / <out-of-scope>
Environment: <runtime versions, services, flags, constraints (e.g., no network)>
Autonomy: <proceed without asking; ask only when blocked>
Deliverables: <what you expect back: code/tests/docs>
Verification: <exact commands/environment to run>
Done when: <explicit stop condition>
Context: <files, logs, screenshots, links>
```

You do not need all of these sections for every prompt. Choose what is applicable to the task at hand. Consider **Verification** and **Done when** in particular. Those alone can dramatically improve outcomes.

## Minimal prompt

```text
Goal: <one sentence>
Scope: <in/out>
Verification: <commands>
Done when: <tests green + behavior check>
Context: <files/logs>
```

## Using skills

If your chat agent supports these skills, name them explicitly in the prompt (the exact skill name) and list in order.
If your project isn’t TypeScript, omit `typescript-style-guide`. The other skills are largely language-agnostic.

Available skills in this repo:

- `typescript-style-guide`: TypeScript refactors/implementation with explicit boundaries, validation, and typed errors.
- `select-design-pattern`: Pick the smallest GoF pattern(s) that fit.
- `select-architecture-pattern`: Pick system/architecture patterns beyond GoF (cloud-native, event-driven, DDD, distributed coordination, AI/ML).
- `spec-driven-development`: Write and maintain specs/contracts/plans/tasks/quickstarts so agents converge.
- `shared-platform-library`: Design a shared platform package to standardize cross-cutting concerns across services.
- `apply-observability-patterns`: Apply logs/metrics/traces correlation patterns for production debugging.
- `apply-resilience-patterns`: Apply timeouts/retries/idempotency/circuit breaker/bulkhead patterns at I/O boundaries.
- `apply-creational-patterns`: Apply Factory/Builder/etc. once a creational approach is chosen.
- `apply-structural-patterns`: Apply Adapter/Decorator/Proxy/etc. when you need to add behavior without changing interfaces.
- `apply-behavioral-patterns`: Apply Strategy/Observer/Chain/etc. when you need pluggable logic or pipelines.
- `consumer-test-coverage`: Add consumer-centric tests. Prefer observable behavior over testing internals.

## Skill recipes

### Enterprise web app default sequence (cohesion-first)

```text
Skills (in order): spec-driven-development, select-architecture-pattern, shared-platform-library, typescript-style-guide, apply-resilience-patterns, apply-observability-patterns, consumer-test-coverage
Goal: implement <feature> for an enterprise web app with stable contracts and predictable failure/telemetry behavior.
Constraints: preserve public contracts unless the spec says otherwise; keep error semantics stable; no hidden I/O at import time
Verification: <test/lint/build commands>
Done when: specs + contracts are updated, tests are green, and the feature is observable + resilient at its boundaries
Context: <spec paths>, <entrypoints>, <SLOs/time budgets>, <existing patterns>
```

### Choose the simplest design pattern

```text
Use select-design-pattern.

Problem: <describe the pressure: multiple providers, pluggable rules, caching/logging wrappers, etc.>
Context: <where the code lives / current approach (e.g., switch statements)>
Deliverables:
- recommend the smallest GoF pattern(s) that fit
- show 1–2 plausible alternatives and why you’re not choosing them
- outline the target module structure, key interfaces, and composition/wiring changes
- propose an incremental migration plan (small steps, low-risk order)
- propose a validation plan (tests + what “done” means)
- call out tradeoffs, risks, and what not to do
```

### Choose an architecture/system pattern

```text
Use select-architecture-pattern.

Problem: <describe the system pressure: partial failures, cross-service consistency, domain boundaries, eventing, scaling, migration, ML lifecycle>
Constraints: <SLAs/SLOs, consistency needs, schema ownership, latency budgets, deployment realities>
Deliverables:
- recommend the smallest architecture pattern(s) that fit
- list assumptions + the key failure modes you’re designing for
- show 1–2 alternatives and why you’re not choosing them
- map to implementation tactics (often GoF wrappers/pipelines) and outline tests/metrics
```

### Write a spec bundle (enterprise web app)

```text
Use spec-driven-development.

Goal: create or update the spec bundle for <service/feature>.
Deliverables:
- system spec updates (if cross-service) and/or `apps/<service>/spec/spec.md`
- contract updates (`contracts/`): OpenAPI/proto/WS message docs
- `plan.md` with phases and wiring notes
- `tasks.md` broken into small tasks with acceptance criteria
- `quickstart.md` with copy/paste commands + “known good” verification
Constraints: keep specs testable (Given/When/Then), explicit non-goals, and stable error semantics
Context: <current behavior>, <files>, <constraints/SLOs>, <what’s changing>
```

### Build a shared platform library (monorepo)

```text
Use shared-platform-library.

Goal: extract/standardize <cross-cutting concern> into `packages/shared` (or equivalent) without changing behavior.
Deliverables:
- proposed module layout and public exports
- one “golden path” primitive (e.g., handler wrapper, client proxy, lifecycle facade)
- migrate at least 2 call sites to prove it works
- tests for the primitive + consumer-visible tests where needed
Constraints:
- no domain/business logic in shared
- no top-level side effects (no hidden I/O on import)
- preserve response shapes and error semantics at boundaries
Context: <duplicated code>, <services involved>, <observability/resilience requirements>
```

### Apply a creational pattern (construction/config)

```text
Use apply-creational-patterns.

Goal: hide complex construction of <client/service> (e.g., multiple transports/providers/configs).
Constraints:
- keep call sites minimal
- keep behavior identical at the boundary
- avoid global singletons unless explicitly required
- make dependencies explicit (constructor params / factory inputs), avoid hidden I/O in constructors
- make resource lifetimes explicit (create/start/stop/dispose) and easy to test
- validate/normalize config at the boundary (parse once, pass typed config inward)
Deliverables:
- a factory/builder approach with clear lifetimes (create/start/stop if relevant)
- tests using fakes/stubs (no network) where possible
- a short usage example (how callers construct and use it)
Context: <current constructors/factories and call sites>
```

### Apply a structural pattern (wrapping without interface change)

```text
Use apply-structural-patterns.

Goal: add <caching/logging/retries/rate limiting/authorization> around <interface> without changing its interface.
Constraints:
- preserve semantics (including error cases)
- keep diff small; avoid moving unrelated files
Deliverables:
- wrapper implementation (Decorator/Proxy/Adapter/etc.)
- tests for observable behavior (cache hit/miss, logging fields, retry limits, etc.)
```

### Apply observability patterns (logs/metrics/traces)

```text
Use apply-observability-patterns.

Goal: add or improve observability for <service>/<feature>/<boundary>.
Requirements:
- structured logs with correlation IDs (traceId/spanId or requestId)
- RED metrics for the boundary (rate/errors/duration)
- traces span the end-to-end request (including downstream calls)
Constraints: avoid high-cardinality metric labels; avoid logging secrets/PII
Deliverables: instrumentation changes + a short local verification checklist (log → trace → metrics)
Context: <routes/rpcs/jobs>, <current logger/otel/metrics setup>
```

### Apply resilience patterns (timeouts/retries/idempotency)

```text
Use apply-resilience-patterns.

Goal: harden <boundary> against partial failures.
Requirements:
- explicit timeouts and cancellation propagation
- bounded retries with backoff+jitter (only if safe)
- idempotency/dedupe strategy when retries exist
Optional: circuit breaker and bulkhead/concurrency limit when dependency is flaky/overloaded
Deliverables: wrapper/utility changes + tests for consumer-visible semantics + failure-mode smoke steps
Context: <call sites>, <error semantics>, <SLO/time budgets>
```

### Apply a behavioral pattern (pluggable logic/pipelines)

```text
Use apply-behavioral-patterns.

Goal: make <logic> pluggable or pipeline-based (e.g., Strategy, Chain of Responsibility, State).
Constraints:
- preserve current outcomes by default
- keep selection rules explicit (no magic)
Deliverables:
- pattern implementation (Strategy/Chain/State/etc.) with clear extension points
- tests proving selection/order and edge cases
```

### Refactor or implement in TypeScript with explicit boundaries

```text
Use typescript-style-guide.

Goal: <implement/refactor area> while keeping boundaries explicit and runtime-safe.
Requirements:
- validate external inputs at boundaries (treat as `unknown`)
- make expected failures explicit (typed result), no throwing for expected failures
Constraints:
- avoid top-level side effects; wire dependencies in a composition root
- keep the module graph acyclic (or reduce cycles)
Verification: <commands>
```

### Add consumer-centric tests/coverage

```text
Use consumer-test-coverage.

Target: <HTTP handler/gRPC method/job/consumer/CLI entrypoint>
Requirements:
- assert client-visible behavior (status codes, response shape, side effects)
- avoid asserting internal calls/implementation details
Coverage:
- baseline:
  - happy path
  - one invalid-input case
  - one unhappy-path that clients can observe (timeouts/downstream errors/permissions)
- add when relevant:
  - auth/permissions
  - idempotency/retries
  - concurrency/race conditions
  - pagination/sorting/filtering
  - rate limiting/backpressure
  - backward compatibility / versioning
Verification: <commands>
```

Sequences below are ordered like a typical workflow: setup → implement → verify → debug → harden. Jump to the one that matches your task.

## Sequence: quickstart/runbook

Use this when you want future you (or other agents) to be able to run/debug the project quickly.

```text
Write or update a Quickstart/runbook.

Requirements:
- prerequisites (versions, env vars, external services)
- how to start (dev/prod-like) and how to stop/clean up
- how to run tests/lint/build (exact commands)
- common failures + how to diagnose (where logs live, what commands to run)
- “known good” verification checklist (what to click/run to confirm it works)

Constraints:
- keep it short and executable (copy/paste commands)
- don’t require hidden local state; document it if unavoidable

Deliverables: updated docs (README/QUICKSTART.md/docs/runbook.md) and any small scripts needed.
```

## Sequence: spec/requirements gap analysis

Use this when the spec/PRD exists but you’re not sure the repo already matches it.

```text
Skills (in order): consumer-test-coverage (optional: select-design-pattern, typescript-style-guide if TS)

Please do a gap analysis between <spec/PRD/issue> and the current implementation.

Output:
1) What’s missing (requirements not implemented)
2) What’s incorrect (behavior mismatches)
3) What’s extra (implementation that doesn’t belong / contradicts the spec)
4) Risky areas (where changes may break consumers)
5) Proposed plan (small steps, in order) + what you’ll verify at each step

Then implement the plan with minimal churn.

Constraints:
- preserve public APIs unless the spec requires changes
- prefer incremental commits/patches over rewrites

Verification: <commands> + <production-like env if applicable>
Done when: gaps are closed and <commands> are green.
```

## Sequence: implement from a spec / PRD / issue

### Kickoff (feature/module implementation)

```text
Skills (in order): typescript-style-guide (if TS), consumer-test-coverage (optional: select-design-pattern, apply-creational-patterns/apply-structural-patterns/apply-behavioral-patterns)

Use typescript-style-guide to implement <feature/module> described in <spec-path or issue link>.
If the design is unclear or there are multiple viable designs:
1) use select-design-pattern to recommend the smallest pattern(s) that fit, then
2) use the matching apply-* skill to implement it (`apply-creational-patterns`, `apply-structural-patterns`, or `apply-behavioral-patterns`).

Requirements:
- <list the observable behaviors / APIs / workflows>

Non-goals:
- <explicitly what not to do (e.g., “don’t redesign the architecture”, “don’t switch frameworks”)>

Constraints:
- preserve existing public APIs unless explicitly required
- preserve existing behavior unless explicitly required
- avoid broad rewrites; prefer small, reviewable changes

Scope:
- in-scope: <paths/modules>
- out-of-scope: <paths/modules>

Autonomy:
- proceed without asking for confirmation between steps
- ask questions only if blocked (missing info, unclear acceptance criteria)

Verification:
- run: <commands> (tests/lint/build)
- if the repo has a “real” environment: verify there too (e.g., `docker compose up --build`, dev server, localstack, k8s, etc.)

Done when:
- <commands> are green
- the feature works end-to-end in the “real” environment (if applicable)

Deliverables:
- implementation changes
- tests for the key behaviors (unit + integration where appropriate) — use consumer-test-coverage to keep tests consumer-centric
- any docs/spec updates needed to keep docs truthful
```

### Follow-up

```text
Before you change any behavior, add or adjust a test that captures the current consumer-visible behavior.
Only refactor after the test pins it down.
```

### Follow-up

```text
Focus only on <scope>. Ignore unrelated cleanup unless it is required to make tests pass.
If you think something else must change, explain why and propose the smallest viable change.
```

## Sequence: E2E tests against a real environment

### Kickoff (spec-driven e2e)

```text
Skills (in order): consumer-test-coverage (optional: typescript-style-guide)

Write E2E tests (Playwright/Cypress/etc.) that verify the deployed app matches <specs/requirements>.

Start the app using the repo’s most production-like local setup (<command(s)>), then run E2E tests against it.
Iterate until the tests pass (fix product bugs or test flakiness as needed).

Non-goals:
- don’t rely on fragile selectors (CSS structure/text) when a stable selector is feasible
- don’t “fix” flakiness by adding arbitrary sleeps; prefer waiting on real conditions

Guidelines:
- Prefer stable selectors (e.g., `data-testid`) over text/CSS
- Assert user-visible behavior (status codes, UI state, navigation), not internal calls
- Use consumer-test-coverage principles: assert the contract at the boundary, not implementation details
- Make tests rerunnable and isolated (unique ids/test data; cleanup when needed)
- Capture useful artifacts on failure (screenshots/logs/traces) if your setup supports it

Deliverables:
- E2E tests
- any helper scripts/docs needed to run them consistently
```

### Follow-up (UI isn’t testable yet)

```text
Update the UI to add stable test selectors for user-performable actions (buttons, inputs, menus).
Keep the naming consistent and “future proof” (avoid brittle DOM-coupled names).
Then update the Playwright tests to use those ids.
Re-run the production-like environment + the tests and iterate until green.
```

## Sequence: triage from logs

### Kickoff (repro → root cause → regression test)

```text
Skills (in order): consumer-test-coverage (optional: typescript-style-guide, select-design-pattern)

I’m seeing this error when <steps to reproduce>:
<paste logs / stack trace>

Expected:
- <what should happen>

Actual:
- <what happens instead>

Non-goals:
- don’t silence the error by swallowing exceptions or lowering log levels
- don’t weaken validation/auth just to “make it pass”

Please:
1) reproduce locally (prefer the repo’s most production-like environment if available),
2) identify the root cause,
3) fix it with minimal churn,
4) add a regression test (use consumer-test-coverage),
5) re-run <commands> and iterate until green.

If you can’t reproduce:
- add the smallest instrumentation/logging to make the failure diagnosable, and
- tell me exactly what to run/click to capture the missing signal.
```

### Follow-up (log triage discipline)

```text
If you need more info, ask for the smallest missing piece (exact service logs, the spec section, or a file path).
Prefer using the observability/log tooling that ships with the repo (dashboards/log search/traces) when available.
```

## Sequence: observability fixes

### Kickoff (dashboards/logs/traces missing)

```text
Skills (optional): apply-structural-patterns, consumer-test-coverage

Our observability is missing <logs/metrics/traces/dashboards>. Please fix what’s wrong end-to-end.

Non-goals:
- don’t “fix” missing signals by disabling instrumentation or sampling everything away
- don’t paper over gaps with fake dashboards; make the underlying signals flow

Approach:
- use the repo’s production-like environment (containers/k8s/etc.) to reproduce
- generate a small, controlled amount of traffic to produce signals (so you can validate fixes)
- use logs/traces to identify ingestion/export/query errors end-to-end
- fix the minimal set of config/instrumentation needed (agents/collectors/exporters/dashboards)
- document the “signal path” (where logs/metrics/traces come from and how they flow)

Deliverables:
- working dashboards/panels
- any config changes required
- a short “how to verify” checklist (what to click/run to see data)
- a short “how to debug when it breaks” checklist (where to look first)
```

## Sequence: refactor with invariants

### Kickoff (choose smallest pattern, then apply)

```text
Skills (in order): select-design-pattern, apply-creational-patterns/apply-structural-patterns/apply-behavioral-patterns, typescript-style-guide (if TS), consumer-test-coverage

First use select-design-pattern to recommend the smallest pattern(s) that fit.
Then implement using the appropriate apply-* skill:
- apply-creational-patterns (construction/config/lifecycle)
- apply-structural-patterns (wrapping, adapters, caching, logging, proxies)
- apply-behavioral-patterns (pipelines, strategies, observers, state machines)
Finally use typescript-style-guide to standardize boundaries/errors, and consumer-test-coverage to keep tests consumer-visible.

Goal: refactor <area> to improve readability/maintainability without changing consumer-visible behavior.

Non-goals:
- no sweeping rewrites
- no renames/moves unless they materially reduce complexity

Constraints:
- no public API changes
- no behavior changes (unless explicitly called out and tested)
- keep the diff reasonably small (avoid large renames/moves)

Deliverables:
- refactor implementation
- tests updated/added only to preserve behavior (add characterization tests first if needed)
- short explanation of the chosen pattern and resulting module structure

Verification:
- run: <commands>

Done when:
- <commands> are green
- behavior matches existing integration/e2e tests
```

### Follow-up (don’t refactor blind)

```text
Only make a refactor if you can keep behavior identical for consumers.
If there’s ambiguity, add a test first to lock behavior down.
```

## Sequence: apply a repo style guide consistently

```text
Skills (in order): typescript-style-guide (if TS)

Goal: make the repo conform to <style guide file(s)> (e.g., `STYLES.md`, lint rules) without changing behavior.

Constraints:
- no behavior changes (unless explicitly required and tested)
- avoid drive-by refactors; keep changes mechanical and reviewable

Approach:
- identify the canonical style sources (lint/format rules + any docs)
- apply automated formatting first (if available), then manual cleanups
- fix type errors and lint errors created by the changes

Verification: <commands>
Done when: formatting/lint is clean and tests are green.
```

## Sequence: monorepo “one command” build

```text
Goal: make `npm run build` (or equivalent) at the repo root build all packages/apps reliably.

Requirements:
- deterministic output locations (`dist/` or similar)
- clear dependency order between packages
- consistent TS config / module resolution (if TS)

Constraints:
- don’t introduce new build tools unless necessary
- keep local dev fast (avoid rebuilding everything on small changes)

Verification:
- clean build from scratch
- incremental rebuild
Done when: root build is reliable and documented.
```

## Sequence: add CI guardrails

```text
Add merge-blocking CI for this repo.

Requirements:
- run tests + lint + build on every PR
- cache dependencies appropriately
- clear failure output for contributors

Optional policy (if applicable):
- restrict who can trigger privileged workflows (maintainers only)
- add a lightweight “guideline check” step (no secrets, no network where possible)

Deliverables: workflow files + docs on how to run the same checks locally.
```

## Sequence: build a CLI tool

```text
Skills (in order): apply-behavioral-patterns (Command), typescript-style-guide (if TS), consumer-test-coverage

Build a CLI named `<cli-name>` for <purpose>.

CLI contract:
- commands/subcommands: <list>
- flags/options: <list>
- exit codes: 0 success, non-zero failures (define meanings)
- output: human-readable by default; optional `--json` for automation

Constraints:
- stable UX: don’t break existing flags/output without a migration plan
- avoid hidden globals; configuration should be explicit

Deliverables:
- implementation + `--help` output + examples
- packaging/install instructions (and a smoke test: “install then run”)
- tests for argument parsing and at least one end-to-end happy path
```

## Sequence: native dependency / architecture mismatch

Use this when you hit errors like “exec format error”, “arm64 vs x86_64”, or `node-gyp`/toolchain failures.

```text
I’m hitting a native dependency issue:
<paste error>

Environment:
- host OS/arch: <e.g., macOS arm64>
- container OS/arch (if relevant): <e.g., linux/amd64>
- runtime versions: <node/python/rust/etc.>

Please propose 2–3 options, ordered by maintainability:
1) switch to a pure-language alternative (no native build) if viable
2) use prebuilt binaries/multi-arch builds if available
3) add the minimum toolchain required to build from source

Then implement the best option under these constraints:
- keep behavior identical for consumers
- keep Docker/dev environment simple

Verification: <commands> + <build/run in prod-like env>
```

## Sequence: debug an unstable external integration

```text
I’m integrating with an external dependency (hardware device / third-party service) and seeing failures:
<paste logs>

Context:
- dependency model/version + protocol docs if available
- exact repro steps + timing
- what should happen vs what happens

Please:
1) add the minimum instrumentation/logging needed to diagnose (don’t spam logs),
2) make the integration resilient (timeouts, retries, backoff, idempotency where appropriate),
3) add a local “replay” or simulation mode if feasible (recorded traces/fixtures),
4) document how to capture the right logs when it breaks again.

Verification: <commands> + a repro checklist I can run.
```

## Sequence: data ingestion → dashboards

```text
Goal: load <dataset> into <store> and ship dashboards/queries that surface the most useful insights.

Requirements:
- fully automated local bring-up (e.g., `docker compose up`)
- deterministic, rerunnable importer/seeder
- dashboards/queries provisioned as code in the repo

Constraints:
- keep the mapping explicit (document labels/fields and their meaning)
- prefer a small set of “high-signal” dashboards over many weak ones

Deliverables:
- compose/env + importer + dashboards
- “how to run” + “how to verify” docs
```

## Short follow-ups that keep agents aligned

```text
Please run tests and iterate until green.
```

```text
Prefer the repo’s most production-like verification environment (containers/k8s/etc.); don’t rely on mocks unless necessary.
```

```text
Don’t change externally-visible semantics. If you must, explain the tradeoff and update tests + spec.
```
