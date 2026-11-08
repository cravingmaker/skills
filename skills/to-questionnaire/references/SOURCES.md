# Sources

Hashes cover the exact pinned bytes before adaptation. Each row maps one retained source file to its receiving local files.

| source | source_url | source_path | source_revision | sha256 | license | copyright_holders | destination_paths | kept_material | local_changes | license_files | notice_files |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| mattpocock | https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/productivity/to-questionnaire/SKILL.md | skills/productivity/to-questionnaire/SKILL.md | 49dd158d1076134a641b33efb035946536778336 | b5eb929842ee0e93d867c5e906d183d350f2f2d149eaeaa86967d94d8eda1d3b | MIT | 2026 Matt Pocock | SKILL.md | Ask about the send, not the subject; recipient and needs; gap-targeted questions; the discovery-questionnaire template and question rules; local file output. | Supplied recipient, purpose, needs, and known facts are reused; only missing items are asked, in one message; the draft is never sent or published. | LICENSE-mattpocock | none |

## Reproduce the comparison

From a clone of each row's source repository, run `git show <source_revision>:<source_path> > upstream.md`, verify `shasum -a 256 upstream.md`, then run `diff -u upstream.md <skill-dir>/<destination_path>` for each destination. A hash mismatch blocks adoption. Expected local rewrites produce diff exit 1. Inspect the complete source and each destination for attribution completeness.

## Excluded files

Upstream host registrations and unused companions are not retained. Owned host policy is generated from the catalog.

Excluded `skills/productivity/to-questionnaire/agents/openai.yaml` at `49dd158d1076134a641b33efb035946536778336`, SHA-256 `9e8a06c38c8842eea8d4922cb9d1ead8e3ace647bab259b943c994a1b4742bc2`: Host settings file; owned host policy is generated from the catalog `invocation` value instead.
