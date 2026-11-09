# Data ownership

Read this when a durable choice changes consistency or write authority.

For each important state, name the authoritative writer, identity, unit and precision, transaction boundary, readers, access authority, and recovery source. Enumerate application, worker, import, maintenance, and administrative writers. Check enforcement at the boundary they all cross.

Specify consistency per operation. Name which completed writes a reader must see, which projections may lag, allowed lag, conflict handling, and behavior during uncertainty. Distinguish transaction isolation from replication freshness and durability.

For a database change plus publication, test the commit-to-publication crash window. An outbox couples local state and publication intent in one commit but can still deliver duplicates. CDC exposes committed changes; it does not automatically supply domain meaning, authorization, or duplicate-safe effects. For cross-service work, name partial completion, compensation limits, and reconciliation. The `async-messaging` skill supplies implementation semantics when needed.

For source archives, compare exact readback with source evidence and keep raw capture separate from derived interpretations. For recovery, restore and reconcile a representative fixture; the existence of a backup is insufficient.

Consult [PostgreSQL transaction isolation](https://www.postgresql.org/docs/current/transaction-iso.html) for the actual server release and [AWS's transactional outbox guidance](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html) for the publication problem. These sources are paraphrased.
