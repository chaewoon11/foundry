---
name: formulation
description: foundry stage 0c — set the frame of the calculation with the user: which equations are implemented, which quantity each gives, how they chain from input to output, and the pseudocode of the whole calculation. Rough shape only, no detailed derivations. Writes foundry/<code>/formulation.md, shows it as a page (artifact, equations in LaTeX) and discusses it in chat. Run by the orchestrator.
argument-hint: "<code>"
disable-model-invocation: true
---

# 0c · Formulation

Prerequisites: `goal.md` (0a) and `literature-review.md` (0b) agreed.

Purpose: shape the calculation the way a potter first shapes the clay — the overall form, not the finish. Decide **which equations the code implements, what each one gives, and how they connect from the input to the output**. Do not derive or check the equations in detail; that is 0d.

## What goes in
- **Conventions**: units, sign and normalisation conventions, taken from `literature-review.md` ("what we take").
- **Steps**, from input to output. Per step:
  - the quantity it produces;
  - the equation that gives it, in its usual form (LaTeX), with the source it comes from;
  - what it needs (input or earlier steps) and what uses it;
  - for existing code: **existing** or **new**.
- **Pseudocode** of the whole calculation, from input to output: 10–20 lines, loops and steps as they will run (e.g. "for each k point: build H(k); diagonalise"), each line tagged with its step number and, for existing code, existing / new. No language, libraries, data structures or performance tricks — that is the developer's choice in stage 3.
- **Approximations**, each named in one line with the reason. They are proposals here; the user confirms them in 0d.
- **What is left out** on purpose, in one line each.

A good frame fits on one screen: typically 3–8 steps.

## How
1. Draft `foundry/<code>/formulation.md` (below) from `goal.md` and `literature-review.md`. This file is the record.
2. **Show it as a page.** Render the same content as `foundry/<code>/pages/formulation.html`: conventions, the chain of steps (a small flow diagram from input to output helps), each equation as display math in LaTeX (MathJax), the pseudocode as a code block, approximations, what is left out. Publish it as an artifact when an Artifact tool is available; otherwise send the HTML file or tell the user to open it in a browser.
3. **Discuss in chat** while the user looks at the page: walk through the chain once from input to output, then through the pseudocode, then ask whether a step is missing, unnecessary, or in the wrong order, and whether the approximations match the user's intent.
4. After each change, update `formulation.md` first, then regenerate and republish the page, so the two never differ.
5. Do not go into derivations, numerical methods or code. If the discussion drifts there, note the point for 0d (derivations) or stage 1 (numerical method) and come back to the frame.
6. When the user agrees with the frame, 0c ends. Commit `formulation.md` and the page, and move on to 0d (`theory-check`).

## `formulation.md`
````markdown
# Formulation: <code>

## Conventions
- <units, signs, normalisations>

## Steps (input → output)
| # | Quantity | Equation | From | Needs | Used by | Existing / new |
|---|---|---|---|---|---|---|
| 1 | | \( … \) | [source] | input | 2 | |

## Pseudocode
```text
read input                                  # step —
for each <loop variable>:                   # step 2, new
    <quantity> = <step 2 equation>(...)
...
write output                                # step —
```

## Approximations (to confirm in 0d)
- <approximation> — <why>

## Left out
- <what> — <why>

## Notes for later
- 0d: <derivation points raised in the discussion>
- Stage 1: <numerical-method points raised in the discussion>
````
