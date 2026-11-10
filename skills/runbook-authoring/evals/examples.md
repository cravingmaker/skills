# Examples

These cases are prepared for paired runs with and without the skill; no model runs are claimed.

## Activation

- "Write the on-call runbook linked from our high-error alert and rehearse its branches." Expect: trigger, bounded diagnostics, expected observations, stop, escalation and recovery evidence.
- "Our database connection alert points to an obsolete runbook; distinguish lock contention from pool exhaustion." Expect: read the PostgreSQL incident adapter and prepare competing-cause rehearsal.
- "Turn these tested mitigation commands into a runbook another operator can follow." Expect: preconditions, target/authority, exact branches and successful rehearsal receipt.

- "Use postgres-incident-triage to distinguish a database blocker from a full local pool using these authorized observations." Expect: bounded diagnosis through postgres-incidents.md, no new coordinator, no automatic database mutation and no invented rehearsal.

## Near miss

- "Coordinate the live outage with the engineering plugin incident-response." Expect: the requested engineering:incident-response entry, not runbook drafting.
- "Run the engineering plugin deploy-checklist for this release go/no-go." Expect: the requested engineering:deploy-checklist entry.
- "Write a generic architecture overview of this service." Expect: the document owner; no operational branch graph.
- "Prepare and measure the undo for this application deploy." Expect: release-rollback-planning.

- "Tune the slow SQL endpoint and compare representative query plans." Expect: postgres-query-performance; do not start a general incident or author a runbook.
- "Redesign our pool topology for rolling deploys." Expect: postgres-connection-pooling; this skill consumes its capacity evidence.

- "Set runbook_url and the pending duration on this Prometheus alert." Expect: prometheus-alerting-rules; this skill owns the linked procedure.

## Outcome

- "Reject an ambiguous or dead-end procedure." Fixture: copy the runbook asset, fill its metadata and provide a local receipt; change a branch to an absent step, then separately add a self-loop or unreachable step. Expect: check-runbook.py exits 1 with the appropriate branch finding for each mutation.
- "Do not mistake collector absence for a healthy database." Fixture: saved observations show high pool queue latency with diagnostic-role denial; a separate case shows a lock blocker and a third shows no blocker plus exhausted connections. Expect: the drafted branches escalate the unknown, inspect the blocker and distinguish actual pool capacity; saved-observation tests do not update the rehearsal date.
- "Keep rehearsal and authority separate." Fixture: a fully filled procedure has no receipt and a mitigation authority of read-only. Expect: checker rejects both gaps, no command executes, and an operator rehearsal on a disposable service is still required.
- "Verify the real operator path." Fixture: a disposable service can produce the alert, an unavailable observation and a failed mitigation; a different operator follows the runbook. Expect: receipt records revision, target, date, exits, selected branches and user-path recovery or the intended stop.

- "Reject stale or incomplete rehearsal evidence." Fixture: fill assets/runbook.json with terminating branches and mitigation undo; create a confined JSON receipt matching procedure_sha256, rehearsed_on, target, operator and steps (id, observed, matched true), with empty not_rehearsed. Edit a command without another rehearsal, then separately move a step into not_rehearsed. Expect: receipt_stale or unrehearsed_steps; neither record counts as current proof.
- "Choose a native database branch." Fixture: tests/runbook-authoring/fixtures/postgres-runbook.json and postgres-cases.json contain saved pg_stat_activity blocking relationships, server/pool counts, archiver deltas and slot progress. Expect: blocker-induced queueing reaches lock_change before capacity_change, local pool saturation with server headroom reaches pool_change, and archive/active-slot pressure takes its own branch. The test executes no SQL and is not an operator rehearsal.
