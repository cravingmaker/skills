# grill-me: claude activation-2

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-2` in `evals/examples.md`.
- **Skill revision.** Commit `312b66d24aa771fa04dec33b4b1a076d2a686079`, tree `e71e66e05d68e9fd0424a26c4b1c63cdd3b08ca4`, actual bytes SHA-256 `c24564cb17f1b8bee5f6c3fbd1e515c851e4d9267eb8a9fa80ecfdb12df2c182`; dirty: `False`.
- **Fixture.** `activation-2`, SHA-256 `490d275d5affd708c106293b17e3ac0e4d65030de55bf457f1291abce759a2e0`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
/grill-me

Use the `grill-me` skill explicitly for this request.

grill-me on the retry policy we sketched above.

Task context supplied to both arms:
Prior retry-policy decisions: three retries at most, exponential backoff with jitter, no retry of 4xx. Open: deadline after which a job must be abandoned. These decisions are settled.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 4 | 0 |
| baseline | false | false | 5 | 0 |

Treatment: 36 response lines; changed files `.cache/npm/_logs/2026-11-09T03_23_10_385Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 43.513 seconds and 4 tool calls; token usage is in the JSON record.

Baseline: 39 response lines; changed files `.cache/npm/_logs/2026-11-09T03_24_53_266Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 42.22 seconds and 5 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: decisions already sketched above are listed as settled; only open choices are asked.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-activation-2-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-activation-2-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-2-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-2-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-2-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-2-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-2-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-2-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-2-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-2-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-2-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-2-claude/baseline/artifacts/`.
