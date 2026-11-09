# Sources

Read this when checking retained upstream contributions, byte hashes, and legal notices. Hashes describe original pre-adaptation bytes.

| source | source_url | source_path | source_revision | sha256 | license | copyright_holders | destination_paths | kept_material | local_changes | license_files | notice_files |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| mattpocock | https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/in-progress/setup-ts-deep-modules/SKILL.md | skills/in-progress/setup-ts-deep-modules/SKILL.md | 49dd158d1076134a641b33efb035946536778336 | 29acca66ac99d4532e2a6f0370d8125d7cba1e87c9ac66573203c75189d3e6c7 | MIT | Copyright (c) 2026 Matt Pocock | SKILL.md; references/typescript-boundaries.md | Public root files, hidden subfolders, tests through entry points, allowed and forbidden import proof. | Optional discovered-layout adapter; no automatic install, product scaffold, commit, or imposed layout; actual setup reapplication and broader graph coverage. | LICENSE-mattpocock | none |
| mattpocock | https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/in-progress/setup-ts-deep-modules/dependency-cruiser.config.cjs | skills/in-progress/setup-ts-deep-modules/dependency-cruiser.config.cjs | 49dd158d1076134a641b33efb035946536778336 | 3c4973bec69f73b2117654abf9e666a7c28665b213be20e6d39869e29842428e | MIT | Copyright (c) 2026 Matt Pocock | assets/dependency-cruiser.cjs | Entry-point rules, same-package exception, test privacy, cycle detection, resolver options. | Escaped the configured root, shortened comments, added unresolved imports and pre-compilation dependencies, removed the inactive layering stub, recorded the tested release. | LICENSE-mattpocock | none |

## Reproduce

Export both inputs from the pinned source checkout and compare each destination listed above. Write comparison files only in an owned temporary directory.

```sh
git -C SOURCE_CHECKOUT show 49dd158d1076134a641b33efb035946536778336:skills/in-progress/setup-ts-deep-modules/SKILL.md > SOURCE_TMP/SKILL.md
git -C SOURCE_CHECKOUT show 49dd158d1076134a641b33efb035946536778336:skills/in-progress/setup-ts-deep-modules/dependency-cruiser.config.cjs > SOURCE_TMP/dependency-cruiser.config.cjs
shasum -a 256 SOURCE_TMP/SKILL.md SOURCE_TMP/dependency-cruiser.config.cjs
diff -u SOURCE_TMP/SKILL.md SKILL_DIRECTORY/SKILL.md
diff -u SOURCE_TMP/SKILL.md SKILL_DIRECTORY/references/typescript-boundaries.md
diff -u SOURCE_TMP/dependency-cruiser.config.cjs SKILL_DIRECTORY/assets/dependency-cruiser.cjs
```

Hashes must match their rows; diff exit 1 is expected for an adaptation. The complete original MIT license follows the adapted-files header in `LICENSE-mattpocock`. The Rust helper, data adapter, remaining references, and fixture implementations are original work.
