# the-true-scotsman

> “No *true* Scotsman would write code like that.”

This repo is a tongue-in-cheek set of **agent skills** meant to teach code assistants to write what humans tend to consider **clean code**: readable, maintainable, testable, and safe to change.

The name is a joke on the “No true Scotsman” fallacy: there will always be someone who declares your code “not *really* clean.” These skills are an attempt to encode the *practical*, human-aligned habits that usually survive that argument in real codebases.

Each skill is a small, self-contained playbook (workflow + checklists + examples) stored in a `SKILL.md` file. Some skills include **language/framework snippets** and **style guides** so an agent can apply the ideas consistently across stacks.

## What’s in here

- `typescript-style-guide/`: A practical TypeScript style guide focused on runtime safety, explicit boundaries, typed errors, and maintainable module structure.
- `select-design-pattern/`: A decision workflow for picking the *simplest* GoF pattern that fits the pressure (creation/structure/behavior).
- `apply-creational-patterns/`: How to apply Factory Method, Abstract Factory, Builder, Prototype, and (careful) Singleton.
- `apply-structural-patterns/`: How to apply Adapter, Bridge, Composite, Decorator, Facade, Flyweight, and Proxy.
- `apply-behavioral-patterns/`: How to apply Chain of Responsibility, Command, Iterator, Mediator, Memento, Observer, State, Strategy, Template Method, and Visitor.
- `consumer-test-coverage/`: Guidance for adding consumer-focused tests that raise coverage without asserting implementation details.

## Install & integrate

This repo is designed to be used directly with **Codex CLI**, but you can also integrate it with other popular code assistants by copying/linking the relevant guides into their “project rules / instructions” mechanism.

### Tool-agnostic (recommended): vendor it into your project

Many assistants can only reliably follow rules that live *inside the repo they’re editing*. A simple approach is to add this repo as a submodule (or just copy the files), then point your assistant at the specific skill(s) you want.

```sh
git submodule add <this-repo-url> tools/the-true-scotsman
```

Then reference files like `tools/the-true-scotsman/typescript-style-guide/SKILL.md` in your assistant’s project instructions.

### Codex CLI (skills)

1. Clone this repo anywhere you like.
2. Symlink (or copy) the skill folders into `$CODEX_HOME/skills` (commonly `~/.codex/skills`).

Example (symlinks):

```sh
git clone <this-repo-url> ~/the-true-scotsman
mkdir -p ~/.codex/skills
ln -s ~/the-true-scotsman/{apply-*,consumer-test-coverage,select-design-pattern,typescript-style-guide} ~/.codex/skills/
```

Usage: in a Codex session, invoke a skill by name in your prompt, e.g. `$typescript-style-guide`.

### GitHub Copilot Chat (VS Code / JetBrains)

Copilot supports “custom instructions” (the exact UI/file name varies by editor/version). The usual pattern is:

1. Create a project instruction file (often under `.github/`) or set workspace instructions in your editor settings.
2. Add a short “rule” that tells Copilot which guide(s) to follow.

Starter snippet:

```md
Follow the-true-scotsman guidelines.
When writing TypeScript, apply `typescript-style-guide/SKILL.md`.
Prefer explicit boundaries, typed errors, and small functions.
```

### Cursor

Add Cursor project rules (commonly via a `.cursorrules` file or the editor’s “Rules” UI) and paste the relevant guidance (for example, the TypeScript style guide’s “Workflow” + “Guidelines” sections).

### Claude Code

Add a project instructions file (commonly `CLAUDE.md`) with the relevant rules (same idea as Cursor). Keep it short and point to the specific skill file(s) you want it to follow.

### Continue.dev / other assistants

If your tool supports a repo-level “rules/instructions” file or a “system prompt” configuration, copy in the relevant guidance from the skill you want (start with `typescript-style-guide/SKILL.md`).

If it supports “always include these files as context”, include one or more of:

- `typescript-style-guide/SKILL.md`
- `apply-*/SKILL.md`
- `select-design-pattern/SKILL.md`

## Philosophy

These skills bias toward practices that make codebases easier for humans to operate over time:

- Prefer clarity over cleverness; optimize for the next reader.
- Make boundaries explicit; validate external inputs at the edges.
- Keep dependencies and lifetimes explicit; avoid hidden globals.
- Treat expected failures as data (typed results) instead of exceptions.
- Use design patterns as names for proven structures, not as goals.

## Growing this repo

The intent is to expand beyond TypeScript into more stacks over time (e.g., Go, Python, Rust, Java, frontend frameworks, data tooling). New additions will generally take the form of:

- a `*-style-guide/` skill for a language/framework, plus
- `references/` and `references/snippets/` for copyable patterns and examples.

## Contributing

If you add a new skill:

1. Create a new folder with a `SKILL.md` containing YAML frontmatter (`name`, `description`).
2. Keep it concise: workflows, checklists, and minimal examples beat long essays.
3. Prefer reusable snippets/templates over prose where it helps agents apply guidance consistently.
