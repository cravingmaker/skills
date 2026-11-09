# Sources

Hashes cover the exact pinned bytes before adaptation. Each row maps one retained source file to its receiving local files.

| source | source_url | source_path | source_revision | sha256 | license | copyright_holders | destination_paths | kept_material | local_changes | license_files | notice_files |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| mattpocock | https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/grill-with-docs/SKILL.md | skills/engineering/grill-with-docs/SKILL.md | 49dd158d1076134a641b33efb035946536778336 | 7de372c13488f1ee96cc11cd8907b56b6809cc93eef776eeddd37de6b6cbe3fe | MIT | 2026 Matt Pocock | SKILL.md | The entry combining grilling with domain-modeling so docs grow during the interview. | Skill-tool calls replaced by reads of the owned skills; domain setup and existing ADRs read first; missing setup names setup-agent-skills; write authority stated. | LICENSE-mattpocock | none |
| superpowers | https://github.com/obra/superpowers/blob/22f0b463e7a5e579904dd6211a520321035526f7/skills/brainstorming/SKILL.md | skills/brainstorming/SKILL.md | 22f0b463e7a5e579904dd6211a520321035526f7 | 2c9ca71f94886f9ca9f4aef055f7cafb3e1a9bdf3aeebf8f4cb547c69405d207 | MIT | 2025 Jesse Vincent | SKILL.md; references/builder-check.md | Look before you ask (read until you can explain how the relevant parts work and what the change touches; never reopen a decision); the builder-check sorting into answered, minor, and theirs piles, asked in one message. | Dropped universal activation, the hard gate, compulsory approaches and design-doc approval, the design-doc location, the writing-plans handoff, and the visual companion. | LICENSE-superpowers | none |
| superpowers | https://github.com/obra/superpowers/blob/22f0b463e7a5e579904dd6211a520321035526f7/skills/brainstorming/builder-check-prompt.md | skills/brainstorming/builder-check-prompt.md | 22f0b463e7a5e579904dd6211a520321035526f7 | 36d51a4723d6f0a3ce5811a0ea3b3a8424f07533947e1355f5d8cb8cce40c55e | MIT | 2025 Jesse Vincent | references/builder-check.md | The fresh-builder prompt. | Runs once, optionally, within the shared budget, on the grilling close; inline reading when no subagent is available. | LICENSE-superpowers | none |

## Reproduce the comparison

From a clone of each row's source repository, run `git show <source_revision>:<source_path> > upstream.md`, verify `shasum -a 256 upstream.md`, then run `diff -u upstream.md <skill-dir>/<destination_path>` for each destination. A hash mismatch blocks adoption. Expected local rewrites produce diff exit 1. Inspect the complete source and each destination for attribution completeness.

## Excluded files

Upstream host registrations and unused companions are not retained. Owned host policy is generated from the catalog.

Excluded `skills/engineering/grill-with-docs/agents/openai.yaml` at `49dd158d1076134a641b33efb035946536778336`, SHA-256 `94cd0ab161fb468a836349f5ed482ba58ce8e709a05c57ce533d739dbd35cca9`: Host settings file; owned host policy is generated from the catalog `invocation` value instead.
