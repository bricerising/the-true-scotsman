# Anti-patterns

This repo is meant to be used by agents under tight context windows. The most common failure modes are “more content” and “more opinions” instead of more *actionable* guidance.

## Skill authoring anti-patterns

- **Essay skills**: long prose without a workflow/checklist. If it can’t be applied in 10 minutes, it belongs in `references/`.
- **No progressive disclosure**: expecting the agent to read multiple skills and all references up front.
- **Frontmatter drift**: missing `name`/`description`, or a `name` that doesn’t match the directory.
- **Ambiguous ordering**: guidance that requires “pattern selection” but doesn’t route the reader through `select-design-pattern` first.
- **Over-prescription**: “always do X” rules that ignore context (constraints, runtime, consumers, team norms).
- **Contradicting the repo’s core stance**: especially around explicit boundaries, explicit dependencies, explicit errors, and explicit lifetimes.

## Implementation anti-patterns (what not to teach)

- **Hidden I/O and globals**: implicit environment reads, singleton mutation, or “magic” containers with unclear lifetimes.
- **Throwing for expected failures**: using exceptions/panics as routine branching in domain logic.
- **Testing internals instead of seams**: brittle unit tests that assert private methods, call order, or mocks instead of consumer-visible behavior.
- **Pattern decoration**: introducing GoF patterns to look “architectural” instead of to solve a concrete pressure.
- **Framework “special pleading”**: claiming a framework forces poor practices when the idiomatic solution can preserve the repo’s principles.

## Repo maintenance anti-patterns

- **Unvalidated changes**: adding skills/scripts without updating `skills-config.json` and running `bash scripts/validate-skills.sh`.
- **One-off tooling**: scripts that only work on the author’s machine, require network access, or silently mutate user environments.

