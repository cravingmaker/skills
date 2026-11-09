# Review round <N>: <artifact name>

<!-- Fill every <placeholder>, delete these comments, and wrap the result in a full brief
     with the agent-briefing skill (standing communication contract, host and return contract).
     Leave out your own preferred answer and any other reviewer's verdict. -->

Review <artifact> and report the defects that matter, each with its evidence and an exact change. "No objections" is a valid result: report only what you can support.

## What to review

- Artifact: <path or link> at <commit, tag, or SHA-256>.
- Requirements: <path, or the requirements inline>.
- Your lens: <for example, "correctness for the agents that will run it", "fit to the existing repository", "security and authorization">.
- Prior round (round 2 onward): your last raw report <path>, and the coordinator's responses <path>.
- Scope for this round: <round 1: the whole artifact; later rounds: the open findings, the diff since the last reviewed revision, and anything that diff exposes>.

## Rubric

Fixed before this review; judge against these criteria, in this order, and add none.

1. <criterion>
2. <criterion>
3. <criterion>

## Open findings

<!-- Round 1: delete this section. -->

| ID | Severity | Coordinator's response | Its evidence |
| --- | --- | --- | --- |
| R1-01 | should | rejected | <the counter-evidence> |
| R1-02 | blocker | accepted, changed in <revision> | <what changed> |

For each ID, either close it (`- R1-01 CLOSED: <reason>`), withdraw it when counter-evidence or an authorized scope change removes it (`- R1-01 WITHDRAWN: <reason>`), or keep it open as a finding with the same ID. Keep a finding open only with evidence that the response does not answer. A finding opened in round r may stay open through round r + 2; after that it needs an `Extension:` line naming new evidence or a material change, or the coordinator takes it to the user as a decision.

## Rules

- **Severity.** `blocker`: the intended case is wrong or unsafe, a hard constraint or authorization is broken, or a required check is missing. `should`: a supported, in-scope defect a user or caller will hit. `nit`: optional polish; it never blocks.
- **Evidence.** Label each finding `executed` (the command you ran and what it printed), `static` (the quoted text and its location), or `hypothesis` (the concern and the check that would settle it). Prefer running a check to arguing. A finding you keep open from an earlier round needs executed or static evidence; when you cannot run its check, leave the finding unresolved and name the spike needed before another round. A scheduled spike is not a closure.
- **Exact change.** Each finding ends with the replacement text, the command, or the check to run.
- **Change positions only on evidence.** When the coordinator's response convinces you, say which evidence did. When it does not, say what it leaves unanswered. Agreement for its own sake is a defect.
- **Length.** Use the fewest words that make each finding accurate. Propose deletions as readily as additions; text that adds nothing is a finding.
- **IDs.** New findings in this round are `R<N>-01`, `R<N>-02`, and so on. A re-raised objection keeps its original ID.
- **Boundary.** Read-only. Write only the report file below. Do not delegate.

## Report

Write the full report to <report path> using this format. Return its status, verdict, and path in the host response, unless the caller explicitly requests the full report there:

```markdown
<COMPLETE | PARTIAL | BLOCKED>: <what the review established; completeness is separate from agreement>
REVIEWED: <artifact> at <revision>; scope: <what you read>
CHECKS: <commands you ran and their results, or "none: reason">
ARTIFACTS: <report path; exact input and output revisions; changed files, or none>
SKILLS: <skills actually loaded and any missing prerequisite>
UNRESOLVED: <unsupported claims and evidence gaps, or verified none>
DECISIONS: <decisions needed and owners, or none>
ASSUMPTIONS: <assumptions, deviations, surprises, and boundary conflicts, or none>
USAGE: <measured usage with receipt, or unknown>

## Prior findings
- <ID> CLOSED: <reason>

## Findings

### R<N>-01 [blocker|should|nit] <file>:<line or section>: <the claim in one sentence>
Evidence (executed|static|hypothesis): <what>
Change: <the exact change>

## Not checked
- <what you could not check, and why>

VERDICT: FULL AGREEMENT
```

When findings remain, the last line is `VERDICT: OBJECTIONS REMAIN (<b> blockers, <s> shoulds, <n> nits)`, with counts that match the findings. Before returning, run:

```sh
python3 <path to agent-debate>/scripts/check-review.py --round <N> --prior <open IDs, comma-separated> <report path>
```

and fix every defect it lists.
