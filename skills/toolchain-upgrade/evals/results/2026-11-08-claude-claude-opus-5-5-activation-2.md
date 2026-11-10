# toolchain-upgrade: claude activation-2

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-2` in `evals/examples.md`.
- **Skill revision.** Commit `c73a5e7b759da865d5ec5deb0760ee5c8451a3aa`, tree `9328c08d911120227d69f8fc36f954d248eb892b`, actual bytes SHA-256 `d20f49fc928b7bc56ebedb49aa7bcc18f54b9a6553be4e1a4accc442189953cd`; dirty: `False`.
- **Fixture.** `tests/eval-harness/fixtures/eval-worker/toolchain`, SHA-256 `bf918837cbbdbb88aff38d49033715aa2b1d5e2dba812e8d4183834783becc1f`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `host default`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [toolchain-upgrade.tar.gz](https://drive.google.com/file/d/1RqNachapqDeVSXaobA4Qxh4x_vRvaJYF/view), folder `2026-11-08-claude-claude-opus-5-5-activation-2/` inside.

## Prompt

```text
Dependabot opened a PR updating typescript-eslint. Is it safe to merge?
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 8 | 0 |
| baseline | false | false | 4 | 0 |

Treatment: 22 response lines; changed files `eslint-policy.json, package-lock.json, package.json`; removed files `none`; validation command present: `requires review`. Workflow cost: 46.171 seconds and 8 tool calls; token usage is in the JSON record.

Baseline: 23 response lines; changed files `none`; removed files `none`; validation command present: `requires review`. Workflow cost: 42.137 seconds and 4 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: release notes read for every skipped version, effective-config differences listed with decisions, and the full checks run.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: `2026-11-08-claude-claude-opus-5-5-activation-2/comparison.json` (local only, not committed).

## Treatment evidence

- Raw JSON trace: `2026-11-08-claude-claude-opus-5-5-activation-2/treatment/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-08-claude-claude-opus-5-5-activation-2/treatment/stderr.txt` (local only, not committed)
- Observed response: `2026-11-08-claude-claude-opus-5-5-activation-2/treatment/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-08-claude-claude-opus-5-5-activation-2/treatment/manifest.json` (local only, not committed)
- Artifacts: `2026-11-08-claude-claude-opus-5-5-activation-2/treatment/artifacts/`.

## Baseline evidence

- Raw JSON trace: `2026-11-08-claude-claude-opus-5-5-activation-2/baseline/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-08-claude-claude-opus-5-5-activation-2/baseline/stderr.txt` (local only, not committed)
- Observed response: `2026-11-08-claude-claude-opus-5-5-activation-2/baseline/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-08-claude-claude-opus-5-5-activation-2/baseline/manifest.json` (local only, not committed)
- Artifacts: `2026-11-08-claude-claude-opus-5-5-activation-2/baseline/artifacts/`.
