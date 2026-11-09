---
name: handoff
description: Write a temporary continuation note so a fresh agent can pick up the current conversation from exact artifacts and the next unmet task. Use when the user asks for a handoff or a fresh-session summary, with any stated focus for the next session.
license: MIT
metadata:
  source: "https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/productivity/handoff/SKILL.md"
  source-revision: "49dd158d1076134a641b33efb035946536778336"
  source-files: "skills/productivity/handoff/SKILL.md"
  local-changes: "Combined both handoff entries; retained OS-temp storage, suggested skills, links and redaction; added exact state, proof and budget; removed background CLI launch."
---

# Handoff

Write a portable continuation note for an agent with no chat history, tailored to the next session's requested focus. Save it in the operating system's temporary directory, outside the current workspace. Resolve that directory through the host or runtime (`TMPDIR`, then the platform fallback; `TEMP` on Windows), and create a unique task-named file without overwriting another note. Use restricted file permissions where supported.

## Capture the continuation

1. Find the authoritative artifacts: the task or spec, run record, plan, decisions, branch/worktree, issue, and PR when present. Link to them by exact path or URL instead of copying their content. Preserve the active constraints and the source of consequential user decisions; an agent's interpretation is not a new human ruling.
2. Record what is on disk and what exists only in conversation. Save otherwise-lost context in the note, including an unfinished attempt, an important rejected path, or an unsaved decision. Keep artifact identities precise enough to detect later drift: hashes or revisions for proof, exact host task/run links for active work.
3. Separate implemented, tested, integrated, published, and merged state. Cite the check, artifact revision, observed result, and known gaps; a commit alone proves none of the later states. Include owned dirty files, partial effects, active or uncertain workers, and unresolved user choices.
4. Carry forward the remaining starts, retries, review rounds, active slots, and reserves from the run's authoritative budget. Use `unknown` for unavailable counters and identify where to reconcile them. A new agent receives the same spent budget and existing authority.
5. Name the first ready unmet condition, its prerequisites, the next concrete action, and any stop boundary. Include a **Suggested skills** section with relevant installed owned names and why each applies. Write each suggestion as "the `<name>` skill" and tell the successor to resolve and read its SKILL.md before using it. A suggestion grants no new authority and is not a command to run every named method.

Use [assets/handoff.md](assets/handoff.md) when a note needs a template. Its headings are a coverage aid; keep the result proportional to the task.

## Verify the note

Read the saved file from its returned path and follow the material pointers. Check that the new reader can find the run, actual work, unresolved choices, and next action using the note alone. Keep requested questions, checklists, or other continuation material reachable in full and in the requested order. Mark stale, missing, private, or inaccessible pointers rather than inventing their contents.

Redact credentials, private tokens, passwords, unnecessary personal data, and sensitive command output from the note. Use safe locators to access-controlled evidence instead of copying secret-bearing source bodies or credential-bearing URLs. Preserve enough non-sensitive identity for the intended successor to locate the right artifact.

The note summarizes continuation; it does not replace authoritative plans or decision records. Temporary storage may be cleared, so state that limit when the expected interruption requires durable retention and point to the existing durable run record. Writing a handoff does not launch a thread or agent, commit changes, push, cancel work, or pause an ongoing authorized task. Those actions use the user's actual instruction and the host's supported mechanisms.

For a known run, use the `decision-log` skill when installed to reconcile and resume it. The `recall` skill, when installed, finds a prior run whose locator is unknown.

Done when the saved note contains no secrets, its material pointers resolve or name a limitation, and the successor can take the next permitted action without reconstructing the conversation. Return its absolute path and a short description of the continuation point. Source files and adaptations: [references/SOURCES.md](references/SOURCES.md).
