# Sources

One row per retained upstream file. Hashes cover the original bytes before adaptation.

| source | source_url | source_path | source_revision | sha256 | license | copyright_holders | destination_paths | kept_material | local_changes | license_files | notice_files |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| tstack | https://github.com/t3dotgg/tstack/blob/1085050f3baed1ac724caa4a8166145fb2ac88af/skills/council/SKILL.md | skills/council/SKILL.md | 1085050f3baed1ac724caa4a8166145fb2ac88af | 598fb2c7cdd48ddd9643cb22999e1b624c357aa6579aa0af0e7268ae16a8a164 | MIT | Copyright (c) 2026 Theo Browne | SKILL.md | Requested typed entry and its dispatch/scope boundary; parent methods have one implementation. | Thin manual dispatcher: authorized code fixes to sol-loop, non-code/design to agent-debate, read-only to a report-only panel; keep distinct requested providers and budget without an unconditional fix loop. | LICENSE-tstack | none |
| tstack | https://github.com/t3dotgg/tstack/blob/1085050f3baed1ac724caa4a8166145fb2ac88af/LICENSE | LICENSE | 1085050f3baed1ac724caa4a8166145fb2ac88af | 8095f9a9f97d074131f6a2ce09b952d12c18b36f09f4e5df0517c4e64e82c851 | MIT | Copyright (c) 2026 Theo Browne | LICENSE-tstack | Complete original legal text. | Retained intact; license header identifies modified local files; original notices use the local crosswalk in SOURCES.md. | LICENSE-tstack | none |

## Reproduce the comparison

For each row, resolve its pinned source checkout and export the exact input, verify its table hash, then compare each receiving path:

```sh
git -C <upstream-checkout> show <source_revision>:<source_path> > upstream.md
shasum -a 256 upstream.md
diff -u upstream.md <skill-dir>/<destination_path>
```

The hash must equal sha256 in that row. Repeat the diff for every destination_paths entry; exit 1 records expected adaptation differences. Complete legal texts and applicable notices remain intact. Source review establishes attribution completeness.
