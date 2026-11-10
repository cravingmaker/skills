# agent-debate: claude activation-3

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-3` in `evals/examples.md`.
- **Skill revision.** Commit `822565a127508fe88dd0909a7d9587a81d304c3e`, tree `73581430e45e6adc9ef1ef27002f70e579f035be`, actual bytes SHA-256 `b343cc78ffc1b7978fe8677ecd0b38102321d4c28dedfe1fed8aa762b679d86a`; dirty: `False`.
- **Fixture.** `tests/eval-harness/fixtures/eval-worker/debate-limit`, SHA-256 `f4878fd5572328c345754456fc665fdfc68351934b94db27afb406bae3cb5efc`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `host default`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [agent-debate.tar.gz](https://drive.google.com/file/d/1Xf5P0jLr6AK1vuNFvvM_mUP5QnYWrmy2/view), folder `2026-11-08-claude-claude-opus-5-5-activation-3-lean-2-debate-limit/` inside.

## Prompt

```text
Keep reviewing the draft with the evaluator until you both fully agree.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | false | 2 | 0 |
| baseline | false | false | 2 | 0 |

Treatment: 11 response lines; changed files `none`; removed files `none`; validation command present: `requires review`. Workflow cost: 19.57 seconds and 2 tool calls; token usage is in the JSON record.

Baseline: 11 response lines; changed files `none`; removed files `none`; validation command present: `requires review`. Workflow cost: 16.036 seconds and 2 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: the per-finding round limit still applies; a finding open after 3 rounds without new evidence goes to the user as a decision with both positions, and the report does not call it agreement.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: `2026-11-08-claude-claude-opus-5-5-activation-3-lean-2-debate-limit/comparison.json` (local only, not committed).

## Treatment evidence

- Raw JSON trace: `2026-11-08-claude-claude-opus-5-5-activation-3-lean-2-debate-limit/treatment/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-08-claude-claude-opus-5-5-activation-3-lean-2-debate-limit/treatment/stderr.txt` (local only, not committed)
- Observed response: `2026-11-08-claude-claude-opus-5-5-activation-3-lean-2-debate-limit/treatment/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-08-claude-claude-opus-5-5-activation-3-lean-2-debate-limit/treatment/manifest.json` (local only, not committed)
- Artifacts: `2026-11-08-claude-claude-opus-5-5-activation-3-lean-2-debate-limit/treatment/artifacts/`.

## Baseline evidence

- Raw JSON trace: `2026-11-08-claude-claude-opus-5-5-activation-3-lean-2-debate-limit/baseline/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-08-claude-claude-opus-5-5-activation-3-lean-2-debate-limit/baseline/stderr.txt` (local only, not committed)
- Observed response: `2026-11-08-claude-claude-opus-5-5-activation-3-lean-2-debate-limit/baseline/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-08-claude-claude-opus-5-5-activation-3-lean-2-debate-limit/baseline/manifest.json` (local only, not committed)
- Artifacts: `2026-11-08-claude-claude-opus-5-5-activation-3-lean-2-debate-limit/baseline/artifacts/`.
