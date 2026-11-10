# Failure handling

Read this when changing status propagation, cleanup, retry or publication.

Check a critical child failure through the script's actual conditional callers: errexit can stay disabled throughout a function called from if or an OR list. Separate a declaration from command substitution so the assignment's status remains visible. Decide which no-match and early-consumer pipeline statuses are acceptable; test them without masking the whole pipeline.

Capture the original status before cleanup, report a cleanup failure separately, and remove only the scratch path the script created. Register traps after that path is valid. Check interrupted children have stopped before asserting the destination, then retry and confirm convergence. Publish only after validation, by rename on the same filesystem.

The Bash set builtin documentation and the installed shell manual define conditional exceptions; verify target-version behavior before relying on it. The behavioral fixture adapter linked from SKILL.md owns the complete test matrix.
