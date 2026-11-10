---
name: github-actions-workflow-authoring
description: Write or restructure GitHub Actions workflows, job graphs, matrices, reusable workflows and composite actions. Use for "add a workflow", "split this job", or "make a reusable workflow", with stable required checks and hosted-run evidence.
license: MIT
compatibility: Python 3.12+ for the optional checker; use repository-pinned actionlint, zizmor and a YAML parser.
---

# GitHub Actions workflow authoring

Deliver a workflow whose events, job dependencies and required check names match the repository's delivery contract.

## Establish the contract

Read the repository guidance, existing workflows and local actions, lockfiles, build commands, rulesets, merge strategy and runner targets.
Use the current repository tools before adding another dependency.
Record the installed tool versions and verify supported syntax against the [GitHub workflow reference](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax).
Resolve remote action references live from their upstream repositories; keep the repository's update and cooldown policy.

Write a small table with event/ref, work to run, runner, produced check name, dependency jobs, artifact inputs/outputs and destination environment.
Include fork PRs, pushes, merge queues, manual runs and reusable callers when they are part of the requested contract.
Preserve the exact check contexts from effective rulesets, including inherited rules; a ruleset list response alone does not contain every rule's details.
Finish this step when each required event reaches a stable gate and each publication or deployment job has a named authority boundary.

## Build the graph

Use [assets/workflow-skeleton.md](assets/workflow-skeleton.md) when choosing the job structure; compare its outline with the repository instead of overwriting a working workflow.

- **Events.** Avoid workflow-level path filters for required checks unless a separate always-reported gate covers the skipped work. Include the merge-queue event when the repository uses it.
- **Jobs.** Keep dependencies explicit and acyclic. Give runner jobs positive timeouts. A reusable-workflow call is a different job form; put its timeout in the called workflow's runner jobs.
- **Gates.** Use a unique static job name for a required gate. It must report failure when a required upstream job fails or is unexpectedly skipped. An unconditional successful `echo` after `always()` is not an aggregate check.
- **Matrices.** Choose representative platforms and failure policy from the actual compatibility contract. Collect results into a stable gate when generated matrix names would change required check contexts.
- **Concurrency.** Cancel superseded validation only when useful. Serialize mutation by destination environment with cancellation disabled at both workflow and job levels; job settings do not shield a job from cancellation of its whole workflow. Separate validation and mutation workflows when their cancellation policies differ. Review pending-run replacement and queue behavior against current GitHub docs.
- **Authority.** Default workflow permissions to `{}` and grant each job only what it needs. Avoid persisted checkout credentials when no later step needs them. Release and publication jobs restore no caches, including implicit setup-action caches.
- **Artifacts.** Name outputs, source revision, digest, lifetime and consuming job. Caches accelerate reproducible dependency installs; artifact outputs carry release inputs.
- **Environments.** Resolve the destination name and read back its existing protections, eligible refs and bypass rules for the target plan. A name in YAML does not establish a protected environment.

Read [references/reusable-workflows.md](references/reusable-workflows.md) when exposing workflow inputs, outputs or secrets, or choosing a composite action.
Read [references/events-and-caches.md](references/events-and-caches.md) when changing event filters, cache keys or another CI system's equivalent trust model.
Finish this step when the proposed graph preserves the table's behavior and required check names.

## Check structure before execution

Run the repository's workflow checks, including `actionlint` and the default zizmor policy.
Parse YAML with an established YAML parser; never use line matching to decide the workflow's structure.
Read [references/checker-input.md](references/checker-input.md) when using the additional graph checker:

```sh
python3 <skill>/scripts/check-workflow-contract.py workflow.json --rules rulesets.json
```

The Python 3.12+ helper reads parsed workflow JSON and fully expanded ruleset JSON.
It checks declarations, positive static runner timeouts, dependency cycles, static required-check names and cancellation risks for jobs that name an environment.
Expression-based timeouts or cancellation need separate resolved/hosted evidence; a helper finding does not make supported GitHub syntax invalid.
It reads files only; JSON results go to stdout, setup diagnostics to stderr; exits are 0 pass, 1 findings and 2 invalid input.
It cannot evaluate expressions, matrix expansion, event coverage, permissions, reusable-check naming or hosted behavior.
Treat an unresolved context as missing evidence, not permission to rename or remove the repository's required check.

When a trust path changes and the method is installed, read the `github-actions-hardening` skill before its security pass.
For a failing run rather than a new graph, use the `fix-ci` skill when installed.
For repository-wide gate enforcement, use the `project-guardrails` skill when installed.
Test-stage choices such as sharding and quarantine belong to the test owner; timing optimization needs measured evidence outside this graph check.
Finish this step when native analyzers and graph checks pass and any limitations have an explicit hosted check.

## Prove the contract

Use a representative hosted event on an authorized branch or disposable repository.
Before dispatch, identify the repository, source SHA, event, inputs and environment; inspect whether the event can publish, deploy or spend money.
A workflow edit does not authorize publication, production changes or purchases.
Exercise one intended success and one failing upstream job; the required gate must turn red for the latter.
Check skipped paths, fork permissions, matrix completion, artifact transfer, concurrency and reusable callers that the change affects.
Record the actual check-run names, conclusions, run URL, head SHA and relevant setting readback.
An `act` run is local emulation and does not prove hosted permissions, OIDC or environment protections.

Done when the requested event graph works in the recorded hosted cases, required check contexts are preserved, and static checks pass.
Report unavailable hosted cases as not run, with the exact remaining proof; do not claim them from local parsing.
Primary references and freshness checks: read [references/sources.md](references/sources.md) when verifying platform or tool behavior.
