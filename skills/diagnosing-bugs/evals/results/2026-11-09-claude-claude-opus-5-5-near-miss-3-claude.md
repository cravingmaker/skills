# diagnosing-bugs: claude near-miss-3

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `near-miss-3` in `evals/examples.md`.
- **Skill revision.** Commit `f5a0c4f4a80ea04590d4330e952921e81ac97bdd`, tree `31d3414b1f15fe96c732cdc57d20dea93934de11`, actual bytes SHA-256 `b4acc5f6036f5cf30f051f33e21420535b1fe5e3f0a7e0c297c518257c37eaa9`; dirty: `False`.
- **Fixture.** `near-miss-3`, SHA-256 `242ffc89e533d1c4a97906db71458752022f1a821ac534dfaf76ed418aac03f8`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
Add a retry to this HTTP call.

Task context supplied identically to both arms:
Add at most one retry on transient ConnectionError in src/http.py; preserve other exceptions and return values.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | false | false | 6 | 0 |
| baseline | false | false | 6 | 0 |

Treatment: 19 response lines; changed files `.cache/npm/_logs/2026-11-09T05_41_16_637Z-debug-0.log, src/__pycache__/http.cpython-315.pyc, src/http.py`; removed files `none`; validation command present: `requires review`. Workflow cost: 36.468 seconds and 6 tool calls; token usage is in the JSON record.

Baseline: 17 response lines; changed files `.cache/npm/_logs/2026-11-09T05_42_35_675Z-debug-0.log, src/__pycache__/http.cpython-315.pyc, src/http.py`; removed files `none`; validation command present: `requires review`. Workflow cost: 36.23 seconds and 6 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: ordinary implementation, no diagnosis loop.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/baseline/artifacts/`.
