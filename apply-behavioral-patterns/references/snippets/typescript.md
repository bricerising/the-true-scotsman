# TypeScript Snippets (Behavioral)

Use these when implementing behavioral patterns in TypeScript (dispatch, routing, and algorithm selection).

If you’re following “Systemic TypeScript” guidelines, prefer:
- closures over `class` (avoid `this` pitfalls; easier serialization)
- return-value error unions for expected failures (avoid `throw`)
- runtime validation when handling `unknown` at boundaries
- explicit ownership/lifetimes for eventing (unsubscribe/shutdown; avoid orphan async loops)
- explicit encode/decode when persisting state (JSON round-trips lose information)

Where it helps, these examples also show common supporting patterns:
- **Factory Method** to choose/create a concrete behavior at the boundary.
- **Decorator/Proxy** to add policies (logging/retry/caching) without changing the behavior’s interface.
- **Adapter** to normalize incompatible handler shapes into a single pipeline.

## Contents

- Strategy
- Chain of Responsibility
- Command
- Observer
- State
- Iterator
- Mediator
- Memento
- Template Method
- Visitor

## Common helpers (throwless Result)

```ts
export type Result<T, E> = { ok: true; value: T } | { ok: false; error: E };
export const ok = <T>(value: T): Result<T, never> => ({ ok: true, value });
export const err = <E>(error: E): Result<never, E> => ({ ok: false, error });
export const toError = (value: unknown): Error => (value instanceof Error ? value : new Error(String(value)));
```

## Strategy (registry + factory + decorator)

```ts
type Kind = 'A' | 'B';

export type Strategy = (value: number) => number;

const base = {
  A: (value) => value + 1,
  B: (value) => value - 1,
} as const satisfies Record<Kind, Strategy>;

// Decorator: wrap a strategy with cross-cutting behavior.
export const withLogging = (name: string, inner: Strategy, log: (line: string) => void): Strategy =>
  (value) => {
    log(`${name}(${value})`);
    return inner(value);
  };

// Factory Method: choose and wire a strategy (often at the composition root).
export const createStrategy = (kind: Kind, dependencies: { log: (line: string) => void }): Strategy =>
  withLogging(kind, base[kind], dependencies.log);

// Avoid `value in base` here: it also matches inherited keys like 'toString'.
export const isKind = (value: string): value is Kind => Object.prototype.hasOwnProperty.call(base, value);
```

## Chain of Responsibility (pipeline + adapter + decorator)

```ts
export type Request = { type: string; payload: unknown };

export type ChainResult<T> =
  | { handled: true; value: T }
  | { handled: false };

export type AsyncHandler<T> = (request: Request) => Promise<ChainResult<T>>;
export type SyncHandler<T> = (request: Request) => ChainResult<T>;

// Adapter: normalize sync handlers into the async pipeline shape.
export const adaptSync = <T>(handler: SyncHandler<T>): AsyncHandler<T> => async (request) => handler(request);

// Decorator: add a policy without changing handler signatures.
export const withTracing = <T>(
  name: string,
  inner: AsyncHandler<T>,
  log: (line: string) => void,
): AsyncHandler<T> => {
  return async (request) => {
    log(`-> ${name}`);
    const result = await inner(request);
    log(`<- ${name}`);
    return result;
  };
};

// Compose a chain into a single handler.
export const composeChain = <T>(handlers: readonly AsyncHandler<T>[]): AsyncHandler<T> => async (request) => {
  for (const handler of handlers) {
    const result = await handler(request);
    if (result.handled) {
      return result;
    }
  }
  return { handled: false };
};

// Example: validate boundary data (`unknown`) and return a throwless Result.
type CreateUserOk = { kind: 'created'; id: string };
type CreateUserError = { kind: 'invalid-payload' };

const isCreateUserPayload = (value: unknown): value is { id: string } =>
  typeof value === 'object' && value !== null && typeof (value as { id?: unknown }).id === 'string';

export const createUserHandler: AsyncHandler<Result<CreateUserOk, CreateUserError>> = async (request) => {
  if (request.type !== 'createUser') {
    return { handled: false };
  }

  if (!isCreateUserPayload(request.payload)) {
    return { handled: true, value: err({ kind: 'invalid-payload' }) };
  }

  return { handled: true, value: ok({ kind: 'created', id: request.payload.id }) };
};
```

## Command (factory + decorator + queue)

