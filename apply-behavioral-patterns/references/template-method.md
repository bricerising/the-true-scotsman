# Template Method

## Intent

Define the skeleton of an algorithm in a base class and let subclasses override specific steps without changing the overall structure.

## Use When

- You already have an inheritance hierarchy and want to standardize the flow while allowing step customization.
- You need consistent ordering and invariants enforced by the base type.
- “Hooks” are enough for extension and you don’t need runtime swapping.

## Prefer Something Else When

- You want runtime swappability or composition (Strategy/Decorator).
- Inheritance would create tight coupling or deep hierarchies.

## Minimal Structure

- Base class has `templateMethod()` that calls `step1()`, `step2()`, ...
- Subclasses override selected steps; optional hooks have defaults in base class

## Implementation Steps

1. Extract the stable algorithm skeleton into the base class.
2. Define steps as protected abstract methods (or overridable hooks).
3. Keep base invariants enforced in the template method (validate before/after steps).
4. Avoid exposing too many steps; keep the extension surface small.

## Pitfalls

- **Inheritance coupling**: changes to base can ripple through subclasses.
- **Fragile base class**: too many hooks makes behavior unpredictable.
- **Hard to combine features**: inheritance doesn’t compose like decorators/strategies.

## Testing Checklist

- Base flow test: steps are invoked in correct order.
- Subclass overrides test: overriding a step changes behavior without breaking invariants.
- Hook default tests for subclasses that don’t override.

