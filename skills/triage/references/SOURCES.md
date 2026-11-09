# Sources

Hashes cover the exact pinned bytes before adaptation. Each row maps one retained source file to its receiving local files.

| source | source_url | source_path | source_revision | sha256 | license | copyright_holders | destination_paths | kept_material | local_changes | license_files | notice_files |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| mattpocock | https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/triage/SKILL.md | skills/engineering/triage/SKILL.md | 49dd158d1076134a641b33efb035946536778336 | 917b0baf74be583e74f110857ed45df2766617f75c00baf61fd136d7af515edf | MIT | 2026 Matt Pocock | SKILL.md | Category and state roles, transitions, PR deltas, attention buckets, the per-item flow with already-built and prior-rejection checks, claim verification, outcomes, quick override, needs-info template, resuming. | Setup outputs replace the setup command; untrusted-content rule and isolated PR runs; drafts unless posting is authorized; attribution from the setup with the upstream line as default; connected tools first; grilling only for real gaps; no execution authority. | LICENSE-mattpocock | none |
| mattpocock | https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/triage/AGENT-BRIEF.md | skills/engineering/triage/AGENT-BRIEF.md | 49dd158d1076134a641b33efb035946536778336 | 7f5f87fed3033df1b06e083c480f3e847b1fbb0647746b8a4c6a50f9f26ef44f | MIT | 2026 Matt Pocock | references/agent-brief.md | Brief principles, template, and all four examples. | Contents list; tracker-neutral wording; faithful restatement and no adopted injected instructions; command syntax removed from one example. | LICENSE-mattpocock | none |
| mattpocock | https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/triage/OUT-OF-SCOPE.md | skills/engineering/triage/OUT-OF-SCOPE.md | 49dd158d1076134a641b33efb035946536778336 | 1fbf9b432130c6380aa65813b55553cfda150309b27c595e183f8e335b8a190d | MIT | 2026 Matt Pocock | references/out-of-scope.md | Purpose, structure, file format and example, naming, reasons, check and write flows, updates. | Contents list; location from the setup with `.out-of-scope/` as the default; writes follow the skill's authority rules. | LICENSE-mattpocock | none |

## Reproduce the comparison

From a clone of each row's source repository, run `git show <source_revision>:<source_path> > upstream.md`, verify `shasum -a 256 upstream.md`, then run `diff -u upstream.md <skill-dir>/<destination_path>` for each destination. A hash mismatch blocks adoption. Expected local rewrites produce diff exit 1. Inspect the complete source and each destination for attribution completeness.

## Excluded files

Upstream host registrations and unused companions are not retained. Owned host policy is generated from the catalog.

Excluded `skills/engineering/triage/agents/openai.yaml` at `49dd158d1076134a641b33efb035946536778336`, SHA-256 `2e683717720cf456d165d0bb1a68bb600d0b6a8ccb61841c172e50d26f95351c`: Host settings file; owned host policy is generated from the catalog `invocation` value instead.
