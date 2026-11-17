---
name: method
description: foundry stage 1, per feature — fix the numerical method and the API of one feature. The spec-writer agent drafts them; the user decides in a short briefing. Writes foundry/<code>/features/<feature>/method.md. Run by the orchestrator.
argument-hint: "<code> <feature>"
---

# 1 · Numerical method & interface

Prerequisite: the feature is next in `roadmap.md`, and all features it depends on are complete.

Purpose: decide **how the equations of this feature are made computable** and **how the code is used from outside**. Nothing more: tolerances come from the method in stage 2, keeping earlier behaviour is handled by regression tests, and the inside of the code is the developer's choice in stage 3.

## 1. Draft (🤖 spec-writer)
Summon `foundry:spec-writer` for this feature with:
- the feature's row of `roadmap.md` (scope, steps, claims, level);
- `formulation.md` (steps, pseudocode) and `theory/claims.md`;
- the API of features it depends on, from their `method.md`;
- for existing code: how it is called today (from `goal.md`). Do not pass the code itself.

It writes `foundry/<code>/features/<feature>/method.md`:
- **Numerical method** — per step of the feature: discretisation or basis, algorithm (e.g. full diagonalisation, iterative solver), convergence parameters with default values, and the expected error behaviour (e.g. error ∝ h², exponential in the basis size). Where there is a real choice, the alternatives with their trade-offs.
- **API** — public functions, inputs with units and valid ranges, outputs with units, what happens with invalid input.
- **Pseudocode** — the pseudocode of `formulation.md` for this feature, now with the method chosen.

## 2. Brief
Show `method.md` as a page (`foundry/<code>/features/<feature>/pages/method.html`, artifact when available, equations in LaTeX) and discuss it in chat.
Ask the user only:
- the **method** where there is a real choice (e.g. finite differences vs a basis expansion: accuracy, cost, what tests become possible);
- the **API**: names, what goes in and comes out, units, which inputs are refused.
Everything derivable (default parameter values, error types, internal conventions) is one list the user approves at once.

Record each answer verbatim in `foundry/<code>/features/<feature>/REVIEW-method.md`. Send all changes back to the spec-writer in one go, show the result, and set `Review status: APPROVED` when the user confirms. Commit and move on to stage 2 (`tests`).

## Feature files (so far)
```
foundry/<code>/features/<feature>/
  method.md
  REVIEW-method.md
  pages/method.html
```
