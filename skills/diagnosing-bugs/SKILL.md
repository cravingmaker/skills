---
name: diagnosing-bugs
description: Diagnose bugs and performance regressions through reproduction, ranked hypotheses and causal checks. Use for failures, slow behavior or "debug this"; an explicitly selected host debug command keeps its route.
license: MIT
metadata:
  source: "https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/engineering/diagnosing-bugs/SKILL.md"
  source-files: "skills/engineering/diagnosing-bugs/SKILL.md"
  source-revision: 49dd158d1076134a641b33efb035946536778336
  local-changes: "Kept the feedback-loop phases; allowed capture and static diagnosis with stated limits when no runtime loop exists; merged pstack's bug-fix, performance, runtime and trace playbooks and attack-the-premise and fix-root-causes principles, and Superpowers' backward tracing and premise reset; defenses go at real trust boundaries; removed mandatory interactive and live gates; audited the HITL template."
---

# Diagnosing bugs

A discipline for hard bugs. Skip phases only when explicitly justified, and say which and why.

When exploring the codebase, read the project's domain glossary (if it exists) to get a clear model of the relevant modules, and check decision records in the area you're touching.

## Redact

This skill has you show commands, outputs and captured artifacts. **Redact every secret first**: write `<REDACTED>` in its place. Build loops against environment variables, so the credential stays in the environment rather than in what you show. Captured artifacts carry auth headers: quote only the lines that carry the signal. Check whether a variable is set rather than printing it, and never dump a whole environment, config or transcript.

If the redacted output is not enough to diagnose the bug, say so and ask the user.

## Phase 1: build a feedback loop

**This is the skill.** If you have a **tight** pass/fail signal for the bug (one that goes red on _this_ bug), bisection, hypothesis testing and instrumentation all just consume it. Spend disproportionate effort here.

Ways to construct one, in roughly this order:

1. **Failing test** at whatever seam reaches the bug: unit, integration, end to end.
2. **Curl / HTTP script** against a running dev server.
3. **CLI invocation** with a fixture input, diffing stdout against a known-good snapshot.
4. **Headless browser script** (Playwright / Puppeteer) that drives the UI and asserts on DOM, console or network.
5. **Replay a captured trace.** Save a real request, payload or event log to disk; replay it through the code path in isolation.
6. **Throwaway harness.** A minimal subset of the system (one service, mocked dependencies) that exercises the bug path with one call.
7. **Property / fuzz loop.** For "sometimes wrong output", run many random inputs and look for the failure mode.
8. **Bisection harness.** If the bug appeared between two known states (commit, dataset, version), automate "boot at state X, check" so you can `git bisect run` it.
9. **Differential loop.** Run the same input through old and new versions (or two configs) and diff the outputs.
10. **Human-in-the-loop script.** Last resort. If a human must click, structure their steps with [assets/hitl-loop.template.sh](assets/hitl-loop.template.sh) and read back what they capture.

Reproduce on the surface the user reported (the browser, the packaged app, the CLI); a unit test shows branch behavior, not that the user's symptom is gone.

**Tighten the loop.** Make it faster (cache setup, skip unrelated init, narrow scope), sharper (assert the specific symptom, not "didn't crash") and more deterministic (pin time, seed randomness, isolate the filesystem, freeze the network). A 30-second flaky loop is barely better than none.

**Non-deterministic bugs.** The goal is a higher reproduction rate, not a clean repro: loop the trigger, parallelise, add stress, narrow timing windows. Wait on the condition you need rather than a fixed sleep. A 50% flake is debuggable; 1% is not, so raise the rate until it is.

**When no runtime loop is possible** (no environment, no access, no reproduction): say so, list what you tried, and ask for (a) access to an environment that reproduces it, (b) a redacted captured artifact (HAR file, log, profile, core dump, recording with timestamps), or (c) permission for temporary instrumentation. Meanwhile, diagnosis from a capture or from the code is valid for a claim it can support: label the result "from capture" or "static", state what it cannot rule out, and never call the cause confirmed without discriminating evidence.

**Completion criterion.** Phase 1 is done when you can name **one command** you have **already run** (show it and its redacted output) that is:

