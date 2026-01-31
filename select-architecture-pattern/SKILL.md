---
name: select-architecture-pattern
description: Choose system patterns (architecture/distributed-systems/ops) for enterprise web apps. Use when designing or refactoring systems that span processes/services, need reliability under partial failure, require eventual consistency, or need clearer domain boundaries and integration seams.
---

# Select System Pattern (Architecture / Distributed Systems)

## Overview

Pick the smallest system/architecture pattern that addresses the pressure (reliability, consistency, domain boundaries, scalability).

Use code patterns for in-process structure; use system patterns when the problem is cross-process or cross-team.

## Workflow

1. Classify the problem: single-process design vs multi-process/distributed.
2. Identify the main pressure (pick 1):
   - Reliability under partial failure (timeouts/retries/circuit breaker/bulkheads)
   - Data consistency across boundaries (saga, event sourcing, CQRS)
   - Domain complexity and ownership (bounded contexts, aggregates, repositories, domain events)
   - Scalable coordination (leader election, sharding)
   - Migration/integration (anti-corruption layer, strangler fig, API gateway/BFF)
   - Streaming/reactivity (pub/sub, reactive streams/backpressure)
   - ML lifecycle (data pipeline, feature store, canary/blue-green, transfer learning)
3. State what’s stable and what can change (contracts, schemas, SLAs).
4. Choose a primary pattern and 0–2 supporting ones (avoid “pattern soup”).
5. Validate with: happy path, failure path, and ops path (metrics/alerts, retries, backoff, fallbacks).
6. Map to implementation tactics (often code-pattern wrappers/pipelines) and a testing strategy.

## Clarifying Questions

- What are the deployable units and trust boundaries (processes/services/teams)?
- Is failure partial (network timeouts, 5xx, queue backlog)? What are the SLOs?
- Do we require strong consistency, or is eventual consistency acceptable?
- Who owns each piece of data? What is the source of truth?
- What is the integration style: synchronous RPC, async events, or both?
- Do operations need to be idempotent? Do we have request IDs?
- What is the expected load profile (spikes, fan-out, long tails)?
- Can we tolerate duplication / reordering of messages?

## Pattern Chooser

### Cloud-Native / Microservices

- **Circuit Breaker**: stop cascading failures when a dependency is down/flaky.
- **Bulkhead**: isolate resource pools so one dependency can’t starve everything.
- **Saga**: multi-step business workflow across services with compensations.
- **API Gateway / BFF**: one entry point / client-specific API to avoid chatty clients.
- **Sidecar / Ambassador**: move cross-cutting networking concerns out of the app process (mesh/proxy).
- **Strangler Fig**: migrate a monolith incrementally by routing slices to new services.

### Functional / Safer Flow

- **Immutability & pure functions**: reduce shared state; make concurrency and testing easier.
- **Higher-order functions & composition**: prefer passing behavior directly over object-heavy indirection.
- **Option/Maybe (and Either/Result)**: make absence and expected failures explicit (avoid `null`).

### Reactive / Event-Driven

- **Pub/Sub**: decouple producers/consumers via events.
- **Transactional outbox + idempotent consumer (inbox)**: avoid dual-write bugs; make at-least-once delivery safe with dedupe.
- **Reactive streams + backpressure**: prevent fast producers from overwhelming slow consumers.
- **Event Sourcing**: store events as source of truth; rebuild state by replay.
- **CQRS**: separate command (write) model from query (read) model.

### Domain-Driven Design (DDD)

- **Bounded Context**: define model boundaries + translations/anti-corruption layers.
- **Aggregate**: enforce invariants within a consistency boundary.
- **Repository**: hide persistence behind an in-memory collection-like interface.
- **Domain Events**: publish business facts; decouple side effects.
- **Anti-Corruption Layer**: translate external/legacy concepts to protect your domain.
- **Hexagonal architecture (ports & adapters)**: keep domain core independent from infrastructure.

### Distributed Coordination & Scale

- **Actor model**: concurrency via message-passing, isolation, supervision.
- **Leader election**: choose a single coordinator for exclusive work.
- **Sharding**: partition data/work across nodes.
- **Idempotency + retries/backoff**: tolerate duplicates and transient failures safely.
- **MapReduce**: batch/distributed processing by map then reduce.

### AI/ML Lifecycle

- **Data pipeline (batch vs streaming; lambda/kappa)**: move data reliably into training/serving.
- **Feature store**: single source of truth for feature definitions/serving.
- **Transfer learning**: adapt a pre-trained model instead of training from scratch.
- **Blue-green/canary model deploys**: reduce risk when shipping new model versions.

## Map To Existing Skills

- Spec + contracts + plans: `spec-driven-development`.
- Shared primitives across services: `shared-platform-library`.
- Observability (logs/metrics/traces correlation): `apply-observability-patterns`.
- Timeouts / retries / idempotency / circuit breaker / bulkheads: `apply-resilience-patterns` (often implemented via `Proxy`/`Decorator`).
- Circuit breaker / caching / rate limiting (in-process structure): often a `Proxy` or `Decorator` (`apply-structural-patterns`).
- Saga orchestration: often a `State` machine + `Command` objects (`apply-behavioral-patterns`).
- Pub/sub + domain events: `Observer` (`apply-behavioral-patterns`).
- Hexagonal architecture: ports are interfaces; adapters are often `Adapter` or `Facade` (`apply-structural-patterns`).
- Option/Result: aligns with typed error boundaries (`typescript-style-guide`).

## Output Template

When recommending a pattern:

- 1–2 sentences: pattern + why it fits (pressure, assumptions).
- 3 bullets: key trade-offs, key failure modes, and a “no-pattern” alternative.
- A minimal implementation plan (boundaries, contracts, data ownership, and tests/metrics).
