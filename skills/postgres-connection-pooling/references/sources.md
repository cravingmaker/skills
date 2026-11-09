# Sources

Read this when checking limits, session features or transport behavior. The instructions and helper are original; sources are cited rather than copied. Read the documentation for the installed driver and deployed pooler/provider at use time.

- [node-postgres pool sizing](https://node-postgres.com/guides/pool-sizing): deployment-wide accounting and external poolers.
- [node-postgres transactions](https://node-postgres.com/features/transactions): client ownership.
- [PgBouncer feature map](https://www.pgbouncer.org/features.html): pooling modes and session compatibility.
- [PgBouncer configuration](https://www.pgbouncer.org/config.html): the scope of client, per-database and per-user server limits.
- [Neon pooling](https://neon.com/docs/connect/connection-pooling): current provider mode, settings and preparation support.
- [Neon serverless driver](https://neon.com/docs/serverless/serverless-driver): HTTP batches, WebSocket APIs and runtime restrictions.
