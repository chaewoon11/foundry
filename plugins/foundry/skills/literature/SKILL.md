---
name: literature
description: foundry stage 0b — review with the user the papers and notes they put in foundry/<code>/literature/, for physical meaning and prior work rather than equations. Writes foundry/<code>/literature-review.md and discusses it in chat. Run by the orchestrator.
argument-hint: "<code>"
disable-model-invocation: true
---

# 0b · Literature review

Prerequisite: `foundry/<code>/goal.md` agreed (0a).

Purpose: read what is needed **to achieve `goal.md`** — what the physics means and how others have done this kind of calculation — before deciding which equations to implement. This is not a search for research gaps: the goal is already set. Read like a researcher preparing to carry out a known task, not like a programmer looking for formulas. Equations appear only where they carry the physical idea; the frame of the calculation comes in 0c.

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
- **Results to compare with**: numbers or figures our code should be able to reproduce.
- **Pitfalls**: conventions, approximations or steps the source flags as delicate.

Across sources, for the goal:
- **The usual way to do it**: how the sources set up this kind of calculation, and where they differ (conventions, approximations).
- **What we take**: the approach, conventions and reference results this code will follow.

## How
1. Confirm the list of sources in `literature/` with the user.
2. Draft `foundry/<code>/literature-review.md` (below).
3. **Discuss in chat**, not item by item: start with the overall picture (the usual way to do this calculation and what we take from it), then the points that matter most for the goal. Ask what the user sees differently, what you missed, what to read more closely. Update the file as the discussion goes.
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
- Results to compare with:
- Pitfalls:

## For the goal
The usual way to do it · where sources differ · what we take

## Reference values worth reproducing
| Source | Figure / table | Quantity | Conditions |

## From the discussion
Points the user raised and what was decided.
```
