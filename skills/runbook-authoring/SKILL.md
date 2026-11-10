---
name: runbook-authoring
description: Write and rehearse an alert-linked operational runbook with diagnostic branches, expected observations, bounded mitigations, abort, recovery and escalation. Use for a missing or stale on-call procedure or bounded PostgreSQL incident diagnosis; live incident coordination and generic docs are separate jobs.
---

# Runbook authoring

Deliver a procedure another operator can follow from its alert to verified recovery or an explicit stop.

## Bind the procedure to its trigger

Read the alert rule, service topology, existing response procedure, ownership, authority and previous incident evidence. Name the symptom, user impact, applicability, target identity, required access, tool versions and time budget. Put a first diagnostic before any mitigation; distinguish an unavailable observation from a healthy result.

Use [assets/runbook.json](assets/runbook.json) as a comparison starter for a machine-checked procedure. It is documentation, never a command runner. Keep secrets, connection strings, raw SQL text and personal records out of receipts and the public runbook. Give each step a bounded command, expected observation, branch on match and branch on mismatch. End every path in recovery, abort or escalation. A mitigation also names its undo, or its irreversible effects and usable recovery prerequisite.

Read [references/postgres-incidents.md](references/postgres-incidents.md) for bounded diagnosis selected through postgres-incident-triage, or when the alert concerns PostgreSQL connections, locks, WAL, replication slots, archive failure or provider availability. Reuse backend diagnosis and change methods conditionally; this skill owns the entry and branching procedure.

For a bounded incident-diagnosis request, follow the existing procedure or prepare the evidence/branch candidate without requiring a new runbook or claiming a new rehearsal. Keep coordination with the incident lead and stop at a prepared mitigation when execution authority or the required database method is unavailable.

Done when an operator can identify the intended target and choose the next diagnostic from the observation without guessing.

## Check the procedure before rehearsal

The Python 3.12+ stdlib helper is offline and read-only:

```sh
python3 scripts/check-runbook.py path/to/runbook.json
```

It checks ownership/alert/rehearsal fields, unique step IDs, bounded commands, mitigation authority and undo, valid branches, reachability and termination. The local JSON receipt must match the procedure SHA-256, target and date, name the operator, and cover each step with a matched observation and no untested steps. It emits the procedure digest, counts and finding codes as JSON on stdout, diagnostics on stderr, and exits 0 for structural pass, 1 for findings or 2 for malformed/unreadable input. `--help` exits 0 without reading a runbook. It never prints or executes commands, fetches links or establishes that receipt claims are true. A pass proves structure only.

Resolve every alert's `runbook_url` against the published location, including anchors and authentication, using the repo's link checker or an authorized read. Check the real owner and escalation contact, not just their presence in JSON. Compare rendered human instructions with the checked procedure; preserve command/branch correspondence.

Done when the structural checker passes, alert links reach the actual procedure and the named owner accepts the scope.

## Rehearse the branches

Start from a declared disposable target with no live jobs, credentials or external effects. Reproduce the trigger and let an operator follow the procedure without author coaching. Exercise the plausible competing cause, an unavailable diagnostic and a failed mitigation. Confirm that expected output discriminates those cases and that stop/recovery checks observe the user's path, not just process status.

Record the exact runbook revision, target, date, command exit codes, observed branches, elapsed time and recovery result in a private receipt. A receipt uses procedure_sha256 from the checker, rehearsed_on, target, operator, steps (id, observed, matched) and not_rehearsed (id and reason). Editing any procedure field invalidates it. Update the last-rehearsed date and digest only after the actual run succeeds; restamping a hash alone supplies no evidence. A dry run or link check does not count as rehearsal; keep unfinished procedures visibly untested.

Prepared mitigation does not grant execution authority. Production changes, data deletion, credential rotation and traffic changes need explicit authorization in the task's scope. Confirm account/project/region/cluster or database identity immediately before mutation. A failed or uncertain effect stops automatic retries; observe state before choosing the next step.

For an application release undo, use the `release-rollback-planning` skill when installed and read first. For a real incident, hand coordination, severity, communication and action serialization to the incident lead; keep this drafting flow within its assigned procedure. For a substantial explanation, use the `clear-communication` skill when installed and read first.

Done when a different operator reaches the correct diagnostic branch and proves recovery or the intended stop in the disposable exercise. Return the runbook, alert links, owner, last successful rehearsal receipt, untested branches and every remaining evidence gap.
