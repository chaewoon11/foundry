---
name: audit
description: Stage 4 — exit-criteria judgment. The auditor builds the coverage table, runs mutation testing and the holdout set, and issues a verdict that routes the workflow.
argument-hint: "[all | coverage | mutation | holdout]"
disable-model-invocation: true
---

# Stage 4: Exit-criteria judgment

Prerequisite: public tests pass (`/develop`).

1. Delegate to the `auditor` agent (default: all three judgments; or only `$ARGUMENTS`). It writes `audit/coverage.md`, `audit/mutation.md`, `audit/holdout.md`, `audit/verdict.md`.
2. Read `audit/verdict.md` and route:

| Verdict | Next step |
|---|---|
| PASS | `/report` |
| FAIL-COVERAGE / FAIL-MUTATION | `/design-tests fix-audit`, then `/develop`, then `/audit` |
| FAIL-HOLDOUT | `/develop` with only the failing kinds; tell the human where the auditor suspects fitting (`audit/private/holdout-diagnosis.md`) |
| SPEC-ISSUE | `/spec issues` |

3. Summarize for the human: the coverage table, kill rate (overall and weakest term), holdout pass/fail counts, the verdict, and the next step.
