---
name: maintain-verification-skill
description: Audit an existing project's verification driver and full declared feature map against source and real behavior. Use when explicitly asked to maintain the driver or audit its coverage, drift, evidence and cleanup.
license: MIT
metadata:
  source: "https://github.com/cursor/plugins/blob/6b0300214a09fd6029cfb7077043125758cd1fd2/pstack/skills/maintain-verification-skill/SKILL.md"
  source-revision: "6b0300214a09fd6029cfb7077043125758cd1fd2"
  source-files: "pstack/skills/maintain-verification-skill/SKILL.md"
  local-changes: "Kept source/map/live coverage and cleanup invariants; removed the generator prerequisite, fixed fan-out, mandatory PRs, schedules and automatic product repairs; separated recipe drift, environment blocks and product regressions."
---

# Maintain a verification skill

Audit the existing driver's declared coverage from source and then drive that coverage on the real surface. The generator is not a prerequisite: an existing driver can be maintained on its own, whatever created it. Keep the edit scope inside the target driver's directory and owned harness/map files, and only when edits are authorized; a read-only audit returns proposed corrections. Product repair, commits, PRs, and schedules need their own existing task authority.

## 1. Locate and bind

Find the requested driver in the actual installed/project inventory, including legacy names and layouts. Read its SKILL.md, owned scripts, map index and every declared feature file; resolve conflicting candidates from context before asking. Record source/build and driver-content identities, declared surface/map boundaries, available tools/auth, and permitted edits/resources. If no target exists, report that absence; do not invent a generator dependency or silently author a new driver. A bounded driver without a full map can have its declared scope audited; report that limitation rather than claiming project-wide coverage.

## 2. Audit source and map

Reconcile the map index with its actual files: missing, orphaned, duplicate and dead entries. For every declared feature, trace source entry points and current user behavior, compare it with the driver, and retain citations and one concrete live recipe. Check changed routes, commands, menus and docs for omitted features using concrete source paths; a suspected omission without source evidence remains a hypothesis. Keep accepted product requirements authoritative; a mismatch is not permission to rewrite expectations to match a regression. Combine overlapping recipes into practical app states without dropping entry points, prerequisites or promised coverage.

Independent source reading or recipe edits may be partitioned when useful and authorized; all seats/retries use the coordinator's finite shared start budget and at most eight live subagents or the lower host/user limit. Children return evidence and scoped recipe proposals, not new controllers; serialize shared app driving under one owner. Inline source work is valid when independence is unnecessary.

## 3. Exercise the declared coverage

Use the existing driver's launch, doctor, drive, evidence, and cleanup contract. Drive every declared feature and the entry points/sub-features its coverage claim promises; one convenient path cannot stand for the rest. Use one owned long-lived instance where appropriate or fresh isolated CLI sessions as the driver specifies. Keep three invariants throughout:

- **Known state.** Doctor before the first drive, for each fresh session, and after a failed or surprising drive. Reset/relaunch a wedged UI that doctor cannot detect instead of continuing from unknown state.
- **Retained evidence.** Capture the action and result, important side effects, exact command/action, artifact identity, and expected versus actual behavior. Confirm earlier artifacts survive each cleanup at the named location.
- **Owned cleanup.** Clean failed-iteration residue as well as successful runs; stop only resources this run owns. Leave another owner's shared instance running and remove only this run's authorized residue. Teardown follows the final drive, including any reproofs.

A doctor failure caused by recipe drift may be corrected within scope and retried once; restart only what the correction invalidated. An unavailable tool/auth/OS/entitlement is a blocked precondition with the attempted route, evidence and affected features; it is not successful feature coverage. Keep unexecuted paths and runtime hypotheses unresolved.

## 4. Classify and correct

| Class | Evidence and action |
| --- | --- |
| Recipe/map drift | Source and observed intended behavior show a stale description, selector, command, or prerequisite. Correct only the authorized driver files and rerun affected proof. |
| Harness gap | The real feature works, but the driver cannot exercise it. Repair the owned harness only within scope, document helper invocation/runtime, and drive it again. |
| Environment block | Required build, tool, auth, platform, or external state is unavailable. Report the exact blocked step and preserve completed evidence. |
| Product regression | The real behavior violates accepted requirements. Report the causal evidence separately; do not weaken the map or repair product code under this skill's scope. |

For a changed helper, prove useful reject/accept/rerun behavior as well as the real journey; syntax success alone is insufficient. Re-read every changed file and re-drive affected features after all corrections; preserve evidence through final owned cleanup.

## 5. Report

Return **clean**, **changed**, or **blocked**, with any product regression explicit. Clean requires complete source and live coverage of the full declared map with no unresolved regression or blocking path; changed describes proven authorized driver corrections, without implying they were committed or published. Incomplete coverage or unresolved environment/product failure remains blocked even when some corrections were made. Give target/revision, feature-to-source and feature-to-drive coverage, actual results/evidence, drift/corrections, blocked or excluded paths, owned cleanup proof and remaining action. Keep concise run notes at the established scratch/evidence location, without adding a repeating schedule or compulsory shipment.

Read [references/SOURCES.md](references/SOURCES.md) when checking provenance and adaptations.
