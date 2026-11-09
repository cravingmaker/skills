# Sources

Read this when checking deployed isolation, lock or driver behavior. These are primary references for original instructions and starters; no source text or code is copied. Consult the documentation matching the installed server and locked driver at use time.

- [PostgreSQL transaction isolation](https://www.postgresql.org/docs/current/transaction-iso.html): anomalies and isolation guarantees.
- [PostgreSQL explicit locking](https://www.postgresql.org/docs/current/explicit-locking.html): row-lock compatibility and deadlocks.
- [PostgreSQL serialization failure handling](https://www.postgresql.org/docs/current/mvcc-serialization-failure-handling.html): complete transaction retries and SQLSTATE classification.
- [PostgreSQL range exclusion](https://www.postgresql.org/docs/current/rangetypes.html#RANGETYPES-CONSTRAINT): overlapping ranges and scalar operator classes.
- [node-postgres transactions](https://node-postgres.com/features/transactions): one client per transaction.
- [SQLx transaction API](https://docs.rs/sqlx/latest/sqlx/struct.Transaction.html): transaction ownership, commit and rollback; resolve to the project's locked crate documentation.
