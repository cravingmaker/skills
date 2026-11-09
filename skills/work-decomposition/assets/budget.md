# Run budget ledger

Run ID: {{same ID as PLAN.md}}. Coordinator: {{single accountant}}. Ledger revision: {{revision}}. Authorization and limits: {{user/session constraint and live host limit}}.

## Allowances

| Resource | Limit | Charged or reserved | Remaining | Evidence |
| --- | --- | --- | --- | --- |
| Total worker starts | {{finite integer}} | {{integer}} | {{integer}} | {{dispatch receipts and uncertain intents}} |
| Retries | {{finite integer}} | {{integer}} | {{integer}} | {{retry records}} |
| Review rounds across the run | {{finite integer}} | {{integer}} | {{integer}} | {{round IDs}} |
| Active subagent runs | {{minimum of 8, user limit, host limit}} | {{including descendants, evals, uncertain starts}} | {{integer}} | {{host receipts and shared-pool reservations}} |
| Starts reserved for integration and verification | {{part of total starts}} | {{remaining reserve}} | {{integer}} | {{how and when the reserve is used}} |

Integration plan: {{owner, direct work or allocated starts, required checks}}. Verification plan: {{owner, direct work or allocated starts, required checks}}. Other runs sharing the concurrency pool: {{reserved slots and coordinator, or none}}. Measured usage: {{native receipts, or unknown; separate estimates}}.

## Dispatch ledger

Write an intent before dispatch; append its receipt and terminal result under the same request key. Keep prior rows when work is retried, replaced, cancelled, or superseded.

| Time | Request key | Task / parent | Purpose / provider | Event | Starts charged | Retries charged | Rounds charged | Active after | Evidence / raw report |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| {{time}} | {{stable key}} | {{task / parent ID}} | {{purpose / route}} | {{intent, receipt, result, cancellation, reconciliation}} | {{delta}} | {{delta}} | {{delta}} | {{count}} | {{path and revision, or unresolved receipt}} |

## Child allocations

| Child | Allowed starts | Retries | Review rounds | Shared concurrency slots | Coordinator confirmation |
| --- | --- | --- | --- | --- | --- |
| {{child ID or none}} | {{within parent total}} | {{integer}} | {{integer}} | {{shared ceiling}} | {{reservation receipt}} |

## Unresolved work and budget changes

| Time | Unmet condition or changed limit | Authority and evidence | Next owner / action |
| --- | --- | --- | --- |
| {{time}} | {{condition or old limit to new limit}} | {{source decision, never inferred from exhaustion}} | {{owner / next step}} |
