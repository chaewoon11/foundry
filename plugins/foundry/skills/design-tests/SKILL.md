---
name: design-tests
description: Build the test set and the oracle from the approved spec — generators, anchor tests, public/holdout split, and the brute-force reference implementation — then brief the test rules for approval. Also strengthens tests after a failed audit.
argument-hint: "[all | oracle | tests | fix-audit]"
disable-model-invocation: true
---

# Test set and oracle

Prerequisite: `spec/REVIEW.md` is APPROVED.

The `oracle` and `test-designer` agents both read only `spec/` and never each other's code or `src/`. They may run in parallel. Report to the human when each starts and finishes.

## Mode: `all` (default)
1. Delegate to the `oracle` agent: implement the reference in `reference/` following the oracle contract in `spec/project.md`. Smoke-test `./scripts/run-oracle`.
2. Delegate to the `test-designer` agent: write anchor tests and generators, generate cases, split 70/30 into `tests/public/` and `tests/holdout/`, and draft `tests/REVIEW.md` (one item per rule). Suggested order: ② transformation → ① anchors → ③ consistency → ④ convergence order → ⑤ oracle comparison → ⑥ external.
3. **Immediately start the briefing** (`brief` skill on `tests/`): one rule per item — what it checks, which terms it activates, the tolerance and why. This is the main human review point of the whole workflow.
4. Apply the collected changes via `test-designer`, re-brief them, and approve `tests/REVIEW.md` once the human confirms.

## Mode: `oracle` / `tests`
Run only step 1 or only steps 2–4 (e.g. after a spec change). For `tests`, new rules are appended to `tests/REVIEW.md` as PENDING and the review reopens.

## Mode: `fix-audit`
1. Read `audit/coverage.md` (rows below threshold) and `audit/mutation.md` (surviving mutants).
2. Delegate to `test-designer` with that list: add rules that activate each missing term and kill each surviving mutant, appended to `tests/REVIEW.md`.
3. Brief only the new rules. Then go to `/develop` (new tests may fail) or directly `/audit`.

## Never
- Pass anything from `src/`, `reference/` or `audit/private/` to the test designer.
- Pass anything from `src/` or `tests/` to the oracle.
