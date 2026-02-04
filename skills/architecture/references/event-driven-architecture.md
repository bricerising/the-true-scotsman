# Event-driven architecture

## Intent
Integrate services by publishing and consuming events rather than synchronous request/response calls.

## Use when
- You can tolerate eventual consistency and want to decouple services temporally.
- You have fan-out consumers (many subscribers to the same business facts).

## Avoid / watch-outs
- Avoid treating events like RPC (“must be immediate and exactly-once”); design for retries and duplicates.
- Define contracts and schema evolution; uncontrolled event changes break consumers.

## Skill mapping
- `architecture`: decide orchestration vs choreography; choose outbox vs CDC.
- `spec`: event contracts, compatibility rules, and NFRs (ordering, durability).
- `resilience`: idempotent consumption, DLQs/quarantine, bounded retries.
- `observability`: lag metrics, correlation IDs, and message-type span attributes.
