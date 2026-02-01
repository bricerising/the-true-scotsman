# enterprise-software-playbook

This repo is an opinionated set of **agent skills** meant to drive cohesive, high-quality **enterprise software**: readable, maintainable, testable, and safe to change.

Each skill is a small, self-contained playbook (workflow + checklists + examples) stored in a `SKILL.md` file. Most skills are language-agnostic; TypeScript is currently the only language-specific style guide.

## Scope (and non-goals)

This playbook is optimized for **enterprise web apps**, especially:

- HTTP/gRPC services, background jobs, and event consumers
- Multi-service systems with reliability/consistency pressures

Non-goals:

- A framework-specific “how to build a React app” guide
- A complete performance tuning handbook (use it selectively, case-by-case)

## What you get

- A default workflow that keeps changes cohesive: **Define → Standardize → Harden → Verify → Mechanics**
- A small library of composable playbooks (“skills”) that an assistant can auto-apply
  - Skills are supported by coding agents like **Codex CLI** and **Claude Code** (and can be vendored into any repo)
- Copy/paste prompt recipes in [`PROMPTS.md`](PROMPTS.md)
- An adoption template for app repos: [`specs/templates/app-repo/AGENTS.md`](specs/templates/app-repo/AGENTS.md)

## 60-second start

1. Install the skills (pick one): [Codex CLI](#codex-cli), [Claude Code](#claude-code), or [vendor via submodule](#tool-agnostic-vendor-it-into-your-project).
2. Add agent instructions to your app repo (start from [`specs/templates/app-repo/AGENTS.md`](specs/templates/app-repo/AGENTS.md)).
3. Paste the “Conversational bootstrap” from [`PROMPTS.md`](PROMPTS.md#conversational-bootstrap-auto-route).

You do **not** need to read this repo cover-to-cover. Start with the three steps above, then open the specific `*/SKILL.md` playbook(s) you need as you go.

Minimal “try it now” prompt:

```text
Use enterprise-web-app-workflow (read enterprise-web-app-workflow/SKILL.md).

Please review this enterprise web application.
```

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
- [`apply-security-patterns/`](apply-security-patterns/SKILL.md): Authn/authz, input validation, injection safety, secrets, SSRF guardrails.
- [`apply-observability-patterns/`](apply-observability-patterns/SKILL.md): Logs/metrics/traces correlation, RED metrics, dashboards/alerts, verification steps.
- [`observability-triage/`](observability-triage/SKILL.md): Debug workflows (log → trace → metrics) for incidents, regressions, and SLO violations.

**Verify (prove behavior)**

- [`consumer-test-coverage/`](consumer-test-coverage/SKILL.md): Consumer-focused tests that raise coverage without asserting implementation details.

**Mechanics (in-process building blocks)**

- [`apply-creational-patterns/`](apply-creational-patterns/SKILL.md): Factory Method, Abstract Factory, Builder, Prototype, and (careful) Singleton.
- [`apply-structural-patterns/`](apply-structural-patterns/SKILL.md): Adapter, Bridge, Composite, Decorator, Facade, Flyweight, and Proxy.
- [`apply-behavioral-patterns/`](apply-behavioral-patterns/SKILL.md): Chain of Responsibility, Command, Iterator, Mediator, Memento, Observer, State, Strategy, Template Method, and Visitor.

## Using these skills

Each folder contains a `SKILL.md` playbook. The primary mode is **conversational**: ask for what you want and let the agent auto-select the right skills. If you want deterministic control, name specific skills explicitly.

For more prompt recipes (including a conversational bootstrap), see [`PROMPTS.md`](PROMPTS.md).

## Philosophy

These skills bias toward practices that make codebases easier for humans to operate over time:

- Prefer clarity over cleverness; optimize for the next reader.
- Make boundaries explicit; validate external inputs at the edges.
- Keep dependencies and lifetimes explicit; avoid hidden globals.
- Treat expected failures as data (typed results) instead of exceptions.
- Use design patterns as names for proven structures, not as goals.

## Docs

- Prompt recipes: [`PROMPTS.md`](PROMPTS.md)
- Glossary (for less familiar terms): [`GLOSSARY.md`](GLOSSARY.md)
- Example walkthrough: [`TUTORIAL.md`](TUTORIAL.md)
- Repo-level specs (source of truth): [`specs/000-index.md`](specs/000-index.md)
- App-repo integration: [`specs/005-application-integration.md`](specs/005-application-integration.md)
- App-repo agent instructions template: [`specs/templates/app-repo/AGENTS.md`](specs/templates/app-repo/AGENTS.md)

## Install & integrate

This repo is designed to be used directly with **Codex CLI**, but you can also integrate it with other popular code assistants by copying/linking the relevant guides into their “project rules / instructions” mechanism.

### Codex CLI

Codex CLI is OpenAI’s terminal-based coding agent: https://github.com/openai/codex

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

Claude Code is Anthropic’s terminal-based coding agent: https://docs.anthropic.com/en/docs/claude-code

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

## Terminology

- **Code patterns**: in-process patterns (classic creational/structural/behavioral patterns, mostly GoF).
- **System patterns**: cross-process patterns (architecture/distributed-systems/ops) that deal with failure, consistency, and integration seams.
- **Operational patterns**: repeatable workflows and cross-cutting policies that make delivery + operations predictable (spec bundles, shared platform primitives, tests, observability, resilience).

The skill list above is grouped by **workflow stage** (Define/Standardize/Harden/Verify/Mechanics), not by scope.

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) and the backlog in [`specs/tasks.md`](specs/tasks.md).

## Feedback

If you try this playbook in a real codebase, feedback is extremely valuable:

- Use GitHub Issues for bugs, confusing docs, and feature requests.
- Include the prompt you used and what you expected vs what happened.
