// Original starter. Compare with the project before copying; pin its existing
// Node/TypeScript/pg versions in the project lockfile, then typecheck and test.
// The pool must support destroying an acquired client with release(true).
// A timeout during COMMIT has an unknown outcome and is never auto-retried.
import { performance } from 'node:perf_hooks';
import { setTimeout as delay } from 'node:timers/promises';

export interface Client {
  query(sql: string, values?: unknown[]): Promise<{ rows: Record<string, unknown>[] }>;
  release(destroy?: boolean): void;
}
export interface Pool { connect(): Promise<Client> }
export interface RetryOptions {
  maxAttempts: number;
  timeoutMs: number;
  baseDelayMs: number;
  maxDelayMs: number;
  signal?: AbortSignal;
}

export class TransactionFailure extends Error {
  readonly sqlState: string | undefined;
  constructor(sqlState?: string) {
    super('Transaction failed; inspect private redacted diagnostics and reconcile any unknown commit outcome.');
    this.sqlState = sqlState;
  }
}

function sqlState(error: unknown): string | undefined {
  const code = (error as { code?: unknown } | null)?.code;
  return typeof code === 'string' && /^[0-9A-Z]{5}$/.test(code) ? code : undefined;
}

async function attempt<T>(pool: Pool, remainingMs: number, signal: AbortSignal | undefined,
                          body: (client: Client) => Promise<T>): Promise<T> {
  let client: Client | undefined;
  let released = false;
  let stopped = false;
  let timer: ReturnType<typeof setTimeout> | undefined;
  let onAbort: (() => void) | undefined;
  const release = (destroy = false) => {
    if (client && !released) { released = true; client.release(destroy); }
  };
  const check = () => { if (stopped || signal?.aborted) throw new TransactionFailure(); };
  const stop = new Promise<never>((_, reject) => {
    onAbort = () => { stopped = true; release(true); reject(new TransactionFailure()); };
    timer = setTimeout(onAbort, remainingMs);
    signal?.addEventListener('abort', onAbort, { once: true });
    if (signal?.aborted) onAbort();
  });
  const operation = (async () => {
    try {
      check();
      client = await pool.connect();
      if (stopped || signal?.aborted) { release(true); check(); }
      await client.query('BEGIN ISOLATION LEVEL SERIALIZABLE');
      check();
      // Database work only: no payment, email, publication or unrelated I/O.
      const value = await body(client);
      check();
      await client.query('COMMIT');
      check();
      return value;
    } catch (error) {
      if (client && !released && !stopped) {
        try { await client.query('ROLLBACK'); }
        catch { release(true); throw new TransactionFailure(); }
      }
      throw error;
    } finally { release(stopped); }
  })();
  try { return await Promise.race([stop, operation]); }
  finally {
    clearTimeout(timer);
    if (onAbort) signal?.removeEventListener('abort', onAbort);
  }
}

export async function serializable<T>(pool: Pool, options: RetryOptions,
                                      body: (client: Client, attempt: number) => Promise<T>) {
  if (!Number.isSafeInteger(options.maxAttempts) || options.maxAttempts < 1 ||
      !Number.isFinite(options.timeoutMs) || options.timeoutMs <= 0 ||
      !Number.isFinite(options.baseDelayMs) || options.baseDelayMs < 0 ||
      !Number.isFinite(options.maxDelayMs) || options.maxDelayMs < 0) {
    throw new Error('Supply a positive attempt/deadline budget and nonnegative backoff limits.');
  }
  const deadline = performance.now() + options.timeoutMs;
  for (let number = 1; number <= options.maxAttempts; number++) {
    const remaining = deadline - performance.now();
    if (remaining <= 0 || options.signal?.aborted) throw new TransactionFailure();
    try {
      const value = await attempt(pool, remaining, options.signal, (client) => body(client, number));
      return { value, attempts: number };
    } catch (error) {
      const code = sqlState(error);
      if (options.signal?.aborted || performance.now() >= deadline ||
          !['40001', '40P01'].includes(code ?? '') || number === options.maxAttempts) {
        throw new TransactionFailure(code);
      }
      const cap = Math.min(options.maxDelayMs, options.baseDelayMs * 2 ** Math.min(number - 1, 30));
      try { await delay(Math.min(Math.random() * cap, Math.max(0, deadline - performance.now())), undefined, { signal: options.signal }); }
      catch { throw new TransactionFailure(); }
    }
  }
  throw new TransactionFailure();
}
