> **Human documentation.** Agents should not read this page unless a person asks them to.

Language: [English](making-skills.md) · [Bahasa Indonesia](id/making-skills.md)

# How the collection was made

The collection was built by adopting useful methods, turning repeated mistakes into checks, and comparing the result with a strong model working without the candidate skill. The most useful later decision was to stop building technical role packages when their measured benefit did not justify their cost. New skills now start with a failing baseline.

This history combines public PRs with a sanitized construction-session summary supplied on 2026-11-10. Campaign totals are dated observations, not fresh experiments or a substitute for the current catalog. The [generated evaluation results](eval-results.md) separately count committed records against current skill-package bytes. The [design explanation](how-and-why.md), [known issues](known-issues.md), and [recommended flow](recommended-flow.md) own the continuing contracts.

## Contents

- [Goals and decisions](#goals-and-decisions)
- [People, agents, models, and limits](#people-agents-models-and-limits)
- [Construction phases and pull requests](#construction-phases-and-pull-requests)
- [Blind drafts and independent review](#blind-drafts-and-independent-review)
- [Adoption and legal provenance](#adoption-and-legal-provenance)
- [Skills and tools used to make skills](#skills-and-tools-used-to-make-skills)
- [Evaluation campaigns and their limits](#evaluation-campaigns-and-their-limits)
- [Cutover to the owned collection](#cutover-to-the-owned-collection)
- [The role experiment and the stop decision](#the-role-experiment-and-the-stop-decision)
- [How to make a new skill now](#how-to-make-a-new-skill-now)
- [Protocol exceptions and lessons](#protocol-exceptions-and-lessons)
- [The retrospective](#the-retrospective)
- [Public summaries and private evidence](#public-summaries-and-private-evidence)

## Goals and decisions

The user wanted mutual understanding without verbosity; an environment of scripts, lint, CI, and hooks that rejects wrong work by construction; and an orchestrator with a fleet of agents. Tokens should pay for useful work, with no unnecessary machinery. The original fleet proposal also included role routers bundling capabilities; that part was later stopped on evidence.

The ownership rule was one skill per job, maintained here. Favorite methods from Matt Pocock's collection, the pstack Claude/Codex port, tstack, and Superpowers could be retained or adapted when their licenses allowed it. Owned `correct` took precedence over the upstream entry. The main flow stayed `grill-with-docs → to-spec → to-tickets → implement or implement-spec → retro`, combined with pstack and tstack practices.

Required dependencies stayed in `metadata.requires`, which controls installation. The proposed `metadata.handoffs` field was dropped: optional routes are conditional prose, checked against known skill names, and do not install anything. Manual invocation belongs in `catalog/skills.yaml` as `invocation: user` and in host adapters, never as a host field in `SKILL.md`. The familiar `/grill-me`, `/council`, `/interrogate`, `/wait-what`, `/bro`, `/pr`, and `/ketchup` entry points were retained, together with `/full-stop`; their actual composition is documented in [typed commands](typed-commands.md).

## People, agents, models, and limits

The human owner set goals, authority, concurrency changes, and stop decisions. The orchestrator was Claude Opus 5.5 through Claude Code in T3 Code. It wrote briefs, integrated results, committed, pushed, and opened PRs. Workers returned uncommitted changes or patches; they did not commit.

Workers used GPT-6.1 Sol at max reasoning effort and Claude Opus 5.5 at high, sometimes max, effort. They researched, drafted, merged drafts, and ran evaluations. GPT-6 Astra at max effort was reserved for independent review and debate against the actual artifact and evidence. Those assignments describe this construction session, not models required to use the collection.

The initial live cap was eight agents, including evaluation model runs; the user later lowered it to six. Evaluation workers commonly ran three to six model runs in parallel and reread an adjustable concurrency setting before each start. One role proposal belonged to one PR. These are different from a total-start or token budget: controlling concurrency alone did not control total cost, a lesson recorded below.

## Construction phases and pull requests

| Phase | Work and result | Public record |
| --- | --- | --- |
| Research | Sol and Opus produced dossiers by role and collection. A 563-row global catalog mapped requested roles and specialties to keep-core, keep-extended, fold, or drop, then incorporated database-administration coverage. | Preparation summarized here; private research inputs are not republished |
| First owned wave | `clear-communication`, adapted from pstack's unslop and related methods with a Vale style; owned `correct`; `project-guardrails`; `toolchain-upgrade`; repository checks. | [PR #1](https://github.com/cravingmaker/skills/pull/1) |
| Foundation | Authoring guide, template, catalog checks, profiles, freshness, paired harness, and installer. | [PR #2](https://github.com/cravingmaker/skills/pull/2) |
| Coordination | `agent-orchestrator` plus `work-decomposition`, `agent-briefing`, `agent-debate`, `result-verification`, and `decision-log`. | [PR #3](https://github.com/cravingmaker/skills/pull/3) |
| Adoption plan | Blind Sol and Opus positions covered 237 and 156 source rows. The coordinator merged explicit positions; three Astra review rounds reached FULL AGREEMENT. The plan described 64 packages, 48 new core skills, typed entries, per-skill changes, and provenance rules. Plan counts describe that stage, not the later 58-package installation. | Plan embodied by [PR #4](https://github.com/cravingmaker/skills/pull/4), [PR #5](https://github.com/cravingmaker/skills/pull/5), [PR #6](https://github.com/cravingmaker/skills/pull/6), and [PR #7](https://github.com/cravingmaker/skills/pull/7) |
| Adoption tooling | Catalog invocation preference, Codex `agents/openai.yaml` generation, Claude `skillOverrides` installation adapter, and prose-name checking in place of handoffs. | [PR #4](https://github.com/cravingmaker/skills/pull/4) |
| Core adoption | Shape and understand; design, build, and verify; ship and continuity, including the cutover checklist. Each followed the plan, independent review to agreement, and Codex evaluation. | [PR #5](https://github.com/cravingmaker/skills/pull/5), [PR #6](https://github.com/cravingmaker/skills/pull/6), [PR #7](https://github.com/cravingmaker/skills/pull/7) |
| Stack checks | Full-stack review and an end-to-end throwaway CLI run. Native Codex skill injection was added to activation detection; replay corrected 63 genuine false-to-true observations. | Stack landed through [PR #8](https://github.com/cravingmaker/skills/pull/8); [worked daily chain](recommended-flow.md#worked-example-adding-json-output-to-a-cli) |
| Main landing | PRs #2–#7 had merged into stacked parent branches, rather than main. PR #8 landed the combined stack. | [PR #8](https://github.com/cravingmaker/skills/pull/8) |
| Claude host campaign | Four rounds, harness corrections and six skill fixes; all 58 core skills reached evaluated at that checkpoint. | [PR #9](https://github.com/cravingmaker/skills/pull/9) |
| Installed cutover | On 2026-11-09 the owned 58-package core replaced the remaining upstream installation on both hosts; retired reservations were released. | [PR #10](https://github.com/cravingmaker/skills/pull/10) |
| Role experiment | Backend and DevOps drafts reached review agreement but were closed unmerged after weak measured incremental value; sysadmin drafting was cancelled. | [PR #11](https://github.com/cravingmaker/skills/pull/11), [PR #12](https://github.com/cravingmaker/skills/pull/12) |
| Cleanup and documentation | The cleanup follow-up removes role traces. The documentation work adds human guidance, a changelog, categorized README, agent procedures, the baseline-first rule, Indonesian mirrors, and evaluation results. These are follow-up work, separate from the earlier main landing. | [PR #14](https://github.com/cravingmaker/skills/pull/14), [PR #13](https://github.com/cravingmaker/skills/pull/13) |
| Baseline-first Outcome evaluation | Five custom Codex Outcome pairs exercised the baseline-first rule of `writing-for-agents`; it became evaluated, so all 58 skills are evaluated. | [PR #15](https://github.com/cravingmaker/skills/pull/15) |

The [changelog](../CHANGELOG.md) distinguishes merged work, stack landing, and closed-unmerged proposals. Retarget an open stacked child to its intended base after its parent lands, inspect the resulting diff, then merge; a merged parent branch is not proof that main contains it.

## Blind drafts and independent review

During the role proposals, each slice received two blind drafts from the same brief, one by Sol and one by Opus. A Sol worker scored them per skill for scope fidelity, correctness and safety, determinism, triggering and evaluations, and economy. It chose a base and grafted only demonstrably better parts from the other draft. Both role packages used five slices. Scripts were deliberately broken to prove that their tests rejected the intended fault.

Astra reviewed the actual integrated result and evidence, rather than a worker's completion claim. Findings carried stable IDs, blocker/should/nit severity, a failure scenario, and a minimal patch. The coordinator fixed or disputed each with evidence, then requested another review. Recorded rounds continued until FULL AGREEMENT; agreement was a review outcome, not proof of runtime behavior. After the role stop, dual drafting was reserved for high-stakes content whose failing baseline first showed a need.

## Adoption and legal provenance

Copying was gated by license: MIT and Apache-2.0 material could be adopted; copyleft, non-commercial, unlicensed material could not. Apache adaptations kept required NOTICE text and changed-file markings. roadmap.sh supplied coverage ideas only and was never copied.

Each retained contributor needed its own legal file. The adaptation recorded its source URL, full commit revision, original file hash, destination files, retained material, and local changes in a per-file manifest. Review compared pinned originals with the destinations. Automated checks catch malformed or missing attribution fields and files; they cannot establish complete attribution or a genuine original hash without inspecting the source. The [provenance contract](how-and-why.md#preserve-provenance) and [authoring schema](../docs/authoring-guide.md#provenance-manifests) give the maintained procedure.

## Skills and tools used to make skills

These methods describe how the construction work was organized. The orchestrator followed them by hand in its own session; this is not a claim that every named skill was actually loaded. Worker briefs required the repository's authoring guide, `AGENTS.md`, and communication house style. Evaluation arms were isolated from installed skill collections: both received the same required dependencies, while only treatment received the candidate copied from the checkout.

| Owned method | Use in making skills |
| --- | --- |
| [`writing-for-agents`](../skills/writing-for-agents/SKILL.md) | Instruction craft, narrow triggers, completion criteria, and the baseline-first requirement |
| [`clear-communication`](../skills/clear-communication/SKILL.md) | Faithful, plain, lean prose and the house style for documents and skill instructions |
| [`agent-orchestrator`](../skills/agent-orchestrator/SKILL.md) | One owner for coordination, integration, and acceptance |
| [`work-decomposition`](../skills/work-decomposition/SKILL.md) | Ownership, dependencies, useful delegation, and finite budgets |
| [`agent-briefing`](../skills/agent-briefing/SKILL.md) | Self-contained worker instructions and named evidence |
| [`agent-debate`](../skills/agent-debate/SKILL.md) | Blind positions and evidence-backed resolution of disagreement |
| [`result-verification`](../skills/result-verification/SKILL.md) | Check reports against source artifacts and rerun acceptance evidence |
| [`decision-log`](../skills/decision-log/SKILL.md) | Preserve decisions, dispatch receipts, and run state across context loss |
| [`project-guardrails`](../skills/project-guardrails/SKILL.md) | Turn enforceable requirements into repository checks |
| [`correct`](../skills/correct/SKILL.md) | Make a repeated real mistake fail the highest suitable check |
| [`research`](../skills/research/SKILL.md) | Primary-source dossiers and adoption facts |
| [`grilling`](../skills/grilling/SKILL.md) | Settle consequential decisions with the user |
| [`change-review`](../skills/change-review/SKILL.md) | Compare an actual change with Standards and Spec |
| [`sol-loop`](../skills/sol-loop/SKILL.md) | Bounded review, repair, and recheck |
| [`benchmark-checklist`](../skills/benchmark-checklist/SKILL.md) | Keep measurement claims comparable and bounded by evidence |
| [`file-pr`](../skills/file-pr/SKILL.md) | PR titles and bodies grounded in the final diff |

| Repository tool | What it checks or does |
| --- | --- |
| Pinned `skills-ref` | Agent Skills reference-schema validation |
| `scripts/check-skills.py` | Owned package rules, manifests, scripts, and legal-file structure |
| `scripts/check-catalog.py` | Catalog membership, names, dependencies, and structural evaluated-status coverage |
| `scripts/build-profiles.py` | Required install closures and profile drift |
| `scripts/build-host-config.py` | Preview, apply, and check owned host invocation policy |
| `scripts/check-freshness.py` | Report version-specific facts that need renewed verification |
| `scripts/build-docs.py` | Generate human inventories and results; reject stale output, broken links, and bilingual drift |
| `scripts/install-skills.py` | Preview and apply owned installations with dependency and ownership checks |
| `scripts/eval-skill.py` and `scripts/evalharness/` | Prepare isolated paired host runs and retain their observations |
| Vale and the `clear-communication` style | Check English prose mechanically |
| zizmor | Analyze GitHub Actions security |
| `tests/<skill>/run.sh` and repository fixture suites | Reject the actual targeted mistake, accept valid work, and test repeated setup |
| `scripts/validate.sh` | Run the deterministic repository checks together; it does not run model evaluations |

The actual authoring, evaluation, installation, and delivery commands are in the [agent-facing procedures](../docs/skill-workflows.md), [evaluation guide](../docs/running-evals.md), and [validation procedure](../docs/validating.md). Tool presence does not authorize model spending, publishing, or merging.

## Evaluation campaigns and their limits

Every paired example used fresh isolated sessions, temporary homes, matching noncandidate settings and dependencies, and no personal settings, plugins, or memory in the evaluation arms. Activation came from actual installed-body reads or trusted native selection: Claude Skill/reads and Codex native injection/reads. A valid comparison establishes isolation and completion, not correct behavior or added value. Invalid attempts never count as skill failure or successful coverage.

The reviewed status policy required valid final-byte pairs for every Activation and Near miss and no unresolved hurt; required Outcome criteria were reviewed in the campaign. The catalog's deterministic gate checks valid/completed record coverage, not all of those semantic conditions. The [results page](eval-results.md) adds digest matching without changing that gate.

| Campaign checkpoint | Reported comparisons and judgments | Qualification |
| --- | --- | --- |
| Codex core work overall | About 1,000 pairs across core campaigns and follow-ups | Approximate campaign total; do not add overlapping checkpoints as unique cases |
| PR #5 | 140 pairs; 37 added / 94 matched / 5 hurt; a 70-pair follow-up reported 17 / 51 / 1 | Listed judgments do not exhaust the pair totals |
| PR #6 | 120 pairs; 39 added / 75 matched / 2 hurt; a 60-pair follow-up | Follow-up outcome breakdown was not supplied |
| PR #7 | 113 pairs; 29 added / 72 matched / 3 hurt; a 50-pair follow-up | Listed judgments do not exhaust the pair totals |
| Later Codex checkpoints | Final campaign 80 pairs; last two skills 30 pairs | Separate campaign checkpoints, not a claim of disjoint totals |
| Claude round 1 | 398 of 423 valid comparisons; Outcome 9 added / 44 matched / 5 hurt | Invalid attempts excluded; hurt prompted correction |
| Claude round 2 | All 25 invalid comparisons rerun valid; corrections to `retro`, `interrogate`, `why`, and `project-guardrails` | Later rounds establish the final corrected behavior |
| Claude rounds 3–4 | `retro` source boundary corrected; final checkpoint 13 added / 1 matched / 0 hurt | A bounded final review set, not the whole campaign |
| Role-cleanup follow-up | Four changed skills had 31 trigger examples rerun on both hosts: 62 pairs | `agent-orchestrator`, `agent-briefing`, `codebase-design`, `writing-for-agents`; the last stayed unevaluated pending its baseline-first Outcome |
| Baseline-first Outcome follow-up | Five custom Codex Outcome pairs for `writing-for-agents` | With supplied baseline reports (fixture premises, not real sessions) or no authorized calls: 2 added / 1 matched / 0 hurt ([recorded pass](../skills/writing-for-agents/evals/results/2026-11-10-codex-gpt-6.1-sol-outcome-4-recorded-pass.md), [recorded fail](../skills/writing-for-agents/evals/results/2026-11-10-codex-gpt-6.1-sol-outcome-4-recorded-fail.md), [no authorized calls](../skills/writing-for-agents/evals/results/2026-11-10-codex-gpt-6.1-sol-outcome-5-unauthorized.md)). Two earlier pairs used a detectable runner double and keep limited conclusions ([double pass](../skills/writing-for-agents/evals/results/2026-11-10-codex-gpt-6.1-sol-outcome-4-passing-baseline.md), [double fail](../skills/writing-for-agents/evals/results/2026-11-10-codex-gpt-6.1-sol-outcome-4-failing-baseline.md)). This campaign used a small controller for Outcome selection; [Run and review evals](../docs/running-evals.md) describes the ordinary route. The skill was then marked evaluated in [PR #15](https://github.com/cravingmaker/skills/pull/15) |

The construction summary reports that every core hurt was corrected and rerun before the evaluated checkpoint. The cleanup checkpoint is later history: changed bytes reset the relevant evidence obligation. The current catalog and generated record view remain separate sources; this history does not silently change either. The harness's ordinary example selector runs Activation and Near miss, so this campaign ran the baseline-first Outcome as separate jobs, with its own exercised evidence.

Strong models matched most tasks. The clearest value came from checks that reject mistakes, authority limits, and required evidence. Manual-only policy hides an entry from a model list but does not prevent a file read; the recorded Claude example did not repeat in a fresh run. See the [known limits](known-issues.md) and [host differences](harness-differences.md) before generalizing any count.

## Cutover to the owned collection

The 2026-11-09 operation inventoried both hosts, preserved a private scoped rollback record, staged the replacement in a temporary home, and checked its files and policy. It uninstalled Matt Pocock's plugin from Claude Code and Codex. The pstack port, tstack, and Superpowers were already absent; they were not newly uninstalled in that operation.

The owned 58 skills were installed to both user skill locations. Fresh sessions verified discovery and typed commands. PR #10 released retired source reservations after the observed state was established. The [archived checklist](cutover.md) preserves the planned gates and rollback discipline; [getting started](getting-started.md) is the current installation guide.

## The role experiment and the stop decision

The proposal covered 17 role routers and their capabilities: backend, frontend, mobile, UI/UX, QA, DevOps, sysadmin, security, data engineer, data analyst, data scientist, technical writer, SEO, business analyst, financial analyst, marketing, and copywriter. After backend, the requested order was DevOps, sysadmin, security, data engineer, data analyst, then data scientist.

`backend-engineer` in PR #11 and `devops-engineer` in PR #12 each contained 22 skills, built in five blind-draft slices and reviewed to FULL AGREEMENT. Sysadmin drafting began but was cancelled. DevOps was never evaluated.

Backend evaluation covered Codex examples and Claude triggers before it was stopped at 147 of 432 planned pairs and 493 of 1,100 budgeted model runs. Of 15 reviewed Outcomes, one added value (`api-design` caught invalid page sizes), 13 matched, one was blocked, and none hurt. Those denominators describe different counters and should not be divided into a single completion rate.

The user concluded that technical role knowledge did not justify building these packages when strong models already performed the tasks. The 44 drafted skills would add about 3,000 description tokens to every session, require more than 1,000 evaluation runs per role, and create maintenance work for fast-changing facts. Review agreement had established draft quality, not economic value over the baseline.

Both PRs closed unmerged with explanatory comments, and their branches were retained for reference. The cleanup follow-up removes role traces. Project-specific domain checks belong in project guardrails through `project-guardrails` and `correct`; a new reusable skill must first demonstrate a gap without it.

## How to make a new skill now

1. Check the existing catalog and coverage for an owner. Define one reusable job and a narrow trigger. A role title or familiar domain alone does not establish a need.
2. Write Activation, Near miss, and observable Outcome examples, plus the fixture, before the skill body. Set run and token budgets before a large campaign and isolate it in a dedicated worktree.
3. Run the Outcome without the candidate skill. If the baseline already meets it, stop; no new skill is needed. If a script can enforce the missing rule, prefer CI, lint, types, a hook, or another project check.
4. Only after a recorded failing baseline, draft checks, authority limits, and required evidence for the gap. Use the template, authoring guide, and license/provenance procedure. Reserve dual drafts for content whose stakes justify them.
5. Add catalog and coverage entries, required dependency edges, examples, and meaningful fixtures. Generate profiles, preview/apply host policy when needed, and generate both handbook editions with useful intent guidance.
6. Review the actual diff and evidence. Prove guardrails reject the targeted mistake, accept valid work, and repeat without drift. Keep unresolved findings visible.
7. Run authorized paired examples in fresh isolated sessions against the final bytes, review Outcome behavior and hurt, and keep the status honest. Validate the selected files in a clean export with Vale required. Commit, publish, or merge only within the task's authority.

This is the maintained [create-a-skill procedure](../docs/skill-workflows.md#create-a-skill), with the [authoring bar](../docs/authoring-guide.md) supplying package details. Writing documentation or running deterministic checks alone does not authorize a new model campaign.

## Protocol exceptions and lessons

| Recorded exception or mistake | Consequence and retained lesson |
| --- | --- |
| Evaluation workers twice read host memory at startup despite their brief; the session attributed the exposure to Codex automatic memory injection. One preflight queried a personal macOS preference domain, with no result or change | A clean project and prose boundary do not guarantee isolation. Enforce discovery and source boundaries in tooling; do not publish personal inputs. This concerns campaign workers, distinct from isolated paired arms. |
| Early Claude scratch writes reached a shared temporary root | Fix per-arm temporary roots; invalidate affected comparisons rather than blaming the skill. |
| Forked children briefly exceeded the concurrency cap | Reject uncontrolled forks and account for every model start. |
| Throwaway PostgreSQL clusters were killed without shutdown | Thirty-two shared-memory segments accumulated until the macOS limit blocked new clusters. Cleanup required user permission; shut down test databases cleanly. |
| The orchestrator switched branches while evaluations read the checkout | Stop affected runs and rerun from a dedicated worktree with stable source bytes. |
| zsh scalar word splitting was assumed twice; macOS system Bash was older | Pass real argument lists or arrays and check the actual interpreter; `/bin/bash` is Bash 3.2. |
| An unrelated evaluation record entered a documentation commit | Untracked records can affect the catalog status gate. Select the candidate explicitly and validate a clean export. |
| A macOS zombie-only process group made `killpg` raise EPERM in a zsh test | Before the fix, 17 of 24 parallel runs failed; after the fix, zero failed. These are the reported repeated-test counts, not a universal reliability estimate. |

The continuing symptoms and responses live in [Gotchas](gotchas.md), while [Known issues](known-issues.md) distinguishes fixed defects from unavailable proof. Keeping the incident here records its lesson without republishing private diagnostics.

## The retrospective

The 2026-11-10 retrospective credited the owned core, deterministic guards that caught real problems, independent review that found substantive defects, and evidence that supported stopping weak-value work. The core outcome was useful even though the role expansion stopped.

It also identified building before measuring, late cost controls that limited concurrency without total token/run budgets, dual drafts where they did not pay, weak evaluation environment hygiene, avoidable coordinator mistakes, and scope drift toward overengineering.

The resulting rules are baseline first, project checks before new skills, dedicated evaluation worktrees, clean-export validation, clean database shutdown, stacked-PR retargeting before merge, and explicit run/token budgets before large work. These rules belong in the relevant maintained procedure or executable guard; the retrospective is the record of why they were adopted.

## Public summaries and private evidence

Committed Markdown records are the public summaries. Raw traces, responses, artifacts, and comparison files stay out of Git for privacy and size. Raw evidence for 1,535 of the 1,541 records is archived privately: one compressed archive per skill (58 files) in the owner's Google Drive, scanned for credentials and tokens before upload, with owner-only access confirmed on the uploaded files. Raw files for the other six records were lost before archiving.

Each record's **Private raw evidence** line links its skill's archive and names the record's folder inside it; only the owner can open the link. Inside a record, the raw paths stay code text labeled "local only, not committed", because they name files inside the archive, not in the repository. Newly written records start with the local-only label and gain the archive line after their evidence is uploaded. The writer preserves that distinction and the documentation check rejects record links to missing repository files. The public [results page](eval-results.md) uses the committed summaries; it never treats absent raw files as newly inspected evidence. Private account details, storage layout, personal paths, and raw transcripts are intentionally not published.
