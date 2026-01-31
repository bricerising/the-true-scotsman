# Success metrics

This repo is “working” when it reliably improves the *human* experience of changing a codebase, not when it produces the most code.

## Leading indicators (fast feedback)

- **Time to green**: agent iterations converge quickly to passing `test/lint/build` commands.
- **Reviewability**: diffs stay small, focused, and easy to reason about.
- **Boundary clarity**: changes introduce or improve explicit input validation and typed/structured failures at edges.
- **Test quality**: added tests assert consumer-visible behavior and reduce regressions without mocking internals.

## Lagging indicators (outcomes)

- **Regression rate**: fewer production bugs / fewer “same bug returns” incidents after agent-assisted changes.
- **Onboarding speed**: new engineers can find patterns quickly and apply them consistently.
- **Change velocity**: teams can modify core logic with less fear (smaller, safer refactors).

## Repo-specific quality checks

- Skills stay small (`SKILL.md` is kept under the line limit; detail lives in `references/`).
- Cross-language guidance stays consistent with `.github/theme-coherence.theme.md`.
- Scripts remain deterministic and runnable without network access.

