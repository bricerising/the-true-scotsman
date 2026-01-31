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

## Using these skills (prompting)

Each folder contains a `SKILL.md` playbook. To get an agent to apply one, **name the skill explicitly** in your prompt and give it enough context (files, constraints, acceptance criteria).

### Example prompts

These are copy/paste prompts that demonstrate how to invoke the skills in this repo: tight scope + explicit constraints + a verification loop.

**1) Safe “cleanup refactor” quickstart (no user input required)**  
Use when you just want to see this repo in action: the agent chooses 1–3 high-impact areas, adds characterization tests, refactors, and iterates until checks are green.

```
Skills (in order): typescript-style-guide (if TS), consumer-test-coverage
Goal: do a safe “clean up” refactor to reduce complexity in the most problematic TypeScript area(s) without changing behavior.
Selection: pick 1–3 targets under `src/` based on size/complexity/churn; tell me which you picked and why.
Constraints: no public API changes; no behavior changes; avoid broad renames/moves; no new deps
Autonomy: proceed without asking for confirmation between steps; ask only when blocked
Approach: add/adjust characterization tests first (consumer-visible), then refactor, then re-run tests and iterate until green
Verification: <test/lint/build commands>
Done when: <commands> are green and the refactor is explained in a short summary (what changed + why it’s safer now)
```

**2) Wrap an interface without changing it (choose a pattern, then apply it)**  
Use when you need to add behavior like caching/retries/logging without changing the public interface. The agent picks the smallest fitting pattern, implements it, and pins the behavior with contract-level tests.

```
Skills (in order): select-design-pattern, apply-structural-patterns, consumer-test-coverage
Goal: add <caching/logging/retries/rate limiting> around <interface> without changing its public contract.
Constraints: preserve error semantics; keep selection/ordering rules explicit; keep diff reviewable
Deliverables: wrapper implementation + consumer-visible tests (hit/miss, retry limits, etc.) + a short usage example
Verification: <test/lint/build commands>
Done when: <commands> are green and tests pin the documented contract at the boundary
Context: <interface path + key call sites + perf/UX constraints>
```

**3) Spec-driven feature implementation (TypeScript + tests)**  
Use when you have a spec/issue and want the agent to implement it with explicit boundaries (validate inputs, model expected failures) and consumer-visible tests.

```
Skills (in order): typescript-style-guide (if TS), consumer-test-coverage
Goal: implement <feature> described in <spec/issue> with a clean boundary (validate external inputs; explicit errors).
Scope: in-scope <paths>; out-of-scope <paths>
Constraints: preserve public APIs; small diff; no hidden globals; no new deps (unless necessary)
Autonomy: proceed without asking between steps; ask only when blocked
Verification: <test/lint/build commands>
Done when: <commands> are green and the feature works end-to-end in the repo’s most production-like local setup
Context: <files/spec/logs>
```

For more templates and reusable prompt sequences, see [`PROMPTS.md`](PROMPTS.md).

## Philosophy

These skills bias toward practices that make codebases easier for humans to operate over time:

- Prefer clarity over cleverness; optimize for the next reader.
- Make boundaries explicit; validate external inputs at the edges.
- Keep dependencies and lifetimes explicit; avoid hidden globals.
- Treat expected failures as data (typed results) instead of exceptions.
- Use design patterns as names for proven structures, not as goals.

## Install & integrate

This repo is designed to be used directly with **Codex CLI**, but you can also integrate it with other popular code assistants by copying/linking the relevant guides into their “project rules / instructions” mechanism.

### Quick install (idempotent)

From this repo root:

```sh
# Install into Codex + Claude skill dirs (symlinks by default)
bash scripts/install.sh --all

# If your environment doesn't like symlinks
bash scripts/install.sh --all --method copy
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

Then either:

- Reference files like `tools/the-true-scotsman/typescript-style-guide/SKILL.md` in your assistant’s project instructions, or
- Generate tool instruction files in your project (Codex/Claude/Cursor/Copilot):

```sh
bash tools/the-true-scotsman/scripts/generate-project-rules.sh --project-dir . --tool all --force
```

This generates:

- `.codex/AGENTS.md`
- `.claude/AGENTS.md`
- `.cursorrules`
- `.github/copilot-instructions.md`

To quickly decide which skill(s) to load for a task:

```sh
python3 tools/the-true-scotsman/scripts/recommend-skills.py --project-dir . --prompt "<your prompt>"
```

## Growing this repo

The intent is to expand beyond TypeScript into more stacks over time (e.g., Go, Python, Rust, Java, frontend frameworks, data tooling). New additions will generally take the form of:

- a `*-style-guide/` skill for a language/framework, plus
- `references/` and `references/snippets/` for copyable patterns and examples.

## Contributing

If you add a new skill:

1. Create a new folder with a `SKILL.md` containing YAML frontmatter (`name`, `description`).
2. Keep it concise: workflows, checklists, and minimal examples beat long essays.
3. Prefer reusable snippets/templates over prose where it helps agents apply guidance consistently.

### Validation

Run `bash scripts/validate-skills.sh` (also runs in CI) to ensure:
- every `*/SKILL.md` has frontmatter and stays small,
- `README.md` stays in sync with the skill directories,
- `skills-config.json` stays consistent with the repo.

## Docs

- `ARCHITECTURE.md`: repo structure + how the scripts work
- `ANTI_PATTERNS.md`: common failure modes when writing skills (and what not to teach)
- `SUCCESS_METRICS.md`: how to tell whether the skills are helping
