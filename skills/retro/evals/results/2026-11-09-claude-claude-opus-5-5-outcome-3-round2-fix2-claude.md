# retro: claude outcome-3

Comparison: **invalid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `outcome-3` in `evals/examples.md`.
- **Skill revision.** Commit `d52ba17daf681100875cf0fb3813c2f329c1652e`, tree `7d08b7495cd80508c7230630b5308b4bf6c9658c`, actual bytes SHA-256 `660394f1cc6fb66ea5fc19a986354811bdbae86373435246a97f77707449629f`; dirty: `True`.
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
| treatment | n/a | true | 1 | 0 |
| baseline | n/a | unavailable | unavailable | 1 |

Treatment: 39 response lines; changed files `.cache/npm/_logs/2026-11-09T11_41_21_882Z-debug-0.log, .fixture/events.jsonl`; removed files `none`; validation command present: `requires review`. Workflow cost: 25.891 seconds and 1 tool calls; token usage is in the JSON record.


Expected deliverable: "The raw session is unavailable; the visible chat shows only a promise to test. Give the retro." Expect: limited coverage and unsupported test claim remain explicit, with no invented transcript findings.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-outcome-3-round2-fix2-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-outcome-3-round2-fix2-claude/comparison.json).

## Invalid comparison

- claude baseline failed (exit 1, timeout False); inspect stderr and trace

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-3-round2-fix2-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-3-round2-fix2-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-3-round2-fix2-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-3-round2-fix2-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-3-round2-fix2-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-3-round2-fix2-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-3-round2-fix2-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-3-round2-fix2-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-3-round2-fix2-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-3-round2-fix2-claude/baseline/artifacts/`.

Activation is not graded for Outcome examples; review the stated behavioral criterion.
