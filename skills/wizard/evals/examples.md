# Examples

Run each prompt with and without this skill. Record the observed behavior against the expectation.

## Activation

- "Make a setup script that walks me through getting Stripe keys into .env and GitHub secrets." Expect: reads .env.example and the workflows, finds the env loader, confirms the stages, copies the template, authors stages, and round-trips dummy values through the project's loader.
- "I need to rotate the database password across three dashboards; walk me through it step by step." Expect: a wizard with one focused stage per dashboard and a `confirm` before each irreversible action.

## Near miss

- "Add STRIPE_KEY=pk_test_123 to .env." Expect: the agent edits the file itself; no wizard.
- "Set up pre-commit hooks for this repo." Expect: the agent can do this itself; no wizard.
- "Write a bash script that runs the migrations." Expect: an ordinary script, not a human-guided wizard.

## Outcome

- With `ENV_FORMAT=dotenv`, the dummy value `O'Reilly` reads back exactly through python-dotenv, Node's parser and `sh`; a value with a backslash or line break is refused with exit 1 and the file is unchanged.
- Repeated runs keep unrelated keys, comments and multi-line values byte for byte, offer saved values without displaying them, and leave one line per key.
- `ENV_FILE` outside the directory, a symlink, or a git-tracked file is refused unless opted in; secrets are entered hidden and never printed; `bash -n` alone is not reported as proof that values persist correctly.
