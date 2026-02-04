# Patterns (index)

This directory contains one short reference file per pattern topic.

Seed source for the initial topic list: https://microservices.io/tags/pattern
We will refine these summaries with additional sources over time.

## Decomposition & ownership

- [Microservice Architecture](microservice-architecture.md)
- [Monolithic Architecture](monolithic-architecture.md)
- [Decompose by business capability](decompose-by-business-capability.md)
- [Decompose by subdomain](decompose-by-subdomain.md)
- [Self-contained service](self-contained-service.md)
- [Service per team](service-per-team.md)
- [Strangler application](strangler-application.md)
- [Anti-corruption layer](anti-corruption-layer.md)

## Data ownership & consistency

- [Aggregate](aggregate.md)
- [Database per service](database-per-service.md)
- [Shared database](shared-database.md)
- [Saga](saga.md)
- [CQRS](cqrs.md)
- [Command-side replica](command-side-replica.md)
- [Event sourcing](event-sourcing.md)
- [Domain event](domain-event.md)
- [Event-driven architecture](event-driven-architecture.md)
- [Transactional outbox](transactional-outbox.md)
- [Transaction log tailing](transaction-log-tailing.md)
- [Polling publisher](polling-publisher.md)
- [Publish events using database triggers](publish-events-using-database-triggers.md)

## Communication & UI composition

- [API Gateway / BFF](api-gateway-bff.md)
- [API Composition](api-composition.md)
- [Remote Procedure Invocation (RPI)](remote-procedure-invocation-rpi.md)
- [Messaging](messaging.md)
- [Domain-specific protocol](domain-specific-protocol.md)
- [Client-side UI composition](client-side-ui-composition.md)
- [Server-side page fragment composition](server-side-page-fragment-composition.md)

## Discovery & configuration

- [Service registry](service-registry.md)
- [Client-side service discovery](client-side-service-discovery.md)
- [Server-side service discovery](server-side-service-discovery.md)
- [Self Registration](self-registration.md)
- [3rd Party Registration](3rd-party-registration.md)
- [Externalized configuration](externalized-configuration.md)

## Reliability & security

- [Circuit Breaker](circuit-breaker.md)
- [Idempotent Consumer](idempotent-consumer.md)
- [Access token](access-token.md)

## Observability

- [Application metrics](application-metrics.md)
- [Log aggregation](log-aggregation.md)
- [Distributed tracing](distributed-tracing.md)
- [Health Check API](health-check-api.md)
- [Audit logging](audit-logging.md)
- [Exception tracking](exception-tracking.md)
- [Log deployments and changes](log-deployments-and-changes.md)

## Deployment

- [Service deployment platform](service-deployment-platform.md)
- [Service mesh](service-mesh.md)
- [Sidecar](sidecar.md)
- [Service instance per container](service-instance-per-container.md)
- [Service instance per VM](service-instance-per-vm.md)
- [Multiple service instances per host](multiple-service-instances-per-host.md)
- [Single Service Instance per Host](single-service-instance-per-host.md)
- [Serverless deployment](serverless-deployment.md)

## Testing

- [Consumer-side contract test](consumer-side-contract-test.md)
- [Service integration contract test](service-integration-contract-test.md)
- [Service component test](service-component-test.md)

## Platform & templates

- [Microservice chassis](microservice-chassis.md)
- [Service Template](service-template.md)
