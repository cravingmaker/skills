# retro: claude outcome-7

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `outcome-7` in `evals/examples.md`.
- **Skill revision.** Commit `d52ba17daf681100875cf0fb3813c2f329c1652e`, tree `7d08b7495cd80508c7230630b5308b4bf6c9658c`, actual bytes SHA-256 `a43c34bce5ae719195a8be49b334a17ab6c20ddbf420e430251a9b733c5d3564`; dirty: `True`.
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
| treatment | n/a | true | 11 | 0 |
| baseline | n/a | false | 4 | 0 |

Treatment: 25 response lines; changed files `.cache/npm/_logs/2026-11-09T15_17_54_757Z-debug-0.log, .fixture/events.jsonl, scratch/issue-draft.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 94.194 seconds and 11 tool calls; token usage is in the JSON record.

Baseline: 15 response lines; changed files `.cache/npm/_logs/2026-11-09T15_19_29_027Z-debug-0.log, .fixture/events.jsonl, scratch/issue-draft.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 44.619 seconds and 4 tool calls; token usage is in the JSON record.


Expected deliverable: "Prepare a local issue draft and compare only the two named similar sessions." Expect: relevant issue search, bounded signature checks and exact hit/miss/unknown pointers; no issue posting or fixed analyst panel.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-outcome-7-round2-fix3-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-outcome-7-round2-fix3-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-7-round2-fix3-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-7-round2-fix3-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-7-round2-fix3-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-7-round2-fix3-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-7-round2-fix3-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-7-round2-fix3-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-7-round2-fix3-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-7-round2-fix3-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-7-round2-fix3-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-7-round2-fix3-claude/baseline/artifacts/`.

Activation is not graded for Outcome examples; review the stated behavioral criterion.

## Round 2 review

Baseline: partial. Treatment: yes. Value: added.

Treatment reads only the four named evidence files, checks D1, compares exactly two sessions with hit/miss/unknown pointers, and writes only a local draft. The child summary is not independent recurrence and actual shipment stays unknown. Baseline produces a useful draft but reads unrelated repository orientation content including unnamed history README/conventions.
