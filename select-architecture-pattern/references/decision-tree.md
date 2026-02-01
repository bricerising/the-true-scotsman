# System Pattern Decision Tree (Pressure → Pattern → Risks)

Use this when a change crosses service/process boundaries and you need a defensible “why this pattern?” answer.

Rule: pick **one primary pressure**, then choose **one primary pattern** and 0–2 supporting patterns.

## 1) Reliability under partial failure

**Pressure**: dependency timeouts/flakiness, cascading failures, long tails, rate limits.

**Candidate patterns**:

- Time budgets + cancellation propagation (baseline)
- Retry with backoff+jitter (only when safe)
- Idempotency + dedupe (required for retries / at-least-once)
- Circuit breaker (stop cascades)
- Bulkheads (isolate resource pools)
- Load shedding / rate limiting

**Primary risks / anti-patterns**:

- Retries without idempotency (duplicate writes, amplification storms)
- Unbounded timeouts (requests pile up, saturate pools)
- Breakers without fallbacks/UX plan (hard failures surprise consumers)

**Related skills**: `apply-resilience-patterns`, `shared-platform-library`, `apply-observability-patterns`.

## 2) Cross-service workflow (multi-step business process)

**Pressure**: one business action spans multiple services and must handle partial failure.

**Candidate patterns**:

- Saga (with compensations)
  - Orchestration (central coordinator)
  - Choreography (events drive transitions)
- Outbox/inbox for reliable event emission + consumption (often supporting)

**Primary risks / anti-patterns**:

- Using a saga to “fake” a distributed transaction (no compensations, no idempotency)
- Missing explicit state machine (workflow becomes implicit and un-debuggable)
- No correlation IDs across steps (ops can’t trace a business action)

**Related skills**: `select-design-pattern` (state machine), `apply-resilience-patterns`, `apply-observability-patterns`, `consumer-test-coverage`.

## 3) Consistency + read scalability pressure

**Pressure**: read models need to scale independently, or read latency differs from write latency, or denormalization is required.

**Candidate patterns**:

- CQRS (separate command/write from query/read)
- Read replicas / cache-aside (supporting tactics; not always “a pattern decision”)

**Primary risks / anti-patterns**:

- CQRS without clear ownership of invariants (writes become inconsistent)
- “Eventually consistent” without product acceptance criteria (surprises users)

**Related skills**: `spec-driven-development` (acceptance + NFRs), `consumer-test-coverage`.

## 4) Auditability / rebuild / temporal correctness

**Pressure**: you must reconstruct past state, support audits, or model a temporal domain.

**Candidate patterns**:

- Event sourcing (events as source of truth)
- Append-only ledger (simpler variant in many domains)

**Primary risks / anti-patterns**:

- Event sourcing for CRUD apps without real audit/temporal need
- Underestimating schema evolution and projection rebuild costs

**Related skills**: `spec-driven-development` (contract/versioning), `apply-observability-patterns` (replay/run observability).

## 5) Integration / migration / legacy pressure

**Pressure**: you must change a legacy system without a flag day.

**Candidate patterns**:

- Strangler Fig (incremental migration)
- Anti-corruption layer (translation boundary)
- API Gateway / BFF (shape/aggregate APIs for clients)

**Primary risks / anti-patterns**:

- Gateways becoming “smart monoliths” (domain logic in gateway)
- No deprecation plan / contract versioning

**Related skills**: `spec-driven-development`, `shared-platform-library`.

## 6) Decoupling + fan-out (event-driven)

**Pressure**: many consumers need the same business fact; you need async decoupling.

**Candidate patterns**:

- Pub/Sub (events)
- Transactional outbox + idempotent consumer (inbox)
- Backpressure / rate controls (supporting)

**Primary risks / anti-patterns**:

- Treating pub/sub like RPC (“it must be immediate and exactly-once”)
- No idempotency/dedupe strategy (duplicates break invariants)
- No dead-letter/quarantine plan for poison messages

**Related skills**: `apply-resilience-patterns`, `apply-observability-patterns`, `consumer-test-coverage`.

## 7) Coordination / exclusivity / scale

**Pressure**: only one worker should do a thing, or work must be partitioned.

**Candidate patterns**:

- Leader election (single coordinator)
- Sharding / partitioning (scale out)
- Actor model (isolate state + concurrency)

**Primary risks / anti-patterns**:

- Leader election without fencing (split brain)
- Sharding without consistent routing keys and rebalancing plan

**Related skills**: `spec-driven-development` (ownership, invariants).

## Compact Anti-Pattern Guardrails

- **Retries without idempotency**: never.
- **Saga misuse**: don’t use saga for simple CRUD; do use it when compensations are real and modeled.
- **Event sourcing misuse**: don’t use it to “sound advanced”; use it when audit/temporal requirements demand it.
- **Pattern soup**: if you can’t explain the primary pressure in one sentence, stop and re-scope.

