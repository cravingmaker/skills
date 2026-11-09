# Examples

Paired model runs are deferred; keep this package unevaluated until the adoption harness records runs with and without it.

## Activation

- "Add a required foreign key to a table with traffic without breaking old workers." Expect: expand, compatible deployment, resumable backfill, deferred validation where supported and a measured contract gate.
- "Rehearse this migration and prove it stops within our lock budget." Expect: an explicitly disposable direct target, conflicting-lock fixture and a separate lock observer.
- "Our backfill stopped after committed batches; prove it resumes without skipped or doubled work." Expect: durable checkpoint and independent exact-key/value reconciliation against an uninterrupted run.

## Near miss

- "Choose the target table shape and tenant-safe keys." Expect: the `postgres-schema-design` skill, when installed and read.
- "Run this one-off correction of three production rows." Expect: the `postgres-change-execution` skill, when installed and read.
- "Plan the database engine major-version upgrade." Expect: the engine-upgrade operational job, with application compatibility evidence kept separate from schema migration phases.

## Outcome

- "Check lint wrapper behavior." Fixture: a local fake pinned Squawk executable returns 0, 1 or 9 for fixed dummy inputs. `scripts/check-migration.sh` returns 0, 1 or 2 respectively, preserves file argument boundaries and never invokes a database command. This proves wrapper behavior only.
- "Reject a wrong rehearsal target before writes." Fixture: a project adapter with inert database calls receives an absent disposable declaration, mismatched target/principal and absent/pooled/unknown connection-mode flags in separate runs. An arbitrary hostname without a pooler marker must still be rejected when its verified mode is pooled. Every run refuses before apply. The skill does not supply a generic apply adapter.
- "Prove live-transition mechanics in isolation." Fixture: the actual project runner on a disposable PostgreSQL target with representative rows, concurrent old/new client writes, a held conflicting lock and interruption after committed backfill work. Expect bounded lock failure, both compatibility paths, exact resumed results and invalid-index inspection if a concurrent build is interrupted.
