# Workflow structure outline

Compare this outline with the repository's existing workflow; it is not replacement YAML.

| Part | Decision to preserve |
| --- | --- |
| Events | Declare the requested PR, push, merge-queue, manual or reusable entry points and their refs. |
| Permissions | Workflow default `{}`; each job grants only its required token scopes. |
| Validation | Runner, checkout without persisted credentials when possible, repository install/build/test commands, explicit timeout. |
| Matrix | Declared target set, fail-fast choice, bounded parallelism and a stable aggregate gate. |
| Gate | Unique static check name, explicit `needs`, runs after failure, inspects every required result. |
| Concurrency | Validation may cancel stale runs; mutation serializes by environment with cancellation disabled at workflow and job levels. |
| Environments | Confirm existing protections and ref eligibility through target readback before dispatch. |
| Artifacts | Source SHA and digest attached to named outputs; downstream jobs consume the same bytes. |
| Release | Trusted event, protected destination when supported, minimal job permissions, no cache restore. |

Resolve every action SHA and tool version live; placeholders and invented pins do not belong in the final workflow.
