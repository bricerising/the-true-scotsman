# TypeScript Snippets (Creational)

Use these as small, idiomatic starting points when applying creational patterns in TypeScript/Node.

If you’re following “Systemic TypeScript” guidelines, prefer:
- closures over `class` (avoid `this` pitfalls; easier serialization)
- return-value error unions for expected failures (avoid `throw`)
- runtime validation when handling `unknown` at boundaries
- avoid import-time wiring in systemic code; wire in a composition root
- make resource lifetimes explicit (`start/stop/dispose`)

Where it helps, these examples also show common supporting patterns:
- **Strategy registry** to avoid long `switch` statements in factories.
- **Decorator/Proxy** to attach policies (retry/logging/caching) at the construction boundary.

## Contents

- Factory Method
- Abstract Factory
- Builder
- Prototype
- Singleton (caution)

## Common helpers (throwless Result)

```ts
export type Result<T, E> = { ok: true; value: T } | { ok: false; error: E };
export const ok = <T>(value: T): Result<T, never> => ({ ok: true, value });
export const err = <E>(error: E): Result<never, E> => ({ ok: false, error });
export const toError = (value: unknown): Error => (value instanceof Error ? value : new Error(String(value)));
```

## Factory Method (module factory seam)

- A low-friction “factory method” in TS is often just an exported constructor function that keeps module exports stable while allowing tests to inject config/dependencies.

- For systemic code, avoid import-time wiring; treat env/config as `unknown`, decode it once, then pass typed config into the factory.

```ts
type Transport = 'grpc' | 'http';

const isTransport = (value: string): value is Transport => value === 'grpc' || value === 'http';

type ClientConfig = {
  transport: Transport;
  url: string;
};

type ConfigError = { kind: 'invalid-transport'; value: string };

export const decodeClientConfig = (env: Record<string, string | undefined>): Result<ClientConfig, ConfigError> => {
  const transportRaw = env.GAME_TRANSPORT;
  if (transportRaw !== undefined && !isTransport(transportRaw)) {
    return err({ kind: 'invalid-transport', value: transportRaw });
  }

  return ok({
    transport: transportRaw ?? 'http',
    url: env.GAME_URL ?? 'http://localhost:3000',
  });
};

export const createClients = (config: ClientConfig) => ({
  gameClient: withRetry(createGameClient(config.transport, { url: config.url })),
});

// In your composition root:
// const config = decodeClientConfig(process.env);
// if (!config.ok) { /* log + exit */ }
// const { gameClient } = createClients(config.value);
```


If you need cross-cutting policies, attach them at the factory boundary (Decorator/Proxy):

```ts
type Player = { id: string; name: string };
type GetPlayerError =
  | { kind: 'network'; message: string }
  | { kind: 'bad-status'; status: number }
  | { kind: 'invalid-payload' };

type GameClient = { getPlayer: (id: string) => Promise<Result<Player, GetPlayerError>> };

export const withRetry = (inner: GameClient, maxAttempts = 3): GameClient => ({
  getPlayer: async (id) => {
    let last: Result<Player, GetPlayerError> | null = null;
    for (let attempt = 1; attempt <= maxAttempts; attempt++) {
      const result = await inner.getPlayer(id);
      last = result;
      if (result.ok) {
        return result;
      }
      if (result.error.kind !== 'network') {
        return result;
      }
    }
    return last ?? err({ kind: 'network', message: 'no-attempts' });
  },
});
```

## Factory Method (typed variant selection)

Use when caller depends on an interface, but the concrete implementation varies.

```ts
type Transport = 'grpc' | 'http';

type Player = { id: string; name: string };
type GetPlayerError =
  | { kind: 'network'; message: string }
  | { kind: 'bad-status'; status: number }
  | { kind: 'invalid-payload' };

export type GameClient = {
  getPlayer: (id: string) => Promise<Result<Player, GetPlayerError>>;
};

const isPlayer = (value: unknown): value is Player =>
  typeof value === 'object' &&
  value !== null &&
  'id' in value &&
  'name' in value &&
  typeof (value as { id?: unknown }).id === 'string' &&
  typeof (value as { name?: unknown }).name === 'string';

const grpcGameClient = (endpoint: string): GameClient => ({
  getPlayer: async (id) => ok({ id, name: `grpc-player (${endpoint})` }),
});

const httpGameClient = (baseUrl: string): GameClient => ({
  getPlayer: async (id) => {
    try {
      const response = await fetch(`${baseUrl}/players/${id}`);
      if (!response.ok) {
        return err({ kind: 'bad-status', status: response.status });
      }
      const json: unknown = await response.json();
      return isPlayer(json) ? ok(json) : err({ kind: 'invalid-payload' });
    } catch (error) {
      return err({
        kind: 'network',
        message: toError(error).message,
      });
    }
  },
});

// Strategy registry: avoids a growing switch as transports grow.
const creators = {
  grpc: (config: { url: string }) => grpcGameClient(config.url),
  http: (config: { url: string }) => httpGameClient(config.url),
} as const satisfies Record<Transport, (config: { url: string }) => GameClient>;

export const createGameClient = (transport: Transport, config: { url: string }): GameClient => creators[transport](config);
```

