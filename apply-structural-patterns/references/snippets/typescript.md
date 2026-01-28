# TypeScript Snippets (Structural)

Use these when implementing structural patterns in TypeScript, especially at IO boundaries.

If you’re following “Systemic TypeScript” guidelines, prefer:
- closures over `class` (avoid `this` pitfalls; easier serialization)
- return-value error unions for expected failures at IO boundaries (avoid `throw`)
- runtime validation when handling `unknown` at boundaries
- thread cancellation/timeouts (`AbortSignal`) through adapters/proxies when relevant
- if failures are expected, model them in return types (`Result`) instead of rejected promises

Where it helps, these examples also show common supporting patterns:
- **Factory Method** to assemble wrapper stacks at the boundary.
- **Decorator/Proxy** to attach policies (logging/retry/caching) without changing interfaces.

## Contents

- Adapter
- Bridge
- Composite
- Decorator
- Facade
- Flyweight
- Proxy

## Common helpers (throwless Result)

```ts
export type Result<T, E> = { ok: true; value: T } | { ok: false; error: E };
export const ok = <T>(value: T): Result<T, never> => ({ ok: true, value });
export const err = <E>(error: E): Result<never, E> => ({ ok: false, error });
export const toError = (value: unknown): Error => (value instanceof Error ? value : new Error(String(value)));
```

## Adapter (normalize `unknown` into domain types)

- When adapting third-party/legacy payloads, normalize `unknown` into your domain types with small helpers. Supporting multiple field names is common during migrations.

```ts
export const numberValue = (value: unknown, fallback = 0) => {
  if (typeof value === "number" && Number.isFinite(value)) return value;
  if (
    typeof value === "string" &&
    value.trim() !== "" &&
    Number.isFinite(Number(value))
  )
    return Number(value);
  return fallback;
};
```

- Keep adapters near IO (gRPC/HTTP/event consumers). Keep core domain code strongly typed and free of `unknown`.

## Adapter (wrap a third-party client behind your interface)

```ts
// Your domain interface (Target)
export interface PaymentsGateway {
  charge(amountCents: number, token: string): Promise<Result<{ id: string }, ChargeError>>;
}

type ChargeError =
  | { kind: "network"; message: string }
  | { kind: "unknown"; error: Error };

// Third-party SDK (Adaptee)
type StripeLike = {
  charges: { create: (request: { amount: number; source: string }) => Promise<{ id: string }> };
};

// Adapter
export const stripeGatewayAdapter = (stripe: StripeLike): PaymentsGateway => ({
  charge: async (amountCents, token) => {
    try {
      // translate domain inputs into SDK shape
      const response = await stripe.charges.create({ amount: amountCents, source: token });
      return ok(response);
    } catch (error) {
      return err({
        kind: "network",
        message: toError(error).message,
      });
    }
  },
});

// Proxy/Decorator: attach policy at the boundary without changing the PaymentsGateway interface.
export const withRetryGateway = (inner: PaymentsGateway, maxAttempts = 3): PaymentsGateway => ({
  charge: async (amountCents, token) => {
    let last: Result<{ id: string }, ChargeError> | null = null;
    for (let attempt = 1; attempt <= maxAttempts; attempt++) {
      const result = await inner.charge(amountCents, token);
      last = result;
      if (result.ok) return result;
      if (result.error.kind !== "network") return result;
    }
    return last ?? err({ kind: "unknown", error: new Error("no-attempts") });
  },
});

// Factory Method: produce the final gateway (adapter + policies) in one place.
export const createPaymentsGateway = (stripe: StripeLike): PaymentsGateway =>
  withRetryGateway(stripeGatewayAdapter(stripe));
```

## Bridge (abstraction + implementor)

Two axes of variation: a stable abstraction delegates to an interchangeable implementor.

```ts
export interface LogSink {
  write(line: string): void;
}

export const consoleSink = (): LogSink => ({ write: (line) => console.log(line) });

export const bufferedSink = (buffer: string[] = []): LogSink => ({
  write: (line) => {
    buffer.push(line);
  },
});

// Abstraction (closure over class)
export const createLogger = (sink: LogSink) => ({
  info: (message: string) => sink.write(`INFO ${message}`),
});

// Decorator: add formatting/policies without changing the LogSink interface.
export const withPrefix = (prefix: string, inner: LogSink): LogSink => ({
  write: (line) => inner.write(`${prefix}${line}`),
});
```

