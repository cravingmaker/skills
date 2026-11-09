# ketchup: claude outcome-6

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `outcome-6` in `evals/examples.md`.
- **Skill revision.** Commit `d78b9956da6f04ed515a45ace4278fed10425be6`, tree `3857041fad3d36252578c8c68143a95a2f550159`, actual bytes SHA-256 `8add78dd29059f38b0a06b88d3444b640b0080dcb7eba3aad9e9b87990969bb3`; dirty: `False`.
- **Fixture.** `outcome-6`, SHA-256 `a625a622902cb86ab3be504e3668438879ca8dba311c8fd218b1466f82b8cd2c`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
/ketchup A wider-window commit was later reverted and another change remains uncommitted.

Supplied task context:
Use only history/current-chat.jsonl, history/index.json and docs/choices.json for this fixture; today is 2026-11-09 Asia/Jakarta. Status inspection is read-only; no CI rerun, watcher, push, merge or new helper. Requested period is Nov2-9. Additional authoritative local period events are .fixture/period-events.json; neither A nor B is shipped.

Disposable local fixture only. README.md documents python3 tools/forge.py and local bare origin. No real GitHub, accounts, credentials, external network or extra model sessions may be used; scope comes only from this request.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | n/a | true | 3 | 0 |
| baseline | n/a | false | 2 | 0 |

Treatment: 64 response lines; changed files `.fixture/events.jsonl, .git/index`; removed files `none`; validation command present: `requires review`. Workflow cost: 104.78 seconds and 3 tool calls; token usage is in the JSON record.

Baseline: 33 response lines; changed files `.cache/npm/_logs/2026-11-09T05_53_41_011Z-debug-0.log, .fixture/events.jsonl, .git/index`; removed files `none`; validation command present: `requires review`. Workflow cost: 34.89 seconds and 2 tool calls; token usage is in the JSON record.


Expected deliverable: "A wider-window commit was later reverted and another change remains uncommitted." Expect: report the real period, avoid a shipment claim for the reverted change, and label uncommitted work pending.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-outcome-6-temp-stop-retry-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-outcome-6-temp-stop-retry-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-6-temp-stop-retry-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-6-temp-stop-retry-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-6-temp-stop-retry-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-6-temp-stop-retry-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-6-temp-stop-retry-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-6-temp-stop-retry-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-6-temp-stop-retry-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-6-temp-stop-retry-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-6-temp-stop-retry-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-6-temp-stop-retry-claude/baseline/artifacts/`.

Activation is not graded for Outcome examples; review the stated behavioral criterion.

## Outcome review

Value: **matched**. Baseline criterion: yes; treatment criterion: yes.

Both use the requested Nov2–9 Asia/Jakarta window and real fixture Git/events: A committed36908d4 then revertedb4a0c10 has no net shipped result; B remains an uncommitted file. Wider history coverage gaps and current proof limits stay explicit; no mutation occurs.
