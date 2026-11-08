---
name: sol-loop
description: Run a bounded review, fix, and recheck loop over an authorized code change, with stable finding IDs and explicit evidence. Use when the user asks for a sol loop or an iterative code review and repair; a read-only review stays report-only.
license: MIT
metadata:
  source: "https://github.com/t3dotgg/tstack/blob/1085050f3baed1ac724caa4a8166145fb2ac88af/skills/sol-loop/SKILL.md"
  source-revision: "1085050f3baed1ac724caa4a8166145fb2ac88af"
  source-files: "skills/sol-loop/SKILL.md"
  local-changes: "Kept bounded rounds and a finding ledger; unified panel code loops; retained unresolved probes and real provider identities; removed fixed models, rarity demotion, branding and unbudgeted review starts."
  requires: "change-review decision-log"
---

# Sol loop

Review, make the smallest authorized repair, and recheck the exact change within one finite budget. Read the `change-review` skill and the `decision-log` skill before use; if either required skill is missing, name it and stop this flow. Loading this skill grants no fix, commit, push, posting, or merge authority. For a read-only request, use the report-only mode of the `change-review` skill and stop after the report.

## Declare the run

1. **Pin.** Reuse the agreed intent, exclusions, base SHA, HEAD, paths, and staged/unstaged/relevant untracked scope. Preserve unrelated changes. Record content identities before each review; do not let an independent reviewer read a moving target.
2. **Budget.** Declare three review/fix rounds by default before the first review starts. A justified security, permissions, auth, data-loss, or concurrency run may declare up to five in advance; honor another finite user-specified cap declared before the run. Never extend the cap mid-run or reset it by renaming a finding. A fresh review after fixes consumes another round.
3. **Seats.** A normal round has one named reviewer/lens. A requested council code panel has the declared distinct provider seats within the same round and budget. Reserve all reviewer starts, replacement attempts, retries, and other descendants with the existing coordinator: at most eight live subagents or the lower host/user limit, plus a finite total-start allowance. Reviewers start no children or controllers; a leaf returns to its coordinator for independent review.
4. **Identity.** Resolve active supported host capabilities and record actual provider/model/effort only if exposed. A plain sol-loop request selects an available Sol route discovered from those capabilities; an explicit reviewer or panel request selects those identities. Honor the requested Sol or other provider; if unavailable, report it and the unfilled seat without substitution. Do not present an inline or same-provider pass as an independent multi-provider panel.
5. **Record.** Use the authoritative run record maintained by the `decision-log` skill for scope, round/start usage, finding ledger, evidence pointers, and durable next action. Reuse an existing record rather than opening a second controller or parallel log format.

Done when scope, remaining authority, provider seats, round cap, start allowance, and record location are explicit.

## Run each round

1. **Review.** Use the `change-review` skill as the report-only primitive. Round one covers the full agreed change; later rounds cover open IDs, changed behavior, affected callers, and evidence invalidated by the new revision. Give each seat the same pinned frame and prior ledger. Freeze scoped edits until reports arrive. Wait through the active host's supported completion mechanism; timeout or failure is not approval. Cancel a replaced run and account for its start.
2. **Validate.** Judge each finding and severity against its actual impact and evidence. Static deterministic defects remain valid; runtime probe claims need real runs. Rare reachable security, concurrency, or data-loss defects can be severe. Repeated panel findings get one root-cause identity, not extra votes. Keep Standards and Spec conclusions separate.
3. **Dispose.** Agree and fix within authorized scope; disagree with source/run evidence; or record an explicit scope withdrawal or deferred follow-up. Do not mark a concern resolved merely because it is disputed, repeated, renamed, or inconvenient. A required unrun probe stays open under its ID.
4. **Repair.** Make the smallest effective correction and focused behavior proof where needed. Preserve defensive checks, compatibility, source fidelity, and rationale. Product changes outside the authorized slice remain findings, without an automatic rewrite. Re-run relevant checks and update the artifact identity and ledger.
5. **Recheck.** If behavior changed or supported concerns remain, use the next reserved round while budget remains. Retain still-applicable evidence; re-run invalidated proof on the new artifact. Each old ID returns as resolved with evidence, still open with reason, or explicitly withdrawn/deferred with its authority and limits.

Read [references/finding-ledger.md](references/finding-ledger.md) when recording finding transitions or resuming a run.

## Stop honestly

Stop when the current artifact has the required review and proof with no unresolved blocking finding or required probe; say what was actually covered. Nits or declined advice alone do not force a new round, and doc/format-only edits need only the checks they invalidate. Stop with unresolved state when the cap/start budget is exhausted, required provider or evidence is unavailable, or a dispute remains after two evidence exchanges. Unanimity, silence, renamed IDs, and budget exhaustion do not establish agreement or proof. Report rounds and starts used/remaining, actual participants, base and final artifact identity, per-axis result, fixed/open/disputed/deferred IDs with evidence, check results, and next action. Report usage only when returned by the host. Continue already authorized delivery only within its existing scope; keep any no-merge boundary and add no compulsory public model branding or watcher.

Read [references/SOURCES.md](references/SOURCES.md) when checking provenance and adaptation boundaries.