```ts
export type CommandError =
  | { kind: 'retryable'; message: string }
  | { kind: 'failed'; message: string }
  | { kind: 'unknown'; error: Error };

export type Command = {
  execute: () => Promise<Result<void, CommandError>>;
  undo?: () => Promise<Result<void, CommandError>>;
};

// Decorator/Proxy: add retry policy without changing the command interface.
export const withRetry = (inner: Command, maxAttempts = 3): Command => {
  const undo = inner.undo;
  return {
    execute: async () => {
      let last: Result<void, CommandError> | null = null;
      for (let attempt = 1; attempt <= maxAttempts; attempt++) {
        const result = await inner.execute().catch((error) => {
          return err({ kind: 'unknown', error: toError(error) });
        });
        last = result;
        if (result.ok) {
          return result;
        }
        if (result.error.kind !== 'retryable') {
          return result;
        }
      }
      return last ?? err({ kind: 'retryable', message: 'no-attempts' });
    },
    undo: undo ? async () => undo() : undefined,
  };
};

// Factory Method: build typed commands from a kind + dependencies.
type CommandKind = 'increment' | 'decrement';
type Counter = { value: number };

const commandFactories = {
  increment: (counter: Counter): Command => ({
    execute: async () => {
      counter.value += 1;
      return ok(undefined);
    },
    undo: async () => {
      counter.value -= 1;
      return ok(undefined);
    },
  }),
  decrement: (counter: Counter): Command => ({
    execute: async () => {
      counter.value -= 1;
      return ok(undefined);
    },
    undo: async () => {
      counter.value += 1;
      return ok(undefined);
    },
  }),
} as const satisfies Record<CommandKind, (counter: Counter) => Command>;

export const createCommand = (kind: CommandKind, counter: Counter): Command => commandFactories[kind](counter);

// Closure over class: a simple in-memory command queue with undo.
export const createCommandQueue = () => {
  const history: Command[] = [];

  const run = async (command: Command) => {
    const result = await command.execute();
    if (result.ok) {
      history.push(command);
    }
    return result;
  };

  const undoLast = async () => {
    const cmd = history.pop();
    if (!cmd?.undo) {
      return ok(undefined);
    }
    return cmd.undo();
  };

  return { run, undoLast };
};
```

## Observer (interface + decorator)

```ts
type Events = {
  userCreated: { id: string };
  userDeleted: { id: string };
};

type Unsubscribe = () => void;

export interface EventBus<E extends Record<string, unknown>> {
  on<K extends keyof E>(event: K, listener: (payload: E[K]) => void): Unsubscribe;
  emit<K extends keyof E>(event: K, payload: E[K]): void;
}

export const createEmitter = <E extends Record<string, unknown>>(): EventBus<E> => {
  const listenersByEvent: Partial<{ [K in keyof E]: Set<(payload: E[K]) => void> }> = {};

  return {
    on: (event, listener) => {
      const listeners = listenersByEvent[event] ?? new Set<(payload: E[typeof event]) => void>();
      listeners.add(listener);
      listenersByEvent[event] = listeners;
      return () => listeners.delete(listener);
    },
    emit: (event, payload) => {
      listenersByEvent[event]?.forEach((listener) => listener(payload));
    },
  };
};

// Decorator: add logging or filtering without changing the EventBus interface.
export const withEventLogging = <E extends Record<string, unknown>>(
  inner: EventBus<E>,
  log: (line: string) => void,
): EventBus<E> => ({
  on: (event, listener) => inner.on(event, listener),
  emit: (event, payload) => {
    log(String(event));
    inner.emit(event, payload);
  },
});

// Usage:
// const bus = createEmitter<Events>();
// bus.on('userCreated', (e) => console.log(e.id));
// bus.emit('userCreated', { id: '123' });
```

## State (discriminated union + transition function)

```ts
export type State =
  | { kind: 'idle' }
  | { kind: 'loading' }
  | { kind: 'error'; message: string };

export type Action =
  | { type: 'load' }
  | { type: 'ok' }
  | { type: 'fail'; message: string };

export const transition = (state: State, action: Action): State => {
  switch (state.kind) {
    case 'idle':
      if (action.type === 'load') {
        return { kind: 'loading' };
      }
      return state;
    case 'loading':
      if (action.type === 'ok') {
        return { kind: 'idle' };
      }
      if (action.type === 'fail') {
        return { kind: 'error', message: action.message };
      }
      return state;
    case 'error':
      if (action.type === 'load') {
        return { kind: 'loading' };
      }
      return state;
  }
};
```

