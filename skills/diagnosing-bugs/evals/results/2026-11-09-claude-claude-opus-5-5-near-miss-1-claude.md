# diagnosing-bugs: claude near-miss-1

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `near-miss-1` in `evals/examples.md`.
- **Skill revision.** Commit `f5a0c4f4a80ea04590d4330e952921e81ac97bdd`, tree `31d3414b1f15fe96c732cdc57d20dea93934de11`, actual bytes SHA-256 `b4acc5f6036f5cf30f051f33e21420535b1fe5e3f0a7e0c297c518257c37eaa9`; dirty: `False`.
- **Fixture.** `near-miss-1`, SHA-256 `f21729ae0f25e3bcc0563bc753d1a87ca1429b907e2fab3eab5bb906b5bc5c1f`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
Use the installed debug command explicitly.

Task context supplied identically to both arms:
The selected host debug command is not exposed by this Codex evaluation; do not substitute another entry.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | false | false | 0 | 0 |
| baseline | false | false | 2 | 0 |

Treatment: 6 response lines; changed files `.cache/npm/_logs/2026-11-09T05_40_30_785Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 10.08 seconds and 0 tool calls; token usage is in the JSON record.

Baseline: 7 response lines; changed files `.cache/npm/_logs/2026-11-09T05_41_52_586Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 20.549 seconds and 2 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: the selected host command keeps its route; diagnosing-bugs is not substituted.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-near-miss-1-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-near-miss-1-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-near-miss-1-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-near-miss-1-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-near-miss-1-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-near-miss-1-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-near-miss-1-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-near-miss-1-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-near-miss-1-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-near-miss-1-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-near-miss-1-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-near-miss-1-claude/baseline/artifacts/`.
