# Acceptance criteria

Agreed **before** any code is written or changed. The level, the criteria table and any number the user set change only with the user's explicit approval. Derived tolerances follow the policy below: the user approves the policy, and any single tolerance can be challenged through a spec issue.
Approval status is recorded in `spec/REVIEW.md`.

## Verification level
**Level:** <!-- L1 | L2 | L3, chosen by the user after the spec content was settled; also in foundry.json -->

Defaults per level (keep unless the user agreed otherwise; then write the agreed value in the table below):

| | L1 light | L2 standard | L3 strict |
|---|---|---|---|
| Test kinds required | ① + ② | ①②③ + ④ or ⑤ | ①–⑥ as available |
| Min. independent kinds activating each term | 1 | 2 | 2 |
| Cases per generated rule | 3–5 | ~10 | ≥ 20 |
| Holdout | none | ≥ 1 rule per kind, 30 % of its cases | every rule, 30 % |
| Oracle | none | optional | required |
| Mutation testing | none | key terms, ≥ 6 mutants each | all terms, ≥ 6 mutants each |
| Mutation kill rate (overall / per term) | — | ≥ 70 % / ≥ 60 % | ≥ 90 % / ≥ 80 % |
| Holdout pass condition | — | all pass | all pass |

## Definition of "verified" (at this level)
Within the scope of model.md, every term (or the key terms, at L2) is active in tests of at least **N** independent kinds, the test set kills at least **R %** of bugs planted term by term, and every holdout test passes.

| Criterion | Value |
|---|---|
| N | |
| R (overall / per term) | |
| Terms subject to mutation testing | |
| Holdout | |

Further rules:
- The unmodified main code must pass every public and holdout test before mutation results count.
- A mutant no test can see counts as survived; excluding it as equivalent is the user's decision, recorded in the audit.
- A mutant counts as killed if any test fails or errors, or the run times out.

## Tolerances
| # | Quantity / comparison | Absolute | Relative | Preconditions | Justification |
|---|---|---|---|---|---|
| 1 | | | | | |

Rules for tolerances not listed: derive from the method's error analysis or round-off, record the derivation in the test metadata, and have it approved at the test-rule briefing. Tolerances are never loosened in response to development progress; a needed change is a spec issue.
