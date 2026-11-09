# Sources

Per-file provenance for the full-stop skill. Each row is one upstream file this skill retains material from, pinned to a full commit, with the byte hash before adaptation. Reproduce a destination diff by fetching the pinned URL and comparing it with the listed local files.

| source | source_url | source_path | source_revision | sha256 | license | copyright_holders | destination_paths | kept_material | local_changes | license_files | notice_files |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| tstack | https://github.com/t3dotgg/tstack/blob/1085050f3baed1ac724caa4a8166145fb2ac88af/skills/full-stop/SKILL.md | skills/full-stop/SKILL.md | 1085050f3baed1ac724caa4a8166145fb2ac88af | 091dcabfcba73e009ddb8e32c498a993a6bb60f8c223d3e21e917f4e52ab9939 | MIT | 2026 Theo Browne | SKILL.md | Explicit entry that does full-send's work and stops with the PR ready; testing permission without a separate full-send request; no merging, auto-merge, queue, default-branch push, protection bypass or delegation of those; disable pending mechanisms; stop at the gate with ready, waiting or blocked; unwatch and report open and unmerged. | Reduced to a thin dispatch into full-send's shared prepare-only mode, which now holds the procedure; incidental, emphatic or quoted "full stop" selects nothing; narrower user constraints still win; shared delivery contract added. | LICENSE-tstack | none |

## Legal files

Each license or notice below is the upstream text, copied unchanged after a header that names the adapted local files.

| Local file | Upstream file | Revision | sha256 |
|---|---|---|---|
| LICENSE-tstack | https://github.com/t3dotgg/tstack/blob/1085050f3baed1ac724caa4a8166145fb2ac88af/LICENSE | 1085050f3baed1ac724caa4a8166145fb2ac88af | 8095f9a9f97d074131f6a2ce09b952d12c18b36f09f4e5df0517c4e64e82c851 |

## Not copied

- tstack `skills/full-stop/agents/openai.yaml`: skipped by plan; host policy is generated from the catalog `invocation` value.

## Reproduce the comparison

From a clone of each row's source repository, run `git show <source_revision>:<source_path> > upstream.md`, verify `shasum -a 256 upstream.md`, then run `diff -u upstream.md <skill-dir>/<destination_path>` for every destination. A hash mismatch blocks adoption. Expected local adaptations produce diff exit 1; read the full input and each receiving file to review attribution.
