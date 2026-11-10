# codebase-design: claude activation-2

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-2` in `evals/examples.md`.
- **Skill revision.** Commit `2af114bf591b88e3fff6824448269b968f967e90`, tree `fbc68f88beedf9d820f618a5dceaafbfdd77e7ba`, actual bytes SHA-256 `d92c64434efdbd144192639981dbd6ca4d020d456158e3b6eb82fbcfd89c45d0`; dirty: `False`.
- **Fixture.** `activation-2`, SHA-256 `4c7f4e00bc441adc626f7ff1cecd9a21aef5165b2ad6f4b1627bbdd4a0f20a8a`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [codebase-design.tar.gz](https://drive.google.com/file/d/1FpJWezKXahMeFelJCxQEz4k6C-_PPTFl/view), folder `2026-11-10-claude-claude-opus-5-5-activation-2-norole/` inside.

## Prompt

```text
Where should the seam go so we can test the pricing logic without the payment gateway?
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 5 | 0 |
| baseline | false | false | 4 | 0 |

Treatment: 27 response lines; changed files `none`; removed files `none`; validation command present: `requires review`. Workflow cost: 38.741 seconds and 5 tool calls; token usage is in the JSON record.

Baseline: 23 response lines; changed files `none`; removed files `none`; validation command present: `requires review`. Workflow cost: 31.021 seconds and 4 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: classifies the dependency (true external), proposes an injected port with production and test adapters, and tests through the module's interface.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: `2026-11-10-claude-claude-opus-5-5-activation-2-norole/comparison.json` (local only, not committed).

## Treatment evidence

- Raw JSON trace: `2026-11-10-claude-claude-opus-5-5-activation-2-norole/treatment/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-10-claude-claude-opus-5-5-activation-2-norole/treatment/stderr.txt` (local only, not committed)
- Observed response: `2026-11-10-claude-claude-opus-5-5-activation-2-norole/treatment/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-10-claude-claude-opus-5-5-activation-2-norole/treatment/manifest.json` (local only, not committed)
- Artifacts: `2026-11-10-claude-claude-opus-5-5-activation-2-norole/treatment/artifacts/`.

## Baseline evidence

- Raw JSON trace: `2026-11-10-claude-claude-opus-5-5-activation-2-norole/baseline/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-10-claude-claude-opus-5-5-activation-2-norole/baseline/stderr.txt` (local only, not committed)
- Observed response: `2026-11-10-claude-claude-opus-5-5-activation-2-norole/baseline/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-10-claude-claude-opus-5-5-activation-2-norole/baseline/manifest.json` (local only, not committed)
- Artifacts: `2026-11-10-claude-claude-opus-5-5-activation-2-norole/baseline/artifacts/`.