## Composite (tree of components)

```ts
export interface Component {
  cost(): number;
}

export const item = (price: number): Component => ({ cost: () => price });
export const bundle = (children: readonly Component[]): Component => ({
  cost: () => children.reduce((sum, c) => sum + c.cost(), 0),
});
```

## Decorator (wrap an interface to add behavior)

```ts
export type User = { id: string; name: string };

type UserRepoError = { kind: "unknown"; error: Error };
export type UserRepoResult = Result<User | null, UserRepoError>;

export interface UserRepo {
  getById(id: string): Promise<UserRepoResult>;
}

export const withTracingUserRepo = (inner: UserRepo, log: (line: string) => void): UserRepo => ({
  getById: async (id) => {
    const start = Date.now();
    try {
      return await inner.getById(id);
    } finally {
      log(`UserRepo.getById(${id}) ${Date.now() - start}ms`);
    }
  },
});

export const withCachingUserRepo = (inner: UserRepo): UserRepo => {
  const cache = new Map<string, Promise<UserRepoResult>>();
  return {
    getById: async (id) => {
      const existing = cache.get(id);
      if (existing) return existing;

      const value = inner
        .getById(id)
        .catch((error) => err({ kind: "unknown", error: toError(error) }))
        .then((result) => {
          if (!result.ok) cache.delete(id);
          return result;
        });

      cache.set(id, value);
      return value;
    },
  };
};

// Factory Method: assemble a decorator stack at the boundary.
export const createUserRepo = (base: UserRepo, dependencies: { log: (line: string) => void }): UserRepo =>
  withCachingUserRepo(withTracingUserRepo(base, dependencies.log));
```

## Facade (hide multi-client orchestration)

```ts
type CheckoutError = { kind: "unknown"; error: Error };

type Inventory = { reserve: (sku: string) => Promise<void> };
type Payments = { charge: (amountCents: number) => Promise<void> };
type Shipping = { createLabel: (sku: string) => Promise<string> };

export const createCheckoutFacade = (services: {
  inventory: Inventory;
  payments: Payments;
  shipping: Shipping;
}) => ({
  checkout: async (sku: string, amountCents: number): Promise<Result<string, CheckoutError>> => {
    try {
      await services.inventory.reserve(sku);
      await services.payments.charge(amountCents);
      const label = await services.shipping.createLabel(sku);
      return ok(label);
    } catch (error) {
      return err({ kind: "unknown", error: toError(error) });
    }
  },
});
```

## Flyweight (share intrinsic state via a factory)

```ts
type Glyph = { char: string; render: (x: number, y: number) => void };

export const createGlyphFactory = () => {
  const cache = new Map<string, Glyph>();
  return {
    get: (char: string): Glyph => {
      const existing = cache.get(char);
      if (existing) return existing;
      const glyph: Glyph = { char, render: () => {} };
      cache.set(char, glyph);
      return glyph;
    },
  };
};

// extrinsic state (x,y) supplied at call time:
// glyphFactory.get("A").render(10, 20)
```

## Proxy (lazy init + policy)

```ts
type BlobStoreError = { kind: "unknown"; error: Error };
type BlobStoreResult = Result<Uint8Array | null, BlobStoreError>;

export interface BlobStore {
  get(key: string): Promise<BlobStoreResult>;
}

export const lazyBlobStore = (create: () => BlobStore): BlobStore => {
  let real: BlobStore | null = null;
  return {
    get: async (key) => {
      try {
        real ??= create();
      } catch (error) {
        return err({ kind: "unknown", error: toError(error) });
      }

      return real.get(key).catch((error) => err({ kind: "unknown", error: toError(error) }));
    },
  };
};

// Proxy: cache results (and de-duplicate concurrent requests).
export const cachedBlobStore = (inner: BlobStore): BlobStore => {
  const cache = new Map<string, Promise<BlobStoreResult>>();
  return {
    get: async (key) => {
      const existing = cache.get(key);
      if (existing) return existing;

      const value = inner
        .get(key)
        .catch((error) => err({ kind: "unknown", error: toError(error) }))
        .then((result) => {
          if (!result.ok) cache.delete(key);
          return result;
        });

      cache.set(key, value);
      return value;
    },
  };
};

// Factory Method: compose proxies in one place (composition root).
export const createBlobStore = (createReal: () => BlobStore): BlobStore =>
  cachedBlobStore(lazyBlobStore(createReal));
```
