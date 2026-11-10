# Examples

These cases are prepared for paired runs with and without the skill; no model runs are claimed.

## Activation

- "Fix this Bash script that reports a failed child but still exits 0." Expect: inspect its real callers and test status propagation, including conditional-call paths.
- "Make this POSIX backup script work on our declared macOS and Linux targets." Expect: declare actual interpreters and utility contracts, then run target-specific checks.
- "Repair this executable zsh script so filenames with spaces and newlines stay intact." Expect: zsh syntax and public executable fixtures rather than Bash lint.

- "Add behavior tests for this shell script on our declared macOS and Linux targets." Expect: read behavior-fixtures.md, test the public executable and report each actual runtime; no separate testing package.

## Near miss

- "My interactive .zshrc loses PATH entries in login terminals." Expect: the zsh-configuration capability; no executable-script workflow.
- "Triage this red GitHub Actions check on the current head." Expect: fix-ci; do not author a shell script without evidence of a script cause.
- "Use the engineering plugin deploy-checklist for release go/no-go." Expect: the requested engineering:deploy-checklist entry; no shell capability.
- "Use the engineering plugin incident-response to coordinate this outage." Expect: the requested engineering:incident-response entry; no script rewrite.
- "What one command prints the working directory?" Expect: answer directly.

- "Wire our existing lint and test commands into the required CI checks." Expect: project-guardrails and workflow authoring; do not rewrite a working script.

## Outcome

- "Check a Bash script whose first line selects sh." Fixture: an executable file begins with #!/bin/sh and contains a Bash array; pass it with --dialect bash and a real Bash interpreter. Expect: check-shell.py exits 1 with shebang_dialect_mismatch.
- "Prove syntax checking does not execute target code." Fixture: a syntactically valid Bash file writes a sentinel path inside a disposable directory, then prints SYNTHETIC_VALUE. Expect: the helper exits 0, creates no sentinel, emits no target text, and repeats with identical JSON.
- "Repair conditional failure handling." Fixture: a critical child exits 7 before a final file publish; call the script from an if condition and interrupt a separate in-progress run. Expect: its documented failure/interruption status, no partial success artifact, cleanup of owned scratch data, and a convergent retry.

- "Check the Bash starter without publishing files." Fixture: run assets/template.bash with help, no arguments, a missing disposable directory, a valid disposable directory twice and an inert failing mktemp stub. Expect: exits 0, 2, 2, 0 and 1 respectively, no leaked scratch directories, and no operation on the failure path.
