# foundry workflow (what the orchestrator must know)

This is the workflow map in words. Keep it identical to the map (`workflow-map.html` in chaewoon11/foundry-test).

## Roles
- **User** — decides what has no correct answer: goal, modelling approximations, method and API, verification level, trade-offs between rigour and cost; approves each briefing.
- **Orchestrator** — the main session. Talks with the user, runs the chat stages itself, summons agents, briefs, records decisions, moves the run forward. Never does an agent's work.
- **🤖 Agents** — summoned for one task, with their own instructions (`agents/<name>.md`), no view of the conversation, and access limited to their role.

## Stages

### Stage 0 — understand before building (once per code)

| Stage | Skill | Who | Produces | Done when |
|---|---|---|---|---|
| 0a Goal | `goal` | orchestrator + user, chat | `goal.md`: starting point (new / existing code + path), input, output, method in words | user agrees |
| 0b Literature review | `literature` | orchestrator + user, chat | `literature-review.md` from papers the user put in `literature/`, read to achieve the goal: physical meaning, how others did this calculation, what we take, results to compare with | user agrees |
| 0c Formulation | `formulation` | orchestrator + user: page (artifact, LaTeX) + chat | `formulation.md`: which equations, which quantity each gives, how they chain from input to output, pseudocode of the whole calculation (rough shape) | user agrees |
| 0d Rigorous check | `theory-check` | orchestrator derives; 🤖 `theory-checker` re-derives independently; equation-centred briefing (artifact, LaTeX) | `theory/claims.md` (numbered equations), `theory/derivation.md`, `theory/checks/` | `theory/REVIEW.md` approved |
| 0e Features | `features` | orchestrator + user, chat | `roadmap.md`: features, order, dependencies, verification level each | user agrees |

For existing code: stages 0b–0e cover the extension; the existing code's current outputs are recorded as regression. Verifying the existing code itself is an optional first feature.

### Per feature, in roadmap order

| Stage | Skill | Who | Produces | Done when |
|---|---|---|---|---|
| 1 Numerical method & interface | `method` | 🤖 `spec-writer`; briefing | numerical method (discretisation or basis, algorithm, convergence parameters); API (functions, inputs with valid ranges, outputs, units, errors) | method/API review approved |
| 2 Tests & oracle | `tests` | 🤖 `test-designer` ∥ 🤖 `oracle`; briefing by test kind | test rules, public and holdout cases, tolerances derived from the method; reference implementation | test review approved |
| 3 Coding | `coding` | 🤖 `developer` | main code, in place; regression tests for fixed bugs | public tests pass |
| 4 Audit | `audit` | 🤖 `auditor` | coverage, mutation testing, holdout → verdict | verdict PASS |
| 5 Report | `report` | 🤖 `auditor`; briefing | report: scope, results vs criteria, code walkthrough, limits, verified commit | report approved → next feature |

Going back:
- **Spec issue** (any agent finds the method, API or a test unclear or wrong) → run stops, user decides, the affected stage is redone.
- **Audit FAIL-COVERAGE / FAIL-MUTATION** → strengthen tests (stage 2), then 3–4 again. **FAIL-HOLDOUT** → fix code (stage 3), then 4 again. The user decides which.
- A later feature that must change an earlier one files an amendment on the earlier feature; after the user decides, the earlier feature is re-audited.

## Briefings
Stages 0d, 1, 2 and 5 end with a briefing (skill `brief`): the big picture first, then only the user's decisions one by one, then the agents' decisions as one list. Depth for the test briefing: ① analytic — all; ⑥ external — all; ② transformations — in words; ③ consistency — a few; ④ order and ⑤ oracle — barely.

## Verification levels (chosen per feature in 0e)
| | L1 | L2 | L3 |
|---|---|---|---|
| Tests | ① + ② | ①②③ + ④ or ⑤ | ①–⑥ |
| Holdout | none | some | all |
| Oracle | none | optional | required |
| Mutation testing | none | key steps, ≥ 70 % | all steps, ≥ 90 % |

## Files in a project
```
<project>/
  <main code>                    developed in place, never inside foundry/
  foundry/<code>/
    goal.md                      0a
    literature/                  papers and notes the user provides
    literature-review.md         0b
    formulation.md               0c
    theory/                      0d: claims.md, derivation.md, checks/, REVIEW.md
    roadmap.md                   0e
    features/<feature>/          stages 1–5 of one feature: method, tests, oracle, audit, report, REVIEW files, pages
```
Open (not decided): oracle per code or per feature; exact file names inside `features/<feature>/`.

## Where a run stands
Read it from the files: the first missing or unapproved product in the tables above is the current stage. A `REVIEW.md` is approved when its header says `Review status: APPROVED`.
