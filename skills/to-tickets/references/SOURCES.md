# Sources

Hashes cover the exact pinned bytes before adaptation. Each row maps one retained source file to its receiving local files.

| source | source_url | source_path | source_revision | sha256 | license | copyright_holders | destination_paths | kept_material | local_changes | license_files | notice_files |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| mattpocock | https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/to-tickets/SKILL.md | skills/engineering/to-tickets/SKILL.md | 49dd158d1076134a641b33efb035946536778336 | 56ec23c5b2782785d4e65bff9e315b6d3aeb4ef977c174a219e99489fada1995 | MIT | 2026 Matt Pocock | SKILL.md; references/ticket-template.md | Tracer-bullet vertical slices, blocking edges and frontier, expand-contract for wide refactors, the breakdown review questions, local one-file-per-ticket and remote issue forms, parent left untouched. | Template gains Status, Proof, and a Blocked by list of ticket numbers or None that import-tickets.py parses; worked example imported by tests/to-tickets; public-consumer compatibility in contract tickets; stable numbering; filing within authority; no implementation or run plan. | LICENSE-mattpocock | none |

## Reproduce the comparison

From a clone of each row's source repository, run `git show <source_revision>:<source_path> > upstream.md`, verify `shasum -a 256 upstream.md`, then run `diff -u upstream.md <skill-dir>/<destination_path>` for each destination. A hash mismatch blocks adoption. Expected local rewrites produce diff exit 1. Inspect the complete source and each destination for attribution completeness.

## Excluded files

Upstream host registrations and unused companions are not retained. Owned host policy is generated from the catalog.

Excluded `skills/engineering/to-tickets/agents/openai.yaml` at `49dd158d1076134a641b33efb035946536778336`, SHA-256 `21bc6215fffcd7614e9f772bb1760e87cc5fc7dcc707e7d282bc9414267a6090`: Host settings file; owned host policy is generated from the catalog `invocation` value instead.
