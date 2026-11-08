---
name: ketchup
description: Give a read-only catch-up on this chat since the user's last human message, with current work state and every pending user choice. Use when the user asks for ketchup or this catch-up; summarize a wider work period only when requested.
license: MIT
metadata:
  requires: "clear-communication"
  source: "https://github.com/cursor/plugins/blob/6b0300214a09fd6029cfb7077043125758cd1fd2/pstack/skills/ketchup/SKILL.md"
  source-revision: "6b0300214a09fd6029cfb7077043125758cd1fd2"
  source-files: "pstack/skills/ketchup/SKILL.md"
  local-changes: "Kept read-only since-last-human status and complete choices; added live revision checks and wider-window mode; distinguished commits from shipment; removed quotas and rendering mandates."
---

# Ketchup

Catch the user up on what changed since the last human message before this catch-up request, then lay out every decision still waiting on them. Notifications, tool results, hook output, and subagent reports do not reset that boundary. Assume the user remembers their own last message and needs the relevant changes after it.

Resolve and read the `clear-communication` skill (required) from the installed inventory. If it is unavailable, name the missing prerequisite and stop this flow. Keep the catch-up read-only: inspect current state without changing code, starting jobs or apps, rerunning CI, posting, merging, or enrolling a watcher.

## Gather the actual state

1. Collect requested work, tool evidence, agent reports, and relevant messages since the boundary. If the boundary or part of the conversation is unavailable, say which period the evidence covers.
2. Check the current state of the PRs, CI runs, tasks, and agents this chat touched through supported read-only host or connected tools. Prefer sufficient connected capabilities, then documented read-only CLI or API queries. Bind checks and reviews to the current relevant head/base and retain unresolved older review threads. A recorded report or previously passing run may be stale; label unavailable live state explicitly.
3. Distinguish written, committed, locally tested, integrated, published, and merged outcomes. A commit is evidence of a commit, not proof of shipment. A passing unit test supports its tested behavior, not an unobserved deployed or native surface. Check every displayed number and correct a prior incorrect figure plainly.
4. Gather **all pending user choices**, including choices raised before the latest message. Remove choices the user has already resolved or actions their existing authority already covers. Work the agent can still do is remaining agent work, rather than a fabricated user approval. Preserve each separate item even when several share one decision.

Done gathering when every material status has current evidence or a stated limitation, and every unresolved user-owned choice has enough context to decide.

## Give a self-contained catch-up

Open with the main change and what, if anything, waits on the user. Summarize each requested outcome in plain words with its actual state: complete, running, failed, blocked, or unchecked. Explain the user-visible change and the evidence that matters, without narrating routine tool steps. Name remaining agent work separately.

For each pending user choice, include the item and existing link, what the user must decide, the recommendation and its evidence, alternatives considered, costs or risk, and prerequisites. For a shared decision, state the decision once and give each affected item its own consequences and risk. Use `unknown` for missing decision-critical facts and explain how that limits the recommendation. Include waiting costs when there is a concrete deadline or other consequence beyond delay. Keep this report complete without requiring the user to follow a link to discover an omitted choice.

Use existing screenshots, a small diagram, or a chart only when it helps explain the change or options. Link only real artifacts, preserve their capture limits, and do not fabricate a screen, number, or missing proof. There is no word, item, picture, or video quota. If nothing changed and no choice remains, say so and stop.

## Requested wider-window mode

Enter this mode only for an explicit period such as yesterday, the last three days, or last week. Resolve concrete start/end dates, time zone, topic/project, and any author scope; state the range used. Use supported scoped history and authored commits as activity evidence, omitting merge-only and cosmetic noise where they add no substance. Check live PR, release, deployment, or artifact state before calling a change merged, published, or shipped. Keep reverted work visible when it affects the account of what remains delivered. Uncommitted work is pending context, rather than authored-commit output or a completed delivery. Do not infer motivation from a commit message. Carry forward pending user choices even when their origin predates the requested range. An ordinary team standup request retains its selected workflow; this skill does not claim every status or standup prompt.

Done when the user can understand the requested period, trust the status distinctions and limits, and decide every pending choice from the reply alone. Source files and adaptations: [references/SOURCES.md](references/SOURCES.md).
