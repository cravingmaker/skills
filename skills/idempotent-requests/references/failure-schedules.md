# Failure schedules

Read this before implementing tests or claiming request retry safety.

## Fixture and independent oracle

Use an explicitly disposable PostgreSQL database at the application's intended major version and extensions.
Reuse the project's real driver, transaction code, and serialization boundary.
Create two tenants, two principals within one tenant, two semantic operations, and a durable business-effect ledger.
Use at least two independent connections and a barrier or latch placed around the actual admission/commit boundary.
Set a bounded test deadline that reports which barrier failed; do not substitute a sleep for an observed schedule.

Use synthetic requests and an owned fake provider with an independent durable effect ledger, stable-key lookup, controllable failures, and an acknowledgement-drop hook.
For crash tests, stop an owned worker process at an explicit hook, restart it, and query the durable store from a fresh connection.
For expiry, use a controllable clock or fixture timestamps and the actual expiry condition.
Do not copy production data or expose connection strings, raw keys, or payloads in reports.

## Required schedules

| Schedule | Controlled interleaving | Independent assertion |
| --- | --- | --- |
| Concurrent duplicates | Release two identical requests together; hold the first at admission or before commit until the second reaches the competing path. | One committed business effect and one completed result; the second follows documented wait/conflict/replay behavior and eventually returns the original identity. |
| Different payload | Admit one request, then reuse its scoped key with changed relevant input, including an in-flight variant. | Rejection without a new effect or replacement of the stored fingerprint/result. |
| Scope separation | Reuse one literal key across two tenants, two principals, and two operations while holding the other dimensions fixed. | Each authorized scope admits its own effect; none can retrieve another scope's result. |
| Crash before commit | Stop the executor after the domain write but before the local effect/result transaction commits. | A fresh connection sees neither effect nor completion; a retry can complete once. |
| Lost response after commit | Commit effect and result, then disconnect or kill the worker before sending a response. | The effect survives and a retry returns the stored original identity without another mutation. |
| In-flight owner failure | Stop a worker after a durable pending phase; start competing recoverers at a barrier. | Recovery ownership follows the chosen protocol; stale work cannot create a second business/provider effect. |
| Retention boundary | Retry immediately before and after expiry, plus an expired pending provider record. | The documented reject/reuse rule holds; unresolved work is retained and business uniqueness remains valid. |
| Provider success, lost acknowledgement | Let the provider ledger commit, drop its acknowledgement, and restart local recovery. | Lookup or same-key reconciliation finds one provider effect; local completion eventually points to it. |
| Provider unavailable during reconciliation | Make lookup fail while the outcome remains unknown. | The operation remains pending/uncertain with bounded retry or manual recovery; no fresh provider identity is issued. |
| Caller restart while unresolved | Persist the original intent/key, stop and restart the caller after losing an acknowledgement, then retry. | The original key survives; the independent ledger still shows one effect. |
| Permission changes | Complete once, revoke the caller's access, then retry with the same key. | The replay respects the chosen access policy and does not disclose protected results. |

Run both commit orders where the selected protocol has different outcomes.
Include the single-store path and external-phase path only when the operation uses them.
For retries after a database serialization/deadlock failure, verify that the whole local transaction can retry without repeating an arbitrary external call.

## Make the proof reject a defect

On the isolated fixture, disable atomic admission; the concurrent-duplicate schedule must observe excess committed effects.
Restore admission, then separate effect and result commits; a crash schedule must expose a durable effect without replay state.
For an external operation, replace stable-key reconciliation with a new provider key; the fake provider ledger must reveal the duplicate.
Restore the implementation and rerun the affected schedule and its allowed control.
These experiments change only the owned disposable fixture, not a production endpoint.

## Evidence

Record the code revision, server and driver versions, connection count, barrier and crash-hook names, fixture setup/cleanup, and test command.
For each case, retain the documented response outcome, durable business row count, deduplication row count/state, provider ledger count, and original result identity.
Label mocked/unit checks separately from real-store and owned-provider results.
If a real PostgreSQL service or provider simulator is unavailable, report the exact unrun schedules; an in-memory map is not substitute proof.
