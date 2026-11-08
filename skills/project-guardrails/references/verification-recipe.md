# Verification recipe

Use this when a project has no repeatable way to launch the real app, exercise a feature the way a user does, and capture evidence. The output is a small project-local skill, `verify-<app>`, in the host's project skills folder (for example `.claude/skills/verify-<app>/` or `.agents/skills/verify-<app>/`). It follows this repository's spec rules: plain frontmatter, a "what + when" description.

## 1. Read the repository first

Answer from the code; ask the user only what cannot be observed.

- **Surface.** What a user touches: web UI, CLI, API, library, desktop app. Pick the primary one.
- **Run.** The repository's own start command, ports, environment variables, seed data.
- **Drive.** Existing harnesses first (Playwright specs, HTTP endpoints, CLI invocations), then a generic recipe.
- **Observe.** Screenshots, transcripts, response bodies, exit codes, database state.
- **Isolate.** Whether two instances can run side by side. If not, the generated skill says so.

If the project does not build or start as it is, fix that first or report it precisely.

## 2. Write the skill with these sections

- **Launch.** The exact command, the ready signal (usable, not just a live process), and teardown.
- **Doctor.** One read-only check: process up, right build, port owned by this run.
- **Drive.** Real commands and stable selectors from this repository.
- **Evidence.** What to capture and where. Exercise the real user path; capture the action and the resulting state, including side effects.
- **Cleanup.** Stop what this run started. Evidence survives cleanup, in a named location.

## 3. Prove it once

Run the generated skill end to end: launch, doctor, drive one feature, capture evidence, clean up, and confirm the evidence still exists. A generated skill that never ran is a draft.

## Credits

Adapted from pstack's `create-verification-skill` (see `LICENSE-pstack`), without its feature-map sweep and maintenance loop.
