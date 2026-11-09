# Sources

One row per retained upstream file. Hashes cover the original bytes before adaptation.

| source | source_url | source_path | source_revision | sha256 | license | copyright_holders | destination_paths | kept_material | local_changes | license_files | notice_files |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| mattpocock | https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/wizard/SKILL.md | skills/engineering/wizard/SKILL.md | 49dd158d1076134a641b33efb035946536778336 | bdf31d48211ea559878f95a4f344aeabf8d85897488ba564382bab0b000daac1 | MIT | Copyright (c) 2026 Matt Pocock | SKILL.md | Wizard concept, four-step process, completion criteria, the template's bar, static tracing. | No-edit rule removed; loader discovery and ENV_FORMAT; existing setup tools first; dummy-value round trip through the project's loader; authority for commits and secret writes. | LICENSE-mattpocock | none |
| mattpocock | https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/wizard/template.sh | skills/engineering/wizard/template.sh | 49dd158d1076134a641b33efb035946536778336 | 6566f147299bc6f1d941e64591ed04385416d543e11f96f564c7228f5018d0ed | MIT | Copyright (c) 2026 Matt Pocock | assets/template.sh | Library UX: colours, banner, stages, open_url, pause, confirm, ask, ask_secret, set_secret, set_var, finish, run_wizard structure. | Shell-quoted dotenv writer and reader replaced by declared-format serialization that refuses unsupported values before writing; in-place upsert preserving other lines and multi-line values; destination, symlink and git-tracking checks; atomic replace; --help and --dry-run; Bash 3.2 replacement fix. | LICENSE-mattpocock | none |

## Reproduce the comparison

For each row, resolve its pinned source checkout and export the exact input, verify its table hash, then compare each receiving path:

```sh
git -C <upstream-checkout> show <source_revision>:<source_path> > upstream.md
shasum -a 256 upstream.md
diff -u upstream.md <skill-dir>/<destination_path>
```

The hash must equal sha256 in that row. Repeat the diff for every destination_paths entry; exit 1 records expected adaptation differences. Complete legal texts and applicable notices remain intact. Source review establishes attribution completeness.
