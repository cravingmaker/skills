# Migration plan

Compare these fields with the project's migration/PR template; keep its existing format.

- Candidate files and SHA-256 digests:
- Target database, direct endpoint and disposable rehearsal identity (no credentials):
- Explicit adapter connection mode and the provider/client evidence proving direct routing:
- Server/client/runner versions and transaction mode:
- Authority for any production/destructive phase:
- Logical rules and final-schema constraints:
- Migration login, creator role, resulting owner and future-object ACLs:
- Old/new application, worker, export and external-consumer assumptions:

| Phase | Exact candidate | Readers/writers supported | Lock and duration bounds | Evidence | Stop condition and repair |
| --- | --- | --- | --- | --- | --- |
| Expand | | | | | |
| Compatible deploy | | | | | |
| Resumable backfill | | | | | |
| Validate | | | | | |
| Contract after measured exit condition | | | | | |

- Representative volume, workload, skew and production differences:
- Lint command/config/output and scoped suppressions:
- Conflicting-lock rehearsal and independent lock samples:
- Old-code/new-schema and new-code/expanded-schema results:
- Interrupted-backfill checkpoint, resumed result and independent reconciliation:
- Concurrent-index interruption/catalog/repair evidence, if applicable:
- Rollback-compatible versions, forward repair and usable recovery reference:
- Remaining unrun checks and responsible owner:
