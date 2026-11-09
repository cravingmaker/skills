# decision-log: claude activation-1

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-1` in `evals/examples.md`.
- **Skill revision.** Commit `66f8700b5f86ced76eeb64d9f42201df5ea9f2be`, tree `b332b5643dfd29fa99b5434f6ab27ef8a2276d34`, actual bytes SHA-256 `cb7caf0d7a5d8dda319677291a3c809ddb078a0177f24b3b0fd51dbd322cf44e`; dirty: `False`.
- **Fixture.** `tests/eval-harness/fixtures/eval-worker/decisions`, SHA-256 `91c8ac2986214145f01e742d126fcdd8af36e6fc1d0344360dd3ab2dfa84107f`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `host default`; each arm has a new session and the same host settings.

## Prompt

```text
Keep a run record for these workers so another agent can resume after compaction.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 11 | 0 |
| baseline | false | false | 4 | 0 |

Treatment: 23 response lines; changed files `runs/migration-02/DECISIONS.md, runs/migration-02/LOG.md, runs/migration-02/PLAN.md, runs/migration-02/briefs/backend-status-v2.r1.md, runs/migration-02/briefs/frontend-status-v2.r1.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 96.188 seconds and 11 tool calls; token usage is in the JSON record.

Baseline: 18 response lines; changed files `RUN_RECORD.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 35.563 seconds and 4 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: durable current state, dispatch intents and receipts, raw reports, and decisions.

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
