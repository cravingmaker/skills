# writing-for-agents: claude near-miss-1

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `near-miss-1` in `evals/examples.md`.
- **Skill revision.** Commit `127c1b77e00a8605ae996555910475c8110c56e6`, tree `98ede78df3b01f35e0f4d6d129e25ab8b8936ed0`, actual bytes SHA-256 `01d6697ae6c876e6429bc0af59ca0852ff588b95166c8a3e3d099772e6ee2f9e`; dirty: `False`.
- **Fixture.** `tests/eval-harness/fixtures/package`, SHA-256 `3fc75a91e565dd737362d2462d654f8fb022854ba2b9e866b545eaf7d94533a5`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
Use anthropic-skills:skill-creator to package these finalized instructions for that host.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | false | false | 4 | 0 |
| baseline | false | false | 3 | 0 |

Treatment: 10 response lines; changed files `none`; removed files `none`; validation command present: `requires review`. Workflow cost: 21.748 seconds and 4 tool calls; token usage is in the JSON record.

Baseline: 9 response lines; changed files `none`; removed files `none`; validation command present: `requires review`. Workflow cost: 17.825 seconds and 3 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: the explicitly selected packaging workflow retains ownership; this skill does not claim host setup solely from the word skill.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-10-claude-claude-opus-5-5-near-miss-1-evalfirst/comparison.json](2026-11-10-claude-claude-opus-5-5-near-miss-1-evalfirst/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-10-claude-claude-opus-5-5-near-miss-1-evalfirst/treatment/trace.jsonl)
- [Standard error](2026-11-10-claude-claude-opus-5-5-near-miss-1-evalfirst/treatment/stderr.txt)
- [Observed response](2026-11-10-claude-claude-opus-5-5-near-miss-1-evalfirst/treatment/response.txt)
- [Input and discovery manifest](2026-11-10-claude-claude-opus-5-5-near-miss-1-evalfirst/treatment/manifest.json)
- Artifacts: `2026-11-10-claude-claude-opus-5-5-near-miss-1-evalfirst/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-10-claude-claude-opus-5-5-near-miss-1-evalfirst/baseline/trace.jsonl)
- [Standard error](2026-11-10-claude-claude-opus-5-5-near-miss-1-evalfirst/baseline/stderr.txt)
- [Observed response](2026-11-10-claude-claude-opus-5-5-near-miss-1-evalfirst/baseline/response.txt)
- [Input and discovery manifest](2026-11-10-claude-claude-opus-5-5-near-miss-1-evalfirst/baseline/manifest.json)
- Artifacts: `2026-11-10-claude-claude-opus-5-5-near-miss-1-evalfirst/baseline/artifacts/`.
