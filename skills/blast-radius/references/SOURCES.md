# Sources

One row per retained upstream file. Hashes cover the original bytes before adaptation.

| source | source_url | source_path | source_revision | sha256 | license | copyright_holders | destination_paths | kept_material | local_changes | license_files | notice_files |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| pstack | https://github.com/cursor/plugins/blob/6b0300214a09fd6029cfb7077043125758cd1fd2/pstack/skills/blast-radius/SKILL.md | pstack/skills/blast-radius/SKILL.md | 6b0300214a09fd6029cfb7077043125758cd1fd2 | 2e10745b97f5862323dcda3b29ca60d56b5c3c98e37020085d26b48efbe0a436 | MIT | Copyright (c) 2026 Lauren Tan | SKILL.md | Trace consumers and contracts a proposed change can affect. | Keep key safety facts, real downstream consumers and proof ladder; distinguish static, executed and observed evidence, preserve public/data contracts and make helper methods conditional. | LICENSE-pstack | none |
| pstack-claude | https://github.com/michael-denyer/pstack-claude/blob/91ab921ab92d9ccfe503c93c3524410277f012e1/plugins/pstack/skills/blast-radius/SKILL.md | plugins/pstack/skills/blast-radius/SKILL.md | 91ab921ab92d9ccfe503c93c3524410277f012e1 | 03f44dbf518c0b87b19b70c57af40cf74dd70fb5affa6550ab508751325760c0 | MIT | Copyright (c) 2026 Lauren Tan; Copyright (c) 2026 Michael Denyer | SKILL.md | Trace consumers and contracts a proposed change can affect. | Keep key safety facts, real downstream consumers and proof ladder; distinguish static, executed and observed evidence, preserve public/data contracts and make helper methods conditional. | LICENSE-pstack-claude | NOTICE.md; NOTICE-skills.md |
| pstack | https://github.com/cursor/plugins/blob/6b0300214a09fd6029cfb7077043125758cd1fd2/pstack/LICENSE | pstack/LICENSE | 6b0300214a09fd6029cfb7077043125758cd1fd2 | bc957ca6bee02792566a1a028d105e02e247c6e77cf057061674273da77b200e | MIT | Copyright (c) 2026 Lauren Tan | LICENSE-pstack | Complete original legal text. | Retained intact; license header identifies modified local files; original notices use the local crosswalk in SOURCES.md. | LICENSE-pstack | none |
| pstack-claude | https://github.com/michael-denyer/pstack-claude/blob/91ab921ab92d9ccfe503c93c3524410277f012e1/LICENSE | LICENSE | 91ab921ab92d9ccfe503c93c3524410277f012e1 | 5b1faca8cef6b7433b49c812c5e9e04bb1eb73b67171d67729983e0b46b9bb78 | MIT | Copyright (c) 2026 Lauren Tan; Copyright (c) 2026 Michael Denyer | LICENSE-pstack-claude | Complete original legal text. | Retained intact; license header identifies modified local files; original notices use the local crosswalk in SOURCES.md. | LICENSE-pstack-claude | NOTICE.md; NOTICE-skills.md |
| pstack-claude | https://github.com/michael-denyer/pstack-claude/blob/91ab921ab92d9ccfe503c93c3524410277f012e1/NOTICE.md | NOTICE.md | 91ab921ab92d9ccfe503c93c3524410277f012e1 | af48c0a58e4872de2369081e11c4faadb0cdf3090f6fc23499cb86c092730c12 | MIT | Copyright (c) 2026 Lauren Tan; Copyright (c) 2026 Michael Denyer | NOTICE.md | Complete original legal text. | Retained intact; license header identifies modified local files; original notices use the local crosswalk in SOURCES.md. | LICENSE-pstack-claude | NOTICE.md; NOTICE-skills.md |
| pstack-claude | https://github.com/michael-denyer/pstack-claude/blob/91ab921ab92d9ccfe503c93c3524410277f012e1/NOTICE-skills.md | NOTICE-skills.md | 91ab921ab92d9ccfe503c93c3524410277f012e1 | 232a21a3bf88991185e6837270cba41cd83646c3998f91942c823fecc4440b4d | MIT | Copyright (c) 2026 Lauren Tan; Copyright (c) 2026 Michael Denyer | NOTICE-skills.md | Complete original legal text. | Retained intact; license header identifies modified local files; original notices use the local crosswalk in SOURCES.md. | LICENSE-pstack-claude | NOTICE.md; NOTICE-skills.md |

## Reproduce the comparison

For each row, resolve its pinned source checkout and export the exact input, verify its table hash, then compare each receiving path:

```sh
git -C <upstream-checkout> show <source_revision>:<source_path> > upstream.md
shasum -a 256 upstream.md
diff -u upstream.md <skill-dir>/<destination_path>
```

The hash must equal sha256 in that row. Repeat the diff for every destination_paths entry; exit 1 records expected adaptation differences. Complete legal texts and applicable notices remain intact. Source review establishes attribution completeness.

## Original-notice crosswalk

NOTICE.md and NOTICE-skills.md are intact originals from the pinned port. Their relative paths and broader component lists describe that upstream distribution, not additional bundled packages here. Upstream-relative links resolve against the pinned source tree recorded in the table. The applicable local legal mapping is LICENSE to LICENSE-pstack-claude; base pstack material additionally retains LICENSE-pstack where contributed. Unrelated cursor-team-kit components, controller scripts, model sheets, hooks and platform mappings are not included.

Only the pstack-derived contributions listed in this manifest are used in this package. The original notices also describe thermos and cursor-team-kit contributions elsewhere upstream; no such behavioral material or agent package is included here.
