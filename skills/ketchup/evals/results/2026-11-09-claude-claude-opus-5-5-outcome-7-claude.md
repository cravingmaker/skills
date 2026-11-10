# ketchup: claude outcome-7

Comparison: **invalid**. Host: `2.1.311 (Claude Code)`. Effective model: `claude-opus-5-5`.

## Inputs

- **Source example.** `outcome-7` in `evals/examples.md`.
- **Skill revision.** Commit `d78b9956da6f04ed515a45ace4278fed10425be6`, tree `3857041fad3d36252578c8c68143a95a2f550159`, actual bytes SHA-256 `8add78dd29059f38b0a06b88d3444b640b0080dcb7eba3aad9e9b87990969bb3`; dirty: `False`.
- **Fixture.** `outcome-7`, SHA-256 `775d45d5dd027ba1a3376cf19cbe82edb288241ada49584cfb12ad6d25080d39`.
- **Standing contract.** SHA-256 `b4ae56649eab02bf1dff5f69b0f382a17d972a93a7cd4354188b031862e5ba01`, identical in both arms.
- **Settings.** Requested model `claude-opus-5-5`; effort `high`; each arm has a new session and the same host settings.
- **Private raw evidence.** Owner-only Google Drive archive [ketchup.tar.gz](https://drive.google.com/file/d/1J_ap53vEN9if1shTpcE-Adf79FZ1ZqXt/view), folder `2026-11-09-claude-claude-opus-5-5-outcome-7-claude/` inside.

## Prompt

```text
/ketchup Catch me up since my last message. Authoritative current snapshot: no work changed, no live run exists and no choices remain. No older PR or product decision belongs to this window.

Supplied task context:
Answer from that complete supplied snapshot; no new work is requested.
```

## Expected and observed

| Arm | Activation expected | Activation observed | Tools | Completion |
| --- | --- | --- | --- | --- |
| treatment | n/a | unavailable | unavailable | not run |
| baseline | n/a | unavailable | unavailable | not run |


Expected deliverable: "No work changed and no choices remain." Expect: a short factual response without invented choices, diagrams, video, or new work.

Deliverable correctness and unnecessary workflow cost require review of each response and artifact. The JSON record separates these judgments from activation detection and records usage, elapsed time, response lines, and changed files.

## Isolation evidence

The first arm's sentinel was absent from the second arm: `True`. Restored file inodes are separate. Each arm's input manifest is checked again immediately before its model call.

Project candidate copies are excluded from both restored fixtures; only the treatment receives a candidate copy. The manifest lists every excluded project path and its hash. Dependencies are installed in both temporary homes.

Full configuration, input revisions, effective discovery inventory, and expectations: `2026-11-09-claude-claude-opus-5-5-outcome-7-claude/comparison.json` (local only, not committed).

## Invalid comparison

- Shared budget limit reached

## Treatment evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-outcome-7-claude/treatment/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-outcome-7-claude/treatment/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-outcome-7-claude/treatment/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-outcome-7-claude/treatment/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-7-claude/treatment/artifacts/`.

## Baseline evidence

- Raw JSON trace: `2026-11-09-claude-claude-opus-5-5-outcome-7-claude/baseline/trace.jsonl` (local only, not committed)
- Standard error: `2026-11-09-claude-claude-opus-5-5-outcome-7-claude/baseline/stderr.txt` (local only, not committed)
- Observed response: `2026-11-09-claude-claude-opus-5-5-outcome-7-claude/baseline/response.txt` (local only, not committed)
- Input and discovery manifest: `2026-11-09-claude-claude-opus-5-5-outcome-7-claude/baseline/manifest.json` (local only, not committed)
- Artifacts: `2026-11-09-claude-claude-opus-5-5-outcome-7-claude/baseline/artifacts/`.

Activation is not graded for Outcome examples; review the stated behavioral criterion.
