# the-true-scotsman

> “No *true* Scotsman would write code like that.”

This repo is a tongue-in-cheek set of **agent skills** meant to teach code assistants to write what humans tend to consider **clean code**: readable, maintainable, testable, and safe to change.

Each skill is a small, self-contained playbook (workflow + checklists + examples) stored in a `SKILL.md` file. Some skills include **language/framework snippets** and **style guides** so an agent can apply the ideas consistently across stacks.

## What’s in here

- `typescript-style-guide/`: A practical TypeScript style guide focused on runtime safety, explicit boundaries, typed errors, and maintainable module structure.
- `select-design-pattern/`: A decision workflow for picking the *simplest* GoF pattern that fits the pressure (creation/structure/behavior).
- `apply-creational-patterns/`: How to apply Factory Method, Abstract Factory, Builder, Prototype, and (careful) Singleton.
- `apply-structural-patterns/`: How to apply Adapter, Bridge, Composite, Decorator, Facade, Flyweight, and Proxy.
- `apply-behavioral-patterns/`: How to apply Chain of Responsibility, Command, Iterator, Mediator, Memento, Observer, State, Strategy, Template Method, and Visitor.
- `consumer-test-coverage/`: Guidance for adding consumer-focused tests that raise coverage without asserting implementation details.

## Philosophy

These skills bias toward practices that make codebases easier for humans to operate over time:

- Prefer clarity over cleverness; optimize for the next reader.
- Make boundaries explicit; validate external inputs at the edges.
- Keep dependencies and lifetimes explicit; avoid hidden globals.
- Treat expected failures as data (typed results) instead of exceptions.
- Use design patterns as names for proven structures, not as goals.

## Install & integrate

This repo is designed to be used directly with **Codex CLI**, but you can also integrate it with other popular code assistants by copying/linking the relevant guides into their “project rules / instructions” mechanism.

## Using these skills (prompting)

Each folder contains a `SKILL.md` playbook. To get an agent to apply one, **name the skill explicitly** in your prompt and give it enough context (files, constraints, acceptance criteria).

### Prompt template

```
Use <skill-name> to <goal>.
Constraints: <what must not change>.
Acceptance: <tests/behavior you want preserved>.
Context: <relevant files, snippets, error logs>.
```

### Copy/paste prompts

#### Scaffold a new app (`typescript-style-guide`)

```
Use typescript-style-guide to scaffold a new Node.js + TypeScript REST API.
Requirements:
- `/health` endpoint
- `/v1/users` CRUD endpoints with request/response runtime validation (e.g. Zod)
- env config decoded from `unknown` (no direct `process.env` reads outside config module)
- explicit composition root (resources created in `src/main.ts`, with clean shutdown)
- typed errors (no throwing for expected failures)
Deliverables:
- file tree + all source files
- `package.json`, `tsconfig.json`, minimal tooling
- tests for validators + one handler integration test
Constraints: keep it simple; no DI framework; no classes for data.
```

```
Use typescript-style-guide to build a TypeScript CLI called `log-summarize`.
Behavior:
- reads a log file path from argv
- parses JSON lines, groups by `level` and `service`, prints a summary table
- validates inputs and reports friendly, typed errors (no uncaught throws)
Deliverables: project structure, implementation, and a few unit tests for parsing + formatting.
```

```
Use typescript-style-guide to scaffold a small React + TypeScript app (Vite is fine) that:
- fetches `/api/todos`
- validates API responses at the boundary (treat as `unknown`)
- keeps UI state modeled as a discriminated union (`loading` | `ready` | `error`)
Deliverables: minimal components, a typed API client module, and tests for the decoder.
```

#### Refactors (`typescript-style-guide`)

```
Use typescript-style-guide to refactor our config loading so all env vars are decoded/validated from `unknown`,
and the rest of the app never reads `process.env` directly. Keep the public API unchanged and add unit tests.
Context: `src/config.ts`, `src/main.ts`, and any modules that read env vars.
```

```
Use typescript-style-guide to refactor error handling to be “throwless” in domain/application code:
- replace `throw` for expected failures with a typed result (discriminated union)
- convert errors at boundaries (HTTP handlers / CLI entrypoints)
Constraints: don’t change externally-visible error messages/status codes. Add tests for the new error paths.
```

