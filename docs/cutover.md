# Core skill cutover

Replace mattpocock-skills, the pstack port, tstack and Superpowers with the owned 58-package core only after this PR is merged and the behavioral and host gates below pass. This checklist records a future operation; shipping the checklist or passing static checks does not perform or prove cutover. A1-08 requires actual uninstall of all four sources. Disabling them alone is incomplete.

## Pass the gates

- Rebuild profiles and generated host files, then run the complete validator with Vale required. Review provenance and normalized source/destination diffs and confirm the exact 58-package closure below.
- Record matched final-skill/no-skill Activation, Near miss and Outcome runs for all new and materially changed skills. Keep missing, failed or inconclusive evidence visible and the affected status unevaluated. Unchanged skills retain only their applicable existing evidence.
- Pass the daily chain from grounded interview through spec, stable tickets, one approved-code runner, review and PR delivery. Preserve exact source hashes, blockers, named Proof, finite shared budget, worker acceptance and integration acceptance without another interview, decomposition or controller.
- Include read-only council, PR-body-only, full-stop helper-chain no-merge, missing-provider, older-unresolved-review, required-bot, missing/stale/proxy-proof and exhausted-round cases. A child never starts a PR watcher; the root watches only on request or while an authorized action still waits.
- In disposable homes and configurations, verify supported Claude Code and Codex discovery, explicit invocation and manual suppression with all four upstream sources and their automatic injections absent. A clean project directory alone does not isolate global plugins. Record host versions, effective policy and loaded skill identities.

## Inventory and rollback

Inventory both hosts at their actual user, project and local scopes before changing anything. Include managed policy and command-line overrides when they affect discovery. Use supported host inventories and inspect only the relevant registration and installation records.

For each of the four sources, record its actual package or registration name, source revision, installation mechanism, scope, registration location, installed skill roots, loose copies, symlinks and resolved targets, and source-owned startup rules, injections and hooks. Detect unregistered tstack copies as well as plugin installations. A registration inventory alone misses loose content.

Record ownership evidence and the exact affected settings keys and values. Identify unrelated plugins, names, files, stricter disabled/manual choices and settings to preserve. Keep independent host reservations, including code-review, review, security-review, init, verify and run-skill-generator, and unrelated plugin names such as standup. Do not collect credentials or unrelated transcript history.

Keep a private, scoped rollback record outside the locations being replaced. Capture the affected registration records, exact owned settings state, copy content identities and recoverable originals, link targets, hook/rule content and ownership, source identities, uninstall/reinstall mechanisms and restore order. Verify that the recorded restore inputs are reachable. Keep secret-bearing configuration out of reports; retain only the permitted affected keys and safe pointers. Record expected state before and after each operation so a partial cutover can be reconciled.

## Stage the replacement

Stage the merged, verified owned tree and its full required closure in a conflict-free temporary target. Use a temporary HOME and separate host/config/cache directories for this staging and its installer checks. Resolve the actual final host directories and settings targets from the inventory; do not assume a plugin override removes plugin content.

The existing installer accepts multiple names. The following 48 new names plus four existing roots resolve to exactly 58 packages, including all ten original packages. This is an explicit argument list, not a core profile:

```sh
set -- \
  grilling grill-with-docs domain-modeling to-spec to-tickets triage wayfinder \
  to-questionnaire setup-agent-skills prototype sharpen research how why \
  grill-me bro wait-what \
  codebase-design architect improve-codebase-architecture implement implement-spec \
  tdd diagnosing-bugs wizard change-review sol-loop blast-radius benchmark-checklist \
  create-verification-skill maintain-verification-skill council interrogate \
  file-pr babysit-pr fix-ci leaving-pr-comments modernize takeover full-send full-stop \
  retro handoff writing-for-agents teach recall ketchup pr \
  agent-orchestrator correct project-guardrails toolchain-upgrade

# Resolve stage_skills_dir to the new conflict-free temporary target first.
scripts/install-skills.py --target "$stage_skills_dir" --mode copy "$@"
scripts/install-skills.py --target "$stage_skills_dir" --mode copy --apply "$@"
```

Inspect the preview before applying. Verify the actual staged file set, bytes, executable modes, generated policy, exact names and 58-package closure, with no external prerequisites. Repeating installation must leave the same tree and owned settings unchanged. Stop on a foreign or edited destination and reconcile it against the inventory; use no force overwrite. Keep the staged tree and rollback record usable before removing any source.

## Uninstall all four sources

Uninstall mattpocock-skills, the pstack port, tstack and Superpowers through each source's actual supported installation mechanism. Use the exact recorded names and scopes; do not guess one universal uninstall command. Remove only proven source-owned loose copies, symlinks and startup injections, rules and hooks that the mechanism leaves behind. Preserve unrelated settings and registrations.

Read back each actual host/plugin inventory and the relevant skill roots after uninstall. Confirm that both registration and loose discovery paths are absent, including non-plugin tstack copies. A disabled entry, removed registration with remaining copies, or hidden skill in a running session is insufficient. This PR removes retired-source name reservations from the catalog; that catalog edit is not evidence that a host source was uninstalled. Skipped upstream names stay uninstalled.

Record each observed result and reconcile uncertain or partial effects before proceeding. If removal fails, keep the gap explicit and restore the scoped prior state when needed; leave no ambiguous mixed installation.

## Install and verify each host

Use the same explicit multiple-name argument list for each confirmed final host skill directory, in copy mode. Preview, then explicitly apply the install. Reconcile existing owned copies from the inventory; do not force replacement.

```sh
# Resolve host_skills_dir from the completed inventory; retain the NAME arguments.
scripts/install-skills.py --target "$host_skills_dir" --mode copy "$@"
scripts/install-skills.py --target "$host_skills_dir" --mode copy --apply "$@"
scripts/build-host-config.py --check
```

Use the implemented host adapters in [installing.md](installing.md) at the confirmed settings targets. For Claude, supply the actual host, target, settings path, settings scope and project root, then inspect the preview and explicitly apply only the owned preference changes. For Codex, install the checked generated files; never generate through an upstream or shared symlink. Preserve unrelated keys, stricter disabled/manual settings and effective precedence. Unsupported schemas or malformed settings are failures to reconcile, not permission to overwrite.

Reopen clean Claude Code and Codex sessions. Verify actual discovery and explicit selection of grill-me, council, interrogate, wait-what, bro, pr and ketchup, plus full-stop, owned correct and every required helper. Check all 58 expected names and every catalog user entry's manual suppression and explicit mode. Test that body-only creates no remote action, full-stop preserves no-merge in deeper helpers, and a child returns PR state without watching. No runtime route may resolve to a retired source cache.

Inspect actual plugin/skill listings and effective settings again. Confirm all four sources and their automatic injections are gone, unrelated names and settings remain, and the owned tree, policy and required closure match the staged identities. Record exact observed versions, states, checks and behavioral evidence. Claim cutover complete only after both hosts pass. On failure, preserve the evidence and restore through the scoped rollback record, then verify the restored state.
