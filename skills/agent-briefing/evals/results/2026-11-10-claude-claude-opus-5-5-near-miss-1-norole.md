# agent-briefing: claude near-miss-1

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `near-miss-1` in `evals/examples.md`.
- **Skill revision.** Commit `775737f530620cee9710c42e6dc69e960f58b101`, tree `3e0d6a7738acf8639c1a6d1530b1959fc7f5caa8`, actual bytes SHA-256 `35437fe4341d683272d54f40fe6efca32586e8fcb59b35fa46d57c5dcc0615b7`; dirty: `False`.
- **Fixture.** `tests/eval-harness/fixtures/eval-worker/routine`, SHA-256 `235b5423636a31cbd44df8be888962f13d2fd93b86385308c67b908430e4e52d`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [agent-briefing.tar.gz](https://drive.google.com/file/d/1FqpvKO1UwLeqNh4Svp5DeVQe_VEueOLL/view), folder `2026-11-10-claude-claude-opus-5-5-near-miss-1-norole/` inside.

## Prompt

```text
Write a creative brief for a summer ad campaign.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | false | false | 2 | 0 |
| baseline | false | false | 2 | 0 |

Treatment: 74 response lines; changed files `none`; removed files `none`; validation command present: `requires review`. Workflow cost: 30.631 seconds and 2 tool calls; token usage is in the JSON record.

Baseline: 74 response lines; changed files `none`; removed files `none`; validation command present: `requires review`. Workflow cost: 29.206 seconds and 2 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: marketing work without an agent dispatch contract.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: `2026-11-10-claude-claude-opus-5-5-near-miss-1-norole/comparison.json` (local only, not committed).

## Treatment evidence

- Raw JSON trace: `2026-11-10-claude-claude-opus-5-5-near-miss-1-norole/treatment/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-10-claude-claude-opus-5-5-near-miss-1-norole/treatment/stderr.txt` (local only, not committed)
- Observed response: `2026-11-10-claude-claude-opus-5-5-near-miss-1-norole/treatment/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-10-claude-claude-opus-5-5-near-miss-1-norole/treatment/manifest.json` (local only, not committed)
- Artifacts: `2026-11-10-claude-claude-opus-5-5-near-miss-1-norole/treatment/artifacts/`.

## Baseline evidence

- Raw JSON trace: `2026-11-10-claude-claude-opus-5-5-near-miss-1-norole/baseline/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-10-claude-claude-opus-5-5-near-miss-1-norole/baseline/stderr.txt` (local only, not committed)
- Observed response: `2026-11-10-claude-claude-opus-5-5-near-miss-1-norole/baseline/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-10-claude-claude-opus-5-5-near-miss-1-norole/baseline/manifest.json` (local only, not committed)
- Artifacts: `2026-11-10-claude-claude-opus-5-5-near-miss-1-norole/baseline/artifacts/`.
