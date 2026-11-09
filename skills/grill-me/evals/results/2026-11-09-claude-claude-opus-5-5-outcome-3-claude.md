# grill-me: claude outcome-3

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `outcome-3` in `evals/examples.md`.
- **Skill revision.** Commit `312b66d24aa771fa04dec33b4b1a076d2a686079`, tree `e71e66e05d68e9fd0424a26c4b1c63cdd3b08ca4`, actual bytes SHA-256 `c24564cb17f1b8bee5f6c3fbd1e515c851e4d9267eb8a9fa80ecfdb12df2c182`; dirty: `False`.
- **Fixture.** `outcome-3`, SHA-256 `490d275d5affd708c106293b17e3ac0e4d65030de55bf457f1291abce759a2e0`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
/grill-me

Use the `grill-me` skill explicitly for this request.

grill-me: my plan is to split the billing service into two deployables.

Supplied task context:
This is an interview only. No build, commit, publish, post or document write is authorized.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | n/a | true | 4 | 0 |
| baseline | n/a | false | 4 | 0 |

Treatment: 30 response lines; changed files `.cache/npm/_logs/2026-11-09T04_58_05_353Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 34.315 seconds and 4 tool calls; token usage is in the JSON record.

Baseline: 28 response lines; changed files `.cache/npm/_logs/2026-11-09T04_58_54_090Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 35.691 seconds and 4 tool calls; token usage is in the JSON record.


Expected deliverable: No build, commit, publish, or post happens because the entry was loaded.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-outcome-3-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-outcome-3-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-3-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-3-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-3-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-3-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-3-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-3-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-3-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-3-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-3-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-3-claude/baseline/artifacts/`.

Activation is not graded for Outcome examples; review the stated behavioral criterion.

## Outcome review

Value: **matched**. Baseline criterion: yes; treatment criterion: yes.

Both return an interview round only. Retained manifests show no project changes; no build, publication, commit or posting occurs.
