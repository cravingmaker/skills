# Transport compatibility

Read this when code expects session state or a particular transaction API.

| Feature | Transaction-pool risk | Proof or alternative |
| --- | --- | --- |
| Session `SET` or `search_path` | A later transaction may use a different backend | Qualify objects or use supported transaction-local settings within one explicit transaction; confirm role defaults separately. |
| Session advisory lock | Acquisition and release may run on different backends | Use a compatible direct path or a transaction-scoped mechanism with the correct invariant. |
| `LISTEN` | Subscription belongs to a backend session | Keep a dedicated compatible listener connection and test reconnect/resubscribe. A notification sender has a different requirement. |
| SQL `PREPARE` and `DEALLOCATE` | SQL session state may be lost or conflict | Check the pooler's documented support; use supported driver protocol preparation and test it separately. |
| Temporary tables and held cursors | State can outlive the allocated transaction backend | Test the exact lifetime or use a direct path. |
| Interactive transaction | Separate query calls may borrow unrelated clients | Hold one client and use the supported interactive API; a non-interactive HTTP batch cannot branch on returned rows. |

Inventory ORM initialization hooks, migration tools, background listeners and driver prepared-statement caches as well as application SQL. Do not label all `SET` or all prepared statements incompatible; scope and protocol matter. Make a small matrix with required feature, real code path, driver and pooler settings, target identity, forced backend reassignment and observed result. Exercise tenant-local settings in successive transactions from different principals to detect leaked state.

On Neon, read current pooling and serverless-driver documentation before choosing HTTP or WebSocket APIs, request lifetimes and preparation behavior. Use a schema-only or synthetic branch for a provider test; production branches may contain private data. Keep credentials out of command output, artifacts and uncaught driver errors.
