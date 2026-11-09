# Sources

Hashes cover the exact pinned bytes before adaptation. Each row maps one retained source file to its receiving local files.

| source | source_url | source_path | source_revision | sha256 | license | copyright_holders | destination_paths | kept_material | local_changes | license_files | notice_files |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| mattpocock | https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/productivity/wait-what/SKILL.md | skills/productivity/wait-what/SKILL.md | 49dd158d1076134a641b33efb035946536778336 | d961bb37defd975c539427edb8f450cdbccdcdd552e213c1ece46676a7970905 | MIT | Copyright (c) 2026 Matt Pocock | SKILL.md | Explicit manual repair signal, delegated to the owned clear-communication parent. | Thin entry only; the parent owns repair and contextual explanation. Preserve original authority; incidental or quoted text selects nothing. | LICENSE-mattpocock | none |

## Reproduce the comparison

From a clone of each row's source repository, run `git show <source_revision>:<source_path> > upstream.md`, verify `shasum -a 256 upstream.md`, then run `diff -u upstream.md <skill-dir>/<destination_path>` for each destination. A hash mismatch blocks adoption. Expected local rewrites produce diff exit 1. Inspect the complete source and each destination for attribution completeness.
