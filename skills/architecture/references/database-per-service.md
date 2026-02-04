# Database per service

## Intent
Make each service the exclusive owner of its data store to reduce coupling and enable independent evolution.

## Use when
- You want clear ownership boundaries and independent deployability.
- You can tolerate eventual consistency for cross-service reporting and workflows.

## Avoid / watch-outs
- Cross-service queries become harder; use API composition or CQRS/read models instead of shared tables.
- Be explicit about integration semantics (events vs RPC) and data duplication rules.

## Skill mapping
- `architecture`: define data ownership and integration style (events/RPC).
- `spec`: document data contracts/events and consistency expectations.
- `testing`: tests that pin consumer-visible behavior under eventual consistency.
