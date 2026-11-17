---
name: features
description: foundry stage 0e — split the code into features with the user: order, dependencies and a verification level each. Writes foundry/<code>/roadmap.md. Run by the orchestrator.
argument-hint: "<code>"
disable-model-invocation: true
---

# 0e · Features

Prerequisites: `formulation.md` (0c) agreed and `theory/REVIEW.md` (0d) approved, unless 0d was skipped.

Purpose: decide how the code grows. Each feature is built and verified on its own (stages 1–5), in order, so every run stays small and earlier features stay protected.

## Propose a split
From the steps of `formulation.md` and the claims in `theory/claims.md`, propose features. Rule of thumb:

> A feature is the smallest piece that has its own exact checks — an analytic case, a limit or a symmetry from `theory/` that tests can use.

Per feature:
- **Scope** in one line: what it adds, in the user's terms.
- **Steps and claims** it implements (from `formulation.md` and `claims.md`).
- **Depends on** which earlier features.
- **Exact checks** available for it (from `theory/`). A feature without any is a sign it should be merged with another.
- **Verification level**, recommended with a reason:

| | L1 light | L2 standard | L3 strict |
|---|---|---|---|
| Use for | small, low-risk parts | most features | new or delicate physics; results that go into a paper |
| Tests | analytic + transformations | + consistency, and order or oracle | all kinds |
| Holdout | none | some | all |
| Oracle | none | optional | required |
| Mutation testing | none | key steps, ≥ 70 % | all steps, ≥ 90 % |

For **existing code** (`goal.md`): the features cover the extension. The existing code's current outputs are recorded as regression in stage 2 of the first feature. If the user also wants the existing code verified, add it as the first feature ("feature 0: existing behaviour"), run without stage 3.

## Agree it in chat
Show the list and talk it through: order, splitting or merging, levels. These are the user's decisions — there is no correct answer. Keep it to one or two rounds.

## Write `foundry/<code>/roadmap.md`
```
# Roadmap: <code>

| # | Feature | Scope | Steps / claims | Depends on | Exact checks | Level | Status |
|---|---|---|---|---|---|---|---|
| 1 | | | steps 1–3 · C1–C8 | — | | L2 | not started |

## Notes
- <why this order, why these levels>
```
When the user agrees, 0e ends. Commit, and start feature 1 at stage 1 (`method`).

## Later
- The user can change the roadmap at any time: split, merge, add, reorder, change a level. Update `roadmap.md` and say what it changes for features already done.
- A new feature that needs new physics goes back through 0b–0d for that part only.
- Update the Status column as features move through stages 1–5.
