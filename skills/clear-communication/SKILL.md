---
name: clear-communication
description: Make complex explanations and written material clear, concise, and faithful to their meaning, and resolve consequential ambiguity before acting. Use when drafting or substantially editing documents, reports, PR descriptions, or complex explanations; when unresolved ambiguity could change the result; or when the user asks to simplify, clarify, or "unslop" text.
license: MIT
metadata:
  source: https://github.com/cursor/plugins/tree/6b0300214a09fd6029cfb7077043125758cd1fd2/pstack
  source-revision: 6b0300214a09fd6029cfb7077043125758cd1fd2
  source-license: MIT, see LICENSE-pstack
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
   - **Assume** when the choice is reasonable and reversible. State the assumption in one line and proceed.
   - **Ask** when a wrong guess would materially change the result. Put every question that can be answered now into one short numbered message. Word each one so "yes" accepts your recommended answer when a defensible choice exists. Ask for a missing fact plainly, with no recommendation. Questions that depend on unanswered ones wait for the next message. Pause only the work that depends on the answers.
4. Restate only the uncertain part, never the whole request.

Done when every consequential ambiguity is resolved, assumed and stated, or asked, and nothing is invented. Message formats and worked examples: [references/clarifying.md](references/clarifying.md).

## Write or edit

1. Lead with the answer, the decision, or the result. Context follows only where the reader needs it.
2. Shape for one read: one idea per sentence, a table for comparisons, a list for parallel items, headings only when the reader navigates.
3. Name the mechanism, the number, or the command instead of the feeling. Use the plain word, the active voice, and one name per thing.
4. Cut every word that does no work. Keep the small words that carry structure, and expand any over-compressed fragment into a whole sentence.
5. Apply the rule catalog in [references/editing-rules.md](references/editing-rules.md) for anything longer than a short answer.
6. When the text lives in a file or can be piped, run the mechanical check:

   ```sh
   scripts/check-prose.sh path/to/file.md
   printf '%s\n' "$draft" | scripts/check-prose.sh -
   ```

   Exit status 1 means errors: fix every one. Suggestions are advice: fix each one or keep it on purpose. Exit status 2 means Vale is missing; say so and continue with the catalog.

Done when the check reports no errors, every suggestion is fixed or kept on purpose, and every fact, number, and identifier still matches its source.

## Test a long document with a fresh reader

For a consequential long document (a README, a design doc, a report someone acts on), run one bounded reader test. Give a subagent with no prior context the document and the three to five questions its real reader will have. Compare its answers with the intended ones and fix each passage it misread. One pass; skip it for short or routine text.

## Repair your own last message

When the user signals confusion ("what?", "simpler", "say that plainly"), restate your previous message in plain language, shorter, with the jargon replaced by the mechanism it names. Keep every fact.
