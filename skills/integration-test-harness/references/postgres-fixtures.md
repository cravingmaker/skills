# PostgreSQL fixtures

Read this when a test claims database behavior.

## Choose and verify the target

Use the project's existing Testcontainers factory, a CI PostgreSQL service or an authorized isolated provider branch. Pin container images and dependencies through the repository's lock and update policy; inspect installed versions before changing them. Check the actual server major, required extensions, locale, timezone, schema and application-role permissions. Connect through the production driver's serialization path and prove an expected rejection or readback before running the behavior case.

A provider-specific case uses the actual HTTP, WebSocket or pooler path. Keep a separate local database lane when it is useful; label its scope honestly. Use the direct endpoint for migration tools that require it, then test application paths through their deployed endpoints.

## Isolation and commit modes

| Mode | Useful for | Limitation |
| --- | --- | --- |
| Fresh database or container per run/worker | Migrations, constraints, separate connections and real commits | Own creation and deletion; include database processes in connection budgets. |
| Namespaced schema in a disposable database | Fast isolated fixtures with real commits | Extensions and global objects may still collide; qualify names and isolate their owners. |
| Transaction rolled back per test | Local SQL behavior on one connection | Hides commit/deferred behavior and is not isolation for other checked-out clients. |

Create a record, commit, close its client, then read through another client when claiming durability. For a deferred constraint, prove rejection at commit; a statement-only assertion can miss it. For an after-commit action, distinguish transaction rollback, durable intent and external acknowledgement. Use exact expected numeric strings or bytes for driver serialization cases, not a float conversion through the same production helper.

## Adapter recipes

For Node, acquire the container through an async resource fixture or `try/finally`, then create a pool from its explicit disposable endpoint. Register pool close and container stop even when migration or readiness fails. The runner's setup module must export the intended fixture instead of accidentally creating one global database for every worker.

For Rust, use the project's locked SQLx test fixture or an explicit disposable database factory. Check how the installed SQLx version treats failed tests and retained databases; add an owner-scoped reaper where cleanup is not automatic. Use a transaction handle for each operation and a distinct connection for committed readback. Compile-time SQL checks do not establish live constraints, commit or concurrency behavior.

Run a migration from the supported starting schema and retain relevant old-code/new-schema coverage. For a race, use the `postgres-concurrency-control` skill's bounded barriers rather than timed sleeps. After cancelling a worker, verify through the fixture owner that no transaction or client remains held before reuse or removal.
