# agent-orchestrator: claude near-miss-3

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `near-miss-3` in `evals/examples.md`.
- **Skill revision.** Commit `66f8700b5f86ced76eeb64d9f42201df5ea9f2be`, tree `faaa8ba405c30dfde02825ff9252ba1ae0502737`, actual bytes SHA-256 `493634536f354182ae89b53b5abf929de6658f5428087aad7149db43c22ee675`; dirty: `False`.
- **Fixture.** `tests/eval-harness/fixtures/eval-worker/leaf`, SHA-256 `f57e16de44b11351b9bc8d81629cd36caec7f6c50542ada61757f015582a23e2`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `host default`; each arm has a new session and the same host settings.

## Prompt

```text
You are the research worker; write only the dossier at this path and do not delegate.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | false | false | 3 | 0 |
| baseline | false | false | 3 | 0 |

Treatment: 13 response lines; changed files `dossier.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 16.93 seconds and 3 tool calls; token usage is in the JSON record.

Baseline: 8 response lines; changed files `dossier.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 17.301 seconds and 3 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: the bounded worker task; the orchestrator does not activate inside the worker.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-08-claude-claude-opus-5-5-near-miss-3/comparison.json](2026-11-08-claude-claude-opus-5-5-near-miss-3/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-08-claude-claude-opus-5-5-near-miss-3/treatment/trace.jsonl)
- [Standard error](2026-11-08-claude-claude-opus-5-5-near-miss-3/treatment/stderr.txt)
- [Observed response](2026-11-08-claude-claude-opus-5-5-near-miss-3/treatment/response.txt)
- [Input and discovery manifest](2026-11-08-claude-claude-opus-5-5-near-miss-3/treatment/manifest.json)
- Artifacts: `2026-11-08-claude-claude-opus-5-5-near-miss-3/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-08-claude-claude-opus-5-5-near-miss-3/baseline/trace.jsonl)
- [Standard error](2026-11-08-claude-claude-opus-5-5-near-miss-3/baseline/stderr.txt)
- [Observed response](2026-11-08-claude-claude-opus-5-5-near-miss-3/baseline/response.txt)
- [Input and discovery manifest](2026-11-08-claude-claude-opus-5-5-near-miss-3/baseline/manifest.json)
- Artifacts: `2026-11-08-claude-claude-opus-5-5-near-miss-3/baseline/artifacts/`.