## State (state objects as flyweights)

When states are immutable/stateless, you can reuse them across contexts (Flyweight-style).

```ts
export type LightState = { kind: 'red' | 'green' | 'yellow'; next: () => LightState };

export const Red: LightState = { kind: 'red', next: () => Green };
export const Green: LightState = { kind: 'green', next: () => Yellow };
export const Yellow: LightState = { kind: 'yellow', next: () => Red };

export const createTrafficLight = (initial: LightState = Red) => {
  let state = initial;
  return {
    tick: () => {
      state = state.next();
    },
    current: () => state.kind,
  };
};
```

## Iterator (generator-based traversal)

```ts
type Node = { value: number; children?: Node[] };

export function* dfs(node: Node): Generator<Node> {
  yield node;
  for (const child of node.children ?? []) {
    yield* dfs(child);
  }
}

// Usage:
// for (const n of dfs(root)) console.log(n.value);
```

## Mediator (central coordinator)

```ts
type CloseReason = 'backdrop' | 'escape' | 'button' | 'program';

type ModalEvent =
  | { type: 'request.open' }
  | { type: 'request.close'; reason: CloseReason }
  | { type: 'backdrop.click' }
  | { type: 'key.escape' };

export interface ModalMediator {
  notify(event: ModalEvent): void;
}

type Telemetry = { track: (event: string, props?: Record<string, unknown>) => void };
type ScrollLock = { lock: () => void; unlock: () => void };

// Colleague: backdrop doesn't close the modal directly. It notifies the mediator.
export type Backdrop = {
  setMediator(mediator: ModalMediator): void;
  show(): void;
  hide(): void;
  click(): void;
};

export const createBackdrop = (view: { show: () => void; hide: () => void }): Backdrop => {
  let mediator: ModalMediator | null = null;
  return {
    setMediator: (nextMediator) => {
      mediator = nextMediator;
    },
    show: view.show,
    hide: view.hide,
    click: () => mediator?.notify({ type: 'backdrop.click' }),
  };
};

// Colleague: modal view delegates close-button behavior to the mediator.
export type Modal = {
  setMediator(mediator: ModalMediator): void;
  show(): void;
  hide(): void;
  focusFirst(): void;
  closeButtonClick(): void;
};

export const createModal = (view: {
  show: () => void;
  hide: () => void;
  focusFirst: () => void;
}): Modal => {
  let mediator: ModalMediator | null = null;
  return {
    setMediator: (nextMediator) => {
      mediator = nextMediator;
    },
    show: view.show,
    hide: view.hide,
    focusFirst: view.focusFirst,
    closeButtonClick: () => mediator?.notify({ type: 'request.close', reason: 'button' }),
  };
};

type KeyEvent = { key: string };
type KeyTarget = {
  addEventListener: (type: 'keydown', listener: (e: KeyEvent) => void) => void;
  removeEventListener: (type: 'keydown', listener: (e: KeyEvent) => void) => void;
};

// Colleague: escape-key handling routes through the mediator (not directly to the modal).
export type EscapeKey = {
  setMediator(mediator: ModalMediator): void;
  enable(): void;
  disable(): void;
};

export const createEscapeKey = (target: KeyTarget): EscapeKey => {
  let mediator: ModalMediator | null = null;
  const onKeyDown = (e: KeyEvent) => {
    if (e.key === 'Escape') {
      mediator?.notify({ type: 'key.escape' });
    }
  };
  return {
    setMediator: (nextMediator) => {
      mediator = nextMediator;
    },
    enable: () => target.addEventListener('keydown', onKeyDown),
    disable: () => target.removeEventListener('keydown', onKeyDown),
  };
};

// Mediator: owns all coordination rules (open/close, scroll lock, telemetry, etc).
export const createModalMediator = (deps: {
  modal: Modal;
  backdrop: Backdrop;
  escapeKey: EscapeKey;
  scrollLock: ScrollLock;
  telemetry: Telemetry;
}): ModalMediator => {
  let isOpen = false;

  const open = () => {
    if (isOpen) {
      return;
    }
    isOpen = true;
    deps.scrollLock.lock();
    deps.backdrop.show();
    deps.modal.show();
    deps.modal.focusFirst();
    deps.escapeKey.enable();
    deps.telemetry.track('modal_open');
  };

  const close = (reason: CloseReason) => {
    if (!isOpen) {
      return;
    }
    isOpen = false;
    deps.escapeKey.disable();
    deps.modal.hide();
    deps.backdrop.hide();
    deps.scrollLock.unlock();
    deps.telemetry.track('modal_close', { reason });
  };

  return {
    notify: (event) => {
      switch (event.type) {
        case 'request.open':
          open();
          return;
        case 'request.close':
          close(event.reason);
          return;
        case 'backdrop.click':
          close('backdrop');
          return;
        case 'key.escape':
          close('escape');
          return;
      }
    },
  };
};

// Wiring (composition root):
// const backdrop = createBackdrop(backdropView);
// const modal = createModal(modalView);
// const escapeKey = createEscapeKey(window);
// const mediator = createModalMediator({ modal, backdrop, escapeKey, scrollLock, telemetry });
// backdrop.setMediator(mediator); modal.setMediator(mediator); escapeKey.setMediator(mediator);
```

