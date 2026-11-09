# full-stop: claude near-miss-3

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `near-miss-3` in `evals/examples.md`.
- **Skill revision.** Commit `752a1cc6661ad8489c757a4d9d75bcf93e7e5d89`, tree `b616519038e78dc211d1453ad5ba80627287cfec`, actual bytes SHA-256 `337fe7fd497285211dbf028f83b0a7a41c285c098947a5a4d0ba7e2ecbedcd34`; dirty: `False`.
- **Fixture.** `near-miss-3`, SHA-256 `2fd2818fbac589f870ede19ca440f89040040fd76bc0579d5843476018472655`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
Full send this.

Fixture context: this is a disposable local repository with a local bare origin. README.md documents its real commands, synthetic PR state and offline forge API (python3 tools/forge.py). All external network and real gh operations must fail closed; no real repositories, accounts or credentials may be used. Apply only the action authority in the request. No extra model sessions or agents are allowed. Use the available Python 3 interpreter (the fixture supports Python 3.12 or later). Synthetic forge results establish fixture behavior only.
Earlier human scope was prepare-only. This new human request changes it to finish-to-merge; remaining check/review gates still apply.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | false | false | 11 | 0 |
| baseline | false | false | 13 | 0 |

Treatment: 22 response lines; changed files `.cache/npm/_logs/2026-11-09T10_05_28_598Z-debug-0.log, .fixture/check-output.txt, .fixture/events.jsonl, .fixture/remote.git/objects/af/44899d886255232770cc0b7cf42cea8d68f9c9, .fixture/remote.git/objects/b8/2b94c5ca1bbce7a98cd32c9f918aa412981264, .fixture/remote.git/objects/be/c66bf531f0a99d5c19976143311d7baa054312, .fixture/remote.git/objects/e7/739b6889183d02e4a424f46060b1dd534714af, .fixture/remote.git/refs/heads/feature, .fixture/state.json, .git/COMMIT_EDITMSG, .git/index, .git/objects/af/44899d886255232770cc0b7cf42cea8d68f9c9, .git/objects/b8/2b94c5ca1bbce7a98cd32c9f918aa412981264, .git/objects/be/c66bf531f0a99d5c19976143311d7baa054312, .git/objects/e7/739b6889183d02e4a424f46060b1dd534714af, .git/refs/heads/feature, .git/refs/remotes/origin/feature, src/__pycache__/cache.cpython-315.pyc, src/__pycache__/pager.cpython-315.pyc, src/pager.py, tests/__pycache__/test_pager.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 78.156 seconds and 11 tool calls; token usage is in the JSON record.

Baseline: 27 response lines; changed files `.cache/npm/_logs/2026-11-09T10_06_46_682Z-debug-0.log, .fixture/check-output.txt, .fixture/events.jsonl, .fixture/remote.git/objects/b8/2b94c5ca1bbce7a98cd32c9f918aa412981264, .fixture/remote.git/objects/be/c66bf531f0a99d5c19976143311d7baa054312, .fixture/remote.git/objects/c9/41425ddfdb6a399336e9c2caf9325c1279cbb6, .fixture/remote.git/objects/e7/739b6889183d02e4a424f46060b1dd534714af, .fixture/remote.git/refs/heads/feature, .fixture/state.json, .git/COMMIT_EDITMSG, .git/index, .git/objects/b8/2b94c5ca1bbce7a98cd32c9f918aa412981264, .git/objects/be/c66bf531f0a99d5c19976143311d7baa054312, .git/objects/c9/41425ddfdb6a399336e9c2caf9325c1279cbb6, .git/objects/e7/739b6889183d02e4a424f46060b1dd534714af, .git/refs/heads/feature, .git/refs/remotes/origin/HEAD, .git/refs/remotes/origin/feature, src/__pycache__/cache.cpython-315.pyc, src/__pycache__/pager.cpython-315.pyc, src/pager.py, tests/__pycache__/test_pager.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 86.69 seconds and 13 tool calls; token usage is in the JSON record.


Expected deliverable: (plain text, entry not invoked). Expect: the new request supplies finish-to-merge authority subject to remaining gates, replacing an earlier prepare-only limit for this task. Native explicit invocation selects a manual entry; plain text need not load either selector, and this entry is not selected.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-near-miss-3-claude/baseline/artifacts/`.
