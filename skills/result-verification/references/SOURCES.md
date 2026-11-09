# Sources

One row per retained upstream file. Hashes cover original bytes before adaptation. The owned methods and existing authority take precedence over upstream workflow defaults.

| source | source_url | source_path | source_revision | sha256 | license | copyright_holders | destination_paths | kept_material | local_changes | license_files | notice_files |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| pstack | https://github.com/cursor/plugins/blob/6b0300214a09fd6029cfb7077043125758cd1fd2/pstack/skills/principle-prove-it-works/SKILL.md | pstack/skills/principle-prove-it-works/SKILL.md | 6b0300214a09fd6029cfb7077043125758cd1fd2 | ec79a15025bac8d33d62011c54f3b612733fd2a024e623b531b3637aa75070e2 | MIT | Copyright (c) 2026 Lauren Tan | SKILL.md | Own the actual proof procedure; clear-communication may state the claim discipline without a second verifier. | Own the actual proof procedure; clear-communication may state the claim discipline without a second verifier. Apply the owning skill adaptation and shared rules in final plan §3. | LICENSE-pstack | none |
| pstack-claude | https://github.com/michael-denyer/pstack-claude/blob/91ab921ab92d9ccfe503c93c3524410277f012e1/plugins/pstack/skills/principle-prove-it-works/SKILL.md | plugins/pstack/skills/principle-prove-it-works/SKILL.md | 91ab921ab92d9ccfe503c93c3524410277f012e1 | d5ad4e2fe1fe0fe5fd7f96ef117ed435a55a536bb1f2ce353c105c31239c0635 | MIT | Copyright (c) 2026 Lauren Tan; Copyright (c) 2026 Michael Denyer | SKILL.md | Own the actual proof procedure; clear-communication may state the claim discipline without a second verifier. | Own the actual proof procedure; clear-communication may state the claim discipline without a second verifier. Apply the owning skill adaptation and shared rules in final plan §3. | LICENSE-pstack-claude | NOTICE.md; NOTICE-skills.md |
| superpowers | https://github.com/obra/superpowers/blob/22f0b463e7a5e579904dd6211a520321035526f7/skills/verification-before-completion/SKILL.md | skills/verification-before-completion/SKILL.md | 22f0b463e7a5e579904dd6211a520321035526f7 | 2befe7fc55bcadaa3d97dd9e8efeb633d2561c0ebe74c5a8b17c4d9e7e4520b3 | MIT | Copyright (c) 2025 Jesse Vincent | SKILL.md | Support success claims with current, applicable evidence. | Keep claim/command/revision/result/limits mapping and independent source checks; reuse evidence whose inputs and output are unchanged; no full rerun before every message or false requirement that static claims need runtime proof. Apply the canonical adaptation and shared rules in final plan §3. | LICENSE-superpowers | none |

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
