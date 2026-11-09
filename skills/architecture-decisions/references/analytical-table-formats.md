# Analytical table formats

Read this when the choice is between plain Parquet files and a table format such as DuckLake, Iceberg or Delta.

## When plain files are enough

Immutable Parquet files with a release manifest (path, row count, checksum, schema, producing job and version) suffice while:

- one process writes each dataset;
- readers accept whole-file or whole-partition replacement;
- history is kept by keeping old files, not by time travel queries;
- deletes are rare enough to rewrite a partition.

## Signals that justify a table format

Each must be a real requirement with a scenario:

- several writers commit to the same table concurrently;
- readers on more than one engine need a consistent snapshot while writes continue;
- queries need time travel or incremental reads over table history;
- row-level deletes or updates at scale (privacy erasure, corrections);
- schema evolution that readers must follow without a rewrite.

## Comparison conditions

Choose conformance cases from the declared requirements and run the same selected cases for each candidate:

- two concurrent writers: both commits survive or one fails cleanly;
- a reader opens a snapshot during a write and sees one consistent version;
- when deletion is required, query results and physical cleanup meet the declared retention and recovery policy in every required engine; check historical snapshots and backups separately;
- add and rename a column: every target engine reads old and new files;
- catalog loss: restore from the declared backup or publication manifest and compare the recovered logical result with an independent expected result.

Engine support for each format version and feature differs and changes often. Read each target engine's current documentation for the format version it writes and reads, and record the access date. Treat "supported" in a vendor blog as unverified until the engine's own docs or a conformance run show it.

## Operational cost to include

Catalog service and its backup, compaction and snapshot expiry schedules, small-file handling, and who runs each. A format with no one to run compaction degrades.

## Sources

Paraphrased, not copied. Verify the required features against the exact engine and format releases used by the trial.

- Apache Iceberg specification and schema evolution: https://iceberg.apache.org/spec/, https://iceberg.apache.org/docs/latest/evolution/
- Delta Lake versioning and utilities: https://docs.delta.io/versioning/, https://docs.delta.io/delta-utility/
- DuckLake: https://ducklake.select/
