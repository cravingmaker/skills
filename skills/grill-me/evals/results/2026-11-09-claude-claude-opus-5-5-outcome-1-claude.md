# grill-me: claude outcome-1

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `outcome-1` in `evals/examples.md`.
- **Skill revision.** Commit `312b66d24aa771fa04dec33b4b1a076d2a686079`, tree `e71e66e05d68e9fd0424a26c4b1c63cdd3b08ca4`, actual bytes SHA-256 `c24564cb17f1b8bee5f6c3fbd1e515c851e4d9267eb8a9fa80ecfdb12df2c182`; dirty: `False`.
- **Fixture.** `outcome-1`, SHA-256 `490d275d5affd708c106293b17e3ac0e4d65030de55bf457f1291abce759a2e0`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
/grill-me

Use the `grill-me` skill explicitly for this request.

grill-me: my plan is to split the billing service into two deployables.

Supplied task context:
Supplied follow-up answers for this bounded sample: failure isolation is the goal; no independent deployment requirement; one shared database; acceptable risk is one reversible feature flag. Return the currently reachable interview or close; do not invent a further human reply.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | n/a | true | 4 | 0 |
| baseline | n/a | false | 4 | 0 |

Treatment: 48 response lines; changed files `.cache/npm/_logs/2026-11-09T04_57_00_566Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 48.074 seconds and 4 tool calls; token usage is in the JSON record.

Baseline: 32 response lines; changed files `.cache/npm/_logs/2026-11-09T04_58_04_633Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 35.508 seconds and 4 tool calls; token usage is in the JSON record.


Expected deliverable: An explicit invocation produces `grilling` rounds and its close, and writes no files.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-outcome-1-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-outcome-1-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-1-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-1-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-1-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-1-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-1-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-1-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-1-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-1-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-1-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-1-claude/baseline/artifacts/`.

Activation is not graded for Outcome examples; review the stated behavioral criterion.

## Outcome review

Value: **matched**. Baseline criterion: partial; treatment criterion: partial.

Both route into grilling-style questions with no file writes and preserve supplied answers/ADRs. Both correctly stop at the next unanswered round; a full multi-turn close is unavailable in this bounded sample.
