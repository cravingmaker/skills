# writing-for-agents: claude near-miss-2

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `near-miss-2` in `evals/examples.md`.
- **Skill revision.** Commit `c45c0856a116f3de30386d810d872f4a6f83fa20`, tree `7584664f87a6d8d82f666564da8046665afc8bc5`, actual bytes SHA-256 `f8a3df3e85fd55c448f5737d27854c81c0368e891947c4eddaaf6ba686788663`; dirty: `False`.
- **Fixture.** `tests/eval-harness/fixtures/package`, SHA-256 `3fc75a91e565dd737362d2462d654f8fb022854ba2b9e866b545eaf7d94533a5`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [writing-for-agents.tar.gz](https://drive.google.com/file/d/1ots6priUT1iEgcma-1YX_7gNugcffhf4/view), folder `2026-11-10-claude-claude-opus-5-5-near-miss-2-norole/` inside.

## Prompt

```text
Install the existing skill without changing its instructions.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | false | false | 3 | 0 |
| baseline | false | false | 5 | 0 |

Treatment: 10 response lines; changed files `none`; removed files `none`; validation command present: `requires review`. Workflow cost: 23.157 seconds and 3 tool calls; token usage is in the JSON record.

Baseline: 10 response lines; changed files `none`; removed files `none`; validation command present: `requires review`. Workflow cost: 31.289 seconds and 5 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: installation follows the selected installer, without rewriting guidance or running a model campaign.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: `2026-11-10-claude-claude-opus-5-5-near-miss-2-norole/comparison.json` (local only, not committed).

## Treatment evidence

- Raw JSON trace: `2026-11-10-claude-claude-opus-5-5-near-miss-2-norole/treatment/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-10-claude-claude-opus-5-5-near-miss-2-norole/treatment/stderr.txt` (local only, not committed)
- Observed response: `2026-11-10-claude-claude-opus-5-5-near-miss-2-norole/treatment/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-10-claude-claude-opus-5-5-near-miss-2-norole/treatment/manifest.json` (local only, not committed)
- Artifacts: `2026-11-10-claude-claude-opus-5-5-near-miss-2-norole/treatment/artifacts/`.

## Baseline evidence

- Raw JSON trace: `2026-11-10-claude-claude-opus-5-5-near-miss-2-norole/baseline/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-10-claude-claude-opus-5-5-near-miss-2-norole/baseline/stderr.txt` (local only, not committed)
- Observed response: `2026-11-10-claude-claude-opus-5-5-near-miss-2-norole/baseline/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-10-claude-claude-opus-5-5-near-miss-2-norole/baseline/manifest.json` (local only, not committed)
- Artifacts: `2026-11-10-claude-claude-opus-5-5-near-miss-2-norole/baseline/artifacts/`.
