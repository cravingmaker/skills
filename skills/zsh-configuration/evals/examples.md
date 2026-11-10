# Examples

These cases are prepared for paired runs with and without the skill; no model runs are claimed.

## Activation

- "Fix my macOS PATH: a command resolves differently in login and non-login zsh." Expect: inspect actual invocation and startup ownership before a narrow change.
- "My .zshrc takes seconds to load; find the cost and verify the change." Expect: comparable before/after mode evidence and a fresh-terminal check.
- "This sourced zsh function changes my caller options after it fails." Expect: local emulation/options and a success/failure caller-state test.

## Near miss

- "Repair an executable zsh backup script." Expect: shell-scripting; do not edit interactive startup files.
- "Fix our launchd job environment and install its missing package." Expect: hand host service/package work to its owner with evidence.
- "Use the engineering plugin deploy-checklist for release approval." Expect: the requested engineering:deploy-checklist flow; no zsh probe.
- "Use the engineering plugin incident-response to coordinate an outage." Expect: the requested engineering:incident-response flow; no startup edits.

## Outcome

- "Preview startup probes on this machine." Fixture: pass --zsh pointing at a nonexistent path without --run. Expect: exit 0, shells_executed 0 and no files or shell calls.
- "Run probes without a disposable marker." Fixture: an otherwise valid directory lacks .zsh-probe-disposable. Expect: exit 2 before any startup code runs.
- "Compare controlled startup modes without disclosing values." Fixture: a marked disposable root has empty baseline and candidate files .zshenv, .zprofile, .zshrc, .zlogin and .zlogout; .zprofile prepends /synthetic-login to PATH and .zshrc prints SYNTHETIC_CREDENTIAL. Expect: source order changes by login/interactive mode, PATH hashes differ only where applicable, output bytes are counted, and neither the credential nor PATH values appear in output.
- "Verify function option scope." Fixture: source assets/zsh-function.zsh in zsh with SH_WORD_SPLIT enabled, call it with one literal argument and then invalid arguments. Expect: unchanged caller option and preserved literal bytes; the failure exits the function with status 2.

- "Compare PATH defects privately." Fixture: a marked disposable candidate login profile prepends the same missing directory twice and an empty entry. Expect: ordered entry hashes show the duplicate, duplicate/empty/missing counts increase and no literal directory appears; a completed probe remains observation data, not a clean verdict.
