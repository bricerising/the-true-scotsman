# Command-side replica

## Intent
Replicate reference data into a command service so it can validate/execute commands without synchronous cross-service reads.

## Use when
- Command handling requires data owned elsewhere, and synchronous reads add latency/failure coupling.
- You can tolerate eventual consistency in replicated reference data.

## Avoid / watch-outs
- Clearly define staleness rules and how you resolve conflicts when the replica lags.
- Replication needs monitoring; stale replicas create subtle correctness bugs.

## Skill mapping
- `architecture`: pick replication mechanism (events/outbox/CDC) and ownership.
- `spec`: define staleness tolerance and conflict/validation semantics.
- `observability`: replica lag metrics and alerting.
- `testing`: tests for stale-data behavior and reconciliation paths.
