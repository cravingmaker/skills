# Sources

Hashes cover the exact pinned bytes before adaptation. Each row maps one retained source file to its receiving local files.

| source | source_url | source_path | source_revision | sha256 | license | copyright_holders | destination_paths | kept_material | local_changes | license_files | notice_files |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| mattpocock | https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/productivity/grilling/SKILL.md | skills/productivity/grilling/SKILL.md | 49dd158d1076134a641b33efb035946536778336 | befdff1e27a1dfe2a294d5871169ac1afe16d983911daa4f32627514a48c1e15 | MIT | 2026 Matt Pocock | SKILL.md | Design tree, frontier rounds, numbered questions with recommended answers, yes-accepts wording, fact finding before asking, wait for confirmation. | Look before asking and reuse settled answers; ask only consequential choices; sub-agent lookups optional and budgeted; checkable close and stop rule; no-doc default mode; resume instead of repeat interviews; failure-mode checks. | LICENSE-mattpocock | none |

## Reproduce the comparison

From a clone of each row's source repository, run `git show <source_revision>:<source_path> > upstream.md`, verify `shasum -a 256 upstream.md`, then run `diff -u upstream.md <skill-dir>/<destination_path>` for each destination. A hash mismatch blocks adoption. Expected local rewrites produce diff exit 1. Inspect the complete source and each destination for attribution completeness.

## Excluded files

Upstream host registrations and unused companions are not retained. Owned host policy is generated from the catalog.

Excluded `skills/productivity/grilling/agents/openai.yaml` at `49dd158d1076134a641b33efb035946536778336`, SHA-256 `1411d7df7d99b7e621a1ff8283c8133cc2464be63d064e52d8ce169c6800ee9b`: Host settings file; owned host policy is generated from the catalog `invocation` value instead.
