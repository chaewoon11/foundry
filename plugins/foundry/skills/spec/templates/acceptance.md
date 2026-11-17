# Acceptance criteria

Agreed **before** any code is written. Changing these numbers requires explicit human approval.

## Definition of "verified"
Within the stated scope, every term of the model is active in tests of at least **N** independent kinds,
the test set kills at least **R%** of per-term planted bugs, and every holdout test that was never
visible during development passes.

| Criterion | Value |
|---|---|
| Min. independent test kinds (①–⑥) activating each term (N) | 2 |
| Mutation kill rate, overall (R) | 90% |
| Mutation kill rate, minimum per term | <!-- e.g. 80% --> |
| Holdout pass condition | all pass |
| Public / holdout split | 70 / 30 |

## Tolerances
| Quantity | Absolute | Relative | Justification |
|---|---|---|---|
| | | | |
