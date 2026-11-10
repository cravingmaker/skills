# Review contract

Read this when exporting a plan, interpreting helper output or changing a CI wrapper.

## Protect and bind

Use the installed engine's help and official JSON-format reference for the exact commands and fields. Redirect saved plan, `show -json` and planning diagnostics into the project's restricted artifact location with private permissions and retention. Avoid shell tracing and broad CI uploads. JSON is often less redacted than the text display.

Hash the saved binary and its JSON export. Record source revision, variable-input digest or secret-version identifiers, engine/provider locks, backend object/version, workspace and authenticated target. A hash proves byte identity only; the helper cannot prove the JSON came from the supplied binary or that the state is current. Establish that relationship in the protected export step.

## Helper contract

Runtime: Python 3.12+ standard library; no providers, network, subprocesses or writes. `--help` exits 0 before file access. Invocation:

```sh
python3 <skill>/scripts/plan-summary.py plan.json --saved-plan saved.plan --detailed-exit-code 2
```

`--saved-plan` and `--detailed-exit-code` are optional when the inputs were not retained; their missing binding stays unresolved. The helper supports plan JSON major format 1 and requires `planned_values`; a state JSON file is not a substitute. Unsupported schemas fail or produce findings; verify the current engine's schema instead of coercing it.

Output is one JSON object on stdout: JSON/binary hashes, captured engine exit code, action counts, rows from changes and drift, output-change counts, unknown-output presence and findings. Errors are fixed diagnostics on stderr with payload withheld. Exits: 0 no helper findings; 1 findings or engine planning error; 2 unusable input. Exit 0 never means approved.

Each row contains a redacted address, type, action list, replacement flag, forcing root attributes, action-reason presence and risk flags. String instance keys are redacted; exact address resolution and full forcing paths stay in private review. Root attributes alone do not identify a nested forcing value. Treat metadata as restricted too: names can carry sensitive context.

Type patterns flag common databases, disks, buckets, storage, encryption keys and IAM/network surfaces. They are not a provider-complete policy. Unknown types, resource modes, action classes, incomplete/deferred work and nonpassing checks need explicit review. Outputs and drift may be material even when no managed resource is created or deleted.

`--stateful-type TYPE` adds an exact provider type to destructive-effect findings; repeat it for additional types. Resolve those types from the installed provider schema and the repository's persistent-data inventory.

## Wrapper checks

Capture the engine's `plan -detailed-exitcode` status before a pipe, negation or another command overwrites it. When shell fail-fast is enabled, use an explicit conditional around the planning command and assign its status in the failing branch. Interpret 0 as successful/no changes, 1 as an error, 2 as successful/changes; reject other statuses. Never turn 1 into a reviewable stale artifact. A two-stage wrapper should pass the captured status and newly generated export to the helper.

Test the actual repository wrapper using a fake engine that exits 0, 1 and 2 and writes only inert fixtures. Require 1 to stop with no stale summary, 0 to reach the no-change branch, and 2 to reach review rather than the error branch. Run the real engine separately in an authorized disposable environment; synthetic exits prove shell control flow only.

The POSIX `scripts/plan-exit.sh STATUS` takes only an already captured numeric status. It emits `plan_changes=false` for 0 and `plan_changes=true` for 2, both with exit 0; engine status 1 or another numeric status exits 1 without stdout. Missing/nonnumeric input exits 2; `--help` exits 0. It reads no plan, executes no supplied command and writes no file. Pass its output to the repository's review branch; a successful classification is not policy approval.

The shipped fixtures test a fail-fast shell wrapper using a fake engine with statuses 0, 1, 2 and 3, plus the summary helper's contradictory status/artifact cases. They prove the classifier and fixture wrapper, not the unseen repository wrapper or hosted plan execution.

## Verdict receipt

Record verdict, plan/JSON hashes, target/state/input/source binding, engine/provider identities, all replacements/deletes with forcing attribute or reason, authority/public-access changes, unknowns, policy evidence, cost assumptions, recovery evidence and conditions with owners. Apply-ready review requires all binding checks. Missing pricing or optional tools remain a named limitation; missing target identity or unresolved destructive effects block a go verdict.
