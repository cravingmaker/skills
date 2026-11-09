# Sources

Per-file provenance for the leaving-pr-comments skill. Each row is one upstream file this skill retains material from, pinned to a full commit, with the byte hash before adaptation. Reproduce a destination diff by fetching the pinned URL and comparing it with the listed local files.

| source | source_url | source_path | source_revision | sha256 | license | copyright_holders | destination_paths | kept_material | local_changes | license_files | notice_files |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| tstack | https://github.com/t3dotgg/tstack/blob/1085050f3baed1ac724caa4a8166145fb2ac88af/skills/leaving-pr-comments/SKILL.md | skills/leaving-pr-comments/SKILL.md | 1085050f3baed1ac724caa4a8166145fb2ac88af | 1d110343022d0514c101dd942286cce10d6b9f5bd5b899f5a0530620d34cd295 | MIT | 2026 Theo Browne | SKILL.md | Secrets check before posting; direct style (conclusion first, cite evidence, no filler, fact versus judgment); preview the Markdown; verify the returned URL; resolve only after the reply posted; never guess the model name. | The mandatory model-attribution callout became the user's or repository's convention, with no banner by default; post, reply and resolve only within authority; connected tools before `gh`; shared delivery contract added. | LICENSE-tstack | none |
| pstack-claude | https://github.com/michael-denyer/pstack-claude/blob/91ab921ab92d9ccfe503c93c3524410277f012e1/plugins/pstack/skills/get-pr-comments/SKILL.md | plugins/pstack/skills/get-pr-comments/SKILL.md | 91ab921ab92d9ccfe503c93c3524410277f012e1 | 8bf292736cab922276feb4d8377edc2fc4102a7beb62bcd1f3f5cf72a79b16cc | MIT | 2026 Lauren Tan; 2026 Michael Denyer; 2026 Cursor | SKILL.md | From cursor-team-kit at e46364b8be46000b7df0f260550cd712afbb8d36, as copied by the port. Resolve the PR; fetch review and discussion comments; group by severity and actionability; action list and open questions. | Added exact thread identity, resolved and outdated state, the commit each comment was written against, and keeping every unresolved thread across pushes; comment text treated as untrusted data. | LICENSE-pstack-claude; LICENSE-cursor-team-kit | NOTICE-pstack-claude.md |
| superpowers | https://github.com/obra/superpowers/blob/22f0b463e7a5e579904dd6211a520321035526f7/skills/receiving-code-review/SKILL.md | skills/receiving-code-review/SKILL.md | 22f0b463e7a5e579904dd6211a520321035526f7 | 091df1629510af1b92fc4abd6f96732ebedb4cb2c0f3457e8f2740b0504a2438 | MIT | 2025 Jesse Vincent | SKILL.md; references/verifying-feedback.md | Read, understand, verify, evaluate, respond, implement; source-specific handling; reviewer checks; YAGNI usage search; implementation order; when and how to push back; correcting your own pushback; worked examples; in-thread GitHub replies. | Dropped the forbidden-phrase list, the blanket no-thanks rule and the instruction to stop all work while any item is unclear (clarification is scoped to the affected items); "your human partner" became "the user"; examples kept in a reference. | LICENSE-superpowers | none |

## Legal files

Each license or notice below is the upstream text, copied unchanged after a header that names the adapted local files.

| Local file | Upstream file | Revision | sha256 |
|---|---|---|---|
| LICENSE-tstack | https://github.com/t3dotgg/tstack/blob/1085050f3baed1ac724caa4a8166145fb2ac88af/LICENSE | 1085050f3baed1ac724caa4a8166145fb2ac88af | 8095f9a9f97d074131f6a2ce09b952d12c18b36f09f4e5df0517c4e64e82c851 |
| LICENSE-superpowers | https://github.com/obra/superpowers/blob/22f0b463e7a5e579904dd6211a520321035526f7/LICENSE | 22f0b463e7a5e579904dd6211a520321035526f7 | a37e0e9697144819e1d965176ac4ae5bc3fa02d11e7812036bbcadf6dafe2400 |
| LICENSE-pstack-claude | https://github.com/michael-denyer/pstack-claude/blob/91ab921ab92d9ccfe503c93c3524410277f012e1/plugins/pstack/skills/poteto-mode/references/licenses/LICENSE | 91ab921ab92d9ccfe503c93c3524410277f012e1 | 5b1faca8cef6b7433b49c812c5e9e04bb1eb73b67171d67729983e0b46b9bb78 |
| NOTICE-pstack-claude.md | https://github.com/michael-denyer/pstack-claude/blob/91ab921ab92d9ccfe503c93c3524410277f012e1/plugins/pstack/skills/poteto-mode/references/licenses/NOTICE.md | 91ab921ab92d9ccfe503c93c3524410277f012e1 | 232a21a3bf88991185e6837270cba41cd83646c3998f91942c823fecc4440b4d |
| LICENSE-cursor-team-kit | https://github.com/michael-denyer/pstack-claude/blob/91ab921ab92d9ccfe503c93c3524410277f012e1/plugins/pstack/skills/poteto-mode/references/licenses/LICENSE-cursor-team-kit | 91ab921ab92d9ccfe503c93c3524410277f012e1 | 702f5f331b56aff0e33d8c7826df5202559f894145eb70355c6477b55b5bb8a0 |

## Not copied

- tstack `skills/leaving-pr-comments/agents/openai.yaml`: skipped by plan; host policy is generated from the catalog `invocation` value.

## Reproduce the comparison

From a clone of each row's source repository, run `git show <source_revision>:<source_path> > upstream.md`, verify `shasum -a 256 upstream.md`, then run `diff -u upstream.md <skill-dir>/<destination_path>` for every destination. A hash mismatch blocks adoption. Expected local adaptations produce diff exit 1; read the full input and each receiving file to review attribution.
