---
name: tests
description: foundry stage 2, per feature — build the test set (test-designer) and, where the level calls for it, the reference implementation (oracle), from the method and the verified equations only; then brief the user by test kind. Run by the orchestrator.
argument-hint: "<code> <feature>"
disable-model-invocation: true
---

# 2 · Tests & oracle

Prerequisite: `FEAT/REVIEW-method.md` approved (stage 1). Below, CODE = `foundry/<code>/`, FEAT = `CODE/features/<feature>/`.

Purpose: write the exam and the answer key **before** the code exists, from the method and the equations — never from the code.

## 0. Oracle or not
By the feature's level (`roadmap.md`): L1 — no oracle; L3 — oracle; L2 — ask the user in one question (more independent reference values vs. extra cost).

## 1. Summon, in parallel
**🤖 oracle** (if any) gets `FEAT/method.md` (the API it must match), `CODE/theory/claims.md`, `CODE/formulation.md`. Never the main code or the tests. It writes a slow, obviously-correct reference in `CODE/reference/` (one oracle per code, extended feature by feature), using a different method than `method.md` where possible.

**🤖 test-designer** gets `FEAT/method.md`, `CODE/theory/` (claims, limits, symmetries), `CODE/literature-review.md` (reference values to reproduce), the feature's level, and a way to run the oracle (never its code). Never the main code. It writes in `FEAT/tests/`:
- `rules.md` — every test rule: kind, what it checks, inputs, tolerance and how it was derived from the method's error behaviour;
- `generators/` — the rules as code;
- `public/` and `holdout/` — generated cases, split as the level requires;
- for existing code, `existing/` — the current outputs of the existing code on a set of inputs, recorded by running it the way `goal.md` says (regression: these must not change).

Report when each finishes. If either finds the method or the equations unclear, stop and take it to the user.

## 2. Brief by test kind
Show `FEAT/pages/tests.html` (artifact when available; equations in LaTeX), built from `rules.md`:

| Kind | Show |
|---|---|
| ① analytic | **all** — problem, exact answer, source |
| ⑥ external (papers, other codes) | **all** — source, figure or table, quantity |
| ② transformations | in words or a short equation each |
| ③ consistency | a few representative ones |
| ④ convergence order, ⑤ oracle | one line each: what they cover, how many |

Then the **weak spots**: steps or bugs only one kind can catch, and parts with no exact check.

Ask the user only trade-offs between rigour and cost (e.g. "this step has no analytic case; add more oracle cases, or accept it?"). The rules and derived tolerances are one list the user approves at once.

Record each answer verbatim in `FEAT/REVIEW-tests.md`. Send all changes to the test-designer (and oracle) at once, show the result, and set `Review status: APPROVED` when the user confirms. Commit and move on to stage 3 (`coding`).

## Feature files (so far)
```
FEAT/
  method.md · REVIEW-method.md
  tests/rules.md · generators/ · public/ · holdout/ · existing/
  REVIEW-tests.md
  pages/method.html · pages/tests.html
CODE/reference/        the oracle (shared by features)
```
