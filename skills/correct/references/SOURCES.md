# Sources

One row per retained upstream file. Hashes cover original bytes before adaptation. The owned methods and existing authority take precedence over upstream workflow defaults.

| source | source_url | source_path | source_revision | sha256 | license | copyright_holders | destination_paths | kept_material | local_changes | license_files | notice_files |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| pstack | https://github.com/cursor/plugins/tree/6b0300214a09fd6029cfb7077043125758cd1fd2/pstack/skills/correct | pstack/skills/correct/SKILL.md | 6b0300214a09fd6029cfb7077043125758cd1fd2 | e347045d00c967a0b831ef883cc6ac79d21329aa10b5968637df95de7febf0ba | MIT | 2026 Lauren Tan | SKILL.md | Recurrence remedy hierarchy | Restricted to evidenced recurrence and authorized remedies | LICENSE-pstack | none |
| pstack | https://github.com/cursor/plugins/blob/6b0300214a09fd6029cfb7077043125758cd1fd2/pstack/skills/principle-encode-lessons-in-structure/SKILL.md | pstack/skills/principle-encode-lessons-in-structure/SKILL.md | 6b0300214a09fd6029cfb7077043125758cd1fd2 | 228963799189f481827d6f28065f278bc2008ffa37030b1234cbd5814d36b9e9 | MIT | Copyright (c) 2026 Lauren Tan | SKILL.md | Keep our recurrence, authorization and smallest-enforcement rules; no second learning loop. | Keep our recurrence, authorization and smallest-enforcement rules; no second learning loop. Apply the owning skill adaptation and shared rules in final plan §3. | LICENSE-pstack | none |
| pstack-claude | https://github.com/michael-denyer/pstack-claude/blob/91ab921ab92d9ccfe503c93c3524410277f012e1/plugins/pstack/skills/correct/SKILL.md | plugins/pstack/skills/correct/SKILL.md | 91ab921ab92d9ccfe503c93c3524410277f012e1 | 7df667ae327c76c958b1bcbcad9759a70c8ad5cdacf5f8d2e3af46a5a7e5f85c | MIT | Copyright (c) 2026 Lauren Tan; Copyright (c) 2026 Michael Denyer | SKILL.md | Turn a recurring mistake into enforceable structure. | Ours wins; keep the existing evidenced-recurrence scope, structural/static/executable priority and reject/accept/rerun proof; merge only compatible source insights; retain authorization boundaries and remove upstream approval/expiry/commit ceremonies. Use the port delta only where it improves this same canonical job; do not restore its implicit framework routing or hard-coded runtime/model settings. Apply the canonical adaptation and shared rules in final plan §3. | LICENSE-pstack-claude | NOTICE.md; NOTICE-skills.md |
| pstack-claude | https://github.com/michael-denyer/pstack-claude/blob/91ab921ab92d9ccfe503c93c3524410277f012e1/plugins/pstack/skills/principle-encode-lessons-in-structure/SKILL.md | plugins/pstack/skills/principle-encode-lessons-in-structure/SKILL.md | 91ab921ab92d9ccfe503c93c3524410277f012e1 | 1568ece8b96017b6e244530f96d937317d0ac602a58f25415d9f90073b378d6c | MIT | Copyright (c) 2026 Lauren Tan; Copyright (c) 2026 Michael Denyer | SKILL.md | Keep our recurrence, authorization and smallest-enforcement rules; no second learning loop. | Keep our recurrence, authorization and smallest-enforcement rules; no second learning loop. Apply the owning skill adaptation and shared rules in final plan §3. | LICENSE-pstack-claude | NOTICE.md; NOTICE-skills.md |

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
