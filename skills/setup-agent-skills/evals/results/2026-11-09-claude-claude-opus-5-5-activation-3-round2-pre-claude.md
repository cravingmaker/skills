# setup-agent-skills: claude activation-3

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `activation-3` in `evals/examples.md`.
- **Skill revision.** Commit `d52ba17daf681100875cf0fb3813c2f329c1652e`, tree `b8e7b63f55acaa2b4f866ca1ae7a4d471bd0419d`, actual bytes SHA-256 `124ab76b9bbe51a2ae051c0c4680a13419b8c816e87e9fec1be9df5265bb766a`; dirty: `False`.
- **Fixture.** `activation-3`, SHA-256 `bc92cb991987ef51222c202cff0614e3bc82e11629dc8d8bceba9a40b09f4217`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
/setup-agent-skills

Use the `setup-agent-skills` skill explicitly for this request.

Re-run setup with exactly these settings.

Task context supplied to both arms:
The selected project instruction target is PROJECT-INSTRUCTIONS.md, an ordinary fixture substitute for the live host instruction file. Do not alter the harness AGENTS.md. Existing domain paths and GitLab identity are authoritative. No remote writes. This is the already configured fixture. Reapply identical settings and demonstrate content deltas, preserving custom prose.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | true | true | 9 | 0 |
| baseline | false | false | 5 | 0 |

Treatment: 35 response lines; changed files `.cache/npm/_logs/2026-11-09T11_21_00_050Z-debug-0.log, PROJECT-INSTRUCTIONS.md`; removed files `none`; validation command present: `requires review`. Workflow cost: 54.371 seconds and 9 tool calls; token usage is in the JSON record.

Baseline: 18 response lines; changed files `.cache/npm/_logs/2026-11-09T11_23_17_105Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 38.235 seconds and 5 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: on the already configured fixture the second run produces no file diff and preserves custom prose before, inside, and after the owned configuration.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-activation-3-round2-pre-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-activation-3-round2-pre-claude/comparison.json).

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-3-round2-pre-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-3-round2-pre-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-3-round2-pre-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-3-round2-pre-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-3-round2-pre-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-activation-3-round2-pre-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-activation-3-round2-pre-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-activation-3-round2-pre-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-activation-3-round2-pre-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-activation-3-round2-pre-claude/baseline/artifacts/`.
