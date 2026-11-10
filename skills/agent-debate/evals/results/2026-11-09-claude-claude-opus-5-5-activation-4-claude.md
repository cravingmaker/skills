# agent-debate: claude activation-4

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-4` in `evals/examples.md`.
- **Skill revision.** Commit `752a1cc6661ad8489c757a4d9d75bcf93e7e5d89`, tree `504ed91c469373da735c254f2afcd410ccb110c1`, actual bytes SHA-256 `b7448e77616e01a522e0ca2c072213573edb15a8678be82120927241d50bcd81`; dirty: `False`.
- **Fixture.** `activation-4`, SHA-256 `a9edfb1236571057fb91a018ebdc148a80b4960907885147652a3416a47695c3`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [agent-debate.tar.gz](https://drive.google.com/file/d/1Xf5P0jLr6AK1vuNFvvM_mUP5QnYWrmy2/view), folder `2026-11-09-claude-claude-opus-5-5-activation-4-claude/` inside.

## Prompt

```text
/council
Use council for a read-only non-code design panel with these named providers.
Named providers: Claude and Codex. Review docs/design.md read-only. Preserve unavailable provider identities; no substitution, code writes, posting or model starts. Shared remaining allowance: 4 starts, 2 rounds, concurrency 2, reserve 1; no actual dispatch is available.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 8 | 0 |
| baseline | false | false | 2 | 0 |

Treatment: 28 response lines; changed files `.cache/npm/_logs/2026-11-09T03_49_56_053Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 52.669 seconds and 8 tool calls; token usage is in the JSON record.

Baseline: 11 response lines; changed files `.cache/npm/_logs/2026-11-09T03_50_59_676Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 31.51 seconds and 2 tool calls; token usage is in the JSON record.


Expected deliverable: See the Outcome criteria.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: `2026-11-09-claude-claude-opus-5-5-activation-4-claude/comparison.json` (local only, not committed).

## Treatment evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-activation-4-claude/treatment/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-activation-4-claude/treatment/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-activation-4-claude/treatment/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-activation-4-claude/treatment/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-4-claude/treatment/artifacts/`.

## Baseline evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-activation-4-claude/baseline/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-activation-4-claude/baseline/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-activation-4-claude/baseline/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-activation-4-claude/baseline/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-4-claude/baseline/artifacts/`.
