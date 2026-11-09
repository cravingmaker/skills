# Sources

One row per retained upstream file. Hashes cover original bytes before adaptation. The owned methods and existing authority take precedence over upstream workflow defaults.

| source | source_url | source_path | source_revision | sha256 | license | copyright_holders | destination_paths | kept_material | local_changes | license_files | notice_files |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| pstack | https://github.com/cursor/plugins/tree/6b0300214a09fd6029cfb7077043125758cd1fd2/pstack | pstack/skills/create-verification-skill/SKILL.md | 6b0300214a09fd6029cfb7077043125758cd1fd2 | d353973547bf8ad8977eca645f4cd4feaed0d32f4b43d1448f906b0a76c4d694 | MIT | 2026 Lauren Tan | SKILL.md; references/capabilities.md | Verification-gap assessment and conditional bounded authoring route | Moved the sole authoring recipe to create-verification-skill; retained assessment and a conditional pointer | LICENSE-pstack | none |
| mattpocock | https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/misc/setup-pre-commit/SKILL.md | skills/misc/setup-pre-commit/SKILL.md | 49dd158d1076134a641b33efb035946536778336 | c9819d7f1e3b198064edc1faa3154224ed67395e9f07f5d3cea4b67cf0a11a98 | MIT | Copyright (c) 2026 Matt Pocock | SKILL.md; references/capabilities.md | Wire staged formatting and lint checks into repository work. | Keep the staged/local/CI parity check and rerun proof; reuse existing package manager and hooks; remove automatic Husky/lint-staged/formatter installation. Apply the canonical adaptation and shared rules in final plan §3. | LICENSE-mattpocock | none |
| pstack | https://github.com/cursor/plugins/blob/6b0300214a09fd6029cfb7077043125758cd1fd2/pstack/skills/principle-build-the-lever/SKILL.md | pstack/skills/principle-build-the-lever/SKILL.md | 6b0300214a09fd6029cfb7077043125758cd1fd2 | 3434b0ad0c640c6f1d7960be7a8986c3bcdc14e26060360dec29903df60074ff | MIT | Copyright (c) 2026 Lauren Tan | SKILL.md; references/capabilities.md | Prefer an existing deterministic command; add a tool only for an actual recurring gap. | Prefer an existing deterministic command; add a tool only for an actual recurring gap. Apply the owning skill adaptation and shared rules in final plan §3. | LICENSE-pstack | none |
| pstack-claude | https://github.com/michael-denyer/pstack-claude/blob/91ab921ab92d9ccfe503c93c3524410277f012e1/plugins/pstack/skills/principle-build-the-lever/SKILL.md | plugins/pstack/skills/principle-build-the-lever/SKILL.md | 91ab921ab92d9ccfe503c93c3524410277f012e1 | 9dc489b420ff2d4ea3676bd2826a9c3568fa8d965269b2a10145c04f6efa334c | MIT | Copyright (c) 2026 Lauren Tan; Copyright (c) 2026 Michael Denyer | SKILL.md; references/capabilities.md | Prefer an existing deterministic command; add a tool only for an actual recurring gap. | Prefer an existing deterministic command; add a tool only for an actual recurring gap. Apply the owning skill adaptation and shared rules in final plan §3. | LICENSE-pstack-claude | NOTICE.md; NOTICE-skills.md |

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
