# fix-ci: claude activation-2

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-2` in `evals/examples.md`.
- **Skill revision.** Commit `d78b9956da6f04ed515a45ace4278fed10425be6`, tree `24e8a2f48b95fa880a759c6a98bb74a37b13c31e`, actual bytes SHA-256 `6dd773ce31704a163ecb5669a6d101d437ae9d04bacb0bd9153e1e8e41c708ba`; dirty: `False`.
- **Fixture.** `activation-2`, SHA-256 `ede2231d7aaa707449c7f5d5bf9c00b909a24adb92908f1780455941ab17f71a`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
The lint job failed on main after my merge.

Fixture context: this is a disposable local repository with a local bare origin. README.md documents its real commands, synthetic PR state and offline forge API (python3 tools/forge.py). All external network and real gh operations must fail closed; no real repositories, accounts or credentials may be used. Apply only the action authority in the request. No extra model sessions or agents are allowed. Use the available Python 3 interpreter (the fixture supports Python 3.12 or later). Synthetic forge results establish fixture behavior only.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 6 | 0 |
| baseline | false | false | 3 | 0 |

Treatment: 19 response lines; changed files `.cache/npm/_logs/2026-11-09T09_52_21_717Z-debug-0.log, .fixture/events.jsonl, .git/index, src/__pycache__/cache.cpython-315.pyc, src/__pycache__/pager.cpython-315.pyc, src/pager.py, tests/__pycache__/test_pager.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 34.988 seconds and 6 tool calls; token usage is in the JSON record.

Baseline: 13 response lines; changed files `.cache/npm/_logs/2026-11-09T09_52_58_174Z-debug-0.log, .fixture/events.jsonl, .git/index, src/__pycache__/cache.cpython-315.pyc, src/__pycache__/pager.cpython-315.pyc, src/pager.py, tests/__pycache__/test_pager.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 26.57 seconds and 3 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: the failing run bound to the current head of main, the first causal error read from the log, and a focused fix.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-activation-2-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-activation-2-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-2-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-2-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-2-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-2-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-2-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-2-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-2-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-2-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-2-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-2-claude/baseline/artifacts/`.
