---
name: release-rollback-planning
description: Write and rehearse the undo before a deploy, bound to artifact digests, config, schema state and the effects rollback cannot reverse, with rollback-versus-roll-forward criteria. Use before a risky deploy, for "how do we roll back this release", or after a rollback failed or was slower than expected.
license: MIT
compatibility: Python 3.12 or later for the read-only checker.
---

# Release rollback planning

Deliver a rollback plan record and a measured drill before the deploy, so the decision during an incident is "run the rehearsed undo" or "roll forward for the stated reason", not an improvised repair.

This skill plans and rehearses. Running a rollback in production needs explicit authorization in the task or incident. Versioning, changelogs and tags belong to the `release-automation` skill; schema change sequencing belongs to the `postgres-migrations` skill when installed; PostgreSQL engine upgrades belong to the `postgres-version-upgrades` skill. Release go/no-go is the QA role's decision; this plan is one of its inputs.

## Record the plan

Compare [assets/rollback-plan.json](assets/rollback-plan.json) with the project format and fill it from live sources; the unfilled starter must fail the checker. Keep config, commands and private receipts free of credentials and personal records. Confirm target identity immediately before mutation; serialize writers and stop on uncertain partial effects. The record holds:

1. **Identity and authority.** Source revision, exact account/project/region/cluster or database, decision owner and existing authority for target/effects. Planning grants no execution permission.
2. **Exact versions.** Candidate and previous artifacts by digest (`repo@sha256:…`), resolved with the registry's tooling (for example `crane digest` or `docker buildx imagetools inspect`), never typed or copied from a tag. Configs by commit SHA or digest. How long the previous artifact and config stay retained; registry cleanup can delete the version rollback needs.
3. **Delivery path.** Push or GitOps. With a GitOps controller, rollback goes through the desired-state repo, or auto-sync is suspended first; otherwise the controller reapplies the candidate. Check the controller's current documentation for its rollback and auto-sync behavior.
4. **Rollback commands and budget.** The exact commands, with no `<placeholders>`, the longest acceptable duration, abort/escalation conditions and an independent recovery observation window.
5. **Schema state.** The expand, migrate or contract phase after this deploy, and whether the previous code runs on it. Prove actual old-code compatibility: a contraction that removes an old-code dependency blocks rollback; contraction alone does not establish incompatibility.
6. **What rollback cannot undo.** Never empty. Read [references/rollback-limits.md](references/rollback-limits.md) to find them: data written or deleted, messages and emails sent, external calls, format migrations, client caches, mobile builds, DNS and certificate changes. Give each its handling.
7. **Decision.** Rollback triggers as signal plus threshold plus source, conditions for rolling forward instead, who decides, and the decision deadline.

Rule of thumb: roll back when the previous version was healthy, it runs on the current schema and configuration, and nothing irreversible blocks it. Roll forward only when rollback is impossible (contracted schema, incompatible data) or slower than an already reviewed fix.

Done when every field holds a live-resolved value and the cannot-undo list names at least the effects the reference's checklist finds.

## Rehearse in a non-production environment

1. Use an explicitly disposable staging target with contained jobs, credentials and external effects, representative schema and the same delivery path as production.
2. Run the recorded rollback commands exactly. Measure through verified user-path recovery, including controller sync, image pulls, warm-up and the agreed observation window. For roll-forward, exercise the reviewed compatible candidate repair and record its recovered artifact; do not try to run incompatible old code.
3. Run a user-path check (a real request through the service, not only a health endpoint) and record the result.
4. Keep a local private receipt with commands/exits and actual effects. Record the drill target/kind, action, date, both artifact and config identities, recovered artifact, measured seconds and user-path result. Bind plan_sha256 to the checker output for the exact plan excluding drill; edits invalidate that proof. Restamping a hash without another drill supplies no evidence.

If the drill fails or exceeds the budget, fix the plan and drill again. Record staging differences in load, data and provider behavior; they limit production timing claims. If no non-production environment exists, record the plan as unrehearsed and say so; do not drill in production without explicit authorization.

## Check the record

```sh
python3 <skill-dir>/scripts/check-rollback-plan.py [--max-drill-age-days 30] plan.json
```

It rejects tag-named artifacts, branch-named configs, identical candidate and previous artifact/config state, missing retention, GitOps plans without auto-sync handling, placeholder commands, a rollback strategy on an incompatible schema, missing source/target/authority or abort/recovery, an empty cannot-undo list, triggers without thresholds, and drills that ran in production, on other digests, over budget or without a passing user-path check. Only finding codes, safe enums/counts and the plan digest reach JSON on stdout; diagnostics on stderr. Exits are 0 structural pass, 1 findings and 2 usage or malformed input. Help exits 0 without effects. It rejects duplicate keys and non-finite numbers and never executes a plan. `--allow-unrehearsed` accepts a draft without a drill. The drill must bind the current plan, exact configs and a confined local receipt. A pass checks declarations and file existence; inspect the receipt and live sources before claiming rehearsal, authorization or target behavior.

Done when the checker exits 0 on the final record, or the report names it as an unrehearsed draft.

## Report

Return the plan path, both digests, strategy, schema phase, the cannot-undo list, the drill environment, date and measured duration, the user-path check result, the checker output, and anything not rehearsed.
