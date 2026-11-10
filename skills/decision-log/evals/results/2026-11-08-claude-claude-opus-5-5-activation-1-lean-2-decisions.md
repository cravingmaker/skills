# decision-log: claude activation-1

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-1` in `evals/examples.md`.
- **Skill revision.** Commit `822565a127508fe88dd0909a7d9587a81d304c3e`, tree `918715dae61a8c22d41bc156c7d3dfe99e150ce7`, actual bytes SHA-256 `1c05a26f828df26fdc26863e7a281b79d5d90686547bd58c7eb881e9d4ff8e74`; dirty: `False`.
- **Fixture.** `tests/eval-harness/fixtures/eval-worker/decisions`, SHA-256 `91c8ac2986214145f01e742d126fcdd8af36e6fc1d0344360dd3ab2dfa84107f`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `host default`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [decision-log.tar.gz](https://drive.google.com/file/d/1XpcYF1WafS-kn5wDnPV6p2X-LUswiXMt/view), folder `2026-11-08-claude-claude-opus-5-5-activation-1-lean-2-decisions/` inside.

## Prompt

```text
Keep a run record for these workers so another agent can resume after compaction.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 16 | 0 |
| baseline | false | false | 4 | 0 |

Treatment: 23 response lines; changed files `runs/migration-02/DECISIONS.md, runs/migration-02/LOG.md, runs/migration-02/PLAN.md, runs/migration-02/briefs/backend-r1.md, runs/migration-02/briefs/frontend-r1.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 117.789 seconds and 16 tool calls; token usage is in the JSON record.

Baseline: 12 response lines; changed files `none`; removed files `none`; validation command present: `requires review`. Workflow cost: 22.268 seconds and 4 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: durable current state, dispatch intents and receipts, raw reports, and decisions.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: `2026-11-08-claude-claude-opus-5-5-activation-1-lean-2-decisions/comparison.json` (local only, not committed).

## Treatment evidence

- Raw JSON trace: `2026-11-08-claude-claude-opus-5-5-activation-1-lean-2-decisions/treatment/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-08-claude-claude-opus-5-5-activation-1-lean-2-decisions/treatment/stderr.txt` (local only, not committed)
- Observed response: `2026-11-08-claude-claude-opus-5-5-activation-1-lean-2-decisions/treatment/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-08-claude-claude-opus-5-5-activation-1-lean-2-decisions/treatment/manifest.json` (local only, not committed)
- Artifacts: `2026-11-08-claude-claude-opus-5-5-activation-1-lean-2-decisions/treatment/artifacts/`.

## Baseline evidence

- Raw JSON trace: `2026-11-08-claude-claude-opus-5-5-activation-1-lean-2-decisions/baseline/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-08-claude-claude-opus-5-5-activation-1-lean-2-decisions/baseline/stderr.txt` (local only, not committed)
- Observed response: `2026-11-08-claude-claude-opus-5-5-activation-1-lean-2-decisions/baseline/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-08-claude-claude-opus-5-5-activation-1-lean-2-decisions/baseline/manifest.json` (local only, not committed)
- Artifacts: `2026-11-08-claude-claude-opus-5-5-activation-1-lean-2-decisions/baseline/artifacts/`.
