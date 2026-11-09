# retro: claude outcome-1

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `outcome-1` in `evals/examples.md`.
- **Skill revision.** Commit `d52ba17daf681100875cf0fb3813c2f329c1652e`, tree `7d08b7495cd80508c7230630b5308b4bf6c9658c`, actual bytes SHA-256 `a43c34bce5ae719195a8be49b334a17ab6c20ddbf420e430251a9b733c5d3564`; dirty: `True`.
- **Fixture.** `outcome-1`, SHA-256 `3a5e6b81ae30042874d408d627a1d20c646874981ee0b0483f0ac3052e8fdfc6`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
/retro An instruction says to add another rule for a repeated banned import, but the repo linter already has an unwired check. What should change?

Supplied task context:
Use only the authorized history/index.json, history/session-target.jsonl and the supplied incident files. Report only, except outcome-specific export or local-draft authority stated here. No real issue posting or remote access. Incident evidence is history/import-incidents.md; inspect the existing validator and check.

Disposable local fixture only. README.md documents python3 tools/forge.py and local bare origin. No real GitHub, accounts, credentials, external network or extra model sessions may be used; scope comes only from this request.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | n/a | true | 8 | 0 |
| baseline | n/a | false | 3 | 0 |

Treatment: 44 response lines; changed files `.cache/npm/_logs/2026-11-09T15_17_26_716Z-debug-0.log, .fixture/events.jsonl`; removed files `none`; validation command present: `requires review`. Workflow cost: 74.865 seconds and 8 tool calls; token usage is in the JSON record.

Baseline: 17 response lines; changed files `.cache/npm/_logs/2026-11-09T15_18_42_120Z-debug-0.log, .fixture/events.jsonl`; removed files `none`; validation command present: `requires review`. Workflow cost: 28.248 seconds and 3 tool calls; token usage is in the JSON record.


Expected deliverable: "An instruction says to add another rule for a repeated banned import, but the repo linter already has an unwired check. What should change?" Expect: check-over-prose selects wiring or repairing the existing mechanism, with recurrence and reject/accept/repeat evidence, rather than another instruction.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-outcome-1-round2-fix3-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-outcome-1-round2-fix3-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-1-round2-fix3-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-1-round2-fix3-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-1-round2-fix3-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-1-round2-fix3-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-1-round2-fix3-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-1-round2-fix3-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-1-round2-fix3-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-1-round2-fix3-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-1-round2-fix3-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-1-round2-fix3-claude/baseline/artifacts/`.

Activation is not graded for Outcome examples; review the stated behavioral criterion.

## Round 2 review

Baseline: partial. Treatment: partial. Value: matched.

Treatment reads the three named records and requested validator/check, demonstrates check weaknesses on owned synthetic scratch inputs, and recommends repair/wiring. It also runs Git history queries for both project paths, although Git history is outside the stated source list, and cites the fixture setup commit in its answer. The source boundary therefore remains incomplete at this digest. Baseline reaches a mechanical remedy but reads unrelated README, policy, source and package files. Keep retro unevaluated pending a clean confirmation at the final digest; this valid comparison records a behavioral miss, not an isolation failure.
