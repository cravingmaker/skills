# clear-communication: claude near-miss-1

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `near-miss-1` in `evals/examples.md`.
- **Skill revision.** Commit `7af466aad380e89b419f204d52baed99995023c3`, tree `3e9df371767cc35ab142b68b3c9428157f525510`, actual bytes SHA-256 `d9aae65318e79659b8e8ea7ebcf9c1cf41409978a9bdc77cf1a455bdcd882e47`; dirty: `True`.
- **Fixture.** `tests/eval-harness/fixtures/package`, SHA-256 `3fc75a91e565dd737362d2462d654f8fb022854ba2b9e866b545eaf7d94533a5`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `host default`; each arm has a new session and the same host settings.

## Prompt

```text
Which command validates this repo?
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | false | false | 2 | 0 |
| baseline | false | false | 2 | 0 |

Expected deliverable: Expect: a direct one-line answer under the standing contract (`./scripts/validate.sh`), no clarifying question, no skill-driven editing pass.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-08-claude-claude-opus-5-5-near-miss-1-isolated/comparison.json](2026-11-08-claude-claude-opus-5-5-near-miss-1-isolated/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-08-claude-claude-opus-5-5-near-miss-1-isolated/treatment/trace.jsonl)
- [Standard error](2026-11-08-claude-claude-opus-5-5-near-miss-1-isolated/treatment/stderr.txt)
- [Observed response](2026-11-08-claude-claude-opus-5-5-near-miss-1-isolated/treatment/response.txt)
- [Input and discovery manifest](2026-11-08-claude-claude-opus-5-5-near-miss-1-isolated/treatment/manifest.json)
- Artifacts: `2026-11-08-claude-claude-opus-5-5-near-miss-1-isolated/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-08-claude-claude-opus-5-5-near-miss-1-isolated/baseline/trace.jsonl)
- [Standard error](2026-11-08-claude-claude-opus-5-5-near-miss-1-isolated/baseline/stderr.txt)
- [Observed response](2026-11-08-claude-claude-opus-5-5-near-miss-1-isolated/baseline/response.txt)
- [Input and discovery manifest](2026-11-08-claude-claude-opus-5-5-near-miss-1-isolated/baseline/manifest.json)
- Artifacts: `2026-11-08-claude-claude-opus-5-5-near-miss-1-isolated/baseline/artifacts/`.
