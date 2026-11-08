# Sources

One row per retained input, with exact pre-adaptation hashes and receiving files. All contributions remain unevaluated.

| source | source_url | source_path | source_revision | sha256 | license | copyright_holders | destination_paths | kept_material | local_changes | license_files | notice_files |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| pstack | https://github.com/cursor/plugins/blob/6b0300214a09fd6029cfb7077043125758cd1fd2/pstack/skills/ketchup/SKILL.md | pstack/skills/ketchup/SKILL.md | 6b0300214a09fd6029cfb7077043125758cd1fd2 | f2923ffd14f6fc778f75a47aaed1f317fb5fd00b5701ca769d6446c74106dead | MIT | Copyright (c) 2026 Lauren Tan | SKILL.md | Since-last-human read-only catch-up, live status and every pending user choice | Use owned communication; current revision and unresolved older feedback; no quotas, app/job startup, watcher or video requirement. | LICENSE-pstack | none |
| pstack-claude | https://github.com/michael-denyer/pstack-claude/blob/91ab921ab92d9ccfe503c93c3524410277f012e1/plugins/pstack/skills/ketchup/SKILL.md | plugins/pstack/skills/ketchup/SKILL.md | 91ab921ab92d9ccfe503c93c3524410277f012e1 | 65e08d735b3e34eb6114e5b8fc99f825fcf06c0c644651497f15685db61e4eaa | MIT | Copyright (c) 2026 Lauren Tan; Copyright (c) 2026 Michael Denyer | SKILL.md | Since-last-human read-only catch-up, live status and every pending user choice | Use owned communication; current revision and unresolved older feedback; no quotas, app/job startup, watcher or video requirement. | LICENSE-pstack-claude | NOTICE.md; NOTICE-skills.md |
| pstack-claude | https://github.com/michael-denyer/pstack-claude/blob/91ab921ab92d9ccfe503c93c3524410277f012e1/plugins/pstack/skills/what-did-i-get-done/SKILL.md | plugins/pstack/skills/what-did-i-get-done/SKILL.md | 91ab921ab92d9ccfe503c93c3524410277f012e1 | 479813c9abaacb5b6b0531f1de7dc5eb2f3bd9673707a992d1073335836e82f8 | MIT | Copyright (c) 2026 Lauren Tan; Copyright (c) 2026 Michael Denyer; Copyright (c) 2026 Cursor | SKILL.md | Explicit date-window authored activity, concrete range and functional change summary | Wider-window mode only; check delivery separately from commits; retain reversions and label pending work; no universal standup trigger. | LICENSE-pstack-claude; LICENSE-cursor-team-kit | NOTICE.md; NOTICE-skills.md |

## Legal crosswalk and review

Every contributing collection's complete license is retained at the skill root with a header naming the adapted files. Exact revisions, licenses, holders, and notices are recorded per file in the manifest.

The port's root and skills-only notices are retained intact with a local header. Their original LICENSE reference maps to LICENSE-pstack-claude, which preserves both Lauren Tan and Michael Denyer; the base source has LICENSE-pstack. Historical notice links resolve in the pinned port tree. Unselected components mentioned there are not included here.
The what-did-i-get-done contribution additionally carries LICENSE-cursor-team-kit and its Cursor credit, as the port's notice requires. Its original source revision is e46364b8be46000b7df0f260550cd712afbb8d36; the exact retained file bytes are bound to the port revision in the manifest.

## Reproduce the comparison

From a clone of each row's source repository, run `git show <source_revision>:<source_path> > upstream.md`, verify `shasum -a 256 upstream.md`, then run `diff -u upstream.md <skill-dir>/<destination_path>` for every destination. A hash mismatch blocks adoption. Expected local adaptations produce diff exit 1; read the full input and each receiving file to review attribution.
