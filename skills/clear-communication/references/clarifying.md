# Clarifying a request

Read this when a request has consequential ambiguity: two reasonable readings that lead to different results.

## Sort what is unknown

- **Facts** live in the environment: file contents, configuration, versions, command output, earlier messages. Look them up. Ask the user for a fact only when no tool or file can supply it.
- **Decisions** belong to the user: scope, trade-offs, naming, priorities, anything with no single right answer. Put these to the user, or assume when the choice is reasonable and reversible.

## The question message

Ask every question that can be answered now in one message. A question whose answer depends on another open question waits for the next message.

```text
Two choices change the result:

1. Should the checker also run in CI? Recommended: yes, so a broken rule fails the pull request.
2. Which Python version should it target? (The repository does not pin one.)

Everything else I will do as described.
```

- Number the questions so the user can answer "1 yes, 2 3.12".
- Word each decision question so "yes" accepts the recommendation.
- Give the reason for a recommendation in one clause.
- Ask for a missing fact plainly; a recommendation there would be a guess.
- Close with what you will do without further input, in one line, only when that is not obvious.

## Stating an assumption

When you proceed on an assumption, state it once, where it matters:

```text
Assuming the checker should cover the template too, since it is copied into every new skill.
```

Pause only the work that depends on an answer. Work that every answer shares continues.

## Restating

Restate only the uncertain part, in the user's terms. When the request is clear, start the work.

## Credits

<!-- skill-names: historical -->
The batching, recommended answers, and the facts-versus-decisions split follow the `grilling` skill in [mattpocock/skills](https://github.com/mattpocock/skills). Looking at context first follows the `brainstorming` skill in [obra/superpowers](https://github.com/obra/superpowers). The house rule of batching only answerable questions, and the word budget, are this repository's.

## Requested goal restatement

When explicitly asked to restate a goal in your own words, describe the supplied problem and outcome using the user's terms. Mark your assumptions separately. Reuse known facts and decisions; do not reopen them or expand the work.

Outside that requested restatement, play back only the unresolved consequential meaning. A fully specified request needs neither an interview nor a summary before action.

## Requested interview

Within a requested interview, read the `grilling` skill when installed and let its frontier rounds determine which dependent questions can be asked next. Its close applies to that interview, not every later task.

For ordinary clarification, keep the answerable-question batching above. Reversible assumptions remain within current authority; they do not grant permission or take over user-owned direction.

<!-- skill-names: end -->