## Memento (snapshot/restore)

```ts
declare const editorMementoBrand: unique symbol;
export type EditorMemento = { readonly [editorMementoBrand]: true };

type EditorSnapshot = {
  text: string;
  selection: { start: number; end: number };
};

const cloneSnapshot = (s: EditorSnapshot): EditorSnapshot => ({
  text: s.text,
  selection: { ...s.selection },
});

// Originator: creates and restores opaque mementos (caretaker cannot inspect).
const snapshots = new WeakMap<EditorMemento, EditorSnapshot>();

export const createEditor = (initialText: string) => {
  let state: EditorSnapshot = { text: initialText, selection: { start: 0, end: 0 } };

  const createMemento = (): EditorMemento => {
    const memento = { [editorMementoBrand]: true } as EditorMemento;
    snapshots.set(memento, cloneSnapshot(state));
    return memento;
  };

  const restore = (memento: EditorMemento) => {
    const snapshot = snapshots.get(memento);
    if (!snapshot) {
      return;
    }
    state = cloneSnapshot(snapshot);
  };

  return {
    getText: () => state.text,
    getSelection: () => ({ ...state.selection }),
    setText: (text: string) => {
      state = { ...state, text };
    },
    setSelection: (start: number, end: number) => {
      state = { ...state, selection: { start, end } };
    },
    createMemento,
    restore,
  };
};

// Caretaker: manages undo/redo stacks without inspecting the snapshot.
export const createHistory = <M>() => {
  const past: M[] = [];
  const future: M[] = [];

  const push = (snapshot: M) => {
    past.push(snapshot);
    future.length = 0;
  };

  const undo = (current: M): M | null => {
    const prev = past.pop() ?? null;
    if (!prev) {
      return null;
    }
    future.unshift(current);
    return prev;
  };

  const redo = (current: M): M | null => {
    const next = future.shift() ?? null;
    if (!next) {
      return null;
    }
    past.push(current);
    return next;
  };

  return { push, undo, redo };
};
```

## Template Method (template function + hooks)

