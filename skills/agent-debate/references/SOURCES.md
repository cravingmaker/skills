# Sources

One row per retained upstream file. Hashes cover original bytes before adaptation. The owned methods and existing authority take precedence over upstream workflow defaults.

| source | source_url | source_path | source_revision | sha256 | license | copyright_holders | destination_paths | kept_material | local_changes | license_files | notice_files |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| pstack | https://github.com/cursor/plugins/blob/6b0300214a09fd6029cfb7077043125758cd1fd2/pstack/skills/arena/SKILL.md | pstack/skills/arena/SKILL.md | 6b0300214a09fd6029cfb7077043125758cd1fd2 | d0adeca6c9b19d43d90ed8f0484f0ddd362f05006d628b8f4cc6c9b55fa4d2b3 | MIT | Copyright (c) 2026 Lauren Tan | SKILL.md | Compare independently generated alternatives against a fixed rubric. | Keep blind first positions, meaningful design diversity, cross-judging and evidence-backed selection/grafting; cap entrants and rounds within the run budget; label sequential nonblind alternatives honestly; do not fake a requested unavailable model/provider. Apply the canonical adaptation and shared rules in final plan §3. | LICENSE-pstack | none |
| pstack-claude | https://github.com/michael-denyer/pstack-claude/blob/91ab921ab92d9ccfe503c93c3524410277f012e1/plugins/pstack/skills/arena/SKILL.md | plugins/pstack/skills/arena/SKILL.md | 91ab921ab92d9ccfe503c93c3524410277f012e1 | 34a4996db637e2172beeb4e6953cf20caad6c7f5586bc2db6a514c45f1ff3c1c | MIT | Copyright (c) 2026 Lauren Tan; Copyright (c) 2026 Michael Denyer | SKILL.md | Compare independently generated alternatives against a fixed rubric. | Keep blind first positions, meaningful design diversity, cross-judging and evidence-backed selection/grafting; cap entrants and rounds within the run budget; label sequential nonblind alternatives honestly; do not fake a requested unavailable model/provider. Use the port delta only where it improves this same canonical job; do not restore its implicit framework routing or hard-coded runtime/model settings. Apply the canonical adaptation and shared rules in final plan §3. | LICENSE-pstack-claude | NOTICE.md; NOTICE-skills.md |
| tstack | https://github.com/t3dotgg/tstack/blob/1085050f3baed1ac724caa4a8166145fb2ac88af/skills/council/SKILL.md | skills/council/SKILL.md | 1085050f3baed1ac724caa4a8166145fb2ac88af | 598fb2c7cdd48ddd9643cb22999e1b624c357aa6579aa0af0e7268ae16a8a164 | MIT | Copyright (c) 2026 Theo Browne | SKILL.md | Non-code provider panels, scoped read-only feedback and honest participant results | Retained requested distinct providers and bounded shared starts/rounds; removed automatic fixes, PR writes, model slugs and agreement by exhaustion | LICENSE-tstack | none |

## Reproduce the comparison

For each table row, resolve the pinned upstream checkout, export its exact bytes and verify the recorded sha256 before comparing every destination_paths entry:

```sh
git -C <upstream-checkout> show <source_revision>:<source_path> > upstream.md
shasum -a 256 upstream.md
diff -u upstream.md <skill-dir>/<destination_path>
```

Expected adaptation differences exit 1; an unmatched source hash invalidates the comparison. The table records source contribution, not a runtime provider or authority grant.

## Original notices

Where present, NOTICE.md and NOTICE-skills.md retain the complete original port text; upstream-relative paths refer to the pinned source tree. Their local license is LICENSE-pstack-claude, with each other contributing source attributed separately. Broader upstream component lists describe that distribution and do not install its controllers, models, hooks or agents here.
