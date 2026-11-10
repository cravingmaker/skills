# work-decomposition: claude near-miss-5

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `near-miss-5` in `evals/examples.md`.
- **Skill revision.** Commit `752a1cc6661ad8489c757a4d9d75bcf93e7e5d89`, tree `7a576f6c0cbf17fcc0a2a47e0dec8e13d2e36291`, actual bytes SHA-256 `a83da8598f67faed667175b6c6782ffa69bb79ece6034a6591a00d2b2a60caaf`; dirty: `False`.
- **Fixture.** `near-miss-5`, SHA-256 `4c7f4e00bc441adc626f7ff1cecd9a21aef5165b2ad6f4b1627bbdd4a0f20a8a`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [work-decomposition.tar.gz](https://drive.google.com/file/d/1Qgx8gOA_xs_qEmchFWh7wpjg1bDz1mv5/view), folder `2026-11-09-claude-claude-opus-5-5-near-miss-5-claude/` inside.

## Prompt

```text
Write an interface design

Task context supplied identically to both arms:
Design the export module interface using src/billing and docs/agents/domain.md. Design artifact only; no execution graph, delegation or product edits.
Retain generated artifacts and probe state inside this fixture's scratch/ directory; use scratch/tmp/ for temporary architecture reports. No real apps, credentials, schedules, commits, remote writes or additional model starts.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | false | false | 11 | 0 |
| baseline | false | false | 11 | 0 |

Treatment: 28 response lines; changed files `.cache/npm/_logs/2026-11-09T03_45_33_184Z-debug-0.log, scratch/billing-export-design.md, scratch/billing_export_sketch.py, scratch/tmp/phase-a-grounding.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 152.691 seconds and 11 tool calls; token usage is in the JSON record.

Baseline: 34 response lines; changed files `scratch/billing-export-design/interface_sketch.py, scratch/billing-export-design/rationale.md, scratch/tmp/grounding.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 190.712 seconds and 11 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: the `architect` skill; no imported execution graph is needed.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: `2026-11-09-claude-claude-opus-5-5-near-miss-5-claude/comparison.json` (local only, not committed).

## Treatment evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-near-miss-5-claude/treatment/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-near-miss-5-claude/treatment/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-near-miss-5-claude/treatment/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-near-miss-5-claude/treatment/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-near-miss-5-claude/treatment/artifacts/`.

## Baseline evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-near-miss-5-claude/baseline/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-near-miss-5-claude/baseline/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-near-miss-5-claude/baseline/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-near-miss-5-claude/baseline/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-near-miss-5-claude/baseline/artifacts/`.
