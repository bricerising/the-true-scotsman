# React Snippets (Behavioral)

These examples assume a React environment (`react` installed, JSX enabled, `React` in scope). They intentionally cover only cases where **React built-ins** (hooks like `useReducer` / `useSyncExternalStore`) change the most idiomatic implementation compared to plain TypeScript. For language-only examples, see `references/snippets/typescript.md`.

## Omitted (not React-specific)

- **Strategy** via “pass a function/prop” and **Chain of Responsibility** pipelines are usually plain TypeScript; see `references/snippets/typescript.md`.

## Contents

- Observer (useSyncExternalStore)
- Command (useReducer-managed history)
- State (useReducer state machine)

## Observer (useSyncExternalStore + adapter)

```tsx
import * as React from "react";

type Listener = () => void;

type Store<T> = { getSnapshot: () => T; subscribe: (l: Listener) => () => void };

// Factory Method: create a minimal external store (Atom).
export type Atom<T> = {
  get: () => T;
  set: (next: T) => void;
  subscribe: (l: Listener) => () => void;
};

export const createAtom = <T,>(initial: T): Atom<T> => {
  let value = initial;
  const listeners = new Set<Listener>();
  return {
    get: () => value,
    set: (next) => {
      value = next;
      listeners.forEach((l) => l());
    },
    subscribe: (l) => {
      listeners.add(l);
      return () => listeners.delete(l);
    },
  };
};

// Adapter: Atom -> Store interface expected by useSyncExternalStore.
export const toStore = <T,>(atom: Atom<T>): Store<T> => ({
  getSnapshot: atom.get,
  subscribe: atom.subscribe,
});

export const useStore = <T,>(store: Store<T>) =>
  React.useSyncExternalStore(store.subscribe, store.getSnapshot);
```

## Command (undoable UI actions with `useReducer`)

Represent user actions as objects; keep undo/redo in one place.

```tsx
import * as React from "react";

type Command = { execute: () => void; undo: () => void };

// Decorator: wrap a command with a policy (telemetry, confirmations, etc.).
const withTelemetry = (name: string, inner: Command): Command => ({
  execute: () => {
    console.log("run", name);
    inner.execute();
  },
  undo: () => {
    console.log("undo", name);
    inner.undo();
  },
});

type History = {
  past: Command[];
  present: Command | null;
  future: Command[];
};

type Action =
  | { type: "push"; command: Command }
  | { type: "undo" }
  | { type: "redo" };

// Strategy registry: one state-transition strategy per action type.
type Transitions = {
  [K in Action["type"]]: (state: History, action: Extract<Action, { type: K }>) => History;
};

const transitions = {
  push: (state, action) => ({
    past: [...state.past, ...(state.present ? [state.present] : [])],
    present: action.command,
    future: [],
  }),
  undo: (state) => {
    const current = state.present;
    const prev = state.past[state.past.length - 1] ?? null;
    return {
      past: state.past.slice(0, -1),
      present: prev,
      future: current ? [current, ...state.future] : state.future,
    };
  },
  redo: (state) => {
    const next = state.future[0] ?? null;
    if (!next) return state;
    return {
      past: [...state.past, ...(state.present ? [state.present] : [])],
      present: next,
      future: state.future.slice(1),
    };
  },
} satisfies Transitions;

const reducer = (state: History, action: Action): History =>
  // TS needs a small cast because `action.type` is a union key; the strategies remain type-checked above.
  (transitions[action.type] as (s: History, a: Action) => History)(state, action);

export const useCommandHistory = () => {
  const [state, dispatch] = React.useReducer(reducer, { past: [], present: null, future: [] });
  const decorate = React.useCallback((cmd: Command) => withTelemetry("ui", cmd), []);
  const run = React.useCallback(
    (command: Command) => {
      const decorated = decorate(command);
      decorated.execute();
      dispatch({ type: "push", command: decorated });
    },
    [decorate, dispatch],
  );

  const undo = React.useCallback(() => {
    state.present?.undo();
    dispatch({ type: "undo" });
  }, [state.present, dispatch]);

  const redo = React.useCallback(() => {
    state.future[0]?.execute();
    dispatch({ type: "redo" });
  }, [state.future, dispatch]);

  return {
    run,
    undo,
    redo,
    canUndo: state.present !== null || state.past.length > 0,
    canRedo: state.future.length > 0,
  };
};
```

## State (state machine via `useReducer`)

You can keep state-specific behavior explicit instead of scattering `if/else` across components.

```tsx
import * as React from "react";

type State =
  | { kind: "idle" }
  | { kind: "loading" }
  | { kind: "error"; message: string };

type Action = { type: "load" } | { type: "ok" } | { type: "fail"; message: string };

const stateReducer = (state: State, action: Action): State => {
  switch (state.kind) {
    case "idle":
      if (action.type === "load") return { kind: "loading" };
      return state;
    case "loading":
      if (action.type === "ok") return { kind: "idle" };
      if (action.type === "fail") return { kind: "error", message: action.message };
      return state;
    case "error":
      if (action.type === "load") return { kind: "loading" };
      return state;
  }
};

export const Example = () => {
  const [state, dispatch] = React.useReducer(stateReducer, { kind: "idle" });
  return (
    <div>
      <button onClick={() => dispatch({ type: "load" })}>Load</button>
      <pre>{JSON.stringify(state)}</pre>
    </div>
  );
};
```
