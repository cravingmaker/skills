# Workflow modes

Use only the branch the current request needs. Reuse accepted artifacts and decisions; moving to the next stage creates no new authority.

## Select the stage

| Present state | Next capability and completion boundary |
| --- | --- |
| Consequential understanding is unsettled | Read the `grill-with-docs` skill for a repo-grounded interview, or the `grilling` skill for a plain interview; reuse known answers. |
| Understanding is accepted but its contract is absent | Read the `to-spec` skill and bind the actual configured sources, acceptance and Proof. |
| The spec is approved but delivery slices are absent | Read the `to-tickets` skill; preserve vertical boundaries, blockers and public compatibility. |
| Approved code tickets exist | Read the `implement-spec` skill; import the exact graph and continue the same coordinator and record. |
| One authorized code slice needs building | Read the `implement` skill; use the `tdd` skill at appropriate accepted seams. |
| The interface shape is unresolved | Read the `architect` skill, optionally using the `agent-debate` skill for independent alternatives. |
| A code change needs judgment | Read the `change-review` skill for a report; the `sol-loop` skill owns an authorized fix loop. |
| Actual acceptance proof is missing | Read the `result-verification` skill; retain a missing observation as unresolved. |

At a phase boundary, check that the downstream owner has the actual accepted inputs, a checkable result and sufficient authority. Resolve only missing consequential information. A file's existence or an agent's confidence cannot establish readiness.

## Coverage or competing attempts

Choose **coverage** when workers own disjoint parts of a required census; name every expected slice, its owner, write boundary, output and Proof. Missing or failed coverage remains a gap. Prefer one deterministic existing command when it covers the whole census cheaply.

Choose **competing attempts** when alternative artifacts can answer the same decision. Give each the same frame, independent output location and fixed rubric; the `agent-debate` skill owns comparison and synthesis. Report dropped attempts and requested unavailable providers. Concurrent independent candidates, sequential nonblind candidates and inline self-review have different evidence value; name the actual mode.

For related integration layers, record the consumed and produced interface, base identity, dependency order and root integration owner. Separate independent owners before serializing a shared file, schema or live app. Preserve recoverable evidence and cleanup only resources proven owned by this run.

## Bounded continuation and recovery

Record the falsifiable stop predicate, finite starts/rounds, next action and remaining reserve before dispatch. Every worker, reviewer, replacement and retry consumes that allowance. Select only task-relevant playbooks; an optional environment-improvement candidate is advice until in scope.

Use supported completion events and reconcile an interrupted dispatch before replacing it. Resume from the authoritative record and exact spec/ticket/artifact identities; completed work stays completed, uncertain effects stay unresolved, and an exhausted budget stays exhausted. Ask only for missing authority or a consequential unresolved decision. No schedule or budget renewal follows from selecting a mode.
