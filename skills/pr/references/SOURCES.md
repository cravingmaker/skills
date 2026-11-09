# Sources

Per-file provenance for the pr skill. Each row is one upstream file this skill retains material from, pinned to a full commit, with the byte hash before adaptation. Reproduce a destination diff by fetching the pinned URL and comparing it with the listed local files.

| source | source_url | source_path | source_revision | sha256 | license | copyright_holders | destination_paths | kept_material | local_changes | license_files | notice_files |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| mattpocock | https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/pr/SKILL.md | skills/engineering/pr/SKILL.md | 49dd158d1076134a641b33efb035946536778336 | ab63f1cf78647389edcd386c9427c5dfca27ed2836930c24773ffee834c19bcd | MIT | 2026 Matt Pocock | SKILL.md | The body-writing trigger ("use when writing a PR body") as a manual entry. | Reduced to dispatch into the file-pr skill's body-only mode; the template, evidence, merge-danger and visual guidance live in file-pr; filing only when requested or already authorized; no push, watch or merge authority; delivery contract added. | LICENSE-mattpocock | none |

## Legal files

Each license or notice below is the upstream text, copied unchanged after a header that names the adapted local files.

| Local file | Upstream file | Revision | sha256 |
|---|---|---|---|
| LICENSE-mattpocock | https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/LICENSE | 49dd158d1076134a641b33efb035946536778336 | 0e7ac423bf2c6e223b7c5b156f8cf72da49d748e56a1641402c31f22ad07dbb5 |

## Not copied

- mattpocock `skills/engineering/pr/agents/openai.yaml`: not copied; host policy is generated from the catalog `invocation` value.
- mattpocock `skills/engineering/pr/CREDITS.md` (sha256 a7a087127665d7298a72280ef6e19c41ad8404523712a788c8dc3ab414bc2497): read in full; it credits the HumanLayer visuals, which this entry does not keep. The file-pr skill carries that credit chain and LICENSE-humanlayer.

## Reproduce the comparison

From a clone of each row's source repository, run `git show <source_revision>:<source_path> > upstream.md`, verify `shasum -a 256 upstream.md`, then run `diff -u upstream.md <skill-dir>/<destination_path>` for every destination. A hash mismatch blocks adoption. Expected local adaptations produce diff exit 1; read the full input and each receiving file to review attribution.
