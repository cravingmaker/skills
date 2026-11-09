# retro: claude outcome-2

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `outcome-2` in `evals/examples.md`.
- **Skill revision.** Commit `d52ba17daf681100875cf0fb3813c2f329c1652e`, tree `7d08b7495cd80508c7230630b5308b4bf6c9658c`, actual bytes SHA-256 `660394f1cc6fb66ea5fc19a986354811bdbae86373435246a97f77707449629f`; dirty: `True`.
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
| treatment | n/a | true | 5 | 0 |
| baseline | n/a | false | 1 | 0 |

Treatment: 40 response lines; changed files `.cache/npm/_logs/2026-11-09T11_38_56_111Z-debug-0.log, .fixture/events.jsonl`; removed files `none`; validation command present: `requires review`. Workflow cost: 43.587 seconds and 5 tool calls; token usage is in the JSON record.

Baseline: 23 response lines; changed files `.cache/npm/_logs/2026-11-09T11_41_34_558Z-debug-0.log, .fixture/events.jsonl`; removed files `none`; validation command present: `requires review`. Workflow cost: 26.717 seconds and 1 tool calls; token usage is in the JSON record.


Expected deliverable: "The session's cumulative token readings are 100, 160, and missing; a child total is already included. Explain usage." Expect: establish counter scope, avoid summing snapshots or double-counting children, and leave the missing interval unknown.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-outcome-2-round2-fix2-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-outcome-2-round2-fix2-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-2-round2-fix2-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-2-round2-fix2-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-2-round2-fix2-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-2-round2-fix2-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-2-round2-fix2-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-2-round2-fix2-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-2-round2-fix2-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-2-round2-fix2-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-2-round2-fix2-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-2-round2-fix2-claude/baseline/artifacts/`.

Activation is not graded for Outcome examples; review the stated behavioral criterion.

## Round 2 review

Baseline: yes. Treatment: yes. Value: matched.

Both preserve100->160 cumulative samples, derive60 and avoid double-counting child40 while leaving final usage unknown. Treatment reads only the named history index/target and no README/conventions body.

This intermediate skill revision was superseded; it does not establish the final-byte coverage gate.
