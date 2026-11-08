# Review report format

This is the format `scripts/check-review.py` checks. It fixes the structure so the coordinator can count, track, and answer findings across rounds; it says nothing about whether a finding is true.

## Layout

```markdown
REVIEWED: <artifact> at <revision or SHA-256>; scope: <what was read>
CHECKS: <commands run and their results, or "none">

## Prior findings
- R1-02 CLOSED: <why, with the evidence that closed it>
- R1-03 WITHDRAWN: <the counter-evidence that settled it>

## Findings

### R2-01 [should] <file>:<line or section>: <the claim in one sentence>
Evidence (executed): <command and observed result>
Change: <the exact change>

<optional mechanism, consequence, or context>

### R1-01 [blocker] <file>:<line>: <claim>
Evidence (static): <quoted text and where it is>
Extension: <the new evidence or material change that justifies a fourth round>
Change: <the exact change>

## Not checked
- <what was out of reach, and why>

VERDICT: OBJECTIONS REMAIN (1 blocker, 1 should, 0 nits)
```

The evaluator template also carries the shared `agent-briefing` return fields: completion status, artifact identity, loaded skills, unresolved claims, decisions, assumptions, and usage. Completion status reports whether the review was performed; the verdict reports whether objections remain.

Lines inside fenced code blocks are ignored, so a report can quote commands, files, or other reports. The `CHECKS:` line and the `Not checked` section are part of the evaluator brief but not enforced: write "none" rather than leaving them out.

## Rules the checker enforces

| Rule | Why |
| --- | --- |
| Exactly one verdict line, and it is the last non-empty line | One parseable outcome per round; no findings after the verdict |
| The verdict is `VERDICT: FULL AGREEMENT` or `VERDICT: OBJECTIONS REMAIN (n blockers, n shoulds, n nits)` | One vocabulary, so a script and a reader agree on the outcome |
| The counts match the findings; `FULL AGREEMENT` has no open findings; `OBJECTIONS REMAIN` has at least one | The verdict cannot hide or invent objections |
| A non-empty `REVIEWED:` line | A verdict applies to one revision; a later change needs its own review |
| Every finding heading is `### <ID> [<severity>] <location>: <claim>` (two to four `#`) | Stable, countable findings |
| IDs are unique, and no ID is both open and closed | Each objection is tracked once |
| Severity is exactly `blocker`, `should`, or `nit` | Severity drives the stop rules |
| At least one `Evidence (<label>):` line per finding, label `executed`, `static`, or `hypothesis` | The coordinator knows how much to trust it and what to rerun |
| A `Change:` line per finding | Every objection is actionable |
| With `--prior`, every listed ID appears as a finding or as `- <ID> CLOSED: <reason>` or `- <ID> WITHDRAWN: <reason>` | No open objection disappears silently |
| With `--round N`, an `R<r>-<n>` finding open for more than `--max-rounds` rounds (default 3) has an `Extension:` line | The round limit holds unless new evidence or a material change justifies more |
| With `--round N`, an `R<r>-<n>` finding carried from an earlier round has `executed` or `static` evidence | A hypothesis opens a finding but does not buy it another round: pause debate until its spike supplies evidence, retaining the unresolved ID |

Field lines may start with `- ` or `* `. Prose between field lines is allowed.

## Finding identifiers

Use `R<round>-<nn>`: `R1-01` is the first finding raised in round 1. The checker accepts any `LETTERS-NUMBER` ID, such as `F-01`, but computes a finding's age only from `R<round>-` IDs. A finding keeps its ID for its whole life, including when it is raised again after a rejection; a new ID for an old objection would reset its rounds, so the coordinator merges such duplicates under the original ID.

A finding has been open for `current round - r + 1` rounds. With the default limit, `R1-01` may stay open in rounds 1, 2, and 3; in round 4 it needs an `Extension:` line, or it goes to the user as a decision.

## Severity

| Severity | Meaning | Effect |
| --- | --- | --- |
| `blocker` | The intended case is wrong or unsafe, a hard constraint or authorization is broken, or a required check is missing | Must be fixed before acceptance |
| `should` | A supported, in-scope defect that a user or caller will hit | Fix it, or record a decision to accept the risk |
| `nit` | Optional polish | Never blocks and never extends a round |

Severity follows consequence, not frequency: a rare data-loss path can be a blocker. A hypothesis can carry any severity; the coordinator runs the deciding check before acting on it.

## Evidence labels

| Label | What it must contain |
| --- | --- |
| `executed` | The command or experiment run and the observed result |
| `static` | The inspectable text, contradiction, or source statement, with its location |
| `hypothesis` | The concern and the check that would confirm or refute it |

Static evidence is legitimate for architecture, licensing, permissions, naming, and readability. A finding never needs executed evidence to be raised; it needs the right label. To stay open past the round that raised it, it needs executed or static evidence.

## What the checker leaves to judgment

- Whether a claim is true: rerun the command or open the source (the `result-verification` skill).
- Whether a re-raised objection is a duplicate under a new ID.
- Whether an `Extension:` line names real new evidence.
- Whether the severity fits the consequence.
- Whether the `Change:` line is exact enough to apply.

A spike stays unresolved in the run record and retains its finding ID. Keep the ID in `--prior` when review resumes with evidence. Use CLOSED only when evidence resolves the finding, or WITHDRAWN when counter-evidence or an authorized scope change removes it. Pending required spikes prevent full agreement and final acceptance.
