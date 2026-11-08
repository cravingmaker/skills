# Sources

Hashes cover the exact pinned bytes before adaptation. Each row maps one retained source file to its receiving local files.

| source | source_url | source_path | source_revision | sha256 | license | copyright_holders | destination_paths | kept_material | local_changes | license_files | notice_files |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| mattpocock | https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/productivity/grill-me/SKILL.md | skills/productivity/grill-me/SKILL.md | 49dd158d1076134a641b33efb035946536778336 | caaf8b8de1684f96e26b28f3c29189db5c89cce4b73e1c93d86164f66ef88637 | MIT | 2026 Matt Pocock | SKILL.md | The manual entry name and its job: a relentless interview to sharpen a plan. | Skill-tool call replaced by reading the owned grilling skill in no-doc mode; dispatch, quoted-text, and authority boundary added; manual-only moved to the catalog. | LICENSE-mattpocock | none |

## Reproduce the comparison

From a clone of each row's source repository, run `git show <source_revision>:<source_path> > upstream.md`, verify `shasum -a 256 upstream.md`, then run `diff -u upstream.md <skill-dir>/<destination_path>` for each destination. A hash mismatch blocks adoption. Expected local rewrites produce diff exit 1. Inspect the complete source and each destination for attribution completeness.

## Excluded files

Upstream host registrations and unused companions are not retained. Owned host policy is generated from the catalog.

Excluded `skills/productivity/grill-me/agents/openai.yaml` at `49dd158d1076134a641b33efb035946536778336`, SHA-256 `c061e39c3e0f9d865fb1b97556d485704af2a8a58f4b8221a8917a5c2074a32b`: Host settings file; owned host policy is generated from the catalog `invocation` value instead.
