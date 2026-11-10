# diagnosing-bugs: claude activation-1

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-1` in `evals/examples.md`.
- **Skill revision.** Commit `f5a0c4f4a80ea04590d4330e952921e81ac97bdd`, tree `31d3414b1f15fe96c732cdc57d20dea93934de11`, actual bytes SHA-256 `b4acc5f6036f5cf30f051f33e21420535b1fe5e3f0a7e0c297c518257c37eaa9`; dirty: `False`.
- **Fixture.** `activation-1`, SHA-256 `88b4855474b282a065efd3be97bcfbc21175cfa96b67e5a01092b9f375ca5d16`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [diagnosing-bugs.tar.gz](https://drive.google.com/file/d/1C4bvkWTEtrkTNts4sBndeX3GgdBNff9d/view), folder `2026-11-09-claude-claude-opus-5-5-activation-1-claude/` inside.

## Prompt

```text
Debug this: the export button throws 'undefined is not a function' in production.

Task context supplied identically to both arms:
User symptom is a production browser click. Local capture ui/export.mjs and executable code-path replay `node ui/repro.mjs` are available; no actual browser is installed. Restore supported click behavior to return an exported result. Label replay versus real-UI proof precisely.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 12 | 0 |
| baseline | false | false | 6 | 0 |

Treatment: 23 response lines; changed files `.cache/npm/_logs/2026-11-09T05_36_56_624Z-debug-0.log, ui/export.mjs, ui/export.test.mjs`; removed files `none`; validation command present: `requires review`. Workflow cost: 78.012 seconds and 12 tool calls; token usage is in the JSON record.

Baseline: 24 response lines; changed files `.cache/npm/_logs/2026-11-09T05_39_50_682Z-debug-0.log, ui/export.mjs`; removed files `none`; validation command present: `requires review`. Workflow cost: 60.892 seconds and 6 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: builds a red-capable loop on the reported surface before theorizing, minimises, ranks 3–5 falsifiable hypotheses, and fixes a proven cause with a regression test at a correct seam.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: `2026-11-09-claude-claude-opus-5-5-activation-1-claude/comparison.json` (local only, not committed).

## Treatment evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-activation-1-claude/treatment/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-activation-1-claude/treatment/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-activation-1-claude/treatment/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-activation-1-claude/treatment/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-1-claude/treatment/artifacts/`.

## Baseline evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-activation-1-claude/baseline/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-activation-1-claude/baseline/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-activation-1-claude/baseline/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-activation-1-claude/baseline/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-1-claude/baseline/artifacts/`.
