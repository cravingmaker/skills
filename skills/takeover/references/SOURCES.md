# Sources

Per-file provenance for the takeover skill. Each row is one upstream file this skill retains material from, pinned to a full commit, with the byte hash before adaptation. Reproduce a destination diff by fetching the pinned URL and comparing it with the listed local files.

| source | source_url | source_path | source_revision | sha256 | license | copyright_holders | destination_paths | kept_material | local_changes | license_files | notice_files |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| tstack | https://github.com/t3dotgg/tstack/blob/1085050f3baed1ac724caa4a8166145fb2ac88af/skills/takeover/SKILL.md | skills/takeover/SKILL.md | 1085050f3baed1ac724caa4a8166145fb2ac88af | 9f00a7c67bf82603af2e80f56e9ce63f1516a1b4339365b79cf786d9d9055465 | MIT | 2026 Theo Browne | SKILL.md | Finish the original goal while preserving credit; do not defend inherited code; read source, findings and corrections; resolve to the actual head and uncommitted work; handoff is context, not proof; replacement PR with separate fixes or requested in-place continuation; authorship, trailers and verified identities; modernize against the base; recheck the source PR; independent verification; merge or close only when authorized; report format. | Exact PR, head, base, checks and unresolved threads recorded before any change; inherited green checks and reports re-established through result-verification; modernize only when the base or conflicts need it; no inherited merge or watch authority; babysitting only as the root under I1-05; no-merge mode carried into helpers; shared delivery contract added. | LICENSE-tstack | none |

## Legal files

Each license or notice below is the upstream text, copied unchanged after a header that names the adapted local files.

| Local file | Upstream file | Revision | sha256 |
|---|---|---|---|
| LICENSE-tstack | https://github.com/t3dotgg/tstack/blob/1085050f3baed1ac724caa4a8166145fb2ac88af/LICENSE | 1085050f3baed1ac724caa4a8166145fb2ac88af | 8095f9a9f97d074131f6a2ce09b952d12c18b36f09f4e5df0517c4e64e82c851 |

## Reproduce the comparison

From a clone of each row's source repository, run `git show <source_revision>:<source_path> > upstream.md`, verify `shasum -a 256 upstream.md`, then run `diff -u upstream.md <skill-dir>/<destination_path>` for every destination. A hash mismatch blocks adoption. Expected local adaptations produce diff exit 1; read the full input and each receiving file to review attribution.
