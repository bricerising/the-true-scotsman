# React Snippets (Creational)

These examples assume a React environment (`react` installed, JSX enabled, `React` in scope). They intentionally cover only cases where **React built-ins** (Context/hooks) change the most idiomatic implementation compared to plain TypeScript. For language-only examples, see `references/snippets/typescript.md`.

## Omitted (not React-specific)

- Simple “factory method” component selection (switching between implementations) is usually just TypeScript control flow; see `references/snippets/typescript.md`.

## Contents

- Abstract Factory (design system via context)
- Builder (normalize/validate config)
- “Singleton” (app-wide service via context)

## Abstract Factory (theme/design-system factory via context)

Use when you need a compatible *family* of components (Button, Link, Modal) that must change together (white-labeling, multi-brand).

```tsx
import * as React from 'react';

type DesignSystem = {
  Button: React.FC<React.ButtonHTMLAttributes<HTMLButtonElement>>;
  Link: React.FC<React.AnchorHTMLAttributes<HTMLAnchorElement>>;
};

type Result<T, E> = { ok: true; value: T } | { ok: false; error: E };
const ok = <T,>(value: T): Result<T, never> => ({ ok: true, value });
const err = <E,>(error: E): Result<never, E> => ({ ok: false, error });

const DesignSystemContext = React.createContext<DesignSystem | null>(null);

type UseDesignSystemError = { kind: 'missing-design-system-provider' };

export const useDesignSystem = (): Result<DesignSystem, UseDesignSystemError> => {
  const value = React.useContext(DesignSystemContext);
  return value ? ok(value) : err({ kind: 'missing-design-system-provider' });
};

export const DesignSystemProvider = ({
  create,
  deps,
  children,
}: {
  create: () => DesignSystem;
  deps: React.DependencyList;
  children: React.ReactNode;
}) => {
  // Factory Method + memoization: build the family once per dependency set.
  const value = React.useMemo(create, deps);
  return <DesignSystemContext.Provider value={value}>{children}</DesignSystemContext.Provider>;
};
```

## Builder (reduce prop explosion with a typed config object)

Use when configuration has many optional parts and must be built stepwise with validation/defaults.

```tsx
import * as React from 'react';

type Result<T, E> = { ok: true; value: T } | { ok: false; error: E };
const ok = <T,>(value: T): Result<T, never> => ({ ok: true, value });
const err = <E,>(error: E): Result<never, E> => ({ ok: false, error });

type QueryConfig = {
  page: number;
  pageSize: number;
  sort?: 'name' | 'createdAt';
};

type BuildError =
  | { kind: 'invalid-page'; page: number }
  | { kind: 'invalid-page-size'; pageSize: number };

type Draft = {
  page: number | null;
  pageSize: number | null;
  sort?: QueryConfig['sort'];
};

const defaults: Draft = { page: null, pageSize: null };

// Builder: chainable steps + one build() that enforces invariants.
const queryBuilder = (draft: Draft = defaults) => ({
  withPage: (page: number) => queryBuilder({ ...draft, page }),
  withPageSize: (pageSize: number) => queryBuilder({ ...draft, pageSize }),
  withSort: (sort: QueryConfig['sort'] | undefined) => queryBuilder({ ...draft, sort }),
  build: (): Result<QueryConfig, BuildError> => {
    const page = draft.page ?? 1;
    const pageSize = draft.pageSize ?? 25;

    if (!Number.isInteger(page) || page < 1) {
      return err({ kind: 'invalid-page', page });
    }
    if (!Number.isInteger(pageSize) || pageSize < 1 || pageSize > 100) {
      return err({ kind: 'invalid-page-size', pageSize });
    }

    return ok({ page, pageSize, sort: draft.sort });
  },
});

const buildQuery = (raw: Partial<QueryConfig>) =>
  queryBuilder()
    .withPage(raw.page ?? 1)
    .withPageSize(raw.pageSize ?? 25)
    .withSort(raw.sort)
    .build();

export const Results = ({ rawConfig }: { rawConfig: Partial<QueryConfig> }) => {
  const result = React.useMemo(() => buildQuery(rawConfig), [rawConfig]);
  if (!result.ok) {
    return <div>Invalid config: {result.error.kind}</div>;
  }
  return <div>page={result.value.page}</div>;
};
```

## “Singleton” (app-wide service via Context)

Use when you need a single shared instance *for the React tree* (e.g., API client). Prefer Context + `useMemo` over module globals so tests and SSR are cleaner.

```tsx
import * as React from 'react';

type Result<T, E> = { ok: true; value: T } | { ok: false; error: E };
const ok = <T,>(value: T): Result<T, never> => ({ ok: true, value });
const err = <E,>(error: E): Result<never, E> => ({ ok: false, error });
const toError = (value: unknown): Error => (value instanceof Error ? value : new Error(String(value)));

type ApiError =
  | { kind: 'aborted' }
  | { kind: 'network'; message: string }
  | { kind: 'bad-status'; status: number }
  | { kind: 'invalid-json'; message: string };

type ApiClient = {
  getJson: (path: string, options?: { signal?: AbortSignal }) => Promise<Result<unknown, ApiError>>;
};

const ApiClientContext = React.createContext<ApiClient | null>(null);

export const ApiClientProvider = ({
  baseUrl,
  children,
}: {
  baseUrl: string;
  children: React.ReactNode;
}) => {
  const client = React.useMemo<ApiClient>(() => {
    return {
      getJson: async (path, options) => {
        try {
          const res = await fetch(`${baseUrl}${path}`, { signal: options?.signal });
          if (!res.ok) {
            return err({ kind: 'bad-status', status: res.status });
          }

          try {
            const json: unknown = await res.json();
            return ok(json);
          } catch (error) {
            return err({ kind: 'invalid-json', message: toError(error).message });
          }
        } catch (error) {
          const e = toError(error);
          if (e.name === 'AbortError') {
            return err({ kind: 'aborted' });
          }
          return err({ kind: 'network', message: e.message });
        }
      },
    };
  }, [baseUrl]);

  return <ApiClientContext.Provider value={client}>{children}</ApiClientContext.Provider>;
};

type UseApiClientError = { kind: 'missing-api-client-provider' };

export const useApiClient = (): Result<ApiClient, UseApiClientError> => {
  const value = React.useContext(ApiClientContext);
  return value ? ok(value) : err({ kind: 'missing-api-client-provider' });
};
```
