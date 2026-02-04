# Decompose by subdomain

## Intent
Align services to DDD subdomains/bounded contexts to keep models coherent and reduce translation churn.

## Use when
- The domain is complex and multiple models exist (different language/meaning per context).
- You want to prevent “one shared model for everything” and make ownership explicit.

## Avoid / watch-outs
- Beware “shared kernel creep”: don’t re-centralize the domain via shared libraries/models.
- Use anti-corruption layers between contexts to keep model boundaries real.

## Skill mapping
- `architecture`: define bounded contexts and translations.
- `spec`: publish contracts (APIs/events) between contexts.
- `design`: implement translation boundaries cleanly (adapters/facades).
