---
name: terraform-plan-review
description: Review a saved Terraform or OpenTofu plan for destructive changes, exposure, unknowns, policy and cost. Use for "review this plan", "will this delete anything", or a plan wrapper that mishandles detailed exit codes. Return a verdict bound to the saved plan's digest.
---

# Terraform plan review

Bind the verdict to one saved plan and its target. Review by default; apply that same artifact only within existing explicit authorization.

For refactors, imports, locks, backend changes or drift reconciliation, read the `terraform-state-operations` skill when installed. Module implementation and organization-wide policy design are separate jobs.

## Establish the review object

1. Record the engine and provider versions, source revision, variable-input identity, backend/state identity, workspace, account or project, and region. Get the account from authenticated readback; a workspace name does not establish isolation.
2. Require the saved binary plan and JSON generated from it, or a supplied JSON export for a limited review. With JSON alone, report its digest and withhold an apply-ready verdict until its relationship to the saved plan is proved.
3. Restrict access to plan files, state and logs. They can contain credentials even when human output marks values sensitive. Generate JSON into a protected file; never paste it into chat, CI logs or a PR.
4. Run the repository's engine formatting/validation, provider lint and configuration checks. Inspect provider/module sources, external data and provisioners before executing untrusted configuration; planning can execute code and contact services.

Done when the plan, inputs and actual target are identified, or the missing binding is a stated blocker.

## Check the plan

Read [references/review-contract.md](references/review-contract.md) when exporting a plan, interpreting fields, or changing a CI wrapper; it defines the helper and wrapper checks.

```sh
python3 <skill>/scripts/plan-summary.py plan.json --saved-plan saved.plan --detailed-exit-code 2
```

Pass the engine's captured exit code, not a guessed value. The helper reads local files only and reports hashes, action counts, redacted addresses, forcing root attributes and risk flags. Exit 0 means no helper findings, 1 means findings, 2 means unusable input; none is a go verdict.

Review every resource action, output change and drift entry, not a sample:

- **Replace/delete:** identify the forcing path or action reason; absent `replace_paths` does not make a replacement harmless. Trace retained data, replicas, snapshots, encryption keys, dependents, restore proof and downtime. Treat stateful replacement or deletion as a stop until the owner accepts the concrete recovery plan.
- **Authority/exposure:** compare effective IAM grants and trust, ingress and egress, public storage, encryption and retention. Inspect actual values privately; a resource-type flag identifies work, not whether permissions expand.
- **Unknowns:** distinguish harmless computed identifiers from unknown policy, public access, target identity or capacity. Resolve material unknowns or make them explicit blocking conditions; `null` and unknown are different.
- **Policy/cost:** run existing plan-JSON policies with allow, deny and unknown fixtures. Record baseline, estimated delta, usage assumptions and omitted charges; check current provider pricing. No purchases or reserved capacity follow from a review.

The helper's stateful and authority type patterns are conservative cues, not a complete provider inventory. Review unmatched types against the installed provider schema and service behavior.

Add `--stateful-type TYPE` for each exact repository-specific type whose data or identity must survive. The read-only `scripts/plan-exit.sh STATUS` classifies a captured detailed status as `plan_changes=false|true`; it never invokes the engine. Test the repository's actual capture path separately.

Done when every destructive action and material unknown has an owner decision, every relevant policy has evidence, and cost uncertainty is visible.

## Verdict and optional application

Return `go`, `go-with-conditions`, or `no-go`, with the saved-plan SHA-256, JSON SHA-256, target/state/source/provider/input binding, findings and evidence. Give each condition a specific owner and observable clearance. A changed artifact or input requires another review.

Before an authorized apply, recheck account/project, region, workspace/state, lock/writer identity and artifact digest. Serialize writers and apply the reviewed saved plan; never regenerate silently. Production apply, destroy, state surgery and force-unlock need explicit task authorization; `-auto-approve` belongs only in an explicitly disposable sandbox.

After apply, read back the changed controls and service/data behavior, then run a normal plan for unexpected residual changes. A state snapshot restores metadata, not deleted infrastructure or application data. On partial failure, preserve evidence and reconcile actual state before another action.

Done when the digest-bound review is complete and either a review-only handoff is ready, or the authorized apply has target-bound readback and unresolved effects recorded. Live references: [references/sources.md](references/sources.md); read them when checking engine fields, support, licensing, policy tools or prices.
