---
name: develop
description: foundry stage 3 for one code — the developer implements or changes the main code until the public tests pass; stops on spec issues. Usually run from foundry:start.
argument-hint: "<code> [focus]"
---

# Stage 3: develop (folder `foundry/<code>/` = CODE)

Prerequisite: `CODE/tests/REVIEW.md` approved.

1. Hand to `foundry:developer`: "Implement / change the main code until `foundry/<code>/scripts/run-public-tests` passes. Follow your escalation rules." Add a focus if given.
   - After a **FAIL-HOLDOUT** verdict pass only the failing test *kinds* from `CODE/audit/holdout.md`, never anything from `CODE/audit/private/`.
2. When it returns:
   - New file in `CODE/spec/issues/` → stop; brief it (`foundry:spec` issues mode).
   - Public tests pass → report (passing / total, files changed, regression tests added, any blocked tool calls) and continue with `foundry:audit`.
   - Still failing → report progress and ask the user whether to continue.

## Never
Edit tests, tolerances or the spec to make things pass; change the solution method inside this loop (that is a spec issue); show the developer holdout tests, generators, oracle code or `CODE/audit/private/`.
