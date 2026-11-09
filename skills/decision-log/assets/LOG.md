# Run event log

Run ID: {{same as PLAN.md}}. Coordinator: {{single writer}}. Append events; retain original records and use a correction event when a fact changes. This scaffold contains no actual dispatch or result.

## Event template

Copy this block for each event and replace the fields. Record dispatch intent before invoking the host, then receipt, result, verification, integration, cancellation, or reconciliation under linked event IDs.

### {{event ID}} / {{timestamp with zone}} / {{event kind}}

- **Identity.** {{run, task, parent task, logical request key, attempt, host task/run link or ID}}
- **Snapshot.** {{brief path/revision/hash, input revision, actual environment and base, owned paths}}
- **Route.** {{resolved provider/model/options and discovery evidence; or direct}}
- **Budget.** {{starts/retries/rounds delta and totals; active/uncertain runs; shared-pool reservation; reserve remaining}}
- **Operation.** {{dispatch intent, receipt, result status, or recovery action; never infer a missing receipt}}
- **Evidence.** {{exact source pointers, raw report path/hash, output revision, result/event/trace/screenshot locator; or unresolved}}
- **Result and interpretation.** {{claim, command and observed result, what the linked evidence proves, omitted checks and reasons}}
- **Usage.** {{native measurements and source; unknown where unavailable; estimates labeled separately}}
- **Disposition.** {{reported, verified, accepted, unresolved, rejected, cancelled, or superseded; decision ID if relevant}}
- **Next.** {{owner and next unmet condition; or closed}}

## Checkpoint template

{{event ID, exact project/run locator, last reconciled workspace and host state, disk versus context-only state, accepted work and proof to reuse, active/uncertain runs and ownership, budget spent/reserved/remaining, unresolved decisions, requested artifact links, next ready action, successor owner, and storage/access limits}}

Checkpoint read-back: {{reopened using only the recorded locator; evidence and all requested artifacts checked for identity, completeness and order; gaps remain explicit}}
