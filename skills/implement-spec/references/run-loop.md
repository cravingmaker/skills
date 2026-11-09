# Run loop details

Read this when resuming a run, running the pre-flight scan, handling a report that is not COMPLETE, running a fix round, or doing the final review. Adapted from Superpowers' subagent-driven-development references.

## Contents

- [Resume](#resume)
- [Pre-flight](#pre-flight)
- [Batching](#batching)
- [Reports](#reports)
- [Cannot verify from the diff](#cannot-verify-from-the-diff)
- [Fix loop](#fix-loop)
- [Final review](#final-review)
- [Rulings](#rulings)

## Resume

Conversation memory does not survive compaction. A coordinator that lost its place and restarted completed tickets is the most expensive failure this loop prevents, so trust the run record and `git log` over your recollection.

- Confirm the record belongs to this spec: its spec path and hash match. A record for another spec, or a stale hash, is not yours to resume; start a fresh record and report the mismatch.
- A ticket with an accepted entry is done; do not restart it. Resume at the first ticket without one.
- A ticket whose last entry is a fix round is mid-loop: resume at the next round, with the counters carried forward.
- A dispatch with no receipt or report stays reserved and unresolved until you reconcile it with the `decision-log` skill: inspect its checkout and branch before starting a replacement.

## Pre-flight

Run once, before the first worker starts. The output is a table in the run record, not a verdict.

- One row for every pair of tickets that share a file or interface: the two tickets, what one produces against what the other consumes, and what you found.
- One row for every ticket: whether its own text agrees with itself, such as the tests it specifies against the code it specifies.
- One row for anything a ticket mandates that the review rubric treats as a defect, such as a test that asserts nothing.

Rule on each finding with the spec as the binding authority and record the ruling beside its row. "The scan is clean" without those rows is not a scan. Review still catches conflicts that only appear during implementation.

## Batching

When several tickets are each a small, independent edit of the same kind (the same one-line fix, constant change or field addition across files), brief one worker with every file and its change, and review its diff as one unit. Keep one worker per ticket for work that needs its own judgment, tests or review. A reviewer of a batch checks the diff file by file; a listed file without its hunk is a missing requirement.

## Reports

Save every report raw before judging it. Treat it as a set of claims to check against the brief, the diff and a rerun of the Proof.

- **COMPLETE with concerns.** Read the concerns first. Correctness or scope concerns are resolved before review; observations (a file is getting large) are recorded and review proceeds.
- **PARTIAL.** Accept nothing that is missing. Decide what changes for the remainder: more context, a smaller ticket, or a ruling.
- **BLOCKED or needs context.** Something must change before another start: supply the missing context, choose a more capable worker, split the ticket, or rule on a plan defect and carry the ruling in the new brief. Never restart the same brief unchanged, and never ignore an escalation.
- **No report, a timeout or a cancellation.** Inspect the checkout, diff and external effects before reusing anything; partial edits are not clean state.

Every restart, replacement and resumed execution is charged to the same budget and keeps the ticket's counters.

## Cannot verify from the diff

A reviewer may list requirements it could not check from the diff alone because they live in unchanged code or span tickets. You hold the cross-ticket context, so resolve each one yourself before accepting the ticket. A confirmed gap enters the fix loop like any other finding.

## Fix loop

The loop starts when review reports a spec gap, a Critical or Important finding, or a cannot-verify item you confirmed.

- Minor findings never enter the loop. Record each as a deferred minor for the final review.
- A finding that conflicts with what the ticket requires is yours to rule on before acting, with the spec as the binding authority. Neither dismiss it because the ticket mandates it nor contradict the ticket without a recorded ruling.
- A round is one fix start plus one scoped re-review. Send the open findings verbatim; the worker fixes them, reruns the covering tests and appends the command and output to its report. Confirm that evidence before starting the re-review.
- The re-review is scoped to the findings and the fix range. It marks each finding addressed or not addressed with file:line evidence, flags new breakage in the fix range, and lists anything outside that range as an out-of-scope observation for the final review. Out-of-scope observations never extend the loop.
- After each round, record the round number, addressed and open finding IDs, and the commit range. Finding IDs stay stable across rounds; a reworded finding is the same finding.
- Repeat up to the declared limit (three by default). A capability change for a stuck worker is a replacement start, charged like any other.
- A small fix may be cheaper for you to make directly than a new start. Make it in the ticket's checkout, rerun the covering tests, record the change and its evidence, and count it as a round; note that it had no independent re-review.

At the limit, stop starting rounds and adjudicate each open finding:

- **Reviewer is wrong or the point is contestable:** park it with a ruling that says why the code stands.
- **Real, but nothing downstream builds on it:** park it with a ruling that it is real and deferred; it is reported as open.
- **Real and load-bearing, or Critical:** the ticket stays unresolved. Rule on the smallest change that unblocks dependent tickets, record it, and carry it into their briefs, or stop if every path forward is a guess.

Adjudicate only at the limit, and record every adjudication; a silent discard is forbidden.

## Final review

When every ticket is merged, reserve one whole-branch reviewer with the `change-review` skill over the range from the integration base to the head. Point it at the deferred minors and parked findings so it can say which must be fixed before merge.

Send all its Critical and Important findings to one fix worker, not one worker per finding, then run one scoped re-review of the fix range. Adjudicate residual findings as at the fix-loop limit. There is no second fix wave; residual load-bearing findings go to the user as decisions.

## Rulings

Record every ruling as `Ruling: <what you decided> — <why> — <what it costs if wrong>`. Before cleanup, collect every ruling, in order, into the final report under "Rulings I made", and every deferred minor under "Deferred minors". Both lists are exhaustive; the report is where the decisions you took on the user's behalf reach them.
