# Monolithic Architecture

## Intent
Keep the system as a single deployable unit to maximize simplicity and iteration speed.

## Use when
- The team is small/medium, the domain is still changing quickly, or ops maturity is limited.
- You can keep clear module boundaries within the monolith (avoid “big ball of mud”).
- You want to defer distributed-systems complexity until the pressures are real.

## Avoid / watch-outs
- Modularize early: clean boundaries prevent later “flag day” rewrites.
- Watch for scaling/ownership pressure points; plan incremental extraction (see Strangler).

## Skill mapping
- `design`: enforce in-process boundaries and testability.
- `architecture`: define seams and extraction strategy (Strangler, anti-corruption layer).
- `spec`: codify contracts early so later extraction preserves behavior.
