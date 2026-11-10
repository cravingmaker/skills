# change-review: claude near-miss-1

Comparison: **valid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `near-miss-1` in `evals/examples.md`.
- **Skill revision.** Commit `f5a0c4f4a80ea04590d4330e952921e81ac97bdd`, tree `c1c7128a2f77648fbe4e47956cb47ac96920c103`, actual bytes SHA-256 `538451b7e504af318d30aae86fa4e2b3abe060a052d48f624be6e3141ec84c9b`; dirty: `False`.
- **Fixture.** `near-miss-1`, SHA-256 `141c63247aff4069f96361a700f9753ccb4ffbbea2a1070f6a2f57fddc0e6deb`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [change-review.tar.gz](https://drive.google.com/file/d/1sdBw3Um325sqJCn796LC4-ImJb2QYHus/view), folder `2026-11-09-claude-claude-opus-5-5-near-miss-1-claude/` inside.

## Prompt

```text
/code-review this PR using Claude Code's built-in command.

Task context supplied identically to both arms:
Explicitly selected Claude built-in is unavailable in this Codex host. Preserve the requested route; do not substitute a skill.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | false | false | 0 | 0 |
| baseline | false | false | 0 | 0 |

Treatment: 13 response lines; changed files `.cache/npm/_logs/2026-11-09T05_49_32_064Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 14.758 seconds and 0 tool calls; token usage is in the JSON record.

Baseline: 11 response lines; changed files `.cache/npm/_logs/2026-11-09T05_50_34_520Z-debug-0.log`; removed files `none`; validation command present: `requires review`. Workflow cost: 15.569 seconds and 0 tool calls; token usage is in the JSON record.


Expected deliverable: Expect: the explicitly selected host built-in keeps its route; change-review is not substituted.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: `2026-11-09-claude-claude-opus-5-5-near-miss-1-claude/comparison.json` (local only, not committed).

## Treatment evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-near-miss-1-claude/treatment/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-near-miss-1-claude/treatment/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-near-miss-1-claude/treatment/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-near-miss-1-claude/treatment/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-near-miss-1-claude/treatment/artifacts/`.

## Baseline evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-near-miss-1-claude/baseline/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-near-miss-1-claude/baseline/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-near-miss-1-claude/baseline/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-near-miss-1-claude/baseline/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-near-miss-1-claude/baseline/artifacts/`.
