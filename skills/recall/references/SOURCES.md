# Sources

One row per retained input, with exact pre-adaptation hashes and receiving files. All contributions remain unevaluated.

| source | source_url | source_path | source_revision | sha256 | license | copyright_holders | destination_paths | kept_material | local_changes | license_files | notice_files |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| pstack | https://github.com/cursor/plugins/blob/6b0300214a09fd6029cfb7077043125758cd1fd2/pstack/skills/recall/SKILL.md | pstack/skills/recall/SKILL.md | 6b0300214a09fd6029cfb7077043125758cd1fd2 | b0ceb996259c3404532f61e4b010df4e3d80d7ddbed85b3c302895723eb62a89 | MIT | Copyright (c) 2026 Lauren Tan | SKILL.md | Scoped prior-run search, topic/identity confirmation, original decision pointers and relevant live state | Unknown locator only; supported host search then documented local records; bounded extracts; known-run reconciliation goes to decision-log; no transcript campaign. | LICENSE-pstack | none |
| pstack-claude | https://github.com/michael-denyer/pstack-claude/blob/91ab921ab92d9ccfe503c93c3524410277f012e1/plugins/pstack/skills/recall/SKILL.md | plugins/pstack/skills/recall/SKILL.md | 91ab921ab92d9ccfe503c93c3524410277f012e1 | 9167d7586de195542b6888b0e859d1d6d52d564afd658220926f1343cdef7c7b | MIT | Copyright (c) 2026 Lauren Tan; Copyright (c) 2026 Michael Denyer | SKILL.md | Scoped prior-run search, topic/identity confirmation, original decision pointers and relevant live state | Unknown locator only; supported host search then documented local records; bounded extracts; known-run reconciliation goes to decision-log; no transcript campaign. | LICENSE-pstack-claude | NOTICE.md; NOTICE-skills.md |

## Legal crosswalk and review

Every contributing collection's complete license is retained at the skill root with a header naming the adapted files. Exact revisions, licenses, holders, and notices are recorded per file in the manifest.

The port's root and skills-only notices are retained intact with a local header. Their original LICENSE reference maps to LICENSE-pstack-claude, which preserves both Lauren Tan and Michael Denyer; the base source has LICENSE-pstack. Historical notice links resolve in the pinned port tree. Unselected components mentioned there are not included here.

## Reproduce the comparison

From a clone of each row's source repository, run `git show <source_revision>:<source_path> > upstream.md`, verify `shasum -a 256 upstream.md`, then run `diff -u upstream.md <skill-dir>/<destination_path>` for every destination. A hash mismatch blocks adoption. Expected local adaptations produce diff exit 1; read the full input and each receiving file to review attribution.
