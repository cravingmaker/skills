> **Human documentation.** Agents should not read this page unless a person asks them to.

# Why and how the collection is made

This is one personal collection with one owned skill per job. Its priorities are shared understanding without verbosity, then an environment that rejects wrong work through structure and checks.

## Contents

- [Why own the collection](#why-own-the-collection)
- [Prefer checks that change the result](#prefer-checks-that-change-the-result)
- [Keep capability and coordination separate](#keep-capability-and-coordination-separate)
- [Draft, review, and evaluate](#draft-review-and-evaluate)
- [What evaluated means](#what-evaluated-means)
- [Preserve provenance](#preserve-provenance)
- [Primary sources](#primary-sources)
- [Understand the validation layers](#understand-the-validation-layers)
- [Read the history](#read-the-history)

## Why own the collection

Favorite methods from Matt Pocock's skills, the pstack Claude/Codex port, tstack, and Superpowers were adopted as owned packages. Some retained useful wording; others were adapted to preserve scope, exact source values, portable execution, and one coherent workflow. The upstream plugins were retired rather than kept as competing instruction sources.

The [observed cutover in PR #10](https://github.com/cravingmaker/skills/pull/10) reports uninstalling Matt's collection on both hosts. The other three sources were already absent. That distinction matters: the result was one owned collection, not a claim that all four had been installed and removed during that operation.

Ownership means the repository maintains the method, fixes it, evaluates it, and preserves its legal attribution. It does not mean original authorship of every retained sentence. The usual shaping-to-building flow remains the one described in the [workflow guide](recommended-flow.md).

## Prefer checks that change the result

A remembered rule can be skipped; a working type, lint rule, or CI check can reject the wrong change. The collection prefers the highest layer that can hold a requirement: architecture and ownership, then types and static checks, then executable proof, with prose for judgment that checks cannot decide.

For example, a hand-maintained dependency table should become generated output with a drift check. A failing hook already present in the project needs repair or wiring before a second hook is added. A good guardrail demonstrates rejection of the real mistake, acceptance of valid work, and repeat setup without a new diff.

Token cost matters where it changes decisions. Short descriptions and conditional references reduce default loading; they do not justify hiding a required completion rule. The goal is mutual understanding, not a rigid word ceiling or a larger software factory.

## Keep capability and coordination separate

A capability owns a reusable job and its completion evidence. `agent-orchestrator` is the core router: it selects methods and coordinates work across agents. Planning, implementation, review, and verification stay in their owning capabilities.

The fleet has one coordinating owner for scope, budget, integration, and final acceptance. Workers receive bounded leaf briefs. Delegation earns its cost through useful isolation, independent work, independent checking, or a requested different capability. The presence of a fleet tool does not make every task a fleet task.

The [routing reference](routing.md) lists the coordinator's flows and required dependencies. The [changelog](../CHANGELOG.md) records why the backend and DevOps proposals were closed unmerged.

## Draft, review, and evaluate

A new skill starts with its examples and a fixture, not its body. The examples run first without any skill. If that baseline already produces the expected outcome, the skill is not written: the model already does the job. This rule comes from the dropped role skills, whose outcome evals mostly matched the no-skill baseline after the full drafting cost had been paid. When the gap is a rule a script can enforce, a project check (CI, lint or a hook) is preferred over a skill.

When the baseline fails, the method is written from primary research or a licensed upstream source, aimed at what the baseline missed: checks, authority limits and required evidence. Its author defines the trigger, concrete deliverable, evidence standard, failure modes, and stopping point.

An independent evaluator reviews the actual artifact and evidence until the remaining substantive findings are resolved. Disagreement is settled with source evidence or a discriminating check; agreement alone is not correctness. Bounded review rules leave unresolved decisions visible rather than treating exhaustion as approval.

The method is then compared with and without the skill in matched fresh sessions on Codex and Claude Code. Required prerequisites and task inputs stay the same in both arms. Only candidate availability changes. A material edit changes the tested bytes and requires matching coverage at the final revision.

The [paired harness documentation](../docs/eval-harness.md) describes preparation, models, fixtures, records, and isolation. It uses real model sessions when an evaluation is run. Preparing examples and fixtures, editing existing instructions, and deterministic validation need no model calls; a new skill body still requires a recorded failing baseline.

## What evaluated means

The catalog uses two states: unevaluated and evaluated. Evaluated means every Activation and Near miss has a valid recorded pair at the final candidate bytes, with no unresolved comparative hurt under the reviewed evidence policy. Required Outcome checks are reviewed as part of the evaluation campaign. The catalog checker verifies structural valid/completed coverage. Final-byte correspondence and unresolved comparative hurt require source and campaign review; the checker does not establish them.

Validity, activation, semantic correctness, and added value are different questions:

| Question | Evidence |
| --- | --- |
| Was the comparison valid? | Fresh sessions, matching inputs/settings, controlled discovery, completed arms |
| Did the method activate? | A supported native selection or successful installed-body read |
| Did the result meet the expectation? | Review of responses, artifacts, commands, and scope |
| Did the skill improve the result? | A matched comparison that separates candidate value from baseline, prerequisites, and host effects |

A valid pair can show a failed expectation. A matched result does not establish superiority to the baseline. Manual-entry positives can measure availability of the requested entry more than a unique method benefit. Shared dependency components also limit per-skill attribution.

At the 2026-11-09 core snapshot, all shipped skills were marked evaluated after the [completed host campaign in PR #9](https://github.com/cravingmaker/skills/pull/9). That statement does not promise perfect activation, every optional branch, real hosted CI, successful production delivery, or a particular future model's behavior. The [known-issues page](known-issues.md) retains those qualifications.

## Preserve provenance

Adapted material keeps its upstream URL, full source revision, source-file inventory, local-change description, and applicable license text. A per-file manifest records original hashes, destinations, retained methods, copyright holders, and legal files. Apache material also keeps required notices and marks changed files.

The [authoring guide's provenance schema](../docs/authoring-guide.md#provenance-manifests) is the maintenance contract. Automated checks establish schema, full revision/hash syntax, legal headers, and file existence. A reviewer still verifies source identity, original bytes, complete attribution, and retained contributions from prompts and assets.

Curricula used as coverage references are not copied merely because they are useful. An upstream plugin's installation status does not erase the attribution obligations of adopted text.

## Primary sources

The primary source is read from each skill's metadata; secondary retained contributions have their own legal files and per-file manifest rows.

<!-- BEGIN GENERATED upstream: generated by scripts/build-docs.py; edit the catalog or SKILL.md files, then rerun it -->

| Primary source | Skills |
| --- | --- |
| [Matt Pocock's skills](https://github.com/mattpocock/skills) | 27: `agent-orchestrator`, `change-review`, `codebase-design`, `diagnosing-bugs`, `domain-modeling`, `grill-me`, `grill-with-docs`, `grilling`, `handoff`, `implement`, `implement-spec`, `improve-codebase-architecture`, `pr`, `prototype`, `research`, `retro`, `setup-agent-skills`, `tdd`, `to-questionnaire`, `to-spec`, `to-tickets`, `triage`, `wait-what`, `wayfinder`, `wizard`, `work-decomposition`, `writing-for-agents` |
| [pstack](https://github.com/cursor/plugins) | 19: `agent-briefing`, `agent-debate`, `architect`, `benchmark-checklist`, `blast-radius`, `bro`, `clear-communication`, `correct`, `create-verification-skill`, `decision-log`, `how`, `ketchup`, `maintain-verification-skill`, `project-guardrails`, `recall`, `result-verification`, `sharpen`, `teach`, `why` |
| [pstack Claude/Codex port](https://github.com/michael-denyer/pstack-claude) | 2: `fix-ci`, `interrogate` |
| [tstack](https://github.com/t3dotgg/tstack) | 9: `babysit-pr`, `council`, `file-pr`, `full-send`, `full-stop`, `leaving-pr-comments`, `modernize`, `sol-loop`, `takeover` |
| Original to this repository | 1: `toolchain-upgrade` |

| Legal file | Skills that carry it |
| --- | --- |
| `LICENSE-cravingmaker` | 1 |
| `LICENSE-cursor-team-kit` | 6 |
| `LICENSE-humanlayer` | 1 |
| `LICENSE-mattpocock` | 31 |
| `LICENSE-pstack` | 37 |
| `LICENSE-pstack-claude` | 39 |
| `LICENSE-superpowers` | 13 |
| `LICENSE-thermos` | 1 |
| `LICENSE-tstack` | 11 |
| `NOTICE-pstack-claude.md` | 6 |
| `NOTICE-skills.md` | 33 |

<!-- END GENERATED upstream -->

## Understand the validation layers

The repository validator checks the pinned Agent Skills reference schema, repository package rules, catalog and dependency consistency, generated profiles and host policy, fixture tests, freshness, workflow security, and prose. A check passing proves its covered property.

Deterministic fixtures need no model calls. Model evaluation needs an explicitly accounted run budget and actual host authentication handled privately. A fixture requiring an unavailable external tool can leave that surface unproved even when wrapper tests pass. An unavailable native surface or reviewer stays an explicit limit.

Human documentation has its own generation and separation checks. See [maintaining these pages](maintaining-docs.md) for the exact command and failure cases.

## Read the history

The [changelog](../CHANGELOG.md) gives one plain-language entry for every merged PR through the documented main snapshot. Public PR bodies provide history, including old draft and "not yet verified" statements. Use the current catalog, current source bytes, later evaluation records, and subsequent PRs to establish today's state.
