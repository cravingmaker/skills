# Sources

Hashes cover the exact pinned bytes before adaptation. Each row maps one retained source file to its receiving local files.

| source | source_url | source_path | source_revision | sha256 | license | copyright_holders | destination_paths | kept_material | local_changes | license_files | notice_files |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| mattpocock | https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/wayfinder/SKILL.md | skills/engineering/wayfinder/SKILL.md | 49dd158d1076134a641b33efb035946536778336 | 9be7b478c389605a24517d27752f278933588da97a1b5921b165f455edf4c5b7 | MIT | 2026 Matt Pocock | SKILL.md; references/map-format.md | Destination, plan-don't-do, refer by name, map as index, ticket types with HITL and AFK, claiming, blocking, frontier, fog of war, out of scope, chart and work modes, one ticket per session. | Configured tracker and its wayfinding operations win, local files by default until publishing is authorized; no 100K-token size, compulsory parallel research, research branches or pushes, or scheduling; reuse of settled decisions; budgeted research subagents; local layout and formats moved to a reference. | LICENSE-mattpocock | none |

## Reproduce the comparison

From a clone of each row's source repository, run `git show <source_revision>:<source_path> > upstream.md`, verify `shasum -a 256 upstream.md`, then run `diff -u upstream.md <skill-dir>/<destination_path>` for each destination. A hash mismatch blocks adoption. Expected local rewrites produce diff exit 1. Inspect the complete source and each destination for attribution completeness.

## Excluded files

Upstream host registrations and unused companions are not retained. Owned host policy is generated from the catalog.

Excluded `skills/engineering/wayfinder/agents/openai.yaml` at `49dd158d1076134a641b33efb035946536778336`, SHA-256 `88bc81a11a6d52ac67aeaa76b8b619e387020d47c5133a4dd4927fd15c4ad073`: Host settings file; owned host policy is generated from the catalog `invocation` value instead.
