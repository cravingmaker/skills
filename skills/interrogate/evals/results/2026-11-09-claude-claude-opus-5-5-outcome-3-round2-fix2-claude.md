# interrogate: claude outcome-3

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `outcome-3` in `evals/examples.md`.
- **Skill revision.** Commit `d52ba17daf681100875cf0fb3813c2f329c1652e`, tree `0081bf09a0026d92425cd3411cd4f11590c1e7ee`, actual bytes SHA-256 `79eaf31d8a5ea0aa326a2701a5142991eea5f5cea45e815469bc0d4380d7eead`; dirty: `True`.
- **Fixture.** `outcome-3`, SHA-256 `141c63247aff4069f96361a700f9753ccb4ffbbea2a1070f6a2f57fddc0e6deb`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [interrogate.tar.gz](https://drive.google.com/file/d/1BPxC0RceYPCX2iHpSX6OTHCxOvrttbO3/view), folder `2026-11-09-claude-claude-opus-5-5-outcome-3-round2-fix2-claude/` inside.

## Prompt

```text
/interrogate Interrogate with a missing provider and an exhausted start allowance.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | n/a | true | 9 | 0 |
| baseline | n/a | false | 9 | 0 |

Treatment: 41 response lines; changed files `.cache/npm/_logs/2026-11-09T14_52_58_416Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 85.224 seconds and 9 tool calls; token usage is in the JSON record.

Baseline: 37 response lines; changed files `.cache/npm/_logs/2026-11-09T14_54_23_507Z-debug-0.log, tests/__pycache__/test_smoke.cpython-315.pyc`; removed files `none`; validation command present: `requires review`. Workflow cost: 78.28 seconds and 9 tool calls; token usage is in the JSON record.


Expected deliverable: "Interrogate with a missing provider and an exhausted start allowance." Expect: report the missing seat and unresolved coverage; no substitute or nested extra reviewer.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: `2026-11-09-claude-claude-opus-5-5-outcome-3-round2-fix2-claude/comparison.json` (local only, not committed).

## Treatment evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-outcome-3-round2-fix2-claude/treatment/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-outcome-3-round2-fix2-claude/treatment/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-outcome-3-round2-fix2-claude/treatment/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-outcome-3-round2-fix2-claude/treatment/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-3-round2-fix2-claude/treatment/artifacts/`.

## Baseline evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-outcome-3-round2-fix2-claude/baseline/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-outcome-3-round2-fix2-claude/baseline/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-outcome-3-round2-fix2-claude/baseline/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-outcome-3-round2-fix2-claude/baseline/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-3-round2-fix2-claude/baseline/artifacts/`.

Activation is not graded for Outcome examples; review the stated behavioral criterion.

## Round 2 review

Baseline: yes. Treatment: yes. Value: matched.

Treatment respects the exhausted human allowance, starts no provider/probe, preserves deterministic static findings and labels runtime/native claims unresolved. Baseline performs an inline probe review without new reviewers; neither changes product files or invents provider participation.
