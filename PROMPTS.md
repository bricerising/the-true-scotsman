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

## Conversational prompt skeleton

```text
Hey — can you help me with <what I want, in one sentence>?

Please work conversationally: auto-select the appropriate enterprise-software-playbook skills and follow:
Define → Standardize → Harden → Verify → Mechanics.

Here’s what matters:
- Requirements: <bullets of observable behavior>
- Non-goals: <explicitly what not to do>
- Constraints: <what must not change>
- Scope: in-scope <paths/modules>; out-of-scope <paths/modules>
- Environment: <runtime versions, services, flags, constraints (e.g., no network)>
- Verification: <exact commands/environment to run>
- Done when: <explicit stop condition>

Context: <files, logs, screenshots, links>
```

You do not need all of these sections for every prompt. Choose what is applicable to the task at hand. Consider **Verification** and **Done when** in particular. Those alone can dramatically improve outcomes.

## Minimal prompt

```text
Can you <one sentence goal>?

Please keep the change small and run the verification commands.

Scope: <in/out>
Verification: <commands>
Done when: <tests green + behavior check>
Context: <files/logs>
```

## Conversational bootstrap (auto-skill routing)

Use this once at the start of a project when you want a coding agent to apply skills automatically without you naming them.

```text
You have access to the enterprise-software-playbook skills. I will not name skills explicitly.

Default behavior:
- You must choose and apply the appropriate skills automatically.
- Follow: Define → Standardize → Harden → Verify → Mechanics.
- Keep overhead proportional to the change (don’t create “spec theater” for tiny edits).
- Ask clarifying questions only when blocked; otherwise proceed.
- Always run the provided verification commands; if none are provided, ask once for the preferred commands and then continue.

If supported, treat `enterprise-web-app-workflow` as the router for selecting the rest.
```

## Using skills

Primary mode is conversational: use the bootstrap above and let the agent auto-select skills.

If you want deterministic control (or you’re debugging why an agent chose something), name skills explicitly in the prompt (exact skill name) and list them in order.
If your project isn’t TypeScript, omit `typescript-style-guide`. The other skills are largely language-agnostic.

Available skills in this repo:

**Define (what are we building?)**

- `enterprise-web-app-workflow`: Auto-route work across skills (conversational mode: choose appropriate skills even if the user doesn’t name them).
- `spec-driven-development`: Write and maintain specs/contracts/plans/tasks/quickstarts so agents converge.
- `select-architecture-pattern`: Pick system pattern(s) for cross-service pressures.
- `select-design-pattern`: Pick code pattern(s) for in-process design pressures.

**Standardize (make it consistent)**

- `shared-platform-library`: Design a shared platform package to standardize cross-cutting concerns across services.
- `typescript-style-guide`: TypeScript refactors/implementation with explicit boundaries, validation, and typed errors.

**Harden (make it survive reality)**

- `apply-resilience-patterns`: Timeouts/retries/idempotency/circuit breaker/bulkhead patterns at I/O boundaries.
- `apply-observability-patterns`: Logs/metrics/traces correlation patterns for production debugging.

**Verify (prove behavior)**

- `consumer-test-coverage`: Add consumer-centric tests. Prefer observable behavior over testing internals.

**Mechanics (in-process building blocks)**

- `apply-creational-patterns`: Apply Factory/Builder/etc. once a creational approach is chosen.
- `apply-structural-patterns`: Apply Adapter/Decorator/Proxy/etc. when you need to add behavior without changing interfaces.
- `apply-behavioral-patterns`: Apply Strategy/Observer/Chain/etc. when you need pluggable logic or pipelines.

## Skill recipes

### Enterprise web app default sequence (cohesion-first)

```text
Can you implement <feature> for an enterprise web app?

Please auto-apply the enterprise-software-playbook workflow (Define → Standardize → Harden → Verify → Mechanics) and choose whatever skills you need.

Constraints:
- preserve public contracts unless the spec says otherwise
- keep error semantics stable
- no hidden I/O at import time

Verification: <test/lint/build commands>
Done when: specs/contracts are updated (if needed), tests are green, and the feature is observable + resilient at its boundaries

Context: <spec paths>, <entrypoints>, <SLOs/time budgets>, <existing patterns>
```

