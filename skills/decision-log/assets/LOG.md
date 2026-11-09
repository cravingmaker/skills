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
- **Evidence.** {{raw report path/hash, exact output revisions, commands and observed results, omitted checks with reasons}}
- **Usage.** {{native measurements and source; unknown where unavailable; estimates labeled separately}}
- **Disposition.** {{reported, verified, accepted, unresolved, rejected, cancelled, or superseded; decision ID if relevant}}
- **Next.** {{owner and next unmet condition; or closed}}

## Checkpoint template

{{event ID, last reconciled workspace and host state, accepted work to reuse, active/uncertain runs, budget spent and reserved, unresolved decisions, next ready action, and successor owner}}
