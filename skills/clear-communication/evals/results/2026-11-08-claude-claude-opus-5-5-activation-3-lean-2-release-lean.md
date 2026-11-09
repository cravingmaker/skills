# clear-communication: claude activation-3

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-3` in `evals/examples.md`.
- **Skill revision.** Commit `6b67b4d0f4517a0cadceef35943bcc24ed40e978`, tree `2d0f93482c7dce02dcb38b9e8695c9925ae5a12a`, actual bytes SHA-256 `73c620f3304358409a4cce2b107386c30c26249f74912d1cbf8a50b1f724040a`; dirty: `False`.
- **Fixture.** `tests/eval-harness/fixtures/eval-worker/release-lean`, SHA-256 `d1ecca3aa1e48b5d563da74ae2579b7d27f3395143457d1686b0cf76223da205`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `host default`; each arm has a new session and the same host settings.

## Prompt

```text
Set up the release pipeline for this repo.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | false | 2 | 0 |
| baseline | false | false | 6 | 0 |

Treatment: 12 response lines; changed files `none`; removed files `none`; validation command present: `requires review`. Workflow cost: 20.201 seconds and 2 tool calls; token usage is in the JSON record.

Baseline: 15 response lines; changed files `.github/workflows/release.yml`; removed files `none`; validation command present: `requires review`. Workflow cost: 43.144 seconds and 6 tool calls; token usage is in the JSON record.


Expected deliverable: (The repo has two package managers' lockfiles and no CI.) Expect: one numbered message with the consequential questions answerable now, each with a recommended answer, and no questions about details the files already answer.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-08-claude-claude-opus-5-5-activation-3-lean-2-release-lean/comparison.json](2026-11-08-claude-claude-opus-5-5-activation-3-lean-2-release-lean/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-08-claude-claude-opus-5-5-activation-3-lean-2-release-lean/treatment/trace.jsonl)
- [Standard error](2026-11-08-claude-claude-opus-5-5-activation-3-lean-2-release-lean/treatment/stderr.txt)
- [Observed response](2026-11-08-claude-claude-opus-5-5-activation-3-lean-2-release-lean/treatment/response.txt)
- [Input and discovery manifest](2026-11-08-claude-claude-opus-5-5-activation-3-lean-2-release-lean/treatment/manifest.json)
- Artifacts: `2026-11-08-claude-claude-opus-5-5-activation-3-lean-2-release-lean/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-08-claude-claude-opus-5-5-activation-3-lean-2-release-lean/baseline/trace.jsonl)
- [Standard error](2026-11-08-claude-claude-opus-5-5-activation-3-lean-2-release-lean/baseline/stderr.txt)
- [Observed response](2026-11-08-claude-claude-opus-5-5-activation-3-lean-2-release-lean/baseline/response.txt)
- [Input and discovery manifest](2026-11-08-claude-claude-opus-5-5-activation-3-lean-2-release-lean/baseline/manifest.json)
- Artifacts: `2026-11-08-claude-claude-opus-5-5-activation-3-lean-2-release-lean/baseline/artifacts/`.