### Choose the simplest code pattern

```text
I’m not sure what the best in-process structure is for this problem:
<describe the pressure: multiple providers, pluggable rules, caching/logging wrappers, etc.>

Can you recommend the smallest code pattern(s) that fit, and keep it practical?

Please include:
- a clear recommendation (and why)
- 1–2 plausible alternatives and why you’re not choosing them
- target module structure + key interfaces + wiring changes
- an incremental migration plan (small steps, low-risk order)
- a validation plan (tests + what “done” means)
- trade-offs/risks + what not to do

Context: <where the code lives / current approach (e.g., switch statements)>
```

### Choose a system pattern

```text
I’m dealing with a cross-service/system pressure:
<partial failures, cross-service consistency, domain boundaries, eventing, scaling, migration, ML lifecycle>

Can you recommend the smallest system pattern(s) that fit?

Please include:
- assumptions + key failure modes you’re designing for
- 1–2 alternatives and why you’re not choosing them
- how this maps to implementation tactics (often code-pattern wrappers/pipelines)
- what tests + metrics would prove it works

Constraints: <SLAs/SLOs, consistency needs, schema ownership, latency budgets, deployment realities>
```

### Write a spec bundle (enterprise web app)

```text
Can you create or update the spec bundle for <service/feature>?

Please keep it testable and concrete (Given/When/Then), include explicit non-goals, and keep error semantics stable.

Deliverables:
- system spec updates (if cross-service) and/or `apps/<service>/spec/spec.md`
- contract updates (`contracts/`): OpenAPI/proto/WS message docs
- `plan.md` with phases and wiring notes
- `tasks.md` broken into small tasks with acceptance criteria
- `quickstart.md` with copy/paste commands + “known good” verification

Context: <current behavior>, <files>, <constraints/SLOs>, <what’s changing>
```

### Build a shared platform library (monorepo)

```text
We have repeated cross-cutting code for <concern>. Can you extract/standardize it into `packages/shared` (or equivalent) without changing behavior?

Constraints:
- no domain/business logic in shared
- no top-level side effects (no hidden I/O on import)
- preserve response shapes and error semantics at boundaries

Deliverables:
- proposed module layout and public exports
- one “golden path” primitive (e.g., handler wrapper, client proxy, lifecycle facade)
- migrate at least 2 call sites to prove it works
- tests for the primitive + consumer-visible tests where needed

Context: <duplicated code>, <services involved>, <observability/resilience requirements>
```

### Apply a creational pattern (construction/config)

```text
Can you hide the complex construction of <client/service> (multiple transports/providers/configs) so call sites stay simple?

Constraints:
- keep behavior identical at the boundary
- avoid global singletons unless explicitly required
- make dependencies explicit (constructor params / factory inputs); avoid hidden I/O in constructors
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
I need to add <caching/logging/retries/rate limiting/authorization> around <interface> without changing its interface.

Constraints:
- preserve semantics (including error cases)
- keep the diff small; avoid moving unrelated files

Deliverables:
- wrapper implementation (Decorator/Proxy/Adapter/etc.)
- tests for observable behavior (cache hit/miss, logging fields, retry limits, etc.)
```

### Apply observability patterns (logs/metrics/traces)

```text
Can you add or improve observability for <service>/<feature>/<boundary>?

What I need:
- structured logs with correlation IDs (`traceId`/`spanId` or `requestId`)
- RED metrics for the boundary (rate/errors/duration)
- traces that span the end-to-end request (including downstream calls)

Constraints:
- avoid high-cardinality metric labels
- avoid logging secrets/PII

Deliverables:
- instrumentation changes
- a short local verification checklist (log → trace → metrics)

Context: <routes/rpcs/jobs>, <current logger/otel/metrics setup>
```

### Apply resilience patterns (timeouts/retries/idempotency)

```text
Can you harden <boundary> against partial failures?

Requirements:
- explicit timeouts and cancellation propagation
- bounded retries with backoff+jitter (only if safe)
- idempotency/dedupe strategy when retries exist

Optional (if needed): circuit breaker and bulkhead/concurrency limit when dependency is flaky/overloaded

Deliverables:
- wrapper/utility changes
- tests for consumer-visible semantics
- failure-mode smoke steps I can run locally

Context: <call sites>, <error semantics>, <SLO/time budgets>
```

