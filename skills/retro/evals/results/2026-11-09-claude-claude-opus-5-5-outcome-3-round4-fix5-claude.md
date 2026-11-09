# retro: claude outcome-3

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `outcome-3` in `evals/examples.md`.
- **Skill revision.** Commit `3a45803857dd58c02c5a7f1bdfdcdfd3a232f1db`, tree `6d98e2044b7c10e2525848e85901015878a4c2d7`, actual bytes SHA-256 `eb0da3d026930271bc68767052c47bc7cc473c2ec0f3e652521b5c4cbe1d433f`; dirty: `True`.
- **Fixture.** `outcome-3`, SHA-256 `a625a622902cb86ab3be504e3668438879ca8dba311c8fd218b1466f82b8cd2c`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
/retro The raw session is unavailable; the visible chat shows only a promise to test. Give the retro.

Supplied task context:
The raw transcript and history export are unavailable; do not use the fixture history files as this session. Visible chat: Human: run the test before claiming success. Assistant: I will test it. No tool result is supplied. Give a report from that limited evidence only.

Disposable local fixture only. README.md documents python3 tools/forge.py and local bare origin. No real GitHub, accounts, credentials, external network or extra model sessions may be used; scope comes only from this request.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | n/a | true | 3 | 0 |
| baseline | n/a | false | 0 | 0 |

Treatment: 25 response lines; changed files `.cache/npm/_logs/2026-11-09T16_21_40_622Z-debug-0.log, .fixture/events.jsonl`; removed files `none`; validation command present: `requires review`. Workflow cost: 34.556 seconds and 3 tool calls; token usage is in the JSON record.

Baseline: 31 response lines; changed files `.cache/npm/_logs/2026-11-09T16_22_14_870Z-debug-0.log, .fixture/events.jsonl`; removed files `none`; validation command present: `requires review`. Workflow cost: 12.651 seconds and 0 tool calls; token usage is in the JSON record.


Expected deliverable: "The raw session is unavailable; the visible chat shows only a promise to test. Give the retro." Expect: limited coverage and unsupported test claim remain explicit, with no invented transcript findings.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-outcome-3-round4-fix5-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-outcome-3-round4-fix5-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-3-round4-fix5-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-3-round4-fix5-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-3-round4-fix5-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-3-round4-fix5-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-3-round4-fix5-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-3-round4-fix5-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-3-round4-fix5-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-3-round4-fix5-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-3-round4-fix5-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-3-round4-fix5-claude/baseline/artifacts/`.

Activation is not graded for Outcome examples; review the stated behavioral criterion.

## Round 4 review

Baseline: yes. Treatment: yes. Value: matched.

Both use only the supplied two-message chat for session evidence, keep execution and results unknown, and make no project/history reads. Treatment loads installed method skills and attempts a prose check from that installed method directory; it accurately reports Vale unavailable, not a pass. It explicitly refuses to link the ambient fixture commit to the unavailable session, rejects a duplicate rule and defers any mechanical gate until evidence is available. Baseline uses no tools. Neither changes product files.

Source boundary: pass. Inspected every treatment tool call (trace lines 8, 16, 25); no treatment commit-log, blame, prior-revision diff or outside-source listing/status/search request occurred.
