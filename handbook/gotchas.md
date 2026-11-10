> **Human documentation.** Agents should not read this page unless a person asks them to.

Language: [English](gotchas.md) · [Bahasa Indonesia](id/gotchas.md)

# Gotchas

Most surprises come from confusing visibility with access, installation with execution, or a draft with delivery authority. Each entry below names the symptom, its cause, and the next useful action.

## Contents

- [Invocation and discovery](#invocation-and-discovery)
- [Installation and host settings](#installation-and-host-settings)
- [Planning and proof](#planning-and-proof)
- [Reviews and delivery](#reviews-and-delivery)
- [Runtime and shell behavior](#runtime-and-shell-behavior)
- [Evaluation records](#evaluation-records)

## Invocation and discovery

A missing automatic suggestion does not prove a missing installed skill. Inspect the full installed inventory, including manual entries, before asking to reinstall a required method.

| Symptom | Cause | What to do |
| --- | --- | --- |
| A manual command is available to you but absent from the model's list | Host policy deliberately suppresses implicit selection | Select the native command; see [every manual entry](typed-commands.md) |
| A natural-language skill name fails to start its manual workflow | Naming text and native selection are different signals | Use Claude's slash entry or Codex's native skill selector |
| A parent reads a manual-only helper | Required composition can read installed instructions | Check the declared required closure and task authority |
| An answer says it used a skill, but the trace shows only a name | Mentioning is not body loading | Look for a supported selection event or successful body read |
| An inventory and the model's visible descriptions differ | Discovery and rendered-list budgets are different surfaces | Inspect both; full inventory does not prove full prompt descriptions |
| A log quotes a command and the agent starts its workflow | Quoted data was mistaken for invocation | Restate the data-only task and keep the unexpected activation as a finding |

The recorded Claude discovery tests did not hit description truncation. The wider Codex cache replay did shorten rendered descriptions while its inventory stayed complete. Those were specific experiments, not a production-wide budget guarantee. See the [discovery proof](install-and-discovery-proof.md#budgets-and-limits).

## Installation and host settings

The installer is conservative about ownership because a same-named folder may belong to something else. Its [canonical contract](../docs/installing.md) explains the receipts and settings precedence.

| Symptom | Cause | What to do |
| --- | --- | --- |
| Preview prints a plan but nothing appears on the host | Preview is the default | Review it, then repeat with `--apply` |
| `--force` still refuses replacement | The folder is foreign or edited, not an unchanged owned install | Reconcile the named content and ownership; do not delete evidence blindly |
| An update is refused after moving the source checkout | The receipt binds its source location | Reconcile that source identity before updating |
| Claude install rejects the settings target | Scope, precedence, schema, or project-root assumptions are unsupported | Supply the effective supported target and native binary |
| A typed entry is visible in one Claude project but implicit in another | The adapter checks the supplied project's precedence, not every project on disk | Check that project's effective local/project/user override; multi-project runtime behavior is untested |
| A linked Git worktree is rejected | The adapter cannot safely infer effective settings placement there | Select the main checkout root or a standalone project |
| Copy and symlink installs expose different extra files | Copy omits evaluation results; a symlink exposes the source folder | Use copy for a stable installed package and keep the source for evaluation evidence |
| An unknown name cannot install | The installer accepts shipped skills and declared external prerequisites | Check the [skill reference](skills.md) for the exact name |
| Removing a plugin leaves an orphaned cache | Existing sessions can still reference its cached files | Verify registration and fresh-session discovery; let the host clear its cache later |
| `codex plugin list` appears stuck | Remote-catalog access can hang | Use a bounded inventory attempt and sufficient local registration/skill evidence; do not retry in a loop |

The cache and catalog-hang items are observations from the documented cutover, not a cleanup command. A leftover cache directory alone is not proof of active plugin discovery.

## Planning and proof

An approved artifact should be consumed with its identity and decisions intact. A fresh context window does not reopen the plan or reset a budget.

| Symptom | Cause | What to do |
| --- | --- | --- |
| The interview asks again about settled choices | The method ignored the conversation or accepted domain decisions | Point to the settled close or ADR; ask only the open consequential frontier |
| A docs-recording interview cannot find domain setup | The paths contract is absent | Configure it or continue as a plain interview without doc writes |
| The configured glossary does not exist | Semantic files are created lazily | Create it when the first term settles; do not invent a second glossary |
| Ticket import rejects otherwise readable Markdown | The importer accepts an exact field grammar | Use the owned template, one-line fields, numeric blockers or `None`, and a real `Proof:` |
| A thin entry stops and names an absent parent | A copied entry lacks its declared prerequisite | Install through the owned resolver; the PR #9 missing-parent cases cover this refusal |
| A graph is imported but dispatch is blocked | Execution overlays, finite budget, ownership, or host capabilities are missing | Fill the coordinator-owned fields and report the actual blocked step |
| Unit tests pass but the story's Proof is unresolved | The declared surface was never observed | Run the named CLI/UI/native/API journey on the exact artifact |
| A worker says COMPLETE but integration fails | Worker and combined revisions differ | Accept the integrated result with its own Proof |
| Evaluation reads change while another task switches branches | Shared checkout bytes moved during a campaign | Stop affected runs and rerun from a dedicated worktree with pinned inputs |
| A large campaign stays under its concurrency cap but costs too much | Active-run limits do not bound total starts or tokens | Set both budgets before the campaign and carry spent counters forward |
| A new context window seems to offer more starts | Resumption was mistaken for a new budget | Carry the original spent, reserved, active, and remaining counters |

See the [ticket importer method](../skills/work-decomposition/SKILL.md#import-approved-tickets) for accepted and rejected field forms. Its strictness prevents a hidden or ambiguous Proof or blocker from silently disappearing.

## Reviews and delivery

Read-only, body-only, prepare-only, and finish-to-merge are separate scopes. Make the desired end explicit before a helper chain starts.

| Symptom | Cause | What to do |
| --- | --- | --- |
| A review starts fixing code | Findings were treated as repair authority | Keep review report-only unless repair was asked for |
| An unavailable panel member is silently replaced | Provider identity was treated as optional | Report the missing seat; preserve the requested provider |
| A probe budget disappears after a wrapper failure | Failed attempts were not charged | Count each execution, including repeats needed only to capture status |
| Filing a PR starts an unwanted watch | Filing was treated as monitoring authority | End filing with link and state; root watches only when requested or an authorized action waits |
| Old threads are ignored after a push | Outdated code was confused with resolved feedback | Retain every unresolved thread until answered or explicitly disposed of |
| A green check belongs to an earlier head | Historical proof was promoted to current readiness | Recheck the current head and relevant base |
| A prepare-only run can still auto-merge | A pre-existing queue or auto-merge entry was left armed | Inspect owned mechanisms, cancel them, and read back their absence |
| The PR is queued but called merged | A pending request was confused with completion | Read back the forge's merged state and destination history |

A no-step billing or quota failure calls for account-owner action, not a code edit. A retry needs evidence of flake or runner failure; the CI method permits one bounded fresh workflow run for those classes. See [delivery boundaries](recommended-flow.md#choose-the-delivery-boundary).

## Runtime and shell behavior

The shell's default interpreter may differ from the one available on PATH. Check the actual runtime before treating a missing feature as an absent environment.

| Symptom | Cause | What to do |
| --- | --- | --- |
| A skill helper refuses an old Python version | Helpers require Python 3.12+, while the shell may default to an older system Python | Use a versioned interpreter or `uv run --python '>=3.12' python` |
| A script using newer Bash syntax fails on macOS | `/bin/bash` is Bash 3.2 | Use the script's declared runtime; do not assume Bash 4 features |
| A variable containing several names becomes one argument in zsh | zsh does not word-split an unquoted scalar like POSIX shell | Use positional arguments with `set --` and `"$@"`, or a real array |
| Claude denies a composite command in a no-prompt run | Permission rules can evaluate its subcommands independently | Inspect the denied operation; use a permitted simple command when sufficient |
| Claude denies a hook-file edit despite general Write permission | Protected paths have additional permission behavior | Keep the real path blocked unless permitted; a stand-in fixture proves only the stand-in |
| A report or continuation note is absent from the repository | The architecture and handoff methods use an OS temporary path | Open the returned path; preserve a durable run in its existing record before temporary cleanup |
| New disposable PostgreSQL clusters stop starting | Killed clusters can leave shared-memory resources | Shut test databases down cleanly; reconcile leftovers within authorized scope |
| A flaky macOS process cleanup reports `killpg` EPERM | A zombie-only process group affected a recorded zsh test | Distinguish a live process from a zombie-only group; see the [incident and repeated-test counts](making-skills.md#protocol-exceptions-and-lessons) |
| A dotenv write refuses a secret-shaped value | The serializer cannot prove the real loader reads it unchanged | Use the declared secret store/manual destination or prove a correct serializer round trip |

Never loosen a parser just to accept a value that reads back differently. The [wizard method](../skills/wizard/SKILL.md) explains its dotenv and shell formats, destination constraints, and refusal rules.

## Evaluation records

Public Markdown summaries mark raw artifacts as local-only code text; those artifacts are retained privately and ignored by Git. A missing raw trace in a public clone is an evidence-access limit, not proof that the comparison never ran.

Treat an invalid record as an attempted comparison, not coverage. Treat a valid record as an isolated completed comparison, then read its behavioral judgment. An old digest or a superseded hurt remains history until final-byte evidence establishes the current state.

Select intended records explicitly and validate a clean export: an untracked record can affect the catalog gate, and a stray record once entered a documentation commit. The [construction lessons](making-skills.md#protocol-exceptions-and-lessons) distinguish campaign-worker boundary breaches from controlled paired arms.

If validation says `Skipped the prose tests: Vale is not installed.`, its exit 0 does not establish prose lint. Install the declared Vale version and use `REQUIRE_VALE=1`; [`scripts/validate.sh`](../scripts/validate.sh) makes that requirement explicit.
