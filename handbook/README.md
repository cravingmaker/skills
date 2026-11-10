> **Human documentation.** Agents should not read this page unless a person asks them to.

Language: [English](README.md) · [Bahasa Indonesia](id/README.md)

# Using the skills collection

This handbook explains what to type, what the agent should do next, and what the evidence actually proves. Start with installation, then use the intent guide for the job in front of you.

## Contents

- [Start and choose](#start-and-choose)
- [Plan, build, and deliver](#plan-build-and-deliver)
- [Understand the limits](#understand-the-limits)
- [How the collection is maintained](#how-the-collection-is-maintained)
- [Words used throughout](#words-used-throughout)
- [Why this lives separately](#why-this-lives-separately)

## Start and choose

| Your question | Read |
| --- | --- |
| How do I install this on Claude Code or Codex? | [Getting started](getting-started.md) |
| Which command do I type, and why is it manual-only? | [Typed commands](typed-commands.md) |
| Which skill fits what I want? | [Choose by intent](choosing-skills.md) |
| What does one particular skill do, and when should it stay out? | [Complete skill reference](skills.md) |

## Plan, build, and deliver

| Your question | Read |
| --- | --- |
| How do I get an idea through spec, tickets, implementation, and review? | [Recommended flow](recommended-flow.md) |
| What does the coordinator load, and what gets installed with it? | [Routing and dependencies](routing.md) |
| How do I stop at a draft, a filed PR, readiness, or a merge? | [Delivery boundaries](recommended-flow.md#choose-the-delivery-boundary) |

## Understand the limits

| Your question | Read |
| --- | --- |
| What commonly surprises people? | [Gotchas](gotchas.md) |
| What is broken, fixed, blocked, or still unproven? | [Known issues](known-issues.md) |
| What do the committed evaluations show at current skill bytes? | [Evaluation results](eval-results.md) |
| Which hosts and versions have evidence? | [Supported harnesses](harnesses.md) |
| How do host mechanics, flows, and results differ? | [Harness differences](harness-differences.md) |

## How the collection is maintained

Read [how the collection was made](making-skills.md), [why and how it is maintained](how-and-why.md), the [merged-PR changelog](../CHANGELOG.md), and [how these pages are generated](maintaining-docs.md). The [authoring guide](../docs/authoring-guide.md), [installation contract](../docs/installing.md), [evaluation harness](../docs/eval-harness.md) remain the agent-facing technical documents. The [cutover checklist](cutover.md) and [install and discovery proof](install-and-discovery-proof.md) are human-only historical records.

## Words used throughout

| Word | Meaning here |
| --- | --- |
| Skill | A folder with a `SKILL.md` that an agent loads when a task calls for it, following the [Agent Skills specification](https://agentskills.io/specification). |
| Capability skill | A skill that does one job, such as `tdd` or `file-pr`. |
| Router | `agent-orchestrator`, the core skill that coordinates work and routes it through capability methods. |
| Model selection | The agent may pick the skill on its own when your request matches its description. Explicit selection depends on the host. |
| Manual only | The catalog marks the skill `invocation: user`: the host suppresses implicit selection, and you select it by typing `/<name>` in Claude Code or `$<name>` in Codex. |
| Requires | A `metadata.requires` edge: the skill cannot work without the other skill, so installing it installs that skill too. |
| Optional route | A sentence such as "use the `how` skill" in a skill's instructions. It is followed only when that branch applies and installs nothing. |
| Profile | The full set of skills the coordinator installs: the router plus every skill reachable through `requires`. |
| Proof | The surface to drive or source to open, and the result to observe there, that shows a story or ticket is done. |
| Evaluated | The catalog status for a skill whose Activation and Near miss examples all have valid paired runs on record, with no unresolved regression against the run without the skill. See [what evaluated means](how-and-why.md#what-evaluated-means). |
| Host or harness | The agent program that loads skills: Claude Code or the Codex CLI. T3 Code is a front end that runs both. |


## Why this lives separately

The handbook is for people and sits outside the skill packages. The installer resolves required skill names and copies or links only their folders under `skills/`; it never installs this directory. Copy mode also omits each skill's `evals/results/` evidence.

No agent-facing instruction or method links here by default. The documentation generator checks those links, while the short repository README provides human navigation. This reduces accidental loading; it cannot make readable files inaccessible to an agent. A person may still ask an agent to read any handbook page.