```ts
type ImportError =
  | { kind: 'read-failed'; message: string }
  | { kind: 'invalid-json'; message: string }
  | { kind: 'invalid-csv'; message: string }
  | { kind: 'invalid-user'; index: number }
  | { kind: 'duplicate-user-id'; id: string }
  | { kind: 'write-failed'; message: string };

type User = { id: string; aliases: string[] };

const isUser = (value: unknown): value is User =>
  typeof value === 'object' &&
  value !== null &&
  typeof (value as { id?: unknown }).id === 'string' &&
  Array.isArray((value as { aliases?: unknown }).aliases) &&
  (value as { aliases: unknown[] }).aliases.every((a) => typeof a === 'string');

type ImportTemplate<T> = {
  read: (input: string) => Promise<Result<string, ImportError>>;
  parse: (raw: string) => Result<T, ImportError>;
  validate?: (parsed: T) => Result<T, ImportError>;
  write: (value: T) => Promise<Result<void, ImportError>>;
};

const safeAsync = async <T>(
  operation: () => Promise<Result<T, ImportError>>,
  onThrow: (e: Error) => ImportError,
): Promise<Result<T, ImportError>> =>
  operation().catch((error) => err(onThrow(toError(error))));

// Template Method: fixed algorithm skeleton + overridable steps/hooks.
export const runImport = async <T>(
  template: ImportTemplate<T>,
  input: string,
): Promise<Result<void, ImportError>> => {
  const raw = await safeAsync(() => template.read(input), (error) => {
    return { kind: 'read-failed', message: error.message };
  });
  if (!raw.ok) {
    return raw;
  }

  const parsed = template.parse(raw.value);
  if (!parsed.ok) {
    return parsed;
  }

  const validate = template.validate ?? ((value: T) => ok(value));
  const validated = validate(parsed.value);
  if (!validated.ok) {
    return validated;
  }

  const written = await safeAsync(() => template.write(validated.value), (error) => {
    return { kind: 'write-failed', message: error.message };
  });
  if (!written.ok) {
    return written;
  }

  return ok(undefined);
};

type Format = 'json' | 'csv';
type Importer = { run: (input: string) => Promise<Result<void, ImportError>> };

type ImporterDependencies = {
  readText: (path: string) => Promise<Result<string, ImportError>>;
  writeUsers: (users: User[]) => Promise<Result<void, ImportError>>;
};

const validateUsers = (users: User[]): Result<User[], ImportError> => {
  const seen = new Set<string>();
  for (const user of users) {
    if (seen.has(user.id)) {
      return err({ kind: 'duplicate-user-id', id: user.id });
    }
    seen.add(user.id);
  }
  return ok(users);
};

const parseJsonUsers = (raw: string): Result<User[], ImportError> => {
  let json: unknown;
  try {
    json = JSON.parse(raw) as unknown;
  } catch (error) {
    return err({ kind: 'invalid-json', message: toError(error).message });
  }
  if (!Array.isArray(json)) {
    return err({ kind: 'invalid-user', index: 0 });
  }
  for (let i = 0; i < json.length; i++) {
    if (!isUser(json[i])) {
      return err({ kind: 'invalid-user', index: i });
    }
  }
  return ok(json);
};

const parseCsvUsers = (raw: string): Result<User[], ImportError> => {
  const lines = raw
    .split('\n')
    .map((l) => l.trim())
    .filter((l) => l !== '' && !l.startsWith('#'));

  // Format: id,alias1|alias2|alias3
  const users: User[] = [];
  for (let line = 0; line < lines.length; line++) {
    const parts = lines[line].split(',');
    const id = (parts[0] ?? '').trim();
    if (!id) {
      return err({ kind: 'invalid-csv', message: `missing id on line ${line + 1}` });
    }
    const aliasesRaw = (parts[1] ?? '').trim();
    const aliases = aliasesRaw ? aliasesRaw.split('|').map((a) => a.trim()).filter(Boolean) : [];
    users.push({ id, aliases });
  }
  return ok(users);
};

const createJsonUsersImporter = (deps: ImporterDependencies): Importer => {
  const template: ImportTemplate<User[]> = {
    read: deps.readText,
    parse: parseJsonUsers,
    validate: validateUsers,
    write: deps.writeUsers,
  };
  return { run: (path) => runImport(template, path) };
};

const createCsvUsersImporter = (deps: ImporterDependencies): Importer => {
  const template: ImportTemplate<User[]> = {
    read: deps.readText,
    parse: parseCsvUsers,
    validate: validateUsers,
    write: deps.writeUsers,
  };
  return { run: (path) => runImport(template, path) };
};

// Factory Method: pick a concrete implementation without changing callers of runImport.
const importerFactories = {
  json: createJsonUsersImporter,
  csv: createCsvUsersImporter,
} as const satisfies Record<Format, (deps: ImporterDependencies) => Importer>;

export const createImporter = (format: Format, deps: ImporterDependencies): Importer => importerFactories[format](deps);
```

## Visitor (tagged union visitor)

```ts
type Expr =
  | { kind: 'num'; value: number }
  | { kind: 'add'; left: Expr; right: Expr };

type ExprVisitor<R> = {
  num: (expr: Extract<Expr, { kind: 'num' }>) => R;
  add: (expr: Extract<Expr, { kind: 'add' }>) => R;
};

export const visitExpr = <R>(expr: Expr, visitor: ExprVisitor<R>): R => {
  switch (expr.kind) {
    case 'num':
      return visitor.num(expr);
    case 'add':
      return visitor.add(expr);
  }
};

export const evalVisitor = {
  num: (e) => e.value,
  add: (e) => visitExpr(e.left, evalVisitor) + visitExpr(e.right, evalVisitor),
} satisfies ExprVisitor<number>;

export const printVisitor = {
  num: (e) => String(e.value),
  add: (e) => `(${visitExpr(e.left, printVisitor)} + ${visitExpr(e.right, printVisitor)})`,
} satisfies ExprVisitor<string>;
```
