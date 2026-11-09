# Sources

One row per retained upstream file. The hash covers the exact bytes before adaptation.

| source | source_url | source_path | source_revision | sha256 | license | copyright_holders | destination_paths | kept_material | local_changes | license_files | notice_files |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| pstack | https://github.com/cursor/plugins/tree/6b0300214a09fd6029cfb7077043125758cd1fd2/pstack | pstack/skills/create-verification-skill/SKILL.md | 6b0300214a09fd6029cfb7077043125758cd1fd2 | d353973547bf8ad8977eca645f4cd4feaed0d32f4b43d1448f906b0a76c4d694 | MIT | 2026 Lauren Tan | references/verification-recipe.md | Conditional launch, doctor, drive, evidence and cleanup method | Rewrote as a bounded local recipe; omitted sweeps and maintenance loops | LICENSE-pstack | none |

## Reproduce the comparison

From a clone of cursor/plugins at the recorded revision, export the source and compare it with this skill's destination:

```sh
git show 6b0300214a09fd6029cfb7077043125758cd1fd2:pstack/skills/create-verification-skill/SKILL.md > upstream.md
shasum -a 256 upstream.md
diff -u upstream.md <skill-dir>/references/verification-recipe.md
```

The hash must match the table. The diff shows the retained method and the local rewrite; diff exits 1 for expected differences. Source review establishes attribution completeness.
