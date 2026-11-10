# Examples

Paired model runs are pending; keep the catalog entry unevaluated.

## Activation

- "Autoscaling exhausts our PostgreSQL connections during rolling deploys." Expect: count peak overlapping app and worker processes, migrations and operator reserve, with pooler clients separate from backends.
- "Can this Neon operation use HTTP, or does it need WebSockets?" Expect: distinguish a fixed transaction batch from an interactive read-then-decide transaction and check deployed support.
- "Our LISTEN handler fails only on the pooled endpoint." Expect: trace backend-session requirements and test a compatible connection path.

- "Find pooled session features in this directory." Expect: run the candidate scanner on only the pooled code, distinguish `SET LOCAL` and transaction advisory locks from session forms, then confirm behavior through reassignment tests.

## Near miss

- "One SQL call scans too many rows." Expect: use the `postgres-query-performance` skill for plans and workload evidence.
- "Concurrent requests lose a stock update." Expect: use the `postgres-concurrency-control` skill for the database invariant.
- "Rehearse this table migration on a hot database." Expect: use the `postgres-migrations` skill when available for rollout and locking evidence.
- "Create a Neon project and production branch." Expect: handle provisioning as a separate authorized job without treating a pool budget as provisioning authority.


## Outcome

- "Check the sample budget." Fixture: the shipped `assets/budget.json`. Expect: 33 server slots, 47 server headroom and 40 of 100 pooler clients; an unchanged rerun emits identical JSON and changes no file.
- "Keep the budgets separate." Fixture: change only the sample pooler's client limit to 39. Expect: exit 1 for the client limit while server demand stays 33; changing `database_limit` to 32 independently fails the server limit.
- "Reject bad accounting." Fixture: set an instance count to `true`, omit the operator reserve, or add an unknown key. Expect: exit 2, a fix-oriented diagnostic and no raw input content in output.
- "Check the session scan." Fixture: the shipped clean and pooled test directories. Expect: 12 candidates on the pooled fixture, none on the transaction-local fixture; an empty directory exits 2 and a bare suppression marker hides nothing.
- "Prove actual compatibility." Fixture: an authorized disposable endpoint, two competing clients and a path using a session feature across commits. Expect: forced backend reassignment and feature-specific evidence, plus separately tested protocol preparation; local container success is not labeled provider evidence.
