# Sources

One row per retained upstream file. Hashes cover the original bytes before adaptation.

| source | source_url | source_path | source_revision | sha256 | license | copyright_holders | destination_paths | kept_material | local_changes | license_files | notice_files |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| mattpocock | https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/improve-codebase-architecture/SKILL.md | skills/engineering/improve-codebase-architecture/SKILL.md | 49dd158d1076134a641b33efb035946536778336 | 552240a5ab5cec6b67c15dd1ad6e9f6962b1bca6ce870059a8c2713760c20392 | MIT | Copyright (c) 2026 Matt Pocock | SKILL.md | Hotspot-first scoping, friction questions, deletion test, card fields, decision-record conflicts, pick-then-explore loop and glossary updates. | Report rendered by a script; evidence required per candidate; repository terms kept; mandatory sub-agent, auto-open and Skill-tool calls removed; spec frontmatter; manual-only moved to the catalog. | LICENSE-mattpocock | none |
| mattpocock | https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/improve-codebase-architecture/HTML-REPORT.md | skills/engineering/improve-codebase-architecture/HTML-REPORT.md | 49dd158d1076134a641b33efb035946536778336 | 581e8bb5a521e46bbda8ca7e19b15948bed882187108092ebb90c62513b77528 | MIT | Copyright (c) 2026 Matt Pocock | references/report-format.md; scripts/render-report.py | Card structure, badges, diagram patterns, legend, top recommendation, tone and phrasings. | Tailwind and Mermaid CDNs removed from the default; securityLevel loose replaced by strict behind an opt-in pinned Mermaid with a network notice; all content escaped by the renderer; vocabulary bans removed. | LICENSE-mattpocock | none |

## Reproduce the comparison

For each row, resolve its pinned source checkout and export the exact input, verify its table hash, then compare each receiving path:

```sh
git -C <upstream-checkout> show <source_revision>:<source_path> > upstream.md
shasum -a 256 upstream.md
diff -u upstream.md <skill-dir>/<destination_path>
```

The hash must equal sha256 in that row. Repeat the diff for every destination_paths entry; exit 1 records expected adaptation differences. Complete legal texts and applicable notices remain intact. Source review establishes attribution completeness.

## Optional renderer dependency

Checked 2026-11-08: the opt-in [Mermaid 11.4.1 full bundle](https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.min.js) is loaded with `sha384-rbtjAdnIQE/aQJGEgXrVUlMibdfTSa4PQju4HDhN3sR2PmaKFzhEafuePsl9H/9I`. Its SHA-256 is `a43bc1afd446f9c4cc66ac5dd45d02e8d65e26fc5344ec0ef787f88d6ddb6f9e`. The bundle is not copied into the skill. The full bundle has no dynamic imports, so its integrity covers the loaded Mermaid code; the default report makes no network request.

```sh
curl --fail --location https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.min.js -o mermaid.min.js
openssl dgst -sha384 -binary mermaid.min.js | openssl base64 -A
```
