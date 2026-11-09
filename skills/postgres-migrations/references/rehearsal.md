# Migration rehearsal

Read this when preparing a native runner or scoped adapter for an isolated migration rehearsal.

## Target contract

Record an explicit disposable target and its cleanup owner before any write. Bind provider project/branch/endpoint, database, server identity, intended principal, creator/owner and direct routing to the invocation. Use a credential store or protected libpq service/passfile; connection strings and passwords stay outside command arguments and logs. Do not guess `DATABASE_URL`, create a database in a shared cluster, reset a branch or copy personal data without authority. For copied data, minimize it and disable copied jobs, subscriptions, external connections and live credentials.

The adapter must require an explicit mode flag, such as `--connection-mode direct`, and refuse an absent disposable declaration, wrong target, unexpected principal, or pooled/unknown routing before applying SQL. Accept only direct mode supported by current provider endpoint inventory and driver routing evidence. Test missing, direct, transaction-pooled, session-pooled and unknown mode values against inert fakes before giving the adapter credentials. A hostname convention is only a use-time diagnostic clue; do not hard-code one as the safety gate.

## Evidence

| Check | Required observation |
| --- | --- |
| Native lint | Exact changed files, pinned linter/config, pass or scoped suppression with reason. |
| Locks | Separate observer samples object locks, wait duration and blockers; candidate times out while a fixture holds a conflicting lock. |
| Volume | Representative row/byte counts, skew, indexes and write workload; record differences from production. |
| Compatibility | Old binary/client reads and writes expanded schema; new binary/client tolerates old data and partially backfilled state. |
| Resume | Stop after a committed batch; restart from the durable checkpoint; exact keys, values and totals match uninterrupted work. |
| Ownership | Actual migration creator produces the intended owner and default ACLs for new tables, sequences and functions. |
| Interrupted index | Detect an invalid index from an interrupted concurrent build; choose documented repair without blindly hiding it behind `IF NOT EXISTS`. |
| Contract | Evidence that old readers/writers and replayed jobs no longer need the removed form. |

Capture bounded native output in an access-controlled location; publish only allowlisted summaries. Do not substitute wall-clock duration for lock samples or assert zero downtime from an unloaded rehearsal. If the database or representative workload is unavailable, return the candidate and exact missing proof without claiming readiness for production.

## Retry and repair

For a verified supported statement, compare ordinary and concurrent index builds, deferred constraint validation, and a validated required-value check before `SET NOT NULL`. Read the installed-major documentation for scans and lock levels; these alternatives can still need brief locks.

A timeout or error stops the current phase. Inspect the migration ledger and actual catalog state before retrying; nontransactional phases may have partial effects. Retry only within the declared attempt/time budget and after identifying what already committed. Rehearse the chosen repair and distinguish preserved data from data that needs recovery.
