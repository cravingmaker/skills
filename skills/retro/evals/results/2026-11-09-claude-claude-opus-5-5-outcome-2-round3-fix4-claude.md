# retro: claude outcome-2

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `outcome-2` in `evals/examples.md`.
- **Skill revision.** Commit `e85790be565e2de21ee2ea7df6abf8ea385454e0`, tree `e96fda3e3d285b35cf382d8e88343ec8cf887173`, actual bytes SHA-256 `487306e29b693efee09f20313eee4384da506c690d7cb009e5445b6363046eb7`; dirty: `True`.
- **Fixture.** `outcome-2`, SHA-256 `a625a622902cb86ab3be504e3668438879ca8dba311c8fd218b1466f82b8cd2c`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
/retro The session's cumulative token readings are 100, 160, and missing; a child total is already included. Explain usage.

Supplied task context:
Use only the authorized history/index.json, history/session-target.jsonl and the supplied incident files. Report only, except outcome-specific export or local-draft authority stated here. No real issue posting or remote access. Supplied authoritative counter samples for this session: cumulative total100, then total160, then missing. The child total40 is included in the first two parent totals. No other usage samples exist.

Disposable local fixture only. README.md documents python3 tools/forge.py and local bare origin. No real GitHub, accounts, credentials, external network or extra model sessions may be used; scope comes only from this request.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | n/a | true | 4 | 0 |
| baseline | n/a | false | 2 | 0 |

Treatment: 49 response lines; changed files `.cache/npm/_logs/2026-11-09T16_00_19_659Z-debug-0.log, .fixture/events.jsonl`; removed files `none`; validation command present: `requires review`. Workflow cost: 50.879 seconds and 4 tool calls; token usage is in the JSON record.

Baseline: 28 response lines; changed files `.cache/npm/_logs/2026-11-09T16_01_10_702Z-debug-0.log, .fixture/events.jsonl`; removed files `none`; validation command present: `requires review`. Workflow cost: 28.455 seconds and 2 tool calls; token usage is in the JSON record.


Expected deliverable: "The session's cumulative token readings are 100, 160, and missing; a child total is already included. Explain usage." Expect: establish counter scope, avoid summing snapshots or double-counting children, and leave the missing interval unknown.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-outcome-2-round3-fix4-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-outcome-2-round3-fix4-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-2-round3-fix4-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-2-round3-fix4-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-2-round3-fix4-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-2-round3-fix4-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-2-round3-fix4-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-2-round3-fix4-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-2-round3-fix4-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-2-round3-fix4-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-2-round3-fix4-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-2-round3-fix4-claude/baseline/artifacts/`.

Activation is not graded for Outcome examples; review the stated behavioral criterion.

## Round 3 review

Baseline: partial. Treatment: yes. Value: added.

Both keep the last cumulative total 160, the 60-token increment, included child 40, and unknown final total. Treatment reads only named index/session and installed method skills, explicitly leaving child/history/incident gaps unread. Baseline additionally searches for unnamed incidents and reads the unauthorized child session. Treatment reports broader session observations with explicit limits; this adds response length, without a source-boundary miss.

Source boundary: pass. Inspected every treatment tool call (trace lines 7, 9, 10, 11); no treatment commit-log, blame, or prior-revision diff request occurred.
