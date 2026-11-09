---
name: bro
description: "Repair the last answer plainly when the user explicitly invokes bro. Quoted or incidental uses of the word do not select this entry."
license: MIT
metadata:
  source: "https://github.com/cursor/plugins/blob/6b0300214a09fd6029cfb7077043125758cd1fd2/pstack/skills/bro/SKILL.md"
  source-revision: "6b0300214a09fd6029cfb7077043125758cd1fd2"
  source-files: "pstack/skills/bro/SKILL.md"
  local-changes: "Replaced the duplicate writing method with a thin manual dispatch to the owned repair-last-message mode; preserved facts, meaning, and task authority."
  requires: "clear-communication"
---

# Bro

On an explicit bro request, read the `clear-communication` skill and select its **Repair your own last message** mode. Preserve the last answer's facts, meaning, uncertainty, and existing task limits.

Quoted or incidental bro text selects nothing. Repair the answer only; this entry starts no new task or writing workspace. If the required skill is unavailable, report it and stop this flow.

## Provenance

Read [the per-file sources](references/SOURCES.md) when checking attribution, original hashes, destinations, and adaptation.
