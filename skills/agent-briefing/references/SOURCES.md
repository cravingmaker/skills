# Sources

Hashes identify exact pinned source bytes before adaptation; the owned run record and budget replace upstream controllers.

| source | source_url | source_path | source_revision | sha256 | license | copyright_holders | destination_paths | kept_material | local_changes | license_files | notice_files |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| pstack | https://github.com/cursor/plugins/blob/6b0300214a09fd6029cfb7077043125758cd1fd2/pstack/skills/principle-guard-the-context-window/SKILL.md | pstack/skills/principle-guard-the-context-window/SKILL.md | 6b0300214a09fd6029cfb7077043125758cd1fd2 | af0b9dd70b43628ce4a59a4d332e9d9ad055084e460f430e7a757495c627e81a | MIT | Copyright (c) 2026 Lauren Tan | SKILL.md; assets/brief.md | Useful scoped pointers and selective reads; no automatic delegation merely to save context. | Useful scoped pointers and selective reads; no automatic delegation merely to save context. Apply the owning skill adaptation and shared rules in final plan §3. | LICENSE-pstack | none |
| pstack-claude | https://github.com/michael-denyer/pstack-claude/blob/91ab921ab92d9ccfe503c93c3524410277f012e1/plugins/pstack/skills/principle-guard-the-context-window/SKILL.md | plugins/pstack/skills/principle-guard-the-context-window/SKILL.md | 91ab921ab92d9ccfe503c93c3524410277f012e1 | 6db84b7d5e67fb4e2e6a260605f2c2e34fbeaa1bc0e49645eef6f00a17543778 | MIT | Copyright (c) 2026 Lauren Tan; Copyright (c) 2026 Michael Denyer | SKILL.md; assets/brief.md | Useful scoped pointers and selective reads; no automatic delegation merely to save context. | Useful scoped pointers and selective reads; no automatic delegation merely to save context. Apply the owning skill adaptation and shared rules in final plan §3. | LICENSE-pstack-claude | NOTICE.md; NOTICE-skills.md |

## Reproduce the comparison

From each source repository, run `git show <source_revision>:<source_path> > upstream.md`, verify `shasum -a 256 upstream.md`, then run `diff -u upstream.md <skill-dir>/<destination_path>` for every destination. A mismatch in the source hash blocks adoption; expected adaptation diffs exit 1. Review the full legal payload and contribution coverage.
