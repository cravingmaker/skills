# PostgreSQL upgrade plan

Compare this outline with the existing change process; fill it from observed evidence and owner decisions before execution. Keep connection strings, raw configuration, SQL bodies and dumps in protected storage.

## Scope and authority

- Change/run ID and owner:
- Plan-only, disposable rehearsal or explicitly authorized production scope:
- Source/destination account, project, region, cluster/branch/endpoint and actual writer:
- Binary/data/tablespace/socket/port identities or supported provider method:
- Outage, data-loss, resource and observation budgets:

## Compatibility matrix

| Component | Source observation | Target observation | Release-note/source evidence | Action or reason for exclusion | Result |
| --- | --- | --- | --- | --- | --- |
| Server/client/binaries and skipped majors | | | | | |
| Extensions/shared libraries and preload | | | | | |
| Architecture/locale/collation/encoding/checksums | | | | | |
| Tablespaces/storage/topology and replication | | | | | |
| Roles/grants/auth/poolers/drivers/jobs | | | | | |

## Rehearsal and cutover

| Step | Exact reviewed command/artifact hash | Preconditions and stop threshold | Independent observation | Elapsed time |
| --- | --- | --- | --- | --- |
| Contain clone and prove destination ownership | | | | |
| Applicable native/provider preflight | | | | |
| Full selected method and resource peaks | | | | |
| Fence all writers/drain and observe final catch-up | | | | |
| Schema/global/sequence/large-object reconciliation | | | | |
| Required statistics/collation/index actions | | | | |
| Fresh real application/access/data/plan checks | | | | |
| Connection switch, acknowledged new write and recovery test | | | | |

## Recovery and completion

- Usable recovery artifact/point, independent restore evidence, scope and measured time:
- Transfer mode and exact point the old cluster becomes unsafe or insufficient:
- Abort before the boundary; forward repair/restore/reconciliation after it:
- Handling of writes accepted after cutover and any approved loss:
- Post-transition backup/recovery coverage and independently verified usability:
- Preserved fallback and approved cleanup horizon:
- Actual post-update versions/extensions, selected nonempty test results and evidence hashes:
- Failed/unrun checks, blockers, decision owner and cleanup state:
