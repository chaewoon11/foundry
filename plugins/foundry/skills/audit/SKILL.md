---
name: audit
description: foundry stage 4 for one code — the auditor judges the test set (coverage, mutation testing, holdout as the level requires) and issues a verdict that routes the run. Usually run from foundry:start.
argument-hint: "<code> [all | coverage | mutation | holdout]"
---

# Stage 4: audit (folder `foundry/<code>/` = CODE)

Prerequisite: public tests pass.

1. Hand to `foundry:auditor` (all judgments the level requires, or only the one asked). Remind it to keep `CODE/progress/auditor.md` and to resume from existing artifacts. While it runs, check that file now and then; if it stops changing for a long time, ask the auditor, and tell the user if it does not answer.
2. Read `CODE/audit/verdict.md` and route:

| Verdict | Next |
|---|---|
| PASS | `foundry:report` |
| FAIL-COVERAGE / FAIL-MUTATION | explain and ask; usually `foundry:design-tests fix-audit`, then develop, then audit again |
| FAIL-HOLDOUT | explain and ask; usually `foundry:develop` with the failing kinds only, then audit again; tell the user where the auditor suspects fitting |
| SPEC-ISSUE | `foundry:spec` issues mode |

3. Summarise for the user: coverage (term × kind), kill rate overall and weakest term, survivors, holdout counts, verdict, next step.
