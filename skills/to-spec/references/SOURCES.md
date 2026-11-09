# Sources

Hashes cover the exact pinned bytes before adaptation. Each row maps one retained source file to its receiving local files.

| source | source_url | source_path | source_revision | sha256 | license | copyright_holders | destination_paths | kept_material | local_changes | license_files | notice_files |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| mattpocock | https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/to-spec/SKILL.md | skills/engineering/to-spec/SKILL.md | 49dd158d1076134a641b33efb035946536778336 | 43ad9cf318e5e7d3d1fa360253a37021796dc87a0c2e595ad262661a10f85088 | MIT | 2026 Matt Pocock | SKILL.md; references/spec-template.md | No-interview synthesis, glossary and ADR use, highest-seam testing rule, the spec template sections, the no-paths rule with the prototype-snippet exception, ready-for-agent label. | Setup outputs replace the setup command; per-story acceptance and real-surface proof; bound sources by SHA-256; domain pointers and open-questions sections; stable story numbers; filing within authority with connected tools first; template moved to a reference. | LICENSE-mattpocock | none |

## Reproduce the comparison

From a clone of each row's source repository, run `git show <source_revision>:<source_path> > upstream.md`, verify `shasum -a 256 upstream.md`, then run `diff -u upstream.md <skill-dir>/<destination_path>` for each destination. A hash mismatch blocks adoption. Expected local rewrites produce diff exit 1. Inspect the complete source and each destination for attribution completeness.

## Excluded files

Upstream host registrations and unused companions are not retained. Owned host policy is generated from the catalog.

Excluded `skills/engineering/to-spec/agents/openai.yaml` at `49dd158d1076134a641b33efb035946536778336`, SHA-256 `1c5b4d1e3d8e52287ef19cc2742fdbbfae1914ac75d33af3e4c8174f08cc55bb`: Host settings file; owned host policy is generated from the catalog `invocation` value instead.
