# Sources

Hashes cover the exact pinned bytes before adaptation. Each row maps one retained source file to its receiving local files.

| source | source_url | source_path | source_revision | sha256 | license | copyright_holders | destination_paths | kept_material | local_changes | license_files | notice_files |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| pstack | https://github.com/cursor/plugins/blob/6b0300214a09fd6029cfb7077043125758cd1fd2/pstack/skills/bro/SKILL.md | pstack/skills/bro/SKILL.md | 6b0300214a09fd6029cfb7077043125758cd1fd2 | aa329d0ceeeecb6822a7174ad76bb07a7826a3c52ceb6a588dec4138815084bb | MIT | Copyright (c) 2026 Lauren Tan | SKILL.md | Explicit manual repair signal, delegated to the owned clear-communication parent. | Thin entry only; the parent owns repair and contextual explanation. Preserve original authority; incidental or quoted text selects nothing. | LICENSE-pstack | none |
| pstack-claude | https://github.com/michael-denyer/pstack-claude/blob/91ab921ab92d9ccfe503c93c3524410277f012e1/plugins/pstack/skills/bro/SKILL.md | plugins/pstack/skills/bro/SKILL.md | 91ab921ab92d9ccfe503c93c3524410277f012e1 | 18acb10aae040eb78058cb07f2f1e0ae607886b64c692082fc804cc6ce86f469 | MIT | Copyright (c) 2026 Lauren Tan; Copyright (c) 2026 Michael Denyer | SKILL.md | Explicit manual repair signal, delegated to the owned clear-communication parent. | Thin entry only; the parent owns repair and contextual explanation. Preserve original authority; incidental or quoted text selects nothing. | LICENSE-pstack-claude | NOTICE.md; NOTICE-skills.md |

## Reproduce the comparison

From a clone of each row's source repository, run `git show <source_revision>:<source_path> > upstream.md`, verify `shasum -a 256 upstream.md`, then run `diff -u upstream.md <skill-dir>/<destination_path>` for each destination. A hash mismatch blocks adoption. Expected local rewrites produce diff exit 1. Inspect the complete source and each destination for attribution completeness.

The port license retains both Lauren Tan and Michael Denyer. Its intact notices include a local crosswalk; only the contributions in this table are retained.
