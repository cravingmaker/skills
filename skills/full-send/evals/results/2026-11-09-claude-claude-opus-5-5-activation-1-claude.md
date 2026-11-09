# full-send: claude activation-1

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-1` in `evals/examples.md`.
- **Skill revision.** Commit `d78b9956da6f04ed515a45ace4278fed10425be6`, tree `484196e75bb76b60eb18ff64f7e4b0c3d33a4e1e`, actual bytes SHA-256 `80ae4ecb34360151758bccbfdd576fca17074a74c90090bb3829293ebef43b74`; dirty: `False`.
- **Fixture.** `activation-1`, SHA-256 `599847a7fac2056b23fd201b4d6efd7bcb1850a4c50f5ecc611bb58ee12ea147`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
/full-send
Full send: fix the off-by-one in the pager and get it merged.

Fixture context: this is a disposable local repository with a local bare origin. README.md documents its real commands, synthetic PR state and offline forge API (python3 tools/forge.py). All external network and real gh operations must fail closed; no real repositories, accounts or credentials may be used. Apply only the action authority in the request. No extra model sessions or agents are allowed. Use the available Python 3 interpreter (the fixture supports Python 3.12 or later). Synthetic forge results establish fixture behavior only.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 26 | 0 |
| baseline | false | false | 10 | 0 |

Treatment: 32 response lines; changed files `.cache/npm/_logs/2026-11-09T10_00_36_713Z-debug-0.log, .fixture/check-output.txt, .fixture/events.jsonl, .fixture/remote.git/objects/b7/8950c632cc206751d4d1103967b64ed3015b99, .fixture/remote.git/objects/b8/2b94c5ca1bbce7a98cd32c9f918aa412981264, .fixture/remote.git/objects/c5/772fd24cc50e73307d26accf9ba7c1f7a7d4f0, .fixture/remote.git/objects/e7/739b6889183d02e4a424f46060b1dd534714af, .fixture/remote.git/refs/heads/feature, .fixture/state.json, .git/COMMIT_EDITMSG, .git/index, .git/objects/b7/8950c632cc206751d4d1103967b64ed3015b99, .git/objects/b8/2b94c5ca1bbce7a98cd32c9f918aa412981264, .git/objects/c5/772fd24cc50e73307d26accf9ba7c1f7a7d4f0, .git/objects/e7/739b6889183d02e4a424f46060b1dd534714af, .git/refs/heads/feature, .git/refs/remotes/origin/HEAD, .git/refs/remotes/origin/feature, run/DECISIONS.md, run/LOG.md, src/__pycache__/cache.cpython-315.pyc, src/__pycache__/pager.cpython-315.pyc, src/pager.py, tests/__pycache__/test_pager.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 172.129 seconds and 26 tool calls; token usage is in the JSON record.

Baseline: 19 response lines; changed files `.cache/npm/_logs/2026-11-09T10_03_27_498Z-debug-0.log, .fixture/check-output.txt, .fixture/events.jsonl, .fixture/remote.git/objects/6e/cfa6b57135fc5bdb2a1759cf2b9185d5b62c50, .fixture/remote.git/objects/bc/4d8b7268ff01f5ac63afe69e3c935d2f6a7fb7, .fixture/remote.git/objects/e1/8f8d33a4496a82a685cd59e0c2c292ff2e8e81, .fixture/remote.git/objects/f8/0a9ffcc36de75c0d131190384078e9f886c4d6, .fixture/remote.git/refs/heads/feature, .fixture/state.json, .git/COMMIT_EDITMSG, .git/index, .git/objects/6e/cfa6b57135fc5bdb2a1759cf2b9185d5b62c50, .git/objects/bc/4d8b7268ff01f5ac63afe69e3c935d2f6a7fb7, .git/objects/e1/8f8d33a4496a82a685cd59e0c2c292ff2e8e81, .git/objects/f8/0a9ffcc36de75c0d131190384078e9f886c4d6, .git/refs/heads/feature, .git/refs/remotes/origin/HEAD, .git/refs/remotes/origin/feature, src/__pycache__/cache.cpython-315.pyc, src/__pycache__/pager.cpython-315.pyc, src/pager.py, tests/__pycache__/test_pager.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 91.798 seconds and 10 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: the change, proof at the current head, a sol-loop review within three rounds, the PR filed through the `file-pr` skill, the root babysitting through the `babysit-pr` skill, and a head-guarded merge only once every gate passes; the report gives the PR link, merge commit and proof.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-activation-1-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-activation-1-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-1-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-1-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-1-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-1-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-1-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-1-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-1-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-1-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-1-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-1-claude/baseline/artifacts/`.
