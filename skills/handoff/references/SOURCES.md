# Sources

One row per retained input, with exact pre-adaptation hashes and receiving files. All contributions remain unevaluated.

| source | source_url | source_path | source_revision | sha256 | license | copyright_holders | destination_paths | kept_material | local_changes | license_files | notice_files |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| mattpocock | https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/in-progress/claude-handoff/SKILL.md | skills/in-progress/claude-handoff/SKILL.md | 49dd158d1076134a641b33efb035946536778336 | 79357a18425d66d4c24048bedf83dceb79d3bba356f38014950f764a7fab4026 | MIT | Copyright (c) 2026 Matt Pocock | SKILL.md; assets/handoff.md | OS-temporary continuation, focus, suggested skills, links and redaction | Merged both entries; added exact proof/ownership/budget; removed provider CLI launching. | LICENSE-mattpocock | none |
| mattpocock | https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/productivity/handoff/SKILL.md | skills/productivity/handoff/SKILL.md | 49dd158d1076134a641b33efb035946536778336 | 4cbb043950dad2ffd3662ff1a5a0b51ae676004b5cae10e3787e8ee7a4ee69d3 | MIT | Copyright (c) 2026 Matt Pocock | SKILL.md; assets/handoff.md | OS-temporary continuation, focus, suggested skills, links and redaction | Merged both entries; added exact proof/ownership/budget; removed provider CLI launching. | LICENSE-mattpocock | none |

## Legal crosswalk and review

Every contributing collection's complete license is retained at the skill root with a header naming the adapted files. Exact revisions, licenses, holders, and notices are recorded per file in the manifest.


## Reproduce the comparison

From a clone of each row's source repository, run `git show <source_revision>:<source_path> > upstream.md`, verify `shasum -a 256 upstream.md`, then run `diff -u upstream.md <skill-dir>/<destination_path>` for every destination. A hash mismatch blocks adoption. Expected local adaptations produce diff exit 1; read the full input and each receiving file to review attribution.
