# Templates

These are “starter shapes” for common platform primitives.

## 1) Boundary Wrapper (Handler Skeleton)

Use when many handlers repeat:

1) decode/validate input
2) call domain service
3) map response
4) timing + logging + metrics + error mapping

Shape:

```ts
export type HandlerContext<Req> = { request: Req };

export type Interceptor<Req, Res> = (
  next: (ctx: HandlerContext<Req>) => Promise<Res>,
) => (ctx: HandlerContext<Req>) => Promise<Res>;

export function createHandler<Req, Res>(options: {
  handler: (ctx: HandlerContext<Req>) => Promise<Res>;
  interceptors?: Array<Interceptor<Req, Res>>;
}): (ctx: HandlerContext<Req>) => Promise<Res> {
  const chain = (options.interceptors ?? []).reduceRight(
    (next, interceptor) => interceptor(next),
    options.handler,
  );
  return (ctx) => chain(ctx);
}
```

Notes:

- Keep operation name explicit (`method`, `route`) and pass it into timing/logging interceptors.
- Wrappers must preserve response shape and error semantics.

## 2) Promise Wrapper for Callback Clients

Use to unify cancellation/timeout behavior across gRPC/SDK clients.

Checklist:

- Support `AbortSignal` (call `cancel()`/`abort()` if available).
- Map timeout to a stable error type.
- Consider returning `Result<T, E>` for expected failures.

## 3) Lifecycle Facade

Use when a service owns long-lived resources (server, subscriptions, workers).

Public surface:

- `start(): Promise<void>`
- `stop(): Promise<void> | void`
- optional `close(): void` (best-effort)

Checklist:

- Concurrency-safe (start/stop races don’t leak running resources).
- Shutdown is explicit and awaited by the owner (composition root).
