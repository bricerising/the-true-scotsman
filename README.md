# enterprise-software-playbook

This repo is an opinionated set of **agent skills** meant to drive cohesive, high-quality **enterprise software**: readable, maintainable, testable, and safe to change.
(An “agent” here is an AI coding assistant; a “skill” is a small playbook it can follow.)

Each skill is a small, self-contained playbook (workflow + checklists + examples) stored in a `SKILL.md` file. Some skills include **language/framework snippets** and **style guides** so an agent can apply the ideas consistently across stacks.

Repo-level specs live in `specs/` (start at [`specs/000-index.md`](specs/000-index.md)). For adopting this library into an application repo, see [`specs/005-application-integration.md`](specs/005-application-integration.md) and [`specs/templates/app-repo/AGENTS.md`](specs/templates/app-repo/AGENTS.md).

Prompt recipes live in [`PROMPTS.md`](PROMPTS.md).

## What’s in here

**Define (what are we building?)**

- [`enterprise-web-app-workflow/`](enterprise-web-app-workflow/SKILL.md): Auto-route work across skills (conversational mode: choose appropriate skills even if the user doesn’t name them).
- [`spec-driven-development/`](spec-driven-development/SKILL.md): Write specs, contracts, plans, and task lists so agents converge on cohesive solutions.
- [`select-architecture-pattern/`](select-architecture-pattern/SKILL.md): Choose the smallest system pattern(s) for cross-service pressures.
- [`select-design-pattern/`](select-design-pattern/SKILL.md): Choose the smallest code pattern(s) for in-process design pressures.

**Standardize (make it consistent)**

- [`typescript-style-guide/`](typescript-style-guide/SKILL.md): TypeScript guidance focused on runtime safety, explicit boundaries, typed errors, and maintainable module structure.
- [`shared-platform-library/`](shared-platform-library/SKILL.md): Design and evolve a shared platform package (`packages/shared`) without becoming a “utils junk drawer”.

**Harden (make it survive reality)**

- [`apply-resilience-patterns/`](apply-resilience-patterns/SKILL.md): Timeouts, retries/backoff, idempotency, circuit breakers, bulkheads.
- [`apply-observability-patterns/`](apply-observability-patterns/SKILL.md): Logs/metrics/traces correlation, RED metrics, dashboards/alerts, verification steps.
- [`observability-triage/`](observability-triage/SKILL.md): Debug workflows (log → trace → metrics) for incidents, regressions, and SLO violations.

**Verify (prove behavior)**

- [`consumer-test-coverage/`](consumer-test-coverage/SKILL.md): Consumer-focused tests that raise coverage without asserting implementation details.

**Mechanics (in-process building blocks)**

- [`apply-creational-patterns/`](apply-creational-patterns/SKILL.md): Factory Method, Abstract Factory, Builder, Prototype, and (careful) Singleton.
- [`apply-structural-patterns/`](apply-structural-patterns/SKILL.md): Adapter, Bridge, Composite, Decorator, Facade, Flyweight, and Proxy.
- [`apply-behavioral-patterns/`](apply-behavioral-patterns/SKILL.md): Chain of Responsibility, Command, Iterator, Mediator, Memento, Observer, State, Strategy, Template Method, and Visitor.

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

Each folder contains a `SKILL.md` playbook. The primary mode is **conversational**: ask for what you want and let the agent auto-select the right skills. If you want deterministic control, name specific skills explicitly.

For more prompt recipes (including a conversational bootstrap), see [`PROMPTS.md`](PROMPTS.md).

### Quick start (adoption)

1. Install the skills (or vendor this repo) via **Install & integrate** below.
2. Add agent instructions to your app repo (start from [`specs/templates/app-repo/AGENTS.md`](specs/templates/app-repo/AGENTS.md)).
3. Start the session with the “Conversational bootstrap” in [`PROMPTS.md`](PROMPTS.md).

### Example prompts

Simply use the following prompt to get started. Provide feedback to direct the agent as necessary.

```
Please review this enterprise web application.
```

If you want deterministic routing via the auto-router skill:

```
Use enterprise-web-app-workflow.

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

Example (symlinks; installs every skill folder in this repo):

```sh
git clone https://github.com/bricerising/enterprise-software-playbook.git ~/enterprise-software-playbook
mkdir -p ~/.codex/skills
for f in ~/enterprise-software-playbook/*/SKILL.md; do
  ln -s "${f%/SKILL.md}" ~/.codex/skills/
done
```

### Claude Code

1. Clone this repo anywhere you like.
2. Symlink (or copy) the skill folders into your Claude Code skills directory (commonly `~/.claude/skills`).

Example (symlinks; installs every skill folder in this repo):

```sh
git clone https://github.com/bricerising/enterprise-software-playbook.git ~/enterprise-software-playbook
mkdir -p ~/.claude/skills
for f in ~/enterprise-software-playbook/*/SKILL.md; do
  ln -s "${f%/SKILL.md}" ~/.claude/skills/
done
```

### Tool-agnostic: vendor it into your project

Many assistants can only reliably follow rules that live *inside the repo they’re editing*. A simple approach is to add this repo as a submodule (or just copy the files), then point your assistant at the specific skill(s) you want.

```sh
git submodule add https://github.com/bricerising/enterprise-software-playbook.git tools/enterprise-software-playbook
```

Then reference files like `tools/enterprise-software-playbook/typescript-style-guide/SKILL.md` in your assistant’s project instructions.

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) and the backlog in [`specs/tasks.md`](specs/tasks.md).
