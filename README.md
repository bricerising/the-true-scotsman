# enterprise-software-playbook

This repo is an opinionated set of **agent skills** meant to drive cohesive, high-quality **enterprise software**: readable, maintainable, testable, and safe to change.

Each skill is a small, self-contained playbook (workflow + checklists + examples) stored in a `SKILL.md` file. Some skills include **language/framework snippets** and **style guides** so an agent can apply the ideas consistently across stacks.

Repo-level specs live in `specs/` (start at `specs/000-index.md`). For adopting this library into an application repo, see `specs/005-application-integration.md` and `specs/templates/app-repo/AGENTS.md`.

## What’s in here

**Define (what are we building?)**

- `enterprise-web-app-workflow/`: Auto-route work across skills (conversational mode: choose appropriate skills even if the user doesn’t name them).
- `spec-driven-development/`: Write specs, contracts, plans, and task lists so agents converge on cohesive solutions.
- `select-architecture-pattern/`: Choose the smallest system pattern(s) for cross-service pressures.
- `select-design-pattern/`: Choose the smallest code pattern(s) for in-process design pressures.

**Standardize (make it consistent)**

- `typescript-style-guide/`: TypeScript guidance focused on runtime safety, explicit boundaries, typed errors, and maintainable module structure.
- `shared-platform-library/`: Design and evolve a shared platform package (`packages/shared`) without becoming a “utils junk drawer”.

**Harden (make it survive reality)**

- `apply-resilience-patterns/`: Timeouts, retries/backoff, idempotency, circuit breakers, bulkheads.
- `apply-observability-patterns/`: Logs/metrics/traces correlation, RED metrics, dashboards/alerts, verification steps.

**Verify (prove behavior)**

- `consumer-test-coverage/`: Consumer-focused tests that raise coverage without asserting implementation details.

**Mechanics (in-process building blocks)**

- `apply-creational-patterns/`: Factory Method, Abstract Factory, Builder, Prototype, and (careful) Singleton.
- `apply-structural-patterns/`: Adapter, Bridge, Composite, Decorator, Facade, Flyweight, and Proxy.
- `apply-behavioral-patterns/`: Chain of Responsibility, Command, Iterator, Mediator, Memento, Observer, State, Strategy, Template Method, and Visitor.

## Terminology

- **Code patterns**: in-process patterns (classic creational/structural/behavioral patterns, mostly GoF).
- **System patterns**: cross-process patterns (architecture/distributed-systems/ops) that deal with failure, consistency, and integration seams.
- **Operational patterns**: repeatable workflows and cross-cutting policies that make delivery + operations predictable (spec bundles, shared platform primitives, tests, observability, resilience).

The skill list above is grouped by **workflow stage** (Define/Standardize/Harden/Verify/Mechanics), not by scope.

## A DDD lens (for organizing skills)

If you model a high-performing engineer as a domain-driven system, the “aggregate roots” this repo tries to standardize are:

- **Decision record**: pressure + constraints + chosen code/system pattern(s) + trade-offs + validation plan (drives alignment).
- **Spec bundle**: `spec.md` + `contracts/` + `plan.md` + `tasks.md` + `quickstart.md` (drives cohesion).
- **Boundary policy**: stable error semantics + time budgets + retries/idempotency + telemetry field contracts (drives operability).
- **Shared platform primitive**: one “golden path” wrapper/facade used by multiple services (drives consistency).
- **Verification loop**: consumer-visible tests + local verification steps/runbooks (drives confidence).

## Using these skills (prompting)

Each folder contains a `SKILL.md` playbook. The primary mode is **conversational**: ask for what you want and let the agent auto-select the right skills (or paste the “Conversational bootstrap” from `PROMPTS.md`). If you want deterministic control, name specific skills explicitly.

### Example prompts

Simply use the following prompt to get started. Provide feedback to direct the agent as necessary.

```
Please review this enterprise web application.
```

If you want it to build a feature, then just start explaining the feature.

## Philosophy

These skills bias toward practices that make codebases easier for humans to operate over time:

- Prefer clarity over cleverness; optimize for the next reader.
- Make boundaries explicit; validate external inputs at the edges.
- Keep dependencies and lifetimes explicit; avoid hidden globals.
- Treat expected failures as data (typed results) instead of exceptions.
- Use design patterns as names for proven structures, not as goals.

## Install & integrate

This repo is designed to be used directly with **Codex CLI**, but you can also integrate it with other popular code assistants by copying/linking the relevant guides into their “project rules / instructions” mechanism.

### Codex CLI (skills)

1. Clone this repo anywhere you like.
2. Symlink (or copy) the skill folders into `$CODEX_HOME/skills` (commonly `~/.codex/skills`).

Example (symlinks):

```sh
git clone <this-repo-url> ~/enterprise-software-playbook
mkdir -p ~/.codex/skills
ln -s ~/enterprise-software-playbook/{apply-*,consumer-test-coverage,select-design-pattern,typescript-style-guide} ~/.codex/skills/
```

### Claude Code

1. Clone this repo anywhere you like.
2. Symlink (or copy) the skill folders into `~/.claude/skills`.

Example (symlinks):

```sh
git clone <this-repo-url> ~/enterprise-software-playbook
mkdir -p ~/.claude/skills
ln -s ~/enterprise-software-playbook/{apply-*,consumer-test-coverage,select-design-pattern,typescript-style-guide} ~/.claude/skills/
```

### Tool-agnostic: vendor it into your project

Many assistants can only reliably follow rules that live *inside the repo they’re editing*. A simple approach is to add this repo as a submodule (or just copy the files), then point your assistant at the specific skill(s) you want.

```sh
git submodule add <this-repo-url> tools/enterprise-software-playbook
```

Then reference files like `tools/enterprise-software-playbook/typescript-style-guide/SKILL.md` in your assistant’s project instructions.

## Growing this repo

The intent is to expand beyond TypeScript into more stacks over time (e.g., Go, Python, Rust, Java, frontend frameworks, data tooling). New additions will generally take the form of:

- a `*-style-guide/` skill for a language/framework, plus
- `references/` and `references/snippets/` for copyable patterns and examples.

## Contributing

If you add a new skill:

1. Create a new folder with a `SKILL.md` containing YAML frontmatter (`name`, `description`).
2. Keep it concise: workflows, checklists, and minimal examples beat long essays.
3. Prefer reusable snippets/templates over prose where it helps agents apply guidance consistently.
