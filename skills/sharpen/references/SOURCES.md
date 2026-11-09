# Sources

Hashes cover the exact pinned bytes before adaptation. Each row maps one retained source file to its receiving local files.

| source | source_url | source_path | source_revision | sha256 | license | copyright_holders | destination_paths | kept_material | local_changes | license_files | notice_files |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| pstack | https://github.com/cursor/plugins/blob/6b0300214a09fd6029cfb7077043125758cd1fd2/pstack/skills/sharpen/SKILL.md | pstack/skills/sharpen/SKILL.md | 6b0300214a09fd6029cfb7077043125758cd1fd2 | 563dfc460c605d311e650726288e2f1cbd61eab817db178d6e7e29643e07e7a2 | MIT | Copyright (c) 2026 Lauren Tan | SKILL.md | Exact complete upstream body: four questions, prompt rewrite, and user-owned choices. | Spec frontmatter, owned description/invocation policy, provenance, names/links, licenses, and packaging only; no body wording change. | LICENSE-pstack | none |
| pstack-claude | https://github.com/michael-denyer/pstack-claude/blob/91ab921ab92d9ccfe503c93c3524410277f012e1/plugins/pstack/skills/sharpen/SKILL.md | plugins/pstack/skills/sharpen/SKILL.md | 91ab921ab92d9ccfe503c93c3524410277f012e1 | c804fef77be5157c6a47125e931ff0f914988316cad544607e837cd805d68f93 | MIT | Copyright (c) 2026 Lauren Tan; Copyright (c) 2026 Michael Denyer | SKILL.md | Exact complete upstream body: four questions, prompt rewrite, and user-owned choices. | Spec frontmatter, owned description/invocation policy, provenance, names/links, licenses, and packaging only; no body wording change. | LICENSE-pstack-claude | NOTICE.md; NOTICE-skills.md |

## Reproduce the comparison

From a clone of each row's source repository, run `git show <source_revision>:<source_path> > upstream.md`, verify `shasum -a 256 upstream.md`, then run `diff -u upstream.md <skill-dir>/<destination_path>` for each destination. A hash mismatch blocks adoption. Expected local rewrites produce diff exit 1. Inspect the complete source and each destination for attribution completeness.

The port license retains both Lauren Tan and Michael Denyer. Its intact notices include a local crosswalk; only the contributions in this table are retained.
