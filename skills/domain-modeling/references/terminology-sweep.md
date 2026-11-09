# Terminology sweep

Read this when a settled term replaces an old one outside the glossary: in UI text, API names, docs, or translations. The glossary stays the authority; the sweep makes every other surface agree with it.

## The term record

Each swept term has one record in the glossary entry, using the format in [glossary-format.md](glossary-format.md):

- **Preferred form:** the exact spelling and casing.
- **Definition:** one or two sentences.
- **Rejected variants:** the `_Avoid_` list, including the old term.
- **Authority:** the `_Source_` link for the decision behind the rename.
- **Context notes:** where a variant is correct in another context, and translation notes for each locale the project ships.

## Sweep

1. Update the glossary record first, within the authority rules in the skill.
2. Search every surface in scope for the old term and each rejected variant: UI strings and message catalogs, docs, API names and schemas, code identifiers, and tests.
3. Classify each hit:
   - **Domain use in prose or UI text:** rename it.
   - **Another context's correct use:** keep it; the context note explains why.
   - **Quoted or source text** (a quotation, a legal text, a log, an external API's field): keep it exactly.
   - **Public identifier** (an API field, a URL, a persisted value, an event name other systems consume): keep it, or plan an expand-contract migration with the project's deprecation policy. Renaming it in place breaks consumers.
   - **Unrelated meaning:** keep it.
4. Change only the hits inside the authorized scope, and report the rest with their class.
5. When the project runs Vale, add the preferred form to its accepted vocabulary and the rejected variants to a substitution rule. Show the rule rejecting an old-term sample and accepting the preferred form before relying on it.

## Report

List each changed hit, each kept hit with its class, and each public identifier left for a migration. Done when every in-scope hit is renamed or kept with a stated class.
