// Offline wrapper/barrier tests only. They do not establish PostgreSQL races.
import assert from 'node:assert/strict';
import test from 'node:test';
import { setTimeout as sleep } from 'node:timers/promises';
import { serializable, TransactionFailure } from '../../skills/postgres-concurrency-control/assets/serializable-retry.ts';
import { barrier, runPair } from '../../skills/postgres-concurrency-control/assets/two-connections.ts';

const options = { maxAttempts: 3, timeoutMs: 2000, baseDelayMs: 0, maxDelayMs: 0 };
const driverError = (code) => Object.assign(new Error('SECRET_SENTINEL'), { code });

function fixture(codes = []) {
  const clients = [];
  return {
    clients,
    async connect() {
      const number = clients.length;
      const client = {
        queries: [], releases: [],
        async query(sql) {
          this.queries.push(sql);
          if (sql === 'COMMIT' && codes[number]) throw driverError(codes[number]);
          return { rows: [{ value: number + 1 }] };
        },
        release(destroy = false) { this.releases.push(destroy); },
      };
      clients.push(client);
      return client;
    },
  };
}

test('commit failure replays the complete body and external effect follows success once', async () => {
  for (const code of ['40001', '40P01']) {
    const pool = fixture([code]);
    const reads = [];
    let externalEffects = 0;
    const result = await serializable(pool, options, async (client, attempt) => {
      const rows = await client.query('READ');
      reads.push([attempt, rows.rows[0].value]);
      await client.query('WRITE');
      return rows.rows[0].value;
    });
    externalEffects++;
    assert.deepEqual(result, { value: 2, attempts: 2 });
    assert.deepEqual(reads, [[1, 1], [2, 2]]);
    assert.equal(externalEffects, 1);
    assert.deepEqual(pool.clients[0].queries, ['BEGIN ISOLATION LEVEL SERIALIZABLE', 'READ', 'WRITE', 'COMMIT', 'ROLLBACK']);
    assert.deepEqual(pool.clients[1].queries, ['BEGIN ISOLATION LEVEL SERIALIZABLE', 'READ', 'WRITE', 'COMMIT']);
    assert.deepEqual(pool.clients.map((client) => client.releases), [[false], [false]]);
  }
});

test('exhaustion is finite and noneligible SQLSTATE or unknown connection failure never retries', async () => {
  const always = fixture(['40001', '40001', '40001']);
  await assert.rejects(serializable(always, { ...options, maxAttempts: 2 }, async () => 1), TransactionFailure);
  assert.equal(always.clients.length, 2);
  for (const code of ['23505', '08006', undefined]) {
    const pool = fixture();
    await assert.rejects(serializable(pool, options, async () => { throw driverError(code); }), (error) => {
      assert.ok(error instanceof TransactionFailure);
      assert.ok(!error.message.includes('SECRET_SENTINEL'));
      return true;
    });
    assert.equal(pool.clients.length, 1);
    assert.deepEqual(pool.clients[0].releases, [false]);
  }
});

test('rollback failure destroys the connection and suppresses retry', async () => {
  const pool = fixture();
  const acquire = pool.connect.bind(pool);
  pool.connect = async () => {
    const client = await acquire();
    client.query = async (sql) => {
      client.queries.push(sql);
      if (sql === 'ROLLBACK') throw driverError('08006');
      return { rows: [] };
    };
    return client;
  };
  await assert.rejects(serializable(pool, options, async () => { throw driverError('40001'); }));
  assert.equal(pool.clients.length, 1);
  assert.deepEqual(pool.clients[0].releases, [true]);
});

test('cancellation during acquisition releases a late client and never runs the body', async () => {
  let resolveClient;
  const connected = new Promise((resolve) => { resolveClient = resolve; });
  const controller = new AbortController();
  let bodyCalls = 0;
  const operation = serializable({ connect: () => connected }, { ...options, signal: controller.signal }, async () => { bodyCalls++; });
  controller.abort();
  await assert.rejects(operation, TransactionFailure);
  const releases = [];
  resolveClient({ query: async () => ({ rows: [] }), release: (destroy) => releases.push(destroy) });
  await sleep(0);
  assert.equal(bodyCalls, 0);
  assert.deepEqual(releases, [true]);
});

test('deadline while commit is pending has unknown outcome and never retries', async () => {
  const pool = fixture();
  let releaseCommit;
  const waiting = new Promise((resolve) => { releaseCommit = resolve; });
  const acquire = pool.connect.bind(pool);
  pool.connect = async () => {
    const client = await acquire();
    client.query = async (sql) => {
      client.queries.push(sql);
      if (sql === 'COMMIT') await waiting;
      return { rows: [] };
    };
    return client;
  };
  await assert.rejects(serializable(pool, { ...options, timeoutMs: 20 }, async () => 1), TransactionFailure);
  assert.equal(pool.clients.length, 1);
  assert.deepEqual(pool.clients[0].releases, [true]);
  releaseCommit();
  await sleep(0);
  assert.deepEqual(pool.clients[0].releases, [true]);
});

test('one-shot barrier accepts two arrivals, rejects a missing peer and rejects overuse', { timeout: 2000 }, async () => {
  const gate = barrier(2, 2000);
  await Promise.all([gate.arrive(), gate.arrive()]);
  await assert.rejects(gate.arrive());
  const missing = barrier(2, 10);
  await assert.rejects(missing.arrive());
});

test('fixture refuses non-disposable and identical-session cases before writes', async () => {
  const clients = [1, 2].map(() => ({
    queries: [],
    async query(sql) { this.queries.push(sql); return { rows: [{ db: 'owned_fixture', pid: 1 }] }; },
    release() {},
  }));
  const target = { disposable: true, expectedDatabase: 'owned_fixture', schema: 'owned', timeoutMs: 1000 };
  let called = false;
  await assert.rejects(runPair(clients[0], clients[1], { ...target, disposable: false }, 'READ COMMITTED', async () => { called = true; }));
  assert.ok(clients.every((client) => client.queries.length === 0));
  await assert.rejects(runPair(clients[0], clients[1], target, 'READ COMMITTED', async () => { called = true; }));
  assert.equal(called, false);
  assert.ok(clients.every((client) => client.queries.at(-1) === 'ROLLBACK'));
});
