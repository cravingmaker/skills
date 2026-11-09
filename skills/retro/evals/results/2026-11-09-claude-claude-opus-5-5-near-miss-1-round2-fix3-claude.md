# retro: claude near-miss-1

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `near-miss-1` in `evals/examples.md`.
- **Skill revision.** Commit `d52ba17daf681100875cf0fb3813c2f329c1652e`, tree `7d08b7495cd80508c7230630b5308b4bf6c9658c`, actual bytes SHA-256 `a43c34bce5ae719195a8be49b334a17ab6c20ddbf420e430251a9b733c5d3564`; dirty: `True`.
- **Fixture.** `near-miss-1`, SHA-256 `a625a622902cb86ab3be504e3668438879ca8dba311c8fd218b1466f82b8cd2c`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
Fix this typo in the heading.

Fixture context: this is a disposable local repository with a local bare origin. README.md documents its real commands, synthetic PR state and offline forge API (python3 tools/forge.py). All external network and real gh operations must fail closed; no real repositories, accounts or credentials may be used. Apply only the action authority in the request. No extra model sessions or agents are allowed. Use the available Python 3 interpreter (the fixture supports Python 3.12 or later). Synthetic forge results establish fixture behavior only.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | false | false | 3 | 0 |
| baseline | false | false | 3 | 0 |

Treatment: 1 response lines; changed files `.cache/npm/_logs/2026-11-09T15_14_51_994Z-debug-0.log, .fixture/events.jsonl, .git/index, heading.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 28.286 seconds and 3 tool calls; token usage is in the JSON record.

Baseline: 1 response lines; changed files `.cache/npm/_logs/2026-11-09T15_15_19_089Z-debug-0.log, .fixture/events.jsonl, .git/index, heading.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 19.584 seconds and 3 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: direct editing without session mining or a standing rule.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-near-miss-1-round2-fix3-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-near-miss-1-round2-fix3-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-near-miss-1-round2-fix3-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-near-miss-1-round2-fix3-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-near-miss-1-round2-fix3-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-near-miss-1-round2-fix3-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-near-miss-1-round2-fix3-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-near-miss-1-round2-fix3-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-near-miss-1-round2-fix3-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-near-miss-1-round2-fix3-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-near-miss-1-round2-fix3-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-near-miss-1-round2-fix3-claude/baseline/artifacts/`.
