# Root-cause tracing

Read this when the error surfaces deep in a call stack, when a fix keeps not holding, or when deciding where a guard belongs. Adapted from Superpowers' root-cause-tracing.md and defense-in-depth.md and pstack's fix-root-causes and attack-the-premise principles.

## Trace backward

The symptom is where a wrong state became visible; the cause is upstream. Walk back one call at a time:

1. **Observe the symptom.** `Error: git init failed in ~/project/packages/core`
2. **Find the immediate cause.** `await execFileAsync('git', ['init'], { cwd: projectDir });`
3. **Ask what called this, with what value.** `WorktreeManager.createSessionWorktree(projectDir)` ← `Session.initializeWorkspace()` ← `Session.create()` ← a test's `Project.create()`. The value: `projectDir = ''`, and an empty `cwd` resolves to `process.cwd()`, the source directory.
4. **Keep going until the value's origin.** The test read `context.tempDir` before `beforeEach` had set it; the setup returned `{ tempDir: '' }`.
5. **Fix at the origin.** Here, make `tempDir` throw if read before setup.

When you can't trace by reading, log a stack trace just before the dangerous operation, with the relevant inputs (directory, cwd, the specific variable, not the whole environment). In tests, write to stderr, since loggers may be suppressed. Then look for the test file, the line and the repeated parameter in the traces.

## Fix the cause, not the place it surfaced

- Ask "why" at each step until the answer is a wrong decision in the code, not a consequence of an earlier one.
- Read the actual error and the actual state. Do not guess.
- Ask whether the triggering state is legitimate. If the system may be in it, the code that broke on it is the cause and handling the state there is the fix. If the state should never exist, a check where it broke hides the bug: guards, retries, swallowed errors, clamped values and discarded state are the usual ways to hide one.
- When something fails only after a restart, suspect persisted state first: config files, caches, lock files, serialized state.
- Check for the pattern, not just the instance; fix every place with the same fault.
- A workaround that needs a paragraph of comment to justify it usually means the code is wrong.
- If the deciding fact took a deep dig, propose the cheap, always-on signal (a log line, an assertion, a metric) that would have shown it at first look.

## Attack the premise

When two or more fixes that share one premise have failed the same check, suspect the premise, not the fixes. Each failed fix is evidence against the belief it assumed.

- **Write the premise down**: the one sentence every failed fix assumed.
- **Test it before the next fix**: find an observation that would come out differently if the premise were false, and make it rerunnable. Look at how failures are distributed, not only how large they are.
- **Follow the evidence.** If it contradicts the premise, the cause is elsewhere: look for what the failures share that the premise did not predict. If it confirms the premise, ask the next "why"; the earlier fixes may have treated a consequence.
- **Remove the condition instead of compensating for it.** A mechanism that cleans up after a cause leaves the cause in place and adds work on every run.

## Where guards belong

After fixing at the origin, consider guards only where they add real protection:

- **At trust boundaries**: user input, network and IPC messages, config, environment, files and any internal privilege transition. "Internal" does not mean trusted; validate where data crosses from a less trusted context.
- **At dangerous operations in a specific context**, such as refusing `git init` outside a temp directory during tests.
- **Not at every layer.** Inside a trusted path, typed data from a validated boundary needs no repeated checks; redundant validation hides where the real check lives.

Keep existing legitimate defensive checks; removing one is a behavior change that needs its own justification. Test a new guard by trying to bypass the layer before it.
