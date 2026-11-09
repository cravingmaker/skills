# agent-debate: claude activation-1

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-1` in `evals/examples.md`.
- **Skill revision.** Commit `66f8700b5f86ced76eeb64d9f42201df5ea9f2be`, tree `5dcf0cae82a13b2a6a5f7b905c638363a4fb5c3e`, actual bytes SHA-256 `f4c65ce5c0ba970242cac9c555c8307be7da18a3d504e9f2da9814dacb99ab94`; dirty: `False`.
- **Fixture.** `tests/eval-harness/fixtures/eval-worker/multitask`, SHA-256 `9f2478f72c4e5fa5d08c40b48adcc3f41bb274a5015366ba0ab65535dcb8de0a`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `host default`; each arm has a new session and the same host settings.

## Prompt

```text
Have Claude and Codex debate whether this service should use a queue or a cron job, then bring me the result.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 4 | 0 |
| baseline | false | false | 3 | 0 |

Treatment: 13 response lines; changed files `reports/background-work-decision.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 27.816 seconds and 4 tool calls; token usage is in the JSON record.

Baseline: 11 response lines; changed files `reports/background-work-decision.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 26.974 seconds and 3 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: the frame, rubric, and budget are on disk before the first dispatch; two blind first positions are saved raw with their lens and model; the disagreements are typed; the final report leads with the recommendation and lists any open decision with both positions.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-08-claude-claude-opus-5-5-activation-1/comparison.json](2026-11-08-claude-claude-opus-5-5-activation-1/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-08-claude-claude-opus-5-5-activation-1/treatment/trace.jsonl)
- [Standard error](2026-11-08-claude-claude-opus-5-5-activation-1/treatment/stderr.txt)
- [Observed response](2026-11-08-claude-claude-opus-5-5-activation-1/treatment/response.txt)
- [Input and discovery manifest](2026-11-08-claude-claude-opus-5-5-activation-1/treatment/manifest.json)
- Artifacts: `2026-11-08-claude-claude-opus-5-5-activation-1/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-08-claude-claude-opus-5-5-activation-1/baseline/trace.jsonl)
- [Standard error](2026-11-08-claude-claude-opus-5-5-activation-1/baseline/stderr.txt)
- [Observed response](2026-11-08-claude-claude-opus-5-5-activation-1/baseline/response.txt)
- [Input and discovery manifest](2026-11-08-claude-claude-opus-5-5-activation-1/baseline/manifest.json)
- Artifacts: `2026-11-08-claude-claude-opus-5-5-activation-1/baseline/artifacts/`.
