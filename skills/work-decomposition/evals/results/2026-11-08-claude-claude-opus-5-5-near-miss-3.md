# work-decomposition: claude near-miss-3

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `near-miss-3` in `evals/examples.md`.
- **Skill revision.** Commit `66f8700b5f86ced76eeb64d9f42201df5ea9f2be`, tree `6002c3edb4a8cbb3dd935a915d342c9f929e7d2d`, actual bytes SHA-256 `1a9113a9514d820a377848388890239c098fa6eb3f0fe74714707faeb30f46ee`; dirty: `False`.
- **Fixture.** `tests/eval-harness/fixtures/eval-worker/leaf`, SHA-256 `f57e16de44b11351b9bc8d81629cd36caec7f6c50542ada61757f015582a23e2`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `host default`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [work-decomposition.tar.gz](https://drive.google.com/file/d/1Qgx8gOA_xs_qEmchFWh7wpjg1bDz1mv5/view), folder `2026-11-08-claude-claude-opus-5-5-near-miss-3/` inside.

## Prompt

```text
You are the assigned writer; edit only this skill and do not delegate.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | false | false | 5 | 0 |
| baseline | false | false | 5 | 0 |

Treatment: 3 response lines; changed files `skills/example/SKILL.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 16.901 seconds and 5 tool calls; token usage is in the JSON record.

Baseline: 3 response lines; changed files `skills/example/SKILL.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 18.48 seconds and 5 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: the bounded leaf assignment.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: `2026-11-08-claude-claude-opus-5-5-near-miss-3/comparison.json` (local only, not committed).

## Treatment evidence

- Raw JSON trace: `2026-11-08-claude-claude-opus-5-5-near-miss-3/treatment/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-08-claude-claude-opus-5-5-near-miss-3/treatment/stderr.txt` (local only, not committed)
- Observed response: `2026-11-08-claude-claude-opus-5-5-near-miss-3/treatment/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-08-claude-claude-opus-5-5-near-miss-3/treatment/manifest.json` (local only, not committed)
- Artifacts: `2026-11-08-claude-claude-opus-5-5-near-miss-3/treatment/artifacts/`.

## Baseline evidence

- Raw JSON trace: `2026-11-08-claude-claude-opus-5-5-near-miss-3/baseline/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-08-claude-claude-opus-5-5-near-miss-3/baseline/stderr.txt` (local only, not committed)
- Observed response: `2026-11-08-claude-claude-opus-5-5-near-miss-3/baseline/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-08-claude-claude-opus-5-5-near-miss-3/baseline/manifest.json` (local only, not committed)
- Artifacts: `2026-11-08-claude-claude-opus-5-5-near-miss-3/baseline/artifacts/`.