- [ ] **Red-capable**: it drives the actual bug path and asserts the **user's exact symptom**, so it goes red on this bug and green once fixed.
- [ ] **Deterministic**: same verdict every run (flaky bugs: a pinned, high reproduction rate).
- [ ] **Fast**: seconds, not minutes.
- [ ] **Agent-runnable**: you can run it unattended; a human only through the template above.

Or, without one, the evidence class and limits are stated as above. Building a theory from code before either exists is the failure this skill prevents.

## Phase 2: reproduce and minimise

Run the loop and watch it go red. Confirm it shows the failure the **user** described, not a nearby one (wrong bug, wrong fix); that it reproduces across runs, or at a high enough rate; and capture the exact symptom so later phases can verify the fix.

Then shrink the repro to the **smallest scenario that still goes red**: cut inputs, callers, config, data and steps one at a time, rerunning after each cut. Done when every remaining element is load-bearing. Read error messages and stack traces completely, and check recent changes (diff, commits, dependency and config changes) on the way.

## Phase 3: hypothesise

Generate **3–5 ranked hypotheses** before testing any. Each must be falsifiable: "If <X> is the cause, then <changing Y> will make the bug disappear / <changing Z> will make it worse." A hypothesis without a prediction is a vibe: sharpen or discard it. Compare against similar working code in the same codebase; list every difference.

Show the ranked list to the user before testing when they are present; they often re-rank instantly. Don't block on it.

## Phase 4: instrument

Each probe maps to a prediction from Phase 3. **Change one variable at a time.** Prefer a debugger or REPL; otherwise targeted logs at the boundaries that distinguish hypotheses, never "log everything and grep". In a multi-component path (CI → build → signing, API → service → database), log what enters and leaves each component once to find where it breaks.

**Tag every debug log** with a unique prefix, such as `[DEBUG-a4f2]`, so cleanup is one grep. When the error is deep in the stack, trace backward to where the bad value originated: [references/root-cause.md](references/root-cause.md).

**Perf branch.** For performance regressions, measure first: a baseline on a realistic workload, then bisect or profile. Use the `benchmark-checklist` skill to vet every number you will claim. Profiles, heap snapshots and recorded traces: [references/playbooks.md](references/playbooks.md).

**Premise reset.** When two fixes that share one premise have failed the same check, stop. Write down the premise every failed fix assumed and run an observation that would come out differently if it were false, before any next fix. If the evidence points at the design itself (each fix reveals new coupling elsewhere), report that finding with its evidence; a redesign is a separate, authorized decision.

## Phase 5: fix and regression test

Fix the root cause: the first place the system did something it should not, or failed to handle a state it should handle. Ask whether the triggering state is legitimate: if it is, handling it where it broke is the fix; if it should never exist, find what produced it. Check for the same fault elsewhere and fix the pattern. Keep legitimate defensive checks, and add a new guard only at a real trust boundary.

Write the regression test **before the fix**, with the `tdd` skill, but only at a **correct seam**: one where the test exercises the real bug pattern as it occurs at the call site. If no correct seam exists, that is the finding: note it, because the architecture is preventing the bug from being locked down.

With a correct seam: turn the minimised repro into a failing test, watch it fail for the predicted reason (if you forced the red by mutating code or a fixture, diff against a pristine copy to prove the mutation landed), apply the smallest fix the evidence justifies, watch it pass, then rerun the Phase 1 loop against the original un-minimised scenario on the user's surface. Revert any change a refuted hypothesis motivated.

## Phase 6: cleanup

Required before declaring done:

- [ ] Original repro no longer reproduces (rerun the Phase 1 loop on the reported surface).
- [ ] Regression test passes, or the absent seam is documented.
- [ ] All `[DEBUG-...]` instrumentation removed (grep the prefix), and any temporary instrumentation in shared environments reverted.
- [ ] Throwaway harnesses and copied HITL scripts deleted, or moved to a clearly marked debug location.
- [ ] The confirmed hypothesis and its evidence are stated in the commit or PR message, so the next debugger learns.

Report: what was broken, the root cause and its evidence class, the fix, and the failing-then-passing output trimmed to the decisive lines. If the hunt stops before a confirmed cause, report the strongest surviving hypothesis, the evidence for and against it, and what would settle it.

## Provenance

Adapted from Matt Pocock's diagnosing-bugs skill, with material from pstack's playbooks and principles and Superpowers' systematic-debugging skill. See [references/SOURCES.md](references/SOURCES.md) and the `LICENSE-*` files.
