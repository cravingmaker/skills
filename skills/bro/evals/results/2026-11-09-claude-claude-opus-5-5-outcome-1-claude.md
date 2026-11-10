# bro: claude outcome-1

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `outcome-1` in `evals/examples.md`.
- **Skill revision.** Commit `312b66d24aa771fa04dec33b4b1a076d2a686079`, tree `20aa7feebf75db7c9ad6765c371f6cb456f1fc87`, actual bytes SHA-256 `b88e494bfaa31f0babf7014a866715fac33e9d9ac5ed83ad1e569027df4bc663`; dirty: `False`.
- **Fixture.** `outcome-1`, SHA-256 `b4a7e81156efb335f6897c42d7a367286264a2b79d5904b1c7f467d2a09b64a8`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [bro.tar.gz](https://drive.google.com/file/d/1C3LuMQDCXBnZnI7Hxe2hM_ar7Amiadb-/view), folder `2026-11-09-claude-claude-opus-5-5-outcome-1-claude/` inside.

## Prompt

```text
/bro Bro, explain your draft PR body more plainly.

Supplied task context:
Previous assistant answer, supplied as context: Draft PR body: rename parseOrderInput to parseOrderPayload. Two unit tests passed; UI and CI were not run. This is a local draft; no filing, push, watch or merge is authorized.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | n/a | true | 1 | 0 |
| baseline | n/a | false | 0 | 0 |

Treatment: 6 response lines; changed files `.cache/npm/_logs/2026-11-09T05_04_34_416Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 8.631 seconds and 1 tool calls; token usage is in the JSON record.

Baseline: 9 response lines; changed files `.cache/npm/_logs/2026-11-09T05_05_19_584Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 6.188 seconds and 0 tool calls; token usage is in the JSON record.


Expected deliverable: "Bro, explain your draft PR body more plainly." Check: the parent repairs the last draft without filing, pushing, watching, or merging.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: `2026-11-09-claude-claude-opus-5-5-outcome-1-claude/comparison.json` (local only, not committed).

## Treatment evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-outcome-1-claude/treatment/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-outcome-1-claude/treatment/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-outcome-1-claude/treatment/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-outcome-1-claude/treatment/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-1-claude/treatment/artifacts/`.

## Baseline evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-outcome-1-claude/baseline/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-outcome-1-claude/baseline/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-outcome-1-claude/baseline/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-outcome-1-claude/baseline/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-1-claude/baseline/artifacts/`.

Activation is not graded for Outcome examples; review the stated behavioral criterion.

## Outcome review

Value: **matched**. Baseline criterion: yes; treatment criterion: yes.

Both restate the draft rename and exact two-unit-test/UI/CI limits, with no filing, push, watch or merge.
