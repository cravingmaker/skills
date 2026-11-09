# project-guardrails: claude outcome-3

Comparison: **invalid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `outcome-3` in `evals/examples.md`.
- **Skill revision.** Commit `d52ba17daf681100875cf0fb3813c2f329c1652e`, tree `775eed6134921ce92d47b739752069b284bb5324`, actual bytes SHA-256 `8f1ac48fdebf11b2ae8522f50d6ac083ef643a4ec39fe2d28d15c0f0af436f4d`; dirty: `True`.
- **Fixture.** `activation-1`, SHA-256 `c47fa158ee6fddfe21f52ab6a76d4f4d02b84ea50bd9b396ca2e6eb37778e362`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.

## Prompt

```text
Audit the current guardrails without changes. Report installed versions and their actual sources. No network or current upstream guidance is available; leave those guidance gaps open instead of guessing.

Disposable local fixture only. No network, installs, real apps, credentials, model starts, commits or remote writes. Keep probe state inside scratch/.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | n/a | unavailable | unavailable | 1 |
| baseline | n/a | unavailable | unavailable | not run |


Expected deliverable: The report lists versions with their sources, and any capability whose current guidance could not be confirmed is reported as open, not filled with a guess.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: [2026-11-09-claude-claude-opus-5-5-outcome-3-round2-fix1-claude/comparison.json](2026-11-09-claude-claude-opus-5-5-outcome-3-round2-fix1-claude/comparison.json).

## Invalid comparison

- claude treatment failed (exit 1, timeout False); inspect stderr and trace

## Treatment evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-3-round2-fix1-claude/treatment/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-3-round2-fix1-claude/treatment/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-3-round2-fix1-claude/treatment/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-3-round2-fix1-claude/treatment/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-3-round2-fix1-claude/treatment/artifacts/`.

## Baseline evidence

- [Raw JSON trace](2026-11-09-claude-claude-opus-5-5-outcome-3-round2-fix1-claude/baseline/trace.jsonl)
- [Standard error](2026-11-09-claude-claude-opus-5-5-outcome-3-round2-fix1-claude/baseline/stderr.txt)
- [Observed response](2026-11-09-claude-claude-opus-5-5-outcome-3-round2-fix1-claude/baseline/response.txt)
- [Input and discovery manifest](2026-11-09-claude-claude-opus-5-5-outcome-3-round2-fix1-claude/baseline/manifest.json)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-3-round2-fix1-claude/baseline/artifacts/`.

Activation is not graded for Outcome examples; review the stated behavioral criterion.