## Abstract Factory (family wiring)

Use when you must create multiple related components that must be compatible (a “family”), and you want to swap the family at configuration time.

```ts
export interface Queue {
  publish(topic: string, payload: unknown): Promise<void>;
}
export interface BlobStore {
  put(key: string, bytes: Uint8Array): Promise<void>;
}

export interface CloudFactory {
  queue(): Queue;
  blobStore(): BlobStore;
}

type Provider = 'aws' | 'gcp';

const awsFactory = (_config: { region: string }): CloudFactory => ({
  queue: () => ({ publish: async () => {} }),
  blobStore: () => ({ put: async () => {} }),
});

const gcpFactory = (_config: { projectId: string }): CloudFactory => ({
  queue: () => ({ publish: async () => {} }),
  blobStore: () => ({ put: async () => {} }),
});

const factories = {
  aws: (config: { region?: string }) => awsFactory({ region: config.region ?? 'us-east-1' }),
  gcp: (config: { projectId?: string }) => gcpFactory({ projectId: config.projectId ?? 'local' }),
} as const satisfies Record<Provider, (config: { region?: string; projectId?: string }) => CloudFactory>;

export const createCloudFactory = (
  provider: Provider,
  config: { region?: string; projectId?: string },
): CloudFactory => factories[provider](config);
```

You can also wrap the factory (Proxy) to apply policies consistently to the whole family:

```ts
const withCloudLogging = (inner: CloudFactory, log: (line: string) => void): CloudFactory => ({
  queue: () => {
    const queueClient = inner.queue();
    return {
      publish: async (topic, payload) => {
        log(`queue.publish:${topic}`);
        return queueClient.publish(topic, payload);
      },
    };
  },
  blobStore: () => {
    const blobStoreClient = inner.blobStore();
    return {
      put: async (key, bytes) => {
        log(`blob.put:${key}`);
        return blobStoreClient.put(key, bytes);
      },
    };
  },
});
```

## Builder (validation + defaults at build time)

Use when construction has many optional parts and must enforce invariants.

```ts
type HttpRequest = {
  method: 'GET' | 'POST';
  url: string;
  headers: Record<string, string>;
  body?: string;
};

type BuildError =
  | { kind: 'missing-url' }
  | { kind: 'body-not-allowed'; method: 'GET' };

type HttpRequestDraft = {
  method: HttpRequest['method'];
  url: string | null;
  headers: Record<string, string>;
  body?: string;
};

const defaults: HttpRequestDraft = { method: 'GET', url: null, headers: {} };

export const httpRequestBuilder = (draft: HttpRequestDraft = defaults) => ({
  withMethod: (method: HttpRequest['method']) => httpRequestBuilder({ ...draft, method }),
  withUrl: (url: string) => httpRequestBuilder({ ...draft, url }),
  withHeader: (key: string, value: string) =>
    httpRequestBuilder({ ...draft, headers: { ...draft.headers, [key]: value } }),
  withBody: (body: string) => httpRequestBuilder({ ...draft, body }),
  build: (): Result<HttpRequest, BuildError> => {
    if (!draft.url) {
      return err({ kind: 'missing-url' });
    }
    if (draft.method === 'GET' && draft.body) {
      return err({ kind: 'body-not-allowed', method: 'GET' });
    }
    return ok({ method: draft.method, url: draft.url, headers: draft.headers, body: draft.body });
  },
});
```

## Prototype (clone with explicit semantics)

Use when cloning is cheaper/cleaner than reconstructing, and you need predictable copy behavior.

```ts
export type Prototype<T> = { clone: (overrides?: Partial<T>) => T };

type Job = {
  id: string;
  name: string;
  tags: string[];
};

export const jobPrototype = (job: Job): Prototype<Job> => ({
  clone: (overrides = {}) => ({
    // shallow copy primitives + arrays explicitly; define deep copy rules per field
    ...job,
    tags: [...job.tags],
    ...overrides,
  }),
});
```

Prototype is often paired with a small “registry factory”:

```ts
type RegistryError = { kind: 'unknown-prototype'; key: string };

export const createPrototypeRegistry = <T,>() => {
  const prototypes = new Map<string, Prototype<T>>();
  return {
    register: (key: string, prototype: Prototype<T>) => {
      prototypes.set(key, prototype);
    },
    create: (key: string, overrides?: Partial<T>): Result<T, RegistryError> => {
      const proto = prototypes.get(key);
      return proto ? ok(proto.clone(overrides)) : err({ kind: 'unknown-prototype', key });
    },
  };
};
```

## Singleton (caution; prefer DI)

If you truly need a single shared instance, keep a creation seam so tests can override/reset it.

```ts
type Client = { ping: () => Promise<void> };

export const createSingleton = <T,>() => {
  let cached: T | null = null;
  return {
    get: (create: () => T): T => (cached ??= create()),
    resetForTest: () => {
      cached = null;
    },
  };
};

// Usage:
// const clientSingleton = createSingleton<Client>();
// const client = clientSingleton.get(makeClient);
```
