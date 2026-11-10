> **Human documentation.** Agents should not read this page unless a person asks them to.

# The recommended flow

The usual path is a grounded interview, an agreed spec, stable tickets, implementation with proof, then a requested retrospective. Enter at the stage your work needs; an already agreed decision or small fix does not need the whole sequence.

## Contents

- [Choose the starting point](#choose-the-starting-point)
- [Set up once when needed](#set-up-once-when-needed)
- [Agree on terms and decisions](#agree-on-terms-and-decisions)
- [Write the agreed spec](#write-the-agreed-spec)
- [Approve stable tickets](#approve-stable-tickets)
- [Implement one slice or the graph](#implement-one-slice-or-the-graph)
- [Branch for uncertainty, defects, and review](#branch-for-uncertainty-defects-and-review)
- [Choose the delivery boundary](#choose-the-delivery-boundary)
- [Review or continue the session](#review-or-continue-the-session)
- [See the shipped router's stage map](#see-the-shipped-routers-stage-map)
- [Worked example: adding JSON output to a CLI](#worked-example-adding-json-output-to-a-cli)

## Choose the starting point

Give the agent the goal, exact inputs, write scope, and desired stopping point. A natural-language request can activate a model-invocable method. Select native commands for manual entries; use `/<name>` in Claude and `$<name>` in Codex.

A useful starting prompt is: "Add JSON output to the word-count CLI, preserve its existing text output and errors, and stop after a local reviewed implementation." A different request, "get this ready without merging," deliberately extends the delivery boundary. Neither request should silently turn into production deployment.

The core path is `grill-with-docs → to-spec → to-tickets → implement or implement-spec → retro`. The final retrospective is requested work, not an automatic extra campaign. The collection combines this path with the source tracing, evidence, review, and delivery methods adopted from pstack and tstack.

## Set up once when needed

Project configuration tells shaping methods where the tracker, glossary, and ADRs live. If it is missing, explicitly ask the setup entry to establish that contract. It maintains one Agent skills block and the applicable files under `docs/agents/`.

For a local example, choose a spec directory, a ticket directory, one glossary, and an ADR directory. The configuration can name semantic files that do not exist yet. They are created only when a term or decision needs recording.

Setup is not required for an ordinary rename, source walkthrough, or local review. When filing configuration is missing, the shaping methods can return drafts instead of inventing a tracker.

## Agree on terms and decisions

Use the docs-recording interview when the design needs decisions preserved with the domain language. Type `/grill-with-docs` or `$grill-with-docs`, then name the plan and any existing constraints.

For the CLI example, ask: "Keep default text output stable; help me settle the JSON schema and error behavior, and record resolved terms at the configured paths." The agent reads existing code and decisions before asking. It asks the current frontier of independent consequential questions, recommends answers, and waits.

The handoff is a confirmed close: settled choices, stated assumptions, deferred decisions with owners, and the next step. Resolved glossary entries are recorded within write scope. An ADR is proposed only for a hard-to-reverse, surprising choice with a real trade-off, and is written when accepted.

Use the no-doc entry when you want the interview to stay in chat. An explicit interview waits for confirmation before acting on its plan. Embedded clarification fills the caller's particular gap without reopening the whole plan.

## Write the agreed spec

Select the spec entry after the understanding is agreed. For example: "Write up this confirmed close as a draft spec; do not file it yet."

The spec preserves scope and uses numbered user stories. Each story states observable acceptance and named Proof: what surface to drive or source to open, and what result to observe. File inputs are bound by SHA-256 so the next stage can detect drift.

For the example CLI, a story might require `--json` to emit a JSON number while the default output stays unchanged. Proof should drive the actual CLI and inspect stdout and exit status. A unit test alone is not the promised CLI observation.

The handoff is the approved spec, its sources and hashes, test seams, acceptance, and Proof. Open questions retain owners and keep the spec in draft. This stage does not restart the interview or implement the feature.

## Approve stable tickets

Select the ticket entry with the exact approved spec. It proposes vertical slices, presents blockers and Proof, and asks you to approve the breakdown before filing. An already approved breakdown is reused.

For the CLI example, one ticket can add the JSON behavior with compatibility checks. A dependent ticket can cover any remaining documented help and error behavior. Each slice must be useful and verifiable; a schema-only ticket followed by an API-only ticket is usually the wrong split.

Local tickets use one `NN-slug.md` file each, stable numbers, Status, acceptance checkboxes, a one-line `Proof:`, and `Blocked by:` numbers or `None`. When available, the owned importer validates them against the exact approved spec. Do not combine them into one file or reword approved requirements during import.

The handoff is the approved graph and exact ticket bodies. Wide mechanical refactors can use expand, migration batches, and contract, while independently deployed consumers keep their compatibility obligations.

## Implement one slice or the graph

Select the single-slice entry for one authorized ticket or agreed change. It grounds the work, chooses meaningful behavior proof, builds the slice, runs relevant checks, self-reviews, and reports COMPLETE, PARTIAL, or BLOCKED. A leaf starts no reviewers or second controller.

Select the graph runner for an approved spec and its tickets. It imports the existing IDs, status, blockers, acceptance, Proof, and source hashes without another interview or decomposition. One coordinator owns the integration branch, records, worker starts, reviewers, retries, and final acceptance.

Before dispatch, it records a finite budget and checks write ownership. Eight is the collection's maximum active subagent count; a lower user or live-host limit wins. Workers receive exact pointers and leaf briefs. The coordinator reruns the named Proof on worker artifacts and again on the integrated result before acceptance or authorized ticket closure.

If required dispatch or host-owned isolation is unavailable, the orchestrator stays at source-bound preflight. It must report worker execution and integration acceptance as blocked. A local edit is not evidence that a requested delegated workflow ran.

## Branch for uncertainty, defects, and review

Choose the branch by the unresolved question, not by a desire to load more skills. The [generated intent guide](choosing-skills.md) and [boundary examples](skills.md) provide the complete lookup.

A prototype answers a bounded design question with a throwaway artifact. For example: "Try two JSON error shapes with realistic CLI consumers; stop at the observed trade-off." It does not promote the prototype to production or require a new branch and push.

Research answers a bounded factual question from primary sources. Use it before a decision that depends on an API or specification fact. A source walkthrough explains the current path; historical rationale needs attributable history.

Diagnosis starts from the reported symptom and a discriminating feedback loop. For example: "This CLI returns exit 0 on malformed JSON; reproduce it, rank causes, and verify the causal fix." Capture-only or static diagnosis can be useful but must keep its evidence limits.

Test-first work uses a meaningful public seam and a failure for the predicted reason before the fix. A trivial reversible edit needs no ceremonial test. Refactoring pins existing behavior before moving it.

A change review reports Standards and Spec separately and makes no product edits. A sol loop adds authorized repairs and rechecks within a declared round limit. A council selects code-fix, design, or report-only panel behavior according to the request; unavailable named providers are reported, not replaced. Adversarial probes keep static proof separate from runtime observations and charge failed attempts to the declared allowance.

## Choose the delivery boundary

State the end you want before shipping starts. A skill name does not erase a narrower instruction such as "draft only," "do not post," or "do not merge."

| Request | Expected end state |
| --- | --- |
| "Write the PR body" | A local title/body draft grounded in the diff; no remote mutation |
| "Create the PR" | The requested PR is filed and read back with its current state |
| "Watch this PR" | The root owns one supported watcher and handles authorized blockers |
| "Full stop; prepare this without merging" | A verified ready PR, or an explicit remaining approval/blocker; open and unmerged |
| "Full send; take this to a merged PR" | A guarded merge after proof, checks, reviews, and repository gates pass |

The body entry dispatches to the PR-writing method's body-only mode, unless the same request or existing task authority permits filing. A filing-only task returns the link and state; it does not automatically start monitoring. Only the root watches, and only when requested or while an already authorized action waits.

Prepare-only mode must propagate no-merge to every helper and child. It inspects owned auto-merge and queue entries, cancels pending mechanisms it owns, and verifies their absence. It also carries the parent method's task-needed testing permission, subject to narrower task and host restrictions.

Finish-to-merge does not waive required checks, bots, CODEOWNERS, approvals, or human requests for changes. Evidence must cover the current head and relevant base. Old unresolved feedback remains relevant after pushes. A queued PR is not a merged PR; merge completion needs readback.

## Review or continue the session

Request a retrospective when you want to learn from the actual session. Supply allowed evidence explicitly when privacy or scope matters. The method separates current files from historical evidence and prefers a working check over another paragraph of instructions.

Use a continuation note for a fresh session, the durable record for a known run, and history discovery when the old locator is unknown. The note preserves exact pointers, remaining budget, uncertain ownership, and the first unmet condition. A catch-up is read-only and keeps every pending user decision, including ones older than its default since-last-human window.

## See the shipped router's stage map

The [generated role flow table](routing.md#on-main-agent-orchestrator) names each shipped router stage and its conditional methods.

## Worked example: adding JSON output to a CLI

On 2026-11-09 the main flow ran end to end in a disposable Codex fixture: a small Python word-count CLI gaining a `--json` flag. This is what each stage produced. It ran on Codex CLI 0.167.0 with `gpt-6.1-sol`; Claude Code was not part of this run.

| Stage | What you would type | What came out |
| --- | --- | --- |
| Setup | `$setup-agent-skills` | One `AGENTS.md` block and three `docs/agents/` files; a repeat run changed nothing; glossary and ADR files stayed absent until needed. |
| Shape | `$grill-with-docs add --json output` | Questions only after reading the code and domain paths. Glossary terms written as they settled; the ADR "exact JSON output contract" and the close written only after acceptance. |
| Spec | `$to-spec` | Five stories, each with observable acceptance and a real CLI Proof; all 11 source hashes matched when filed; no second interview. |
| Tickets | `$to-tickets` | Two vertical slices (stories 1 to 3, and 4 to 5), ticket 02 blocked by 01; the importer exited 0. |
| Build | `$implement-spec` | One coordinator, two workers and one fresh reviewer: 3 of 12 budgeted starts. Ticket 01's test failed for the predicted reason before the feature, then passed. Final acceptance ran all five Proofs (22 CLI invocations) and eight tests. The reviewer found no Standards or Spec findings. |
| Ship | "open a PR" | The integration branch pushed to a local bare remote and a simulated PR read back with its head, base, checks and threads. No watcher, no merge. |
| Learn | `$retro` | A report that separated a harness defect from intentional test seeds and proposed no unsupported skill rewrite. |

What this run did not prove: native subagent spawning (workers ran through a serial adapter), real GitHub APIs, bots, watches or merges, and any Claude Code behavior. The run also disclosed an outer-evaluator read of installed harness guidance before checking the pinned implementation; the fixture pass does not attest that the evaluator made zero real-home reads. It found one defect, in the eval harness rather than in any skill: Codex's activation counter missed native `$<name>` selection. It was fixed before the stack landed on `main`.

