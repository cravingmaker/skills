# Sources

Hashes cover the exact pinned bytes before adaptation. Each row maps one retained source file to its receiving local files.

| source | source_url | source_path | source_revision | sha256 | license | copyright_holders | destination_paths | kept_material | local_changes | license_files | notice_files |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| mattpocock | https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/domain-modeling/SKILL.md | skills/engineering/domain-modeling/SKILL.md | 49dd158d1076134a641b33efb035946536778336 | 7b925d7b1e341a2eeae33ad68a8a8c0ab889a38ddd22a7598e4c240e5a7556a3 | MIT | 2026 Matt Pocock | SKILL.md | Active domain discipline: challenge against the glossary, sharpen fuzzy terms, concrete scenarios, cross-reference with code, inline glossary updates, the three ADR criteria, lazy file creation. | Paths from docs/agents/domain.md instead of fixed file names; write authority; source links; accepted-ADR immutability and supersession; boundary with decision-log; terminology sweep pointer. | LICENSE-mattpocock | none |
| mattpocock | https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/domain-modeling/GLOSSARY-FORMAT.md | skills/engineering/domain-modeling/GLOSSARY-FORMAT.md | 49dd158d1076134a641b33efb035946536778336 | 21dcc40cdec8e151a829b98ab1517c1867bc444e3665134a98c6983411996801 | MIT | 2026 Matt Pocock | references/glossary-format.md | Glossary structure, rules, single and multi-context layouts, and the map example. | Example paths become placeholders filled from the setup; optional `_Source_` line added; existing project format wins. | LICENSE-mattpocock | none |
| mattpocock | https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/domain-modeling/ADR-FORMAT.md | skills/engineering/domain-modeling/ADR-FORMAT.md | 49dd158d1076134a641b33efb035946536778336 | 944c92aa790e8fbdc9199640b170979abb8a34ba8d0fe18c2a01a63bce140ca0 | MIT | 2026 Matt Pocock | references/adr-format.md | Template, optional sections, numbering, the three criteria, and what qualifies. | Directory from the setup; added the supersession procedure and what does not qualify; existing project format wins. | LICENSE-mattpocock | none |

## Reproduce the comparison

From a clone of each row's source repository, run `git show <source_revision>:<source_path> > upstream.md`, verify `shasum -a 256 upstream.md`, then run `diff -u upstream.md <skill-dir>/<destination_path>` for each destination. A hash mismatch blocks adoption. Expected local rewrites produce diff exit 1. Inspect the complete source and each destination for attribution completeness.

## Excluded files

Upstream host registrations and unused companions are not retained. Owned host policy is generated from the catalog.

Excluded `skills/engineering/domain-modeling/agents/openai.yaml` at `49dd158d1076134a641b33efb035946536778336`, SHA-256 `f6bf2aa996c6e6f53fdd0708e18a0d16a56aed8322cca59fedbe3c0d2c75f06b`: Host settings file; owned host policy is generated from the catalog `invocation` value instead.
