# council: claude outcome-4

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `outcome-4` in `evals/examples.md`.
- **Skill revision.** Commit `f5a0c4f4a80ea04590d4330e952921e81ac97bdd`, tree `645edc1b3f8b5c5c00854bc61d0d6fc29130ffbc`, actual bytes SHA-256 `b24055566d7c79f421cbb22a5ec0337e4290b06d7d90fb76b6c3191c0957771d`; dirty: `False`.
- **Fixture.** `outcome-4`, SHA-256 `c6a4f6092a051f8dcda2bda3debfd28763fe8dc66a92e944630fb3195124812f`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
/council Council read-only: discuss this non-code policy.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | n/a | true | 6 | 0 |
| baseline | n/a | false | 3 | 0 |

Treatment: 16 response lines; changed files `.cache/npm/_logs/2026-11-09T05_00_33_745Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 25.402 seconds and 6 tool calls; token usage is in the JSON record.

Baseline: 7 response lines; changed files `.cache/npm/_logs/2026-11-09T05_02_01_764Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 18.343 seconds and 3 tool calls; token usage is in the JSON record.


Expected deliverable: "Council read-only: discuss this non-code policy." Expect: report-only agent-debate panel, no document publication or code loop.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-outcome-4-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-outcome-4-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-4-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-4-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-4-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-4-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-4-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-4-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-4-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-4-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-4-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-4-claude/baseline/artifacts/`.

Activation is not graded for Outcome examples; review the stated behavioral criterion.

## Outcome review

Value: **matched**. Baseline criterion: partial; treatment criterion: partial.

Both select a report-only non-code route and ask for the absent policy. No product/doc publication or code loop occurs. Real panel execution is blocked by the no-delegation fixture.
