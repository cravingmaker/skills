# Builder check

Read this before running the optional builder check in step 3.

The check asks one fresh reader, who cannot talk to the user, which questions they would still need answered before they could plan the build. It runs once.

## Prompt

Give a fresh subagent this prompt. Fill in the domain and the location of the close or the written understanding.

```
You are a talented [DOMAIN, e.g. "software engineer", "event planner",
"bakery consultant"]. You've been handed a design and asked to put
together a plan to build what it describes. You will not be able to
talk to the person who wrote it.

Read [DOCUMENT_PATH or the pasted close].

Report only the questions you'd still need answered before you could plan
this well: places where you'd have to guess and a wrong guess would
matter. For each, give the question and why the answer changes the plan.
Rank them by importance.

Skip anything the design explicitly leaves to the builder, and anything
you could reasonably decide yourself. Skip nitpicks about wording.

If nothing important is left, say "nothing important left".
```

## Sort the answers

Sort what the builder asks into three piles:

- **Answered already** by the conversation or the project: add the answer to the close.
- **Minor:** a sensible builder could settle it without changing what gets built. Settle it yourself and mark it in the close as your call.
- **Theirs:** only the user can answer it, and the answer changes what gets built.

Bring the "theirs" pile to the user in one message, most important first, as one more `grilling` round. Update the close with the answers and list the calls you made. That is the only round the check produces.
