---
name: design-tests
description: foundry stage 2 for one code — build the test set (and the oracle at L2/L3 when planned) from the approved spec, then brief the test rules. Also strengthens tests after a failed audit. Usually run from the foundry skill.
argument-hint: "<code> [all | oracle | tests | fix-audit]"
---

# Stage 2: tests and oracle (folder `foundry/<code>/` = CODE)

Prerequisite: `CODE/spec/REVIEW.md` approved.

## all (default)
1. If the spec plans an oracle: hand to `foundry:oracle` — implement `CODE/reference/` per the oracle contract; check `CODE/scripts/run-oracle` runs.
2. Hand to `foundry:test-designer` — rules and cases per the verification level, `CODE/tests/REVIEW.md` drafted. Steps 1 and 2 may run in parallel; the test designer generates oracle cases last.
3. Report when each finishes; if a spec issue appears, stop and brief it.
4. **Brief the test rules** (`foundry:brief`): what each rule checks, which terms, the tolerance and why. This is the main point where the user's trust enters. Apply changes through `foundry:test-designer`, re-brief, approve when the user confirms.

Ends when `CODE/tests/REVIEW.md` is approved. The foundry skill then continues with `foundry:develop`.

## oracle / tests
Only step 1, or only steps 2–4 (e.g. after a spec change). New rules are appended to `CODE/tests/REVIEW.md` as PENDING and that review reopens.

## fix-audit
Give `foundry:test-designer` the empty rows of `CODE/audit/coverage.md` and the surviving mutants from `CODE/audit/mutation.md`; brief only the new rules; then develop (new tests may fail) and re-audit.

## Never
Pass main code, oracle code or `CODE/audit/private/` content to the test designer; pass main code or tests to the oracle.
