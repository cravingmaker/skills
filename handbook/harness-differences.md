> **Human documentation.** Agents should not read this page unless a person asks them to.

Language: [English](harness-differences.md) · [Bahasa Indonesia](id/harness-differences.md)

# Claude Code, Codex, and T3 Code

The skill method is shared, while discovery, invocation policy, activation traces, and available execution tools differ. The evidence supports specific differences; it does not isolate host effects from model, permission, or fixture effects.

## Contents

- [Technical differences](#technical-differences)
- [Typing and following a flow](#typing-and-following-a-flow)
- [Subagents and delegation](#subagents-and-delegation)
- [PR tooling and waiting](#pr-tooling-and-waiting)
- [Questions and completion](#questions-and-completion)
- [Permission and sandbox differences](#permission-and-sandbox-differences)
- [Observed result differences](#observed-result-differences)
- [What cannot be concluded](#what-cannot-be-concluded)

## Technical differences

The table describes the recorded CLIs and the repository's adapters. Custom host roots must be resolved from the actual session.

| Concern | Claude Code | Codex |
| --- | --- | --- |
| Default user skill target used at cutover | `~/.claude/skills` | `~/.codex/skills` |
| Relevant isolation root | Private HOME and `CLAUDE_CONFIG_DIR` | Private HOME and `CODEX_HOME`; also account for `~/.agents/skills` |
| Explicit selection | Native `/<name>` command | Native `$<name>` skill selection |
| Manual-only storage | Selected `skillOverrides` in an explicit settings file | Owned generated `agents/openai.yaml` in the skill folder |
| Manual-only value | `user-invocable-only`, preserving stricter `off` | `policy.allow_implicit_invocation: false` |
| Inventory observation in discovery tests | SDK initialize response advertises commands | App-server `skills/list` |
| Activation evidence | Successful Skill or direct Read, trusted native slash replay, or supported visible Bash body read | Exact native selected-skill provenance/body, or a supported successful simple installed-file reader |
| Evaluation execution | Headless stream-JSON session with controlled user settings source | `codex exec --json` with controlled configuration and a fresh session |
| Description-budget observation | No truncation in the tested rendered-list scenarios | Wider-cache replay shortened rendered descriptions while inventory retained full descriptions |

The [installation contract](../docs/installing.md), [paired harness](../docs/eval-harness.md), and [discovery proof](install-and-discovery-proof.md) define the details. A model's assertion that it used a skill is insufficient on either host.

## Typing and following a flow

Use native selection for manual entries on both hosts. The same entry should select the same method and preserve the same scope. The observed Claude `/grill-me` command opened the owned interview in no-doc mode; Codex manual-positive evaluations used native `$<name>` selection.

The selected entry may read a required parent without another user command. That is method composition. It does not authorize a second interview, implementation, posting, or merging beyond the current request.

A missing automatic listing can be intentional for a manual entry. The agent should check the full installed inventory before reporting a required skill unavailable. The [command reference](typed-commands.md) gives both host spellings and the selected modes.

## Subagents and delegation

A role router supplies decisions and handoffs; the host supplies dispatch and isolation. The collection does not hard-code one provider map or require separate agents for every method.

The orchestrator records one finite allowance before launch. Workers are leaves unless their brief explicitly allocates further work from the same ledger. A lower host or user concurrency cap overrides the collection ceiling. A requested unavailable model/provider is reported without substitution.

T3 Code can expose native same-provider work, cross-provider delegation, host-owned checkouts, task completion, and cancellation. Which route is appropriate depends on the current tool descriptions and user-requested settings. Those facilities do not make a new top-level thread equivalent to a subagent.

The paired-example harness disables delegation on both hosts. The separate daily-chain fixture exercised isolated serial CLI workers through a disclosed adapter. It did not prove native simultaneous worker dispatch, provider panels, cancellation races, or every T3 lifecycle.

## PR tooling and waiting

Use a sufficient connected forge or host tool before a CLI fallback. The shared method keeps body drafting, filing, monitoring, and merge authority distinct on both hosts. It returns every created or updated PR layer and reads back head/base/check/review state.

T3 Code may require session linking and provide a PR watch mechanism. In that environment, follow its actual linking and completion contract. The root owns one watcher; children return PR state without watching.

When a supported completion mechanism exists, handle available work, arm it, and yield as the host requires. A plain CLI environment may provide a supported blocking check command; it does not imply T3's exact watch API. If no supported mechanism exists, return one bounded status pass and the next action. Do not build a polling loop to emulate a missing tool.

## Questions and completion

The [delivery method](../skills/full-send/SKILL.md#asking-the-user) asks blocking questions through the active host's question tool. If that tool is absent or returns no answer, it leaves the PR open and unmerged and puts the question first in its final message. The recorded campaigns do not establish which interactive front ends supply that tool.

The paired harness drives CLIs directly; no paired comparison establishes a T3 Code question, watch or delegation lifecycle. The [historical routing trial](install-and-discovery-proof.md#misroutes-budget-and-limits) also records Claude suggesting native agent definitions for an unavailable role, although both hosts correctly loaded no role skill. That suggestion is not this collection's role installation procedure.

## Permission and sandbox differences

A skill's scope is not a sandbox, and test-needed authority does not bypass system or harness enforcement.

| Recorded evaluation setup | Claude Code | Codex |
| --- | --- | --- |
| Approval behavior | `dontAsk` with allowed Read/Write/Edit/Bash/Skill and denied delegation/web tools | Approval policy `never` |
| Command filesystem | Claude sandbox with controlled working directories | `workspace-write` sandbox |
| Command network | No allowed network domains | Command network disabled |
| Other sources | Controlled user settings, no external plugins/connectors/hooks/auto memory | Controlled config; bundled skills/plugins/apps/hooks/memories/delegation disabled |
| Observed obstruction | Protected hook writes, some composite commands, and real npm spawning denied | Some equivalent fixture probes could execute; protected project/Git surfaces still needed specific fixture treatment |

These are harness configurations, not recommendations for weakening a real user's permissions. The source adapter and [PR #9](https://github.com/cravingmaker/skills/pull/9) establish the recorded behavior. Server-enforced settings outside local traces remain a limit.

An empty Claude settings-source list hid user skills on the recorded version, so the harness enables only its controlled temporary user source. A clean project alone does not remove user plugins or memory context. A long Claude temporary path also triggered shared-temp fallback before the harness correction. Those confounds explain why some attempted comparisons were invalid rather than behavioral evidence.

The [construction incidents](making-skills.md#protocol-exceptions-and-lessons) also record two campaign-worker startup memory reads and one personal-preference probe despite brief boundaries. Those worker incidents are separate from the configured paired arms. Treat host-injected context, per-arm temporary roots, fork rejection, and stable dedicated worktrees as conditions to verify; a prose promise is insufficient.

## Observed result differences

Read these as bounded observations with their confounds. The record does not support a general ranking of the two hosts.

| Case | Observed difference | Supported interpretation |
| --- | --- | --- |
| Authorized offline PR edit | One Claude treatment's combined edit/readback was denied; fresh Claude and Codex pairs completed it | A historical permission-confounded completion failure, not a proven skill-body defect |
| Hook setup and runtime probes | Claude denied protected-path writes and real npm in the recorded fixtures; a custom hook fixture separated the trigger question, and some Codex probes ran | Tool/permission availability affects attainable proof; stand-ins do not establish real staged-hook parity |
| Final retrospective duplicate-rule case | Both final treatments reject duplicate guidance and respect named sources; Claude has an off-topic source-label nit | Similar core result with one retained response defect; no host-wide accuracy inference |
| Earlier short factual PR draft | A Codex trial loaded the communication method unnecessarily; later description retests on both hosts address the targeted boundary | Historical extra workflow cost, not a universal trigger rate |
| Missing manual parent | Typed entries stop rather than inventing absent parent procedures in the later Claude campaign | Availability and dependency discipline matter; the comparison does not isolate a new parent method |

The [final retrospective record](../skills/retro/evals/results/2026-11-09-claude-claude-opus-5-5-outcome-6-round4-fix5-claude.md), [questionnaire repeat](../skills/to-questionnaire/evals/results/2026-11-09-claude-claude-opus-5-5-near-miss-3-round2-pre-claude.md), and [PR #9 results](https://github.com/cravingmaker/skills/pull/9) retain these qualifications. The [known-issues page](known-issues.md) distinguishes fixed defects from current limits.

## What cannot be concluded

The host-default models differ, and permission/settings fixtures can differ across campaigns. Individual paired arms are matched within one host; that does not create a controlled cross-host experiment.

Do not infer general superiority, cost savings, universal manual suppression, or future-version reliability. No unavailable independent reviewer, production/native surface, real hosted CI gate, or merge should receive result credit. T3-specific tools should be described as available in a session, not as guaranteed by the skill package.