### Apply a behavioral pattern (pluggable logic/pipelines)

```text
I need to make <logic> pluggable or pipeline-based (e.g., Strategy, Chain of Responsibility, State).

Constraints:
- preserve current outcomes by default
- keep selection rules explicit (no magic)

Deliverables:
- pattern implementation with clear extension points
- tests proving selection/order and key edge cases
```

### Refactor or implement in TypeScript with explicit boundaries

```text
Can you <implement/refactor area> in TypeScript while keeping boundaries explicit and runtime-safe?

Requirements:
- validate external inputs at boundaries (treat as `unknown`)
- make expected failures explicit (typed result); don’t throw for expected failures

Constraints:
- avoid top-level side effects; wire dependencies in a composition root
- keep the module graph acyclic (or reduce cycles)

Verification: <commands>
```

### Add consumer-centric tests/coverage

```text
Can you add consumer-centric tests for <HTTP handler/gRPC method/job/consumer/CLI entrypoint>?

Please:
- assert client-visible behavior (status codes, response shape, side effects)
- avoid asserting internal calls/implementation details

Coverage baseline:
- happy path
- one invalid-input case
- one unhappy-path clients can observe (timeouts/downstream errors/permissions)

Add when relevant:
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
Can you write or update a Quickstart/runbook for this project so future us (and other agents) can run/debug it quickly?

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
Can you do a gap analysis between <spec/PRD/issue> and the current implementation, then close the gaps?

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
Can you implement <feature/module> described in <spec-path or issue link>?

Please keep boundaries explicit and runtime-safe, and keep tests consumer-visible.

If the design is unclear or there are multiple viable designs, propose the smallest fitting code pattern(s) and explain why before implementing.

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
Before you change any behavior, please add or adjust a test that captures the current consumer-visible behavior.
Only refactor after the test pins it down.
```

### Follow-up

```text
Please focus only on <scope>. Ignore unrelated cleanup unless it is required to make tests pass.
If you think something else must change, explain why and propose the smallest viable change.
```

## Sequence: E2E tests against a real environment

### Kickoff (spec-driven e2e)

```text
Can you write E2E tests (Playwright/Cypress/etc.) that verify the deployed app matches <specs/requirements>?

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
Can you update the UI to add stable test selectors for user-performable actions (buttons, inputs, menus)?

Please keep the naming consistent and “future proof” (avoid brittle DOM-coupled names).
Then update the Playwright tests to use those ids.
Re-run the production-like environment + the tests and iterate until green.
```

## Sequence: triage from logs

### Kickoff (repro → root cause → regression test)

```text
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
Our observability is missing <logs/metrics/traces/dashboards>. Can you fix what’s wrong end-to-end?

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
Please recommend the smallest pattern(s) that fit, then apply them.

Use this as a guide when choosing the kind of refactor:
- creational: construction/config/lifecycle
- structural: wrapping, adapters, caching, logging, proxies
- behavioral: pipelines, strategies, observers, state machines

If this is a TypeScript area, keep boundaries/errors consistent with the repo’s TypeScript conventions.
If behavior is ambiguous, add a characterization test first (consumer-visible).

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
Please only make a refactor if you can keep behavior identical for consumers.
If there’s ambiguity, add a test first to lock behavior down.
```

## Sequence: apply a repo style guide consistently

```text
Please help me make this repo conform to <style guide file(s)> (e.g., `STYLES.md`, lint rules) without changing behavior.

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
Can you make `npm run build` (or equivalent) at the repo root build all packages/apps reliably?

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
Can you add merge-blocking CI for this repo?

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
Can you build a CLI named `<cli-name>` for <purpose>?

Please structure it so each subcommand is implemented as an explicit “command” (easy to test, easy to extend).

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
Can you help me load <dataset> into <store> and ship dashboards/queries that surface the most useful insights?

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
Please prefer the repo’s most production-like verification environment (containers/k8s/etc.); don’t rely on mocks unless necessary.
```

```text
Please don’t change externally-visible semantics. If you must, explain the tradeoff and update tests + spec.
```
