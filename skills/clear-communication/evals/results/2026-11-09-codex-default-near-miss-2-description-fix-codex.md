# clear-communication: codex near-miss-2

Comparison: **invalid**. Host: `codex-cli 0.167.0`. Effective model: `default`.

## Inputs

- **Source example.** `near-miss-2` in `evals/examples.md`.
- **Skill revision.** Commit `b7d5b85899f2cfe0b6ce7e2e715565848a9436ec`, tree `3c1d6e767164d88cf2ea77ef9eb49d73e360bb7c`, actual bytes SHA-256 `50e5d3e75b98078be5aef095c579602f97be163c257098372291d64bb340a4d1`; dirty: `True`.
- **Fixture.** `near-miss-2`, SHA-256 `4a3929ae41dc6693d05c2e7f0e2d972d1741613369b0aa68ec0ab4ecb6b4d248`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `host default`; effort `host default`; each arm has a new session and the same host settings.

## Prompt

```text
Fix the typo in line 3 of AGENTS.example.md.

Task context supplied to both arms:
The harness owns live AGENTS.md; fix line 3 in AGENTS.example.md instead.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | false | unavailable | unavailable | not run |
| baseline | false | unavailable | unavailable | not run |


Expected deliverable: Expect: the fix, with no restatement of the request and no questions.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-codex-default-near-miss-2-description-fix-codex/comparison.json](2026-11-09-codex-default-near-miss-2-description-fix-codex/comparison.json).

## Invalid comparison

- Shared budget limit reached

## Treatment evidence

- [Raw JSON trace](2026-11-09-codex-default-near-miss-2-description-fix-codex/treatment/trace.jsonl)
- [Standard error](2026-11-09-codex-default-near-miss-2-description-fix-codex/treatment/stderr.txt)
- [Observed response](2026-11-09-codex-default-near-miss-2-description-fix-codex/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-codex-default-near-miss-2-description-fix-codex/treatment/manifest.json)
- Artifacts: `2026-11-09-codex-default-near-miss-2-description-fix-codex/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-codex-default-near-miss-2-description-fix-codex/baseline/trace.jsonl)
- [Standard error](2026-11-09-codex-default-near-miss-2-description-fix-codex/baseline/stderr.txt)
- [Observed response](2026-11-09-codex-default-near-miss-2-description-fix-codex/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-codex-default-near-miss-2-description-fix-codex/baseline/manifest.json)
- Artifacts: `2026-11-09-codex-default-near-miss-2-description-fix-codex/baseline/artifacts/`.
