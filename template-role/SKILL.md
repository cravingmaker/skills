---
name: template-role
description: Equip this agent as a <role>, routing its work through the role's capability skills. Use when the user invokes template-role or asks the agent to act as a <role>.
metadata:
  requires: "clear-communication"
---

# <Role>

<Mission: what this role delivers, in one or two sentences.>

<Quality bar: the standard the role holds, as checkable statements.>

Before relying on a capability below, read its `SKILL.md`; the summaries here are orientation only. When a required capability is not installed, say which one is missing and stop that flow.

## Flows

Enter at the step the task needs; no flow is a mandatory pipeline.

### <A common job>

1. <Condition or step> → the `<capability>` skill.
2. <Next step> → the `<capability>` skill.

## Handoffs

- <Adjacent work> → the <other-role> role, with <what to hand over>.

## Done

- <Completion criterion and the evidence to report.>

Optional related work: when <condition> applies and it is installed, read the `<skill-name>` skill before relying on it.
