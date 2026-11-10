# full-send: claude activation-3

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-3` in `evals/examples.md`.
- **Skill revision.** Commit `d78b9956da6f04ed515a45ace4278fed10425be6`, tree `484196e75bb76b60eb18ff64f7e4b0c3d33a4e1e`, actual bytes SHA-256 `80ae4ecb34360151758bccbfdd576fca17074a74c90090bb3829293ebef43b74`; dirty: `False`.
- **Fixture.** `activation-3`, SHA-256 `599847a7fac2056b23fd201b4d6efd7bcb1850a4c50f5ecc611bb58ee12ea147`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [full-send.tar.gz](https://drive.google.com/file/d/1K-FhcZT_DhoBfuySp0UCDxZFt9oZfKre/view), folder `2026-11-09-claude-claude-opus-5-5-activation-3-claude/` inside.

## Prompt

```text
/full-stop Fix the pager bug and prepare the PR.

Fixture context: this is a disposable local repository with a local bare origin. README.md documents its real commands, synthetic PR state and offline forge API (python3 tools/forge.py). All external network and real gh operations must fail closed; no real repositories, accounts or credentials may be used. Apply only the action authority in the request. No extra model sessions or agents are allowed. Use the available Python 3 interpreter (the fixture supports Python 3.12 or later). Synthetic forge results establish fixture behavior only.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 26 | 0 |
| baseline | false | false | 2 | 0 |

Treatment: 34 response lines; changed files `.cache/npm/_logs/2026-11-09T10_01_41_657Z-debug-0.log, .fixture/check-output.txt, .fixture/events.jsonl, .fixture/remote.git/objects/46/6279a2fd02ff7d1b5bc87fa6cfd916b3a25585, .fixture/remote.git/objects/b8/2b94c5ca1bbce7a98cd32c9f918aa412981264, .fixture/remote.git/objects/c5/772fd24cc50e73307d26accf9ba7c1f7a7d4f0, .fixture/remote.git/objects/e7/739b6889183d02e4a424f46060b1dd534714af, .fixture/remote.git/refs/heads/feature, .fixture/state.json, .git/COMMIT_EDITMSG, .git/index, .git/objects/46/6279a2fd02ff7d1b5bc87fa6cfd916b3a25585, .git/objects/b8/2b94c5ca1bbce7a98cd32c9f918aa412981264, .git/objects/c5/772fd24cc50e73307d26accf9ba7c1f7a7d4f0, .git/objects/e7/739b6889183d02e4a424f46060b1dd534714af, .git/refs/heads/feature, .git/refs/remotes/origin/HEAD, .git/refs/remotes/origin/feature, src/__pycache__/cache.cpython-315.pyc, src/__pycache__/pager.cpython-315.pyc, src/pager.py, tests/__pycache__/test_pager.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 162.089 seconds and 26 tool calls; token usage is in the JSON record.

Baseline: 11 response lines; changed files `.cache/npm/_logs/2026-11-09T10_04_23_881Z-debug-0.log, .fixture/events.jsonl`; removed files `none`; validation command present: `requires review`. Workflow cost: 22.082 seconds and 2 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: prepare-only mode; every helper carries no-merge; the run ends with a ready, waiting or blocked verdict and the PR open and unmerged.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: `2026-11-09-claude-claude-opus-5-5-activation-3-claude/comparison.json` (local only, not committed).

## Treatment evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-activation-3-claude/treatment/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-activation-3-claude/treatment/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-activation-3-claude/treatment/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-activation-3-claude/treatment/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-3-claude/treatment/artifacts/`.

## Baseline evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-activation-3-claude/baseline/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-activation-3-claude/baseline/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-activation-3-claude/baseline/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-activation-3-claude/baseline/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-3-claude/baseline/artifacts/`.

## Activation observation correction

The original detector did not recognize this successful Bash body read. A retrospective parse verifies the installed candidate path, recorded input-file hashes and visible candidate body. Activation is corrected to true; model starts and behavioral judgments are unchanged. Original JSON and Markdown remain in the ignored raw record backup.
