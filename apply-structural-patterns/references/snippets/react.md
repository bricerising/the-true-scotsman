# React Snippets (Structural)

These examples assume a React environment (`react` installed, JSX enabled, `React` in scope). They intentionally cover only cases where **React built-ins** (Context/hooks, `memo`, `lazy`, `Suspense`, `cloneElement`) change the most idiomatic implementation compared to plain TypeScript. For language-only examples, see `references/snippets/typescript.md`.

## Omitted (not React-specific)

- **Composite** recursion over a tree and **Adapter** mapping between data shapes are usually plain TypeScript; see `references/snippets/typescript.md`.

## Contents

- Decorator (cloneElement)
- Facade (custom hook)
- Proxy (lazy + gating)
- Bridge (context-based implementation)

## Decorator (wrap behavior with React built-ins)

Wrap a component to add behavior (concern stays outside the core component). In React this often looks like “decorate children” with `React.cloneElement`.

```tsx
import * as React from "react";

export const WithTracking = ({
  eventName,
  children,
}: {
  eventName: string;
  children: React.ReactElement<{ onClick?: React.MouseEventHandler }>;
}) => {
  const child = React.Children.only(children);
  const wrappedOnClick = React.useCallback<React.MouseEventHandler>(
    (e) => {
      console.log("track", eventName);
      child.props.onClick?.(e);
    },
    [eventName, child.props.onClick],
  );

  return React.cloneElement(child, { onClick: wrappedOnClick });
};
```

## Facade (custom hook hides a subsystem)

Hide data-fetching + caching + transformation behind a single hook.

```tsx
import * as React from "react";

type User = { id: string; name: string };

export const useUserProfile = (userId: string) => {
  const [user, setUser] = React.useState<User | null>(null);
  const [loading, setLoading] = React.useState(true);

  React.useEffect(() => {
    let cancelled = false;
    setLoading(true);
    fetch(`/api/users/${userId}`)
      .then((r) => r.json())
      .then((u: User) => {
        if (!cancelled) setUser(u);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [userId]);

  return { user, loading };
};
```

## Proxy (lazy loading / gated access / memoization)

Use a component as a stand-in that controls access or defers loading.

```tsx
import * as React from "react";

const SettingsPage = React.lazy(() => import("./SettingsPage"));

type ViewAccess =
  | { kind: "allowed" }
  | { kind: "denied"; reason?: string };

export const SettingsRoute = ({ access }: { access: ViewAccess }) => {
  if (access.kind === "denied") return <div>Not authorized{access.reason ? `: ${access.reason}` : null}</div>;
  return (
    <React.Suspense fallback={<div>Loading…</div>}>
      <SettingsPage />
    </React.Suspense>
  );
};
```

`React.memo` acts like a caching proxy for rendering:

```tsx
import * as React from "react";

export const memoize = <P,>(Component: React.FC<P>) => React.memo(Component);
```

## Bridge (abstraction decoupled from implementation via injected “renderer”)

Two axes: the stable “toast API” your app depends on (abstraction) vs how toasts are actually rendered/delivered (implementor). Context selects the implementor; callers only use the abstraction.

```tsx
import * as React from "react";

type ToastKind = "info" | "success" | "error";

type ToastItem = {
  id: string;
  kind: ToastKind;
  message: string;
  durationMs: number;
};

// Implementor: low-level toast delivery (UI, native bridge, logging, etc).
export type ToastImplementor = {
  push(toast: ToastItem): void;
  dismiss(id: string): void;
};

// Abstraction: what the app uses. It can grow independently of the implementor.
export type ToastService = {
  info(message: string, options?: { durationMs?: number }): void;
  success(message: string, options?: { durationMs?: number }): void;
  error(message: string, options?: { durationMs?: number }): void;
  dismiss(id: string): void;
};

type Result<T, E> = { ok: true; value: T } | { ok: false; error: E };
const ok = <T,>(value: T): Result<T, never> => ({ ok: true, value });
const err = <E,>(error: E): Result<never, E> => ({ ok: false, error });

const ToastImplContext = React.createContext<ToastImplementor | null>(null);

export const ToastProvider = ({
  implementor,
  children,
}: {
  implementor: ToastImplementor;
  children: React.ReactNode;
}) => <ToastImplContext.Provider value={implementor}>{children}</ToastImplContext.Provider>;

const createToastService = (implementor: ToastImplementor): ToastService => {
  const pushToast = ({ kind, message, durationMs = 4000 }: { kind: ToastKind; message: string; durationMs?: number }) => {
    const id = globalThis.crypto?.randomUUID?.() ?? `t_${Date.now()}_${Math.random().toString(16).slice(2)}`;
    implementor.push({ id, kind, message, durationMs });
  };

  return {
    info: (message, options) => pushToast({ kind: "info", message, durationMs: options?.durationMs }),
    success: (message, options) => pushToast({ kind: "success", message, durationMs: options?.durationMs }),
    error: (message, options) => pushToast({ kind: "error", message, durationMs: options?.durationMs }),
    dismiss: (id) => implementor.dismiss(id),
  };
};

type UseToastError = { kind: "missing-toast-provider" };

export const useToast = (): Result<ToastService, UseToastError> => {
  const implementor = React.useContext(ToastImplContext);
  return React.useMemo(() => {
    if (!implementor) return err({ kind: "missing-toast-provider" });
    return ok(createToastService(implementor));
  }, [implementor]);
};

// Implementor #1: in-app host that renders toasts (common in web apps).
export const ToastHost = ({ children }: { children: React.ReactNode }) => {
  const [toasts, setToasts] = React.useState<ToastItem[]>([]);

  const dismiss = React.useCallback((id: string) => {
    setToasts((existingToasts) => existingToasts.filter((toast) => toast.id !== id));
  }, []);

  const implementor = React.useMemo<ToastImplementor>(
    () => ({
      push: (toast) => {
        setToasts((existingToasts) => [...existingToasts, toast]);
        globalThis.setTimeout(() => dismiss(toast.id), toast.durationMs);
      },
      dismiss,
    }),
    [dismiss],
  );

  return (
    <ToastProvider implementor={implementor}>
      {children}
      <div role="region" aria-label="Notifications" style={{ position: "fixed", bottom: 12, right: 12 }}>
        {toasts.map((toast) => (
          <div key={toast.id} role="status">
            <strong>{toast.kind}</strong> {toast.message}
            <button onClick={() => dismiss(toast.id)}>Dismiss</button>
          </div>
        ))}
      </div>
    </ToastProvider>
  );
};

// Implementor #2: swap the renderer for tests/SSR/CLI without changing call sites.
export const createConsoleToastImplementor = (): ToastImplementor => ({
  push: (t) => console.log("[toast]", t.kind, t.message),
  dismiss: () => {},
});
```

Now the rest of the app depends on the `ToastService` abstraction (via `useToast()`), while implementations vary by provider (implementor).
