---
name: audit
description: foundry stage 4, per feature — the auditor agent checks whether the test set can be trusted (coverage, mutation testing, holdout, as the level requires) and gives a verdict that decides where the run goes next. Run by the orchestrator.
argument-hint: "<code> <feature>"
---

# 4 · Audit

Prerequisite: all public tests pass (stage 3). Below, CODE = `foundry/<code>/`, FEAT = `CODE/features/<feature>/`.

Purpose: passing the public tests means something only if the tests are sharp. The audit checks **the test set, not the code**: are all steps exercised, would the tests catch a bug, and does the code pass tests it has never seen?

## 1. Summon 🤖 auditor
Give it the feature's level and where everything is. It may read everything; it changes nothing outside `FEAT/audit/`.

What it does, by level (`roadmap.md`):

| Check | Question | L1 | L2 | L3 |
|---|---|---|---|---|
| Coverage | Is every step of the feature exercised by tests — with inputs where the step actually matters? | ≥ 1 kind per step | ≥ 2 kinds per step | ≥ 2 kinds per step |
| Mutation testing | Plant realistic bugs in a copy of the code (a sign, a factor ½ or 2π, an index); do the tests catch them? | — | key steps, ≥ 70 % caught | all steps, ≥ 90 % caught |
| Holdout | Does the code pass the tests the developer never saw? | — | all pass | all pass |

The original code is never modified; mutants live in copies.

## 2. Watch
Tell the user it has started. Check `FEAT/progress/auditor.md` now and then; if it stops changing for a long time, ask the auditor, and tell the user if it does not answer. When resumed, the auditor continues from its files.

## 3. Route on the verdict
The auditor writes `FEAT/audit/verdict.md` with one of:

| Verdict | Meaning | Next |
|---|---|---|
| **PASS** | the tests are sharp and the code passes them | stage 5 (`report`) |
| **FAIL-COVERAGE** / **FAIL-MUTATION** | the tests are too weak somewhere | explain to the user; usually back to stage 2 to strengthen those tests, then 3 and 4 again |
| **FAIL-HOLDOUT** | the code fits the public tests but not the unseen ones | explain to the user; usually back to stage 3, telling the developer only which kinds failed, then 4 again |
| **ISSUE** | the auditor found a problem in the method or the equations | explain to the user; back to stage 1 or 0d |

On a failure the user chooses what to do; do not pick for them.

## 4. Summarise for the user
In a few lines: steps × kinds covered, share of planted bugs caught (overall and the weakest step), holdout passed / total, the verdict, the next step. Surviving mutants: list them; whether one counts as harmless is the user's decision, never the auditor's.
