# retro: claude outcome-7

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `outcome-7` in `evals/examples.md`.
- **Skill revision.** Commit `3a45803857dd58c02c5a7f1bdfdcdfd3a232f1db`, tree `6d98e2044b7c10e2525848e85901015878a4c2d7`, actual bytes SHA-256 `eb0da3d026930271bc68767052c47bc7cc473c2ec0f3e652521b5c4cbe1d433f`; dirty: `True`.
- **Fixture.** `outcome-7`, SHA-256 `1e150473e8d87eae1e2dbbb6d4a04dab533a1086c2e3ccafb5f40ceb7d386d48`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
/retro Prepare a local issue draft and compare only the two named similar sessions.

Supplied task context:
Use only the authorized history/index.json, history/session-target.jsonl and the supplied incident files. Report only, except outcome-specific export or local-draft authority stated here. No real issue posting or remote access. Compare only history/session-target.jsonl and history/session-child.jsonl. Search the local issue inventory incident/local-issues.json. Write a local draft to scratch/issue-draft.md; no posting.

Disposable local fixture only. README.md documents python3 tools/forge.py and local bare origin. No real GitHub, accounts, credentials, external network or extra model sessions may be used; scope comes only from this request.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | n/a | true | 13 | 0 |
| baseline | n/a | false | 5 | 0 |

Treatment: 16 response lines; changed files `.cache/npm/_logs/2026-11-09T16_23_06_226Z-debug-0.log, .fixture/events.jsonl, scratch/issue-draft.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 101.629 seconds and 13 tool calls; token usage is in the JSON record.

Baseline: 15 response lines; changed files `.cache/npm/_logs/2026-11-09T16_24_48_380Z-debug-0.log, .fixture/events.jsonl, scratch/issue-draft.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 57.484 seconds and 5 tool calls; token usage is in the JSON record.


Expected deliverable: "Prepare a local issue draft and compare only the two named similar sessions." Expect: relevant issue search, bounded signature checks and exact hit/miss/unknown pointers; no issue posting or fixed analyst panel.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-outcome-7-round4-fix5-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-outcome-7-round4-fix5-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-7-round4-fix5-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-7-round4-fix5-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-7-round4-fix5-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-7-round4-fix5-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-7-round4-fix5-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-7-round4-fix5-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-7-round4-fix5-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-7-round4-fix5-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-7-round4-fix5-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-7-round4-fix5-claude/baseline/artifacts/`.

Activation is not graded for Outcome examples; review the stated behavioral criterion.

## Round 4 review

Baseline: partial. Treatment: yes. Value: added.

Treatment measures and reads only the four named evidence files and installed method guidance, checks the exact draft path with ls -la scratch/issue-draft.md, and writes the authorized local issue draft. It searches the supplied local inventory, finds D1, compares only target and child with hit/miss/unknown limits, rejects independent recurrence from a derivative summary, and keeps actual shipment unknown. Its optional prose check of an owned temporary lint copy reports Vale unavailable. The previous scratch-directory listing does not recur. Baseline additionally inventories the workspace and reads README, history schema/conventions and ignore rules; it acknowledges one unauthorized read afterward. No issue is posted.

Source boundary: pass. Inspected every treatment tool call (trace lines 9, 12, 14, 16, 17, 22, 27, 30, 32, 33, 36, 77, 80); no treatment commit-log, blame, prior-revision diff or outside-source listing/status/search request occurred.
