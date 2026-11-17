---
name: literature
description: foundry stage 0b — review with the user the papers and notes they put in foundry/<code>/literature/, for physical meaning and prior work rather than equations. Writes foundry/<code>/literature-review.md and discusses it in chat. Run by the orchestrator.
argument-hint: "<code>"
disable-model-invocation: true
---

# 0b · Literature review

Prerequisite: `foundry/<code>/goal.md` agreed (0a).

Purpose: understand **what the physics means and what has been done**, before deciding which equations to implement. Read like a researcher preparing a project, not like a programmer looking for formulas. Equations appear only where they carry the physical idea; the frame of the calculation comes in 0c.

## Sources
- The user puts papers, theses, notes or code documentation in `foundry/<code>/literature/`.
- You (the orchestrator) read them yourself. They contain no main code, so this does not touch the information barriers.
- Read one source at a time; for a long source, read the parts that matter for `goal.md` (abstract, introduction, method, main results, conclusions) first.
- If an obviously important reference is missing (e.g. the original paper of a method every source cites), name it and ask whether the user wants to add it. Do not add sources yourself.

## What to look for
Per source:
- **Question and answer**: what problem it addresses and what it finds, in two or three sentences.
- **Physical picture**: what the model describes, which interactions matter, what is neglected.
- **Method**: what was computed and how, in words.
- **What it establishes**: results that are now accepted; numbers or figures that can serve as reference values later.
- **Limits**: what it does not cover or gets wrong, as the source itself or later work says.

Across sources:
- **How the field developed**: who did what, in which order, what each step added.
- **What is established and what is open.**
- **Where this code fits**: what it reproduces, what it adds, what it deliberately leaves out — in relation to `goal.md`.

## How
1. Confirm the list of sources in `literature/` with the user.
2. Draft `foundry/<code>/literature-review.md` (below).
3. **Discuss in chat**, not item by item: start with the overall picture (how the field developed, where this code fits), then the points that matter for the goal. Ask what the user sees differently, what you missed, what to read more closely. Update the file as the discussion goes.
4. When the user agrees with the review, 0b ends. Commit and move on to 0c (`formulation`).

## `literature-review.md`
```
# Literature review: <code>

## Sources
| # | Reference | One line |
|---|---|---|

## Per source
### [1] <short reference>
- Question and answer:
- Physical picture:
- Method:
- Establishes:
- Limits:

## The field
How it developed · what is established · what is open

## Where this code fits
Reproduces · adds · leaves out (relative to goal.md)

## Reference values worth reproducing
| Source | Figure / table | Quantity | Conditions |

## From the discussion
Points the user raised and what was decided.
```
