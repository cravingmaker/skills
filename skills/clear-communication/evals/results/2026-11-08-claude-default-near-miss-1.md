# clear-communication: claude near-miss-1

Comparison: **invalid**. Host: `2.1.311 (Claude Code)`. Effective model: `default`.

## Inputs

- **Source example.** `near-miss-1` in `evals/examples.md`.
- **Skill revision.** Commit `7af466aad380e89b419f204d52baed99995023c3`, tree `3e9df371767cc35ab142b68b3c9428157f525510`, actual bytes SHA-256 `d9aae65318e79659b8e8ea7ebcf9c1cf41409978a9bdc77cf1a455bdcd882e47`; dirty: `False`.
- **Fixture.** `tests/eval-harness/fixtures/package`, SHA-256 `3fc75a91e565dd737362d2462d654f8fb022854ba2b9e866b545eaf7d94533a5`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `host default`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [clear-communication.tar.gz](https://drive.google.com/file/d/1aeIJGrgJVddiMx2OHdnS48QfZC4ZRETW/view), folder `2026-11-08-claude-default-near-miss-1/` inside.

## Prompt

```text
Which command validates this repo?
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | false | unavailable | unavailable | 0 |
| baseline | false | unavailable | unavailable | not run |

Expected deliverable: Expect: a direct one-line answer under the standing contract (`./scripts/validate.sh`), no clarifying question, no skill-driven editing pass.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: `2026-11-08-claude-default-near-miss-1/comparison.json` (local only, not committed).

## Invalid comparison

- Claude loaded plugins or MCP servers; comparison is invalid

## Treatment evidence

- Raw JSON trace: `2026-11-08-claude-default-near-miss-1/treatment/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-08-claude-default-near-miss-1/treatment/stderr.txt` (local only, not committed)
- Observed response: `2026-11-08-claude-default-near-miss-1/treatment/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-08-claude-default-near-miss-1/treatment/manifest.json` (local only, not committed)
- Artifacts: `2026-11-08-claude-default-near-miss-1/treatment/artifacts/`.

## Baseline evidence

- Raw JSON trace: `2026-11-08-claude-default-near-miss-1/baseline/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-08-claude-default-near-miss-1/baseline/stderr.txt` (local only, not committed)
- Observed response: `2026-11-08-claude-default-near-miss-1/baseline/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-08-claude-default-near-miss-1/baseline/manifest.json` (local only, not committed)
- Artifacts: `2026-11-08-claude-default-near-miss-1/baseline/artifacts/`.
