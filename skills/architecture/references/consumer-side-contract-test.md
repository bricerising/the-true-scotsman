# Consumer-side contract test

## Intent
Have the consumer define and run tests that assert the provider’s API/contract meets the consumer’s expectations.

## Use when
- Multiple consumers depend on a provider and breaking changes are costly.
- You want fast feedback on compatibility without full end-to-end environments.

## Avoid / watch-outs
- Contracts must be managed intentionally (versioning, publishing, ownership).
- Avoid over-specifying implementation details; focus on consumer-visible semantics.

## Skill mapping
- `spec`: treat contracts as source-of-truth (schemas, error semantics, compatibility rules).
- `testing`: add consumer-focused contract tests and keep them stable.
