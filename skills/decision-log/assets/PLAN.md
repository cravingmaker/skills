# Run plan

This is an unconfigured scaffold, not a started or completed run. Populate the empty identity fields, add the tasks, and set finite allowances before dispatch. The `work-decomposition` skill defines and checks this JSON block; keep exactly one fenced JSON block in this file.

```json
{
  "run_id": "",
  "workspace": "",
  "integration_owner": "",
  "tasks": [],
  "budget": {
    "coordinator": "",
    "worker_starts": {"limit": 0, "used": 0},
    "retries": {"limit": 0, "used": 0},
    "review_rounds": {"limit": 0, "used": 0},
    "concurrency": {"ceiling": 8, "active": 0},
    "reserve": {"worker_starts": 0, "plan": ""}
  }
}
```

## Outcome and authority

- **Goal.** {{observable user result}}
- **Scope.** {{included work and exclusions}}
- **Authority.** {{user/session authorization and unresolved actions}}
- **Inputs.** {{specification revision, code base, source dates, required hashes}}
- **Terminology.** {{shared definitions or authoritative pointer}}
- **Acceptance.** {{checkable requirements and the commands or evidence that establish them}}

## Current state

Plan revision: {{revision and timestamp}}. Phase: {{unstarted, active, checkpointed, or closed}}. Last reconciled event: {{LOG.md event ID or none}}. Budget ledger: {{current authoritative section or file, same run ID}}.

| Task | State | Owner | Input / output revision | Host run / request key | Raw report | Evidence gap / next action |
| --- | --- | --- | --- | --- | --- | --- |
| {{task}} | {{planned, dispatching, active, reported, verified, integrated, accepted, blocked, failed, cancelled, superseded, or uncertain}} | {{owner}} | {{hashes or commits}} | {{receipt or unresolved intent}} | {{path or missing}} | {{next step}} |

## Ownership and dependencies

{{for each task: inputs, outputs, artifact/decision dependencies, literal write paths, shared resources, and acceptance; reflect the checked fields in the JSON block}} {{one integration owner, how overlapping integration writes wait for worker completion, and how late outputs are handled}}

## Open decisions and risks

{{decision/finding ID, consequence, owner, evidence needed, and affected tasks; or none}}

## Next ready work

{{first unmet acceptance condition; prerequisites; permitted next action; current budget and slot availability}}

## Closure

{{final integrated revision, checks, unresolved limits, resource receipts or unknown, active work reconciled, and handoff owner}}
