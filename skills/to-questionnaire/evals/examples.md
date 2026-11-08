# Examples

Run each prompt with and without this skill in an empty working directory. Record the observed behavior against the expectation.

## Activation

- "to-questionnaire: I need to pick a payment provider but our finance lead, Dana, knows the settlement and refund constraints. I need to know which settlement windows and chargeback rules we must support. It goes to Dana by email next week." Expect: no questions to the user; a draft file whose questions cover settlement windows and chargeback rules, pitched to a finance lead.
- "Make a questionnaire for our infra contractor about the migration." Expect: one message asking only what the user needs back; then the draft.

## Near miss

- "Grill me on the payment provider choice." Expect: the `grilling` skill; no questionnaire.
- "Draft an email to Dana asking when they're free." Expect: an email draft, not a questionnaire.
- "Write a customer satisfaction survey for our users." Expect: a survey for many respondents, not a one-recipient discovery questionnaire.

## Outcome

- When recipient, purpose, and needs are all supplied, no question is asked before the draft is written.
- Every stated need maps to at least one question, and no question asks for a fact the user already gave.
- The draft exists as a local file at the reported path, and nothing is emailed, posted, or published.
