# Sources

Hashes cover the exact pinned bytes before adaptation. Each row maps one retained source file to its receiving local files.

| source | source_url | source_path | source_revision | sha256 | license | copyright_holders | destination_paths | kept_material | local_changes | license_files | notice_files |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| pstack | https://github.com/cursor/plugins/tree/6b0300214a09fd6029cfb7077043125758cd1fd2/pstack/skills/correct | pstack/skills/correct/SKILL.md | 6b0300214a09fd6029cfb7077043125758cd1fd2 | e347045d00c967a0b831ef883cc6ac79d21329aa10b5968637df95de7febf0ba | MIT | 2026 Lauren Tan | SKILL.md | Recurrence remedy hierarchy | Restricted to evidenced recurrence and authorized remedies | LICENSE-pstack | none |

## Reproduce the comparison

From a clone of cursor/plugins, export each table row with `git show <source_revision>:<source_path> > upstream.md`, verify `shasum -a 256 upstream.md`, then run `diff -u upstream.md <skill-dir>/<destination_path>` for every destination. A hash mismatch blocks adoption. Expected local rewrites produce diff exit 1. Review the complete input and each destination for attribution completeness.
