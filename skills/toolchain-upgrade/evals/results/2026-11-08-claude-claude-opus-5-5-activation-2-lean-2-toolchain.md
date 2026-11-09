# toolchain-upgrade: claude activation-2

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-2` in `evals/examples.md`.
- **Skill revision.** Commit `6b67b4d0f4517a0cadceef35943bcc24ed40e978`, tree `508f41334902b4a89adfc150ab840f2620f74542`, actual bytes SHA-256 `f0ab047d02b4d4652427fca6947c5b18c6ad4da35c5ca3842c014571c4182608`; dirty: `False`.
- **Fixture.** `tests/eval-harness/fixtures/eval-worker/toolchain`, SHA-256 `bf918837cbbdbb88aff38d49033715aa2b1d5e2dba812e8d4183834783becc1f`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `host default`; each arm has a new session and the same host settings.

## Prompt

```text
Dependabot opened a PR updating typescript-eslint. Is it safe to merge?
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 7 | 0 |
| baseline | false | false | 4 | 0 |

Treatment: 47 response lines; changed files `none`; removed files `none`; validation command present: `requires review`. Workflow cost: 51.094 seconds and 7 tool calls; token usage is in the JSON record.

Baseline: 20 response lines; changed files `none`; removed files `none`; validation command present: `requires review`. Workflow cost: 36.187 seconds and 4 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: release notes read for every skipped version, effective-config differences listed with decisions, and the full checks run.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-08-claude-claude-opus-5-5-activation-2-lean-2-toolchain/comparison.json](2026-11-08-claude-claude-opus-5-5-activation-2-lean-2-toolchain/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-08-claude-claude-opus-5-5-activation-2-lean-2-toolchain/treatment/trace.jsonl)
- [Standard error](2026-11-08-claude-claude-opus-5-5-activation-2-lean-2-toolchain/treatment/stderr.txt)
- [Observed response](2026-11-08-claude-claude-opus-5-5-activation-2-lean-2-toolchain/treatment/response.txt)
- [Input and discovery manifest](2026-11-08-claude-claude-opus-5-5-activation-2-lean-2-toolchain/treatment/manifest.json)
- Artifacts: `2026-11-08-claude-claude-opus-5-5-activation-2-lean-2-toolchain/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-08-claude-claude-opus-5-5-activation-2-lean-2-toolchain/baseline/trace.jsonl)
- [Standard error](2026-11-08-claude-claude-opus-5-5-activation-2-lean-2-toolchain/baseline/stderr.txt)
- [Observed response](2026-11-08-claude-claude-opus-5-5-activation-2-lean-2-toolchain/baseline/response.txt)
- [Input and discovery manifest](2026-11-08-claude-claude-opus-5-5-activation-2-lean-2-toolchain/baseline/manifest.json)
- Artifacts: `2026-11-08-claude-claude-opus-5-5-activation-2-lean-2-toolchain/baseline/artifacts/`.
