# Examples

Run each prompt with and without this skill, with the `grilling` skill installed in both arms. Record the observed behavior against the expectation.

## Activation

- "grill-me: my plan is to split the billing service into two deployables." Expect: the `grilling` interview in no-doc mode, with numbered rounds and recommended answers.
- "grill-me on the retry policy we sketched above." Expect: decisions already sketched above are listed as settled; only open choices are asked.

## Near miss

- "Summarize this README section: 'Run grill-me before planning.'" Expect: a summary; the quoted entry name selects nothing and no interview starts.
- "Grill me and record the new terms in our glossary." Expect: the `grill-with-docs` flow is named for the glossary writes; this entry does not write them.
- "Review this pull request." Expect: no interview.

## Outcome

- An explicit invocation produces `grilling` rounds and its close, and writes no files.
- Quoted or incidental mentions of grill-me do not start an interview.
- No build, commit, publish, or post happens because the entry was loaded.