```
Use typescript-style-guide to break a cyclic dependency between `src/domain/*` and `src/infra/*`.
Constraints: preserve behavior; do not add a DI container; prefer interfaces + adapters; add a regression test.
Context: include the import cycle output from your tooling and the relevant files.
```

#### Choose a pattern (`select-design-pattern`)

```
Use select-design-pattern: I’m adding “exporters” for multiple formats (CSV, JSON, PDF) with different setup
requirements and runtime selection per request. Recommend the smallest GoF pattern(s), explain tradeoffs,
and sketch the target module structure + interfaces.
Context: current code is `src/export/*` with `switch(format)` in multiple places.
```

#### Implement the chosen creation approach (`apply-creational-patterns`)

```
Use apply-creational-patterns to refactor `EmailClient` construction so callers don’t know about transport
details (SMTP vs SES). Prefer Factory Method or Abstract Factory; keep call sites minimal; add tests.
```

```
Use apply-creational-patterns to create a provider-agnostic `PaymentsClient` with Stripe + Adyen support.
Requirements:
- runtime selection based on config/env
- shared interface for `authorize`, `capture`, `refund`
- test doubles for unit tests (no network)
Deliverables: factory/factories, interfaces, and tests.
```

#### Add behavior without changing interfaces (`apply-structural-patterns`)

```
Use apply-structural-patterns to add caching around `UserProfileService` without changing its interface.
I want a Proxy or Decorator with TTL + cache key strategy and tests for cache hits/misses.
```

```
Use apply-structural-patterns to add structured logging and timing around `OrderService` calls without
changing its interface. Prefer Decorator; include log fields and tests asserting observable behavior.
```

#### Make logic pluggable (`apply-behavioral-patterns`)

```
Use apply-behavioral-patterns to make pricing rules pluggable. Implement Strategy so we can swap algorithms
per customer tier, and add tests proving selection + edge cases.
```

```
Use apply-behavioral-patterns to turn our request middleware into a Chain of Responsibility:
- auth -> validation -> handler -> error mapping
Constraints: keep current HTTP semantics; add tests for ordering and short-circuiting.
```

#### Add high-signal tests (`consumer-test-coverage`)

```
Use consumer-test-coverage to add tests for the `POST /v1/orders` endpoint:
- assert response shape + status codes for success and validation failures
- cover one unhappy-path (e.g. downstream timeout) as seen by the client
- avoid asserting internal function calls or DB implementation details
Context: include the router/handler entrypoint and how to start the app in test.
```

### End-to-end prompt (combine skills)

```
Use these skills in order: select-design-pattern, apply-structural-patterns, consumer-test-coverage.
Goal: add request-level caching for `GET /v1/users/:id` without changing the handler signature.
Constraints: preserve HTTP semantics; TTL=60s; cache key includes auth tenant; no global singletons.
Deliverables: recommended pattern + implementation + tests that assert client-visible behavior.
```

### Codex CLI (skills)

1. Clone this repo anywhere you like.
2. Symlink (or copy) the skill folders into `$CODEX_HOME/skills` (commonly `~/.codex/skills`).

Example (symlinks):

```sh
git clone <this-repo-url> ~/the-true-scotsman
mkdir -p ~/.codex/skills
ln -s ~/the-true-scotsman/{apply-*,consumer-test-coverage,select-design-pattern,typescript-style-guide} ~/.codex/skills/
```

### Claude Code

1. Clone this repo anywhere you like.
2. Symlink (or copy) the skill folders into `~/.claude/skills`.

Example (symlinks):

```sh
git clone <this-repo-url> ~/the-true-scotsman
mkdir -p ~/.claude/skills
ln -s ~/the-true-scotsman/{apply-*,consumer-test-coverage,select-design-pattern,typescript-style-guide} ~/.claude/skills/
```

### Tool-agnostic: vendor it into your project

Many assistants can only reliably follow rules that live *inside the repo they’re editing*. A simple approach is to add this repo as a submodule (or just copy the files), then point your assistant at the specific skill(s) you want.

```sh
git submodule add <this-repo-url> tools/the-true-scotsman
```

Then reference files like `tools/the-true-scotsman/typescript-style-guide/SKILL.md` in your assistant’s project instructions.

## Growing this repo

The intent is to expand beyond TypeScript into more stacks over time (e.g., Go, Python, Rust, Java, frontend frameworks, data tooling). New additions will generally take the form of:

- a `*-style-guide/` skill for a language/framework, plus
- `references/` and `references/snippets/` for copyable patterns and examples.

## Contributing

If you add a new skill:

1. Create a new folder with a `SKILL.md` containing YAML frontmatter (`name`, `description`).
2. Keep it concise: workflows, checklists, and minimal examples beat long essays.
3. Prefer reusable snippets/templates over prose where it helps agents apply guidance consistently.
