# Behavior fixtures

Read this when adding or fixing tests for a shell script. Tests run the script as a separate process with its declared interpreter and assert exits, stdout, stderr and files. Exercise its public executable; source only a library whose public contract is sourcing.

## Harness choice

- Use the repository's existing harness first.
- bats-core with bats-support, bats-assert and bats-file is the usual choice for bash and sh. Pin its version through the repository's dependency mechanism or a pinned checkout; resolve the current release live, never from memory. Use `run --separate-stderr` so stdout and stderr are asserted apart.
- For zsh scripts, or when bats is not wanted, a POSIX `sh` test file that calls the script, captures `$?`, and compares files is enough.
- Stub external commands (network clients, cloud CLIs) with small executables placed first on `PATH` inside the test directory. Stubs record their arguments and return the status the case needs. Real side effects stay inside a `mktemp -d` directory the test owns and deletes.

## Required cases

Cover each case that applies to the script's contract:

| Case | What the test asserts |
| --- | --- |
| Success | Exit 0, exact stdout, nothing unexpected on stderr, expected files. |
| Each documented failure | The promised nonzero status and a message naming the fix. Assert each documented status on the path that produces it; a text match for exit statements is not coverage. |
| Argument errors | Usage on stderr, the usage status, no side effects. |
| Hostile names | Paths with a space, a tab, a newline, a leading dash, and a glob character pass through unchanged. |
| Empty and unset values | Empty string and unset variable are distinguished where the contract says so. |
| Missing dependency | With the utility removed from `PATH`, the script fails early with the install hint. |
| Failed child | A stubbed child that exits nonzero, including from inside a function called in a conditional, makes the script fail with its documented status and publishes no success artifact. |
| Interruption | SIGINT or SIGTERM during work leaves no partial output, cleans temp files, and returns the documented interruption status; check 128 + signal when that is the contract. |
| Rerun | Running twice gives the same end state; an interrupted run followed by a full run converges. |
| Concurrency | When two runs can overlap, the second waits or fails clearly instead of corrupting state. |

## Matrix

Run the suite on every declared target: the declared Linux environment and a macOS environment for macOS. When macOS `/bin/bash` is a target, run the suite with `/bin/bash` explicitly, since `env bash` on a runner may find a newer bash first. Pin hosted runner images by name and confirm the current labels in the CI provider's documentation. Wire the CI job through the repository's existing check command; the `project-guardrails` skill owns that wiring when installed.

A local run on one machine proves that machine only. Report each target and interpreter the suite actually ran on.
