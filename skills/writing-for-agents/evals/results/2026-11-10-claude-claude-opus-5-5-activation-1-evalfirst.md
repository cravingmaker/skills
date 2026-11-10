# writing-for-agents: claude activation-1

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-1` in `evals/examples.md`.
- **Skill revision.** Commit `127c1b77e00a8605ae996555910475c8110c56e6`, tree `98ede78df3b01f35e0f4d6d129e25ab8b8936ed0`, actual bytes SHA-256 `01d6697ae6c876e6429bc0af59ca0852ff588b95166c8a3e3d099772e6ee2f9e`; dirty: `False`.
- **Fixture.** `tests/eval-harness/fixtures/package`, SHA-256 `3fc75a91e565dd737362d2462d654f8fb022854ba2b9e866b545eaf7d94533a5`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.
- **Private raw evidence.** Not retained: the raw files were lost before the private archive was made.

## Prompt

```text
Rewrite this SKILL.md so the agent follows the right branch and knows when it is done.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 5 | 0 |
| baseline | false | false | 10 | 0 |

Treatment: 11 response lines; changed files `none`; removed files `none`; validation command present: `requires review`. Workflow cost: 22.609 seconds and 5 tool calls; token usage is in the JSON record.

Baseline: 163 response lines; changed files `none`; removed files `none`; validation command present: `requires review`. Workflow cost: 147.323 seconds and 10 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: precise context pointers, progressive disclosure, positive steps, checkable completion, and local authoring/provenance rules.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: `2026-11-10-claude-claude-opus-5-5-activation-1-evalfirst/comparison.json` (local only, not committed).

## Treatment evidence

- Raw JSON trace: `2026-11-10-claude-claude-opus-5-5-activation-1-evalfirst/treatment/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-10-claude-claude-opus-5-5-activation-1-evalfirst/treatment/stderr.txt` (local only, not committed)
- Observed response: `2026-11-10-claude-claude-opus-5-5-activation-1-evalfirst/treatment/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-10-claude-claude-opus-5-5-activation-1-evalfirst/treatment/manifest.json` (local only, not committed)
- Artifacts: `2026-11-10-claude-claude-opus-5-5-activation-1-evalfirst/treatment/artifacts/`.

## Baseline evidence

- Raw JSON trace: `2026-11-10-claude-claude-opus-5-5-activation-1-evalfirst/baseline/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-10-claude-claude-opus-5-5-activation-1-evalfirst/baseline/stderr.txt` (local only, not committed)
- Observed response: `2026-11-10-claude-claude-opus-5-5-activation-1-evalfirst/baseline/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-10-claude-claude-opus-5-5-activation-1-evalfirst/baseline/manifest.json` (local only, not committed)
- Artifacts: `2026-11-10-claude-claude-opus-5-5-activation-1-evalfirst/baseline/artifacts/`.
