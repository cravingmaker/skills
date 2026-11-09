# wizard: claude activation-2

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-2` in `evals/examples.md`.
- **Skill revision.** Commit `f5a0c4f4a80ea04590d4330e952921e81ac97bdd`, tree `15559f705666b52d92b17093c2948016f670d20e`, actual bytes SHA-256 `cf752a967fd312374401a921bf6a11ed58082a606198d9442104f3c3ab8a6d87`; dirty: `False`.
- **Fixture.** `activation-2`, SHA-256 `90eb9afcdc30a4ee9c44cc262ba377ced34d824fbfe958a21927e9eb86a033db`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
I need to rotate the database password across three dashboards; walk me through it step by step.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 11 | 0 |
| baseline | false | false | 2 | 0 |

Treatment: 26 response lines; changed files `.cache/npm/_logs/2026-11-09T05_42_50_175Z-debug-0.log, scripts/rotate-db-password.sh`; removed files `none`; validation command present: `requires review`. Workflow cost: 245.215 seconds and 11 tool calls; token usage is in the JSON record.

Baseline: 24 response lines; changed files `none`; removed files `none`; validation command present: `requires review`. Workflow cost: 48.074 seconds and 2 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: a wizard with one focused stage per dashboard and a `confirm` before each irreversible action.

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
