# Editing rules

Apply these when writing or editing anything longer than a short answer. Example phrases are in code font so the linter skips them. Rule numbers are the stable IDs of pstack's `unslop` catalog, so missing numbers are rules this repository does not use. Each rule marked **Vale** is also checked by `scripts/check-prose.sh`: *error* fails the check, *suggestion* is advice.

Accuracy outranks every rule. When a rule would change a fact, a quotation, a technical term, or a stated uncertainty, keep the original.

## Content

- **3. Superficial "-ing" phrases.** "highlighting...", "ensuring...", "reflecting..." tacked onto a sentence. Delete the phrase, or state the consequence as its own sentence with its evidence.
- **5. Vague attributions.** "Experts believe", "Some argue". Name the source or delete the claim.

## Language

- **7. AI vocabulary.** `delve`, `tapestry`, `testament`, `pivotal`, `showcase`, `foster`, `garner`, `intricate`, `interplay`, `vibrant`, `enduring`, `underscore`. Use the plain word that fits. **Vale:** suggestion.
- **8. Fancy "is".** `serves as`, `stands as`, `boasts`. Say "is" or "has". **Vale:** suggestion.
- **9. "Not just X, but Y."** State the point directly.
- **10. Forced triads.** Use the natural number of items, not three by habit.
- **11. Synonym cycling.** One name per thing, everywhere in the document.
- **12. False ranges.** "from X to Y" where X and Y share no scale. List the items.

## Style

- **13. Em dashes.** Allowed by default. A project can ban them by setting `ClearCommunication.EmDash = YES` in its Vale config. **Vale:** error when enabled.
- **14. Colon crutches.** A colon introduces a list or an example, not a dramatic reveal mid-sentence.
- **15. Bold overuse.** Bold names an item in a lead-in or one critical term, not every noun.
- **16. Inline-header lists.** "**Performance:** Performance improved" restates its label. A bold lead-in that ends in a period and is followed by new detail is fine.
- **17. Title-case headings.** Use sentence case; proper names keep their capitals. **Vale:** suggestion.
- **18. Decorative emoji.** Remove them from headings and bullets. **Vale:** error in headings.
- **19. Curly quotes.** Use straight quotes. **Vale:** error.

## Communication artifacts

- **20. Chatbot phrases.** `I hope this helps`, `Great question`, `Feel free to ask`. Delete them. **Vale:** error.
- **22. Sycophancy.** `You're absolutely right`. Respond to the substance. **Vale:** error.

## Filler

- **23. Filler phrases.** `in order to` is "to"; `due to the fact that` is "because"; `it is important to note that` is nothing. **Vale:** error.
- **24. Stacked hedges.** `could potentially` becomes "may". Keep one hedge that states the real uncertainty. **Vale:** suggestion.
- **25. Generic conclusions.** "The future looks bright." End on the specific next step or fact, or end without a conclusion.

## Jargon

- **26. Metaphor nouns.** `north star`, `flywheel`, `paradigm`, `nexus`, `bedrock`, `endgame`. Name the concrete thing. Technical terms such as "vector", "primitive", and "surface" stay when they are the precise term. **Vale:** suggestion for the listed words.

## Plain speech

- **27. Say what it does, not how it feels.** "a column rename fails the build", not "types that follow your schema". If a sentence could appear unchanged in another project's docs, it says nothing about this one.
- **28. Dense sentences.** If the reader must backtrack, split the sentence. One idea per sentence; a long sentence that carries one idea with its condition stays.
- **29. Active voice.** Name the actor: "the compiler validates queries". Passive is fine when the actor is unknown or irrelevant.
- **30. Adverb props.** "runs quickly" becomes the number; "significantly improves" becomes the measured change.
- **31. Plain words.** "use", not `utilize`; "help", not `facilitate`; "many", not `numerous`; "before", not `prior to`. **Vale:** suggestion.
- **32. Mannered prose.** Aphorisms, personified code, figurative verbs. Say the literal thing.
- **33. Over-compression.** Dropped articles, verbless fragments, arrows, and unexplained abbreviations. "Parser rejects bad date → exit 2" becomes "The parser rejects a bad date and exits with code 2." This rule adds words.

## Technical writing essentials

- **Pick the document type first.** Tutorial (learning by doing), how-to (steps to a goal), reference (facts for lookup), explanation (why). One type per document; link the others.
- **Use the codebase's words.** Write the real symbol, file, flag, or command, in code font.
- **Write instructions as commands,** with the condition first: "To delete the document, click Delete."
- **Keep "only" and "not" next to the word they change,** and make every "it", "they", and "this" point at one obvious thing.
- **Keep the articles and small structural words.** "Remove the backup file" reads one way; "Remove backup file" reads two.
- **Mix sentence lengths.** Short sentences land a point; longer ones carry a fact with its condition.
- **Link with words that say where the link goes,** never "click here".
- **PR descriptions and commit messages** follow every rule above except document type. A reviewer reads a PR body in under a minute.

## Explaining something

When the reader asks to understand rather than to act:

- Infer what they need from why they are asking and what they already know; do not quiz them.
- Give the smallest complete answer first: what the thing is and how it works, in a sentence or two. Add depth when they ask.
- Show the code, the diff, or the output when that is faster than describing it.
