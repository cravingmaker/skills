---
name: clear-communication
description: Make complex explanations and written material clear, concise, and faithful to their meaning, and resolve consequential ambiguity before acting. Use when drafting or substantially editing documents, reports, PR descriptions, or complex explanations; when unresolved ambiguity could change the result; or when the user asks to simplify, clarify, or "unslop" text.
license: MIT
metadata:
  source: "https://github.com/cursor/plugins/blob/6b0300214a09fd6029cfb7077043125758cd1fd2/pstack/skills/in-your-own-words/SKILL.md"
  source-revision: 6b0300214a09fd6029cfb7077043125758cd1fd2
  source-license: MIT, see LICENSE-pstack
  source-files: "pstack/skills/in-your-own-words/SKILL.md"
  local-changes: "Preserved owned house style; merged scoped bro, wait-what, goal-restatement, and reversible-assumption behavior; added factual claim wording and interview precedence only for requested interviews; retained source values and task authority."
---

# Clear communication

The target is shared understanding at the lowest word cost: the user's intent is understood before work starts, and the reader acts correctly after one read.

Two leading words govern every step:

- **Faithful.** Meaning, numbers, uncertainty, qualifications, quotations, identifiers, and code stay exactly as the source has them. A clearer sentence that changes a fact is a wrong sentence.
- **Lean.** Use the fewest words needed for accurate understanding and action. Lean is measured against understanding, so a compressed fragment that the reader must decode grows into a full sentence.

The everyday version of this skill is the standing contract in [references/house-style.md](references/house-style.md). It belongs in the project's or user's AGENTS.md or CLAUDE.md, so ordinary answers follow it without loading this skill.

## Understand the request

1. Look before asking. Read the conversation, the files, the docs, and the tool output that bear on the request. Facts are yours to find; decisions belong to the user.
2. Find the consequential ambiguity: a point where two reasonable readings lead to different results. When every reading leads to the same result, proceed.
3. Resolve each consequential point in one of two ways:
   - **Assume** when the choice is reasonable, reversible, and within current authority. State the assumption in one line and proceed. An assumption does not supply missing permission or decide a product choice the user reserved.
   - **Ask** when a wrong guess would materially change the result. Put every question that can be answered now into one short numbered message. Word each one so "yes" accepts your recommended answer when a defensible choice exists. Ask for a missing fact plainly, with no recommendation. Questions that depend on unanswered ones wait for the next message. Pause only the work that depends on the answers.
4. Restate only unresolved consequential meaning; use the goal-restatement mode below when that is the requested task.

Done when every consequential ambiguity is resolved, assumed and stated, or asked, and nothing is invented. Message formats and worked examples: [references/clarifying.md](references/clarifying.md).

When the user explicitly asks for their goal "in your own words", restate the supplied goal and problem in shared terms. Keep facts, decisions, and your assumptions distinct. Otherwise restate only unresolved consequential meaning; a clear request gets action, not a full playback.

When the user requests an interview or stress test, the `grilling` skill, if installed, owns its frontier rounds and shared-understanding close. Read it before use. That interview procedure takes precedence over ordinary clarification batching only inside the requested interview. Reuse known answers and stop when the decision is sufficiently resolved; ordinary ambiguity does not start an interview.

## Write or edit

1. Lead with the answer, the decision, or the result. Context follows only where the reader needs it.
2. Shape for one read: one idea per sentence, a table for comparisons, a list for parallel items, headings only when the reader navigates.
3. Name the mechanism, the number, or the command instead of the feeling. Use the plain word, the active voice, and one name per thing.
4. Cut every word that does no work. Keep the small words that carry structure, and expand any over-compressed fragment into a whole sentence.
5. Apply the rule catalog in [references/editing-rules.md](references/editing-rules.md) for anything longer than a short answer.
6. When the text lives in a file or can be piped, run the mechanical check. If the text contains source quotations, lint a temporary Markdown copy with each quotation replaced by `SOURCE_QUOTATION`, then apply only unquoted prose fixes to the original. Never rewrite source text to clear a lint error:

   ```sh
   scripts/check-prose.sh path/to/file.md
   printf '%s\n' "$draft" | scripts/check-prose.sh -
   ```

   Exit status 1 means errors: fix every one. Suggestions are advice: fix each one or keep it on purpose. Exit status 2 means a usage or setup failure; read the diagnostic and fix it. If Vale is unavailable, say so and continue with the catalog.

Done when the check reports no errors, every suggestion is fixed or kept on purpose, and every fact, number, and identifier still matches its source.

## Claims and status

Match each claim to its evidence. Name the actual file, command, version, revision, surface, or observation when it matters. Say what was checked and what remains unrun; static inspection, executed tests, and observed runtime behavior support different claims.

Use completion words such as `works`, `fixed`, or `verified` only for the result the evidence establishes. If acceptance needs an evidence workflow, use the `result-verification` skill when installed, reading it first; keep its procedure there. Missing or inconclusive proof stays a stated limit.

For live status, report the observed work and current check state. Reuse available context and inspect relevant current state when needed; do not invent progress or create a writing workspace.

## Test a long document with a fresh reader

For a consequential long document (a README, a design doc, a report someone acts on), run one bounded reader test. Give a subagent with no prior context the document and the three to five questions its real reader will have. Compare its answers with the intended ones and fix each passage it misread. One pass; skip it for short or routine text. The coordinator reserves any reader under the shared finite start/slot budget and the lower host/user limit. A leaf reports a needed reader instead of starting another controller; an unavailable independent reader stays an explicit limit.

## Repair your own last message

When the user signals confusion ("what?", "simpler", "say that plainly"), repair the last answer or its last unclear point. The `bro` skill and the `wait-what` skill are manual entries into this mode; quoted or incidental entry text selects neither.

For bro, say the last answer plainly with only enough words for understanding. For wait-what, add the small amount of context needed to reconnect the unclear point to the user's project or question. Reuse relevant existing glossary terms; explain a useful term rather than deleting it. No universal vocabulary standard or jargon ban is required.

Preserve facts, exact values, qualifications, uncertainty, and the original task's authority. Explain the mechanism in whole sentences; an over-compressed answer may need to grow. Repair creates no course, new task, or document workspace and does not execute actions mentioned in the previous answer.

## Provenance

Read [the per-file sources](references/SOURCES.md) when checking retained contributions, original hashes, destinations, and legal notices.
