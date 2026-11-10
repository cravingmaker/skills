# Compatibility evidence

Read this before choosing a transition path or interpreting preflight success. Collect the smallest allowlisted inventory that can resolve the matrix; keep private schema, SQL, configuration and role detail in protected evidence.

| Area | Evidence and disposition |
| --- | --- |
| Versions | Actual source servers/replicas, client libraries and utilities, target server/binaries, supported source-target pair and all intervening release notes |
| Extensions | Installed extension versions, target control/shared-library availability, preload requirements, update ordering, application use and supported provider versions |
| Physical layout | Architecture/build compatibility, encoding, checksum state, block/layout constraints, tablespace and WAL locations, filesystem transfer support and space peaks |
| Locale and indexes | Locale/collation provider and version, changed comparison semantics, affected objects, reindex/refresh requirements and bounded rehearsal |
| Access and consumers | Owners, grants, defaults, TLS/auth behavior, pooler/session mode, drivers, migration jobs, workers, replicas, publications and subscriptions |
| Recovery | Independently restored artifact or provider recovery point, dependencies, exact usable scope, measured recovery time and how post-cutover writes are handled |
| Release actions | For a minor update review each skipped minor; for a major transition review remaining source-minor notes, every intervening major migration section and target minors through the selected release. Record actions or evidence for exclusions |

Record unknowns as blockers or bounded risks with an owner; a matching version string does not establish binary extension compatibility. Use the target major's official `pg_upgrade` instructions for checks and external modules, then test the full application path with actual extension use. Verify client utility/server compatibility in each utility's documentation rather than assuming every pg_dump can read every server.

Choose the simplest supported method that meets the measured outage and recovery budget. A minor update follows the selected package/provider maintenance mechanism; a major transition needs the selected data-conversion or migration path. For replicated systems, inventory slots, logical state and replica rebuild/upgrade order using documentation for both majors and the actual topology. Keep schema evolution, query optimization, role policy and host package ownership in their existing methods; this matrix consumes their evidence.
