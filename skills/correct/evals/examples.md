# Examples

Run each prompt with and without this skill in a fixture project that contains the mistake in its history. Record the observed behavior against the expectation.

## Activation

- "You imported from the internal module again. That's the third time." Expect: the recurrence named with its evidence, a remedy at the highest workable layer (for example, an export map or lint rule that makes the internal import fail), and proof on the real past import.
- "Make it impossible to forget the `await` on `db.query` again." Expect: a type or lint remedy whose error names the fix, proven against the earlier mistake.

- A judgment mistake recurred twice and no mechanical check can decide it. Expect a scoped standards rule with a bad/good example that the `change-review` skill reads.

## Near miss

- "Fix this typo in the README." Expect: the typo fixed; no structural remedy.
- "This test failed once in CI; can you look?" Expect: a diagnosis of the single failure; no recurrence machinery.

- A single reviewer prefers a different name. Expect task-scoped judgment without a standing rule or history sweep.

## Outcome

- The remedy rejects the historical mistake and accepts valid code, both shown with command output.
- When a type or lint remedy works, no rule is added to the agent instructions.
- No commits, history sweeps, or instruction-file edits happen unless the user asked.
- The smallest effective remedy rejects the past mistake, accepts the valid counterexample and repeats without another content edit. Structural enforcement adds no duplicate prose; edits, commits and instruction changes preserve existing authorization.
