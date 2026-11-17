---
name: theory-check
description: foundry stage 0d — derive every equation of formulation.md rigorously, have the theory-checker agent re-derive each one independently, and brief the user on the equations (artifact page, LaTeX). Writes foundry/<code>/theory/. Run by the orchestrator.
argument-hint: "<code>"
disable-model-invocation: true
---

# 0d · Rigorous check

Prerequisite: `formulation.md` agreed (0c).

Why: code and tests will both be built from these equations. If an equation is wrong, both implement the same wrong equation and every test passes. This stage is where that is caught.

## 1. Derive (you, the orchestrator)
Write `foundry/<code>/theory/derivation.md`: every equation in `formulation.md`, derived step by step down to the problem the code solves numerically.
- conventions first (units, signs, normalisations, index orders), stated once and used throughout;
- each approximation where it enters, with what it neglects;
- each step with its source (paper, book, equation number);
- exactly solvable limits and simple cases the equations must reproduce;
- symmetries and what they imply for the results.

Then write `foundry/<code>/theory/claims.md`: every equation or statement the code will rely on, numbered `C1, C2, …`. Each claim is **self-contained** — symbols defined, conventions stated — so it can be checked without reading `derivation.md`.

## 2. Check independently (🤖 theory-checker)
Summon `foundry:theory-checker` with `goal.md`, `literature-review.md`, the sources in `literature/` and `theory/claims.md`. **Never give it `derivation.md`** or your reasoning: its derivations must be its own.
It returns, in `theory/checks/`, a verdict per claim — **agrees / disagrees / not checkable** — with its derivation, its sources (other than yours where possible), and symbolic checks (sympy) where possible.

## 3. Settle disagreements
For each claim the checker disputes, compare its derivation with yours.
- If you were wrong: correct `derivation.md` and `claims.md`, and note it.
- If you still hold: write down precisely why, with sources.
Do not change a claim just to agree. One round only; whatever is still disputed goes to the user.

## 4. Brief (equation-centred, as a page)
Render `foundry/<code>/pages/theory.html` and publish it as an artifact (otherwise send the HTML file). Every equation in LaTeX (MathJax).
- **The claims as equations**, grouped by the steps of `formulation.md`, each marked agreed / corrected / disputed by the check.
- **Approximations** from `formulation.md`, each with what it neglects.
- **Disputed claims**: both derivations side by side, and where they part.
- Limits and symmetries the equations satisfy.

Then ask the user only what is theirs to decide, one question at a time:
- each **approximation**: keep, change or drop;
- each **disputed claim**: which derivation holds, or what to read to settle it.
Everything the check confirmed is approved as one list.

Record each answer verbatim in `foundry/<code>/theory/REVIEW.md` at once. When everything is decided, apply the changes, update the page, and set `Review status: APPROVED`. Commit and move on to 0e (`features`).

## Files
```
foundry/<code>/theory/
  derivation.md     your step-by-step derivation (not shown to the checker)
  claims.md         numbered, self-contained equations C1, C2, …
  checks/           the checker's derivations, sympy scripts, report.md
  REVIEW.md         the user's decisions
foundry/<code>/pages/theory.html
```

## Skip
For code with no theory (pure data processing), the user may skip 0d.
