# Domain-specific protocol

## Intent
Define a protocol/schema that models domain concepts explicitly (instead of “generic” messages) to reduce ambiguity and drift.

## Use when
- You have multiple services interacting in a domain and want stable, explicit semantics.
- Generic protocols create accidental coupling or confusion (fields mean different things to different teams).

## Avoid / watch-outs
- Version deliberately; avoid breaking consumers with incompatible schema changes.
- Keep the protocol tied to a bounded context; don’t force one model across all contexts.

## Skill mapping
- `spec`: contracts, versioning rules, and compatibility expectations.
- `architecture`: bounded contexts and translations (anti-corruption layers where needed).
- `testing`: contract tests and schema-compatibility checks where available.
