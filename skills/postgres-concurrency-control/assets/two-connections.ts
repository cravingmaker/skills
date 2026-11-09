// Original fixture starter; no dependency install or database creation.
// Compare with the project's locked pg/TypeScript APIs. The caller must supply
// two checked-out clients, seed counter(value=0) or duty(id=1,2; active=true),
// and own timeout/cancellation, independent committed readback and cleanup.
import type { Client } from './serializable-retry.ts';

export interface Fixture {
  disposable: true;
  expectedDatabase: string;
  schema: string;
  timeoutMs: number;
}

export function barrier(parties: number, timeoutMs: number) {
  if (!Number.isInteger(parties) || parties < 2 || !Number.isFinite(timeoutMs) || timeoutMs <= 0) {
    throw new Error('Supply at least two parties and a positive barrier deadline.');
  }
  let arrived = 0;
  let timer: ReturnType<typeof setTimeout> | undefined;
  let resolve!: () => void;
  let reject!: (error: Error) => void;
  const gate = new Promise<void>((yes, no) => { resolve = yes; reject = no; });
  // A peer can fail before anyone arrives; still observe that shared rejection.
  void gate.catch(() => {});
  const abort = () => { clearTimeout(timer); reject(new Error('Barrier failed; settle both participants.')); };
  return {
    abort,
    async arrive() {
      arrived++;
      if (arrived > parties) throw new Error('Create a fresh one-shot barrier for each schedule.');
      if (arrived === 1) timer = setTimeout(abort, timeoutMs);
      if (arrived === parties) { clearTimeout(timer); resolve(); }
      await gate;
    },
  };
}

function schema(fixture: Fixture) {
  if (fixture.disposable !== true || !fixture.expectedDatabase ||
      !/^[a-z_][a-z0-9_]*$/.test(fixture.schema) ||
      !Number.isSafeInteger(fixture.timeoutMs) || fixture.timeoutMs <= 0) {
    throw new Error('Supply an explicit disposable database identity, safe schema and finite timeout.');
  }
  return '"' + fixture.schema + '"';
}

export async function runPair(left: Client, right: Client, fixture: Fixture,
                              isolation: 'READ COMMITTED' | 'REPEATABLE READ',
                              operation: (client: Client, id: number, meet: () => Promise<void>, schema: string) => Promise<void>) {
  const quoted = schema(fixture);
  if (!['READ COMMITTED', 'REPEATABLE READ'].includes(isolation)) {
    throw new Error('Use a declared fixture isolation level.');
  }
  const gate = barrier(2, fixture.timeoutMs);
  const clients = [left, right];
  try {
    // Hold both transactions before probing backend identity, including behind
    // a transaction pooler. The caller also bounds acquisition and socket I/O.
    const begun = await Promise.allSettled(clients.map((client) => client.query('BEGIN ISOLATION LEVEL ' + isolation)));
    if (begun.some((result) => result.status === 'rejected')) throw new Error('Could not start both transactions.');
    const identities = await Promise.all(clients.map((client) => client.query('SELECT current_database() AS db, pg_backend_pid() AS pid')));
    if (identities.some((result) => result.rows[0]?.db !== fixture.expectedDatabase ||
        !Number.isSafeInteger(result.rows[0]?.pid) || Number(result.rows[0]?.pid) <= 0) ||
        identities[0].rows[0]?.pid === identities[1].rows[0]?.pid) {
      throw new Error('Use two independent sessions on the declared disposable target.');
    }
    const results = await Promise.allSettled(clients.map(async (client, index) => {
      try {
        await client.query("SELECT set_config('statement_timeout', $1, true), set_config('lock_timeout', $1, true)", [String(fixture.timeoutMs)]);
        await operation(client, index + 1, () => gate.arrive(), quoted);
        await client.query('COMMIT');
      } catch {
        gate.abort();
        throw new Error('Race participant failed; inspect private redacted diagnostics.');
      }
    }));
    if (results.some((result) => result.status === 'rejected')) throw new Error('Race failed; inspect the owned fixture.');
  } finally {
    gate.abort();
    // Owner must discard a client if rollback fails, then release both clients.
    const cleanup = await Promise.allSettled(clients.map((client) => client.query('ROLLBACK')));
    if (cleanup.some((result) => result.status === 'rejected')) throw new Error('Discard clients whose rollback failed.');
  }
}

export async function lostUpdate(left: Client, right: Client, fixture: Fixture, atomic: boolean) {
  return runPair(left, right, fixture, 'READ COMMITTED', async (client, _id, meet, namespace) => {
    const result = await client.query('SELECT value FROM ' + namespace + '.counter');
    const old = Number(result.rows[0]?.value);
    if (!Number.isSafeInteger(old)) throw new Error('Seed one integer counter row.');
    await meet();
    if (atomic) await client.query('UPDATE ' + namespace + '.counter SET value = value + 1');
    else await client.query('UPDATE ' + namespace + '.counter SET value = $1', [old + 1]);
  });
}

export async function writeSkew(left: Client, right: Client, fixture: Fixture) {
  return runPair(left, right, fixture, 'REPEATABLE READ', async (client, id, meet, namespace) => {
    const result = await client.query('SELECT count(*) AS count FROM ' + namespace + '.duty WHERE active');
    await meet();
    if (Number(result.rows[0]?.count) > 1) {
      await client.query('UPDATE ' + namespace + '.duty SET active = false WHERE id = $1', [id]);
    }
  });
}

// Repair write skew by using serializable() for each worker with a fresh pair
// of attempt-1 read barriers. Later attempts MUST re-read without that barrier.
// Observe count(active) >= 1 from an independent client after both settle.
