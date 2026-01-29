# Prompt Library (project-agnostic)

These are copy/paste **prompt sequences** that work well across most software projects (apps, services, CLIs, libraries, monorepos).

They work best because they:

- Front-load **scope** + **constraints** + **verification**
- Force an **iteration loop** (“run it until green”)
- Anchor work to **consumer-visible behavior** (specs/tests), not internals

Replace placeholders like `<service>`, `<spec-path>`, `<commands>`, etc.

## Using skills (recommended)

If your chat agent supports these skills, name them explicitly in the prompt (the exact skill name) and list an order.
If your project isn’t TypeScript, omit `typescript-style-guide` (the other skills are largely language-agnostic).

Available skills in this repo:

- `typescript-style-guide`: TypeScript refactors/implementation with explicit boundaries, validation, and typed errors.
- `select-design-pattern`: Pick the smallest GoF pattern(s) that fit.
- `apply-creational-patterns`: Apply Factory/Builder/etc. once a creational approach is chosen.
- `apply-structural-patterns`: Apply Adapter/Decorator/Proxy/etc. when you need to add behavior without changing interfaces.
- `apply-behavioral-patterns`: Apply Strategy/Observer/Chain/etc. when you need pluggable logic or pipelines.
- `consumer-test-coverage`: Add consumer-centric tests (prefer observable behavior over internals).

## Skill recipes (copy/paste starters)

### Choose the simplest pattern

```text
Use select-design-pattern.

Problem: <describe the pressure: multiple providers, pluggable rules, caching/logging wrappers, etc.>
Context: <where the code lives / current approach (e.g., switch statements)>
Deliverables:
- recommend the smallest GoF pattern(s) that fit
- outline the target module structure and interfaces
- call out tradeoffs and what not to do
```

### Apply a creational pattern (construction/config)

```text
Use apply-creational-patterns.

Goal: hide complex construction of <client/service> (e.g., multiple transports/providers/configs).
Constraints: keep call sites minimal; no behavior change; add/adjust tests.
Context: <current constructors/factories and call sites>
```

### Apply a structural pattern (wrapping without interface change)

```text
Use apply-structural-patterns.

Goal: add <caching/logging/retries/rate limiting/authorization> around <interface> without changing its interface.
Constraints: preserve semantics; keep diff small; add tests for observable behavior.
```

### Apply a behavioral pattern (pluggable logic/pipelines)

```text
Use apply-behavioral-patterns.

Goal: make <logic> pluggable or pipeline-based (e.g., Strategy, Chain of Responsibility, State).
Constraints: preserve current outcomes; add tests proving selection/order and edge cases.
```

### Refactor or implement in TypeScript with explicit boundaries

```text
Use typescript-style-guide.

Goal: <implement/refactor area> while keeping boundaries explicit and runtime-safe.
Requirements:
- validate external inputs at boundaries (treat as `unknown`)
- make expected failures explicit (typed result), no throwing for expected failures
Verification: <commands>
```

### Add consumer-centric tests/coverage

```text
Use consumer-test-coverage.

Target: <HTTP handler/gRPC method/job/consumer/CLI entrypoint>
Requirements:
- assert client-visible behavior (status codes, response shape, side effects)
- avoid asserting internal calls/implementation details
Verification: <commands>
```

## Prompt skeleton (recommended)

```text
Skills (in order): <skill-1>, <skill-2>, <skill-3> (optional)
Goal: <what you want, in one sentence>
Requirements: <bullets of behavior>
Constraints: <what must not change>
Scope: <in-scope paths/modules> / <out-of-scope>
Deliverables: <what you expect back: code/tests/docs>
Verification: <exact commands/environment to run>
Done when: <explicit stop condition>
Context: <files, logs, screenshots, links>
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

Constraints:
- preserve existing public APIs unless explicitly required
- preserve existing behavior unless explicitly required
- avoid broad rewrites; prefer small, reviewable changes

Scope:
- in-scope: <paths/modules>
- out-of-scope: <paths/modules>

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

### Follow-up (pin behavior before refactoring)

```text
Before you change any behavior, add or adjust a test that captures the current consumer-visible behavior.
Only refactor after the test pins it down.
```

### Follow-up (keep it focused)

```text
Focus only on <scope>. Ignore unrelated cleanup unless it is required to make tests pass.
If you think something else must change, explain why and propose the smallest viable change.
```

## Sequence: E2E tests against a real environment (Playwright/Cypress/etc.)

### Kickoff (spec-driven e2e)

```text
Skills (in order): consumer-test-coverage (optional: typescript-style-guide)

Write E2E tests (Playwright/Cypress/etc.) that verify the deployed app matches <specs/requirements>.

Start the app using the repo’s most production-like local setup (<command(s)>), then run E2E tests against it.
Iterate until the tests pass (fix product bugs or test flakiness as needed).

Guidelines:
- Prefer stable selectors (e.g., `data-testid`) over text/CSS
- Assert user-visible behavior (status codes, UI state, navigation), not internal calls
- Use consumer-test-coverage principles: assert the contract at the boundary, not implementation details

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

## Sequence: triage from logs (keep it production-ish)

### Kickoff (repro → root cause → regression test)

```text
Skills (in order): consumer-test-coverage (optional: typescript-style-guide, select-design-pattern)

I’m seeing this error when <steps to reproduce>:
<paste logs / stack trace>

Expected:
- <what should happen>

Actual:
- <what happens instead>

Please:
1) reproduce locally (prefer the repo’s most production-like environment if available),
2) identify the root cause,
3) fix it with minimal churn,
4) add a regression test (use consumer-test-coverage),
5) re-run <commands> and iterate until green.
```

### Follow-up (log triage discipline)

```text
If you need more info, ask for the smallest missing piece (exact service logs, the spec section, or a file path).
Prefer using the observability/log tooling that ships with the repo (dashboards/log search/traces) when available.
```

## Sequence: refactor with invariants (patterns + tests)

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

Constraints:
- no public API changes
- no behavior changes (unless explicitly called out and tested)
- keep the diff reasonably small (avoid large renames/moves)

Deliverables:
- refactor implementation
- tests updated/added only to preserve behavior
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

## Sequence: observability fixes (logs/metrics/traces/dashboards)

### Kickoff (dashboards/logs/traces missing)

```text
Skills (optional): apply-structural-patterns, consumer-test-coverage

Our observability is missing <logs/metrics/traces/dashboards>. Please fix what’s wrong end-to-end.

Approach:
- use the repo’s production-like environment (containers/k8s/etc.) to reproduce
- use logs to identify ingestion/export errors
- fix the minimal set of config/instrumentation needed (agents/collectors/exporters/dashboards)

Deliverables:
- working dashboards/panels
- any config changes required
- a short “how to verify” checklist (what to click/run to see data)
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
