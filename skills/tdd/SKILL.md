---
name: tdd
description: Test-driven development through public seams, with a failing test that measures the right behavior before the fix. Use when the user wants to build features or fix bugs test-first, mentions red-green-refactor, asks for a regression test, or wants integration tests.
license: MIT
metadata:
  requires: "codebase-design"
  source: "https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/tdd/SKILL.md"
  source-files: "skills/engineering/tdd/SKILL.md"
  source-revision: 49dd158d1076134a641b33efb035946536778336
  local-changes: "Merged pstack's cheap-regression cadence, better-no-test-than-a-bad-test rule and evidence report, pstack's test-behavior principle, and Superpowers' predicted-failure check and test-quality gates; unattended approved work records the highest suitable existing seam instead of waiting for confirmation; removed universal TDD, delete-and-restart and forced failing commits."
---

# Test-driven development

TDD is the red → green loop. This skill is the reference that makes that loop produce tests worth keeping: what a good test is, where tests go, the anti-patterns, and the rules of the loop. Consult every section before and during the loop, not after.

When exploring the codebase, read the project's domain glossary (if it exists) so test names and interface vocabulary match its language, and respect decision records in the area you're touching. For module, interface, depth and seam vocabulary, read the `codebase-design` skill: it is a reference to consult, not a session to run.

## When to use it

Use the loop when the user asks for test-first work or a regression test, when an approved ticket names test-first work, or when a bug or behavior has a cheap, meaningful test path. Skip a new test when the only available test would be a bad one (see below), and use the closest useful executable check instead. A trivial, reversible change (a typo, a config value no logic reads) needs no new test.

**Prefer no new test over a bad test.** A bad test mostly tests mocks, encodes current implementation details, depends on timing or unrelated global state, needs expensive infrastructure for a small change, or would be deleted right after proving the fix. When you skip, say why and name the check you used instead.

## What a good test is

Tests verify behavior through public interfaces, not implementation details. Behavior is what the code's users can observe: return values, errors, state they can read back, and effects on systems outside the code (a request sent, a row written, a message emitted). A good test reads like a specification: "user can checkout with valid cart" tells you exactly what capability exists.

Judge each test against two imagined edits:

- **Break the behavior** (a wrong value, a skipped effect, an effect done twice). If the test still passes, it proves nothing.
- **Change only the internals** (same observable results, restructured code). If the test now fails, it is pinned to the implementation.

Keep a test that catches the first edit and survives the second. Expected values come from an independent source of truth: a known-good literal, a worked example, the spec. See [references/tests.md](references/tests.md) for examples and gates, and [references/mocking.md](references/mocking.md) for where mocks belong.

## Seams: where tests go

A **seam** is the public interface you test at: where you observe behavior without reaching inside. Tests live at seams, never against internals.

Use the seams already agreed: in the spec or ticket, or by the user. When no seam is agreed:

- **With the user present,** propose the seams before writing a test, each with a one-line note on what it catches and what it misses, and confirm them. Agreeing seams up front puts testing effort on the critical paths and complex logic instead of every edge case.
- **In unattended approved work,** choose the highest existing seam that reaches the behavior through its real call path, record the seam and its catch/miss note in your report, and proceed. Do not stall the run waiting for confirmation.

When the shape of that interface is itself in question (how deep the module is, where the seam belongs, what the interface should expose), use the `codebase-design` skill's vocabulary and heuristics.

## Anti-patterns

- **Implementation-coupled**: mocks internal collaborators, tests private methods, or verifies through a side channel (querying the database instead of using the interface). The tell: the test breaks when you refactor but behavior hasn't changed.
- **Tautological**: the assertion recomputes the expected value the way the code does (`expect(add(a, b)).toBe(a + b)`, a snapshot derived by hand the same way, a constant asserted equal to itself), so it passes by construction.
- **Horizontal slicing**: writing all tests first, then all implementation. Bulk tests verify imagined behavior and commit to test structure before you understand the implementation. Work in **vertical slices**: one test → one implementation → repeat, each test a **tracer bullet** that responds to what the last cycle taught you.
- **Change detector**: only an intentional decision (a constant's value, exact message wording no caller reads) can fail it. Test the behavior that depends on the decision instead; a constant that is a documented promise to users is behavior, so name that promise.

## Rules of the loop

1. **Name the break.** Before writing the test body, name the production change that should make it fail. If you cannot name one, redesign the test around an observable behavior.
2. **Red, for the predicted reason.** Write the failing test first and run it. Confirm it fails because the behavior is missing or wrong, not because of a typo, an import error, a missing fixture or other setup. Quote the failure content, not just the assertion line: an exception, an empty result and the predicted mismatch all print red, and only the predicted mismatch proves the test measures the behavior. A test that passes before the change is a finding about the test or about existing behavior.
3. **Green, minimally.** Write only enough code to pass. Don't anticipate future tests or add speculative features. Fix the code, not the test; never weaken an assertion to match a wrong implementation.
4. **One slice at a time.** One seam, one test, one minimal implementation per cycle.
5. **Refactor only on green.** Remove duplication and improve names within the slice, rerunning the tests after each step. Structural changes beyond the slice belong in review (the `change-review` skill), not in the loop.
6. **Run the project's suite.** A green run of your new test is not a green suite. Before calling the work done, run the project's relevant test command and report every failure it shows by name, including ones you did not cause.

Keep the work you are changing. Do not delete existing code to restart test-first, and do not rewrite existing tests to fit new code unless the expected behavior genuinely changed and you say why. Preserve exact values, numeric precision, unknown fields, rationale comments and existing consumer behavior. Red evidence lives in your run output and report; it does not need a separately landed failing commit.

## Bugs

For a bug, make the broken behavior executable before changing production code: the smallest focused test at a seam that reproduces the real failure as it occurs at the call site. If the only seam available cannot replicate the chain that triggers the bug, that test gives false confidence; record the missing seam as a finding and use the closest executable check. Flaky bugs need a deterministic test where possible; name the signal being locked down. Land the focused regression first, then consider sibling coverage for a broader class.

## Report

Done when every slice went red for its predicted reason, then green, and the relevant suite passed. Report the evidence, not just the outcome:

- the failing-before test or check, with its failure quoted and trimmed to the decisive lines;
- the passing-after run and the suite command with its result;
- the seam chosen and why, when it was not agreed beforehand;
- when failing-before evidence could not be shown, why, and the closest check used instead.

## Provenance

Adapted from Matt Pocock's tdd skill, with material from pstack's tdd skill and test-behavior principle and Superpowers' test-driven-development skill. See [references/SOURCES.md](references/SOURCES.md) and the `LICENSE-*` files.
