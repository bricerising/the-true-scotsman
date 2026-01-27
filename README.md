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
