# ketchup: claude outcome-1

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `outcome-1` in `evals/examples.md`.
- **Skill revision.** Commit `d78b9956da6f04ed515a45ace4278fed10425be6`, tree `3857041fad3d36252578c8c68143a95a2f550159`, actual bytes SHA-256 `8add78dd29059f38b0a06b88d3444b640b0080dcb7eba3aad9e9b87990969bb3`; dirty: `False`.
- **Fixture.** `outcome-1`, SHA-256 `a625a622902cb86ab3be504e3668438879ca8dba311c8fd218b1466f82b8cd2c`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
/ketchup Since my last human prompt, a notification and worker report arrived; an older access choice remains unresolved.

Supplied task context:
Use only history/current-chat.jsonl, history/index.json and docs/choices.json for this fixture; today is 2026-11-09 Asia/Jakarta. Status inspection is read-only; no CI rerun, watcher, push, merge or new helper.

Disposable local fixture only. README.md documents python3 tools/forge.py and local bare origin. No real GitHub, accounts, credentials, external network or extra model sessions may be used; scope comes only from this request.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | n/a | true | 2 | 0 |
| baseline | n/a | false | 1 | 0 |

Treatment: 58 response lines; changed files `.cache/npm/_logs/2026-11-09T05_06_25_848Z-debug-0.log, .fixture/events.jsonl`; removed files `none`; validation command present: `requires review`. Workflow cost: 29.072 seconds and 2 tool calls; token usage is in the JSON record.

Baseline: 30 response lines; changed files `.cache/npm/_logs/2026-11-09T05_08_55_459Z-debug-0.log, .fixture/events.jsonl`; removed files `none`; validation command present: `requires review`. Workflow cost: 18.267 seconds and 1 tool calls; token usage is in the JSON record.


Expected deliverable: "Since my last human prompt, a notification and worker report arrived; an older access choice remains unresolved." Expect: notifications do not reset the window, live work is checked, and the older user choice remains included.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-outcome-1-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-outcome-1-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-1-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-1-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-1-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-1-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-1-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-1-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-1-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-1-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-1-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-1-claude/baseline/artifacts/`.

Activation is not graded for Outcome examples; review the stated behavioral criterion.

## Outcome review

Value: **matched**. Baseline criterion: partial; treatment criterion: partial.

Both anchor at the last human message, keep later notification/worker report inside the window, reject stale-head shipped claims and preserve the older12 retention choices (1/2 share a decision). Live forge/check inspection is outside the explicit three-file input scope and stays unrun. The named access choice is absent; both report that gap rather than invent one. Lack of a receipt does not itself prove tests never ran.
