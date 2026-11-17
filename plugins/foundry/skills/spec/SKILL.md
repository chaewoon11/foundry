---
name: spec
description: foundry stage 1 for one code — settle the spec with the user, recommend and set the verification level, write the acceptance criteria, brief everything, and put the scripts in place. Also handles spec issues. Usually run from the foundry skill.
argument-hint: "<code> [new | issues]"
---

# Stage 1: spec (code: the one named, folder `foundry/<code>/` = CODE)

Goal: fix **what is solved, how it is judged, and when it is done** — before any code exists or changes.

## new (default)
1. **Discuss the main choices** with the user: equations, units and conventions, scope, boundary conditions, method, whether an independent oracle is possible, language, and — for existing code — what is new and what must stay unchanged. Offer defaults; let the user pick.
2. **Draft** — hand to `foundry:spec-writer`, quoting the agreed choices: write `model.md`, `terms.md`, `project.md`; leave acceptance criteria for later.
3. **Verification level** — recommend one with reasons from the draft (number of terms, new vs modified code, oracle feasibility, how the code will be used, expected cost) and let the user pick:

   | | L1 light | L2 standard | L3 strict |
   |---|---|---|---|
   | Use for | one-off scripts, analysis tools | general research code | core methods in papers, long-lived code |
   | Test kinds | ① + ② | ①②③ + ④ or ⑤ | ①–⑥ as available |
   | Cases per rule | 3–5 | ~10 | ≥ 20 |
   | Holdout | none | some rules | all rules |
   | Oracle | none | optional | required |
   | Mutation testing | none | key terms, ≥ 70 % | all terms, ≥ 90 % |
   | Coverage | 1 kind per term | 2 kinds per term | ≥ 2 kinds per term |
   | Briefing | summary + 🔴 items | 🟡🔴 one by one, 🟢 grouped | every item |

   Write the chosen level into `CODE/foundry.json` (`"level"`) and commit.
4. **Criteria** — hand to `foundry:spec-writer` again: fill `acceptance.md` from the level, and draft `CODE/spec/REVIEW.md`.
5. **Brief** the spec (`foundry:brief`, depth by level). Apply the collected edits through `foundry:spec-writer`, re-brief changed items, approve when the user confirms.
6. **Scripts** — you (not an agent) adapt `CODE/scripts/` to the contract in `project.md`: `build`, `run-public-tests`, `run-oracle` (if there is an oracle) are project-specific; `run-holdout`, `holdout_summary.py` and `mutate` are templates already in place — adjust paths and the test runner if needed. Every script must honour `FOUNDRY_SRC` (see `project.md`) so mutation testing can point the tests at a copy of the main code. Tell the user in one line each what the scripts do, and commit.

Ends when `CODE/spec/REVIEW.md` is approved and the scripts run. The foundry skill then continues with `foundry:design-tests`.

## issues
For each open file in `CODE/spec/issues/` (no `## Resolution`): brief it as one item (record in `CODE/spec/issues/REVIEW.md`): what was found, where, the options, your view. After the user decides, hand to `foundry:spec-writer` to update the spec and append `## Resolution`; re-brief the changes; then redo what the resolution names (tests, oracle, code) through the matching stage.
