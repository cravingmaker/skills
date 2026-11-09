# Examples

Run each prompt with and without this skill in a fixture project that contains the mistake in its history. Record the observed behavior against the expectation.

## Activation

- "You imported from the internal module again. That's the third time." Expect: the recurrence named with its evidence, a remedy at the highest workable layer (for example, an export map or lint rule that makes the internal import fail), and proof on the real past import.
- "Make it impossible to forget the `await` on `db.query` again." Expect: a type or lint remedy whose error names the fix, proven against the earlier mistake.

## Near miss

- "Fix this typo in the README." Expect: the typo fixed; no structural remedy.
- "This test failed once in CI; can you look?" Expect: a diagnosis of the single failure; no recurrence machinery.

## Outcome

- The remedy rejects the historical mistake and accepts valid code, both shown with command output.
- When a type or lint remedy works, no rule is added to the agent instructions.
- No commits, history sweeps, or instruction-file edits happen unless the user asked.
