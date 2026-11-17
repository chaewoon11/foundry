---
name: report
description: Write the final verification report after a PASS verdict.
disable-model-invocation: true
---

# Verification report

1. Check `audit/verdict.md` is **PASS** and newer than the last change to `src/`, `tests/` and `spec/`. If not, stop and suggest `/audit`.
2. Delegate to the `auditor` agent to write `audit/report.md`:
   - Scope (from `spec/model.md`) and what is explicitly out of scope
   - Acceptance criteria (from `spec/acceptance.md`) and measured values
   - Coverage table (term × test kind)
   - Mutation kill rate, per term and overall; surviving mutants and why they are acceptable, if any
   - Holdout results
   - Resolved spec issues and the decisions taken
   - Remaining limitations (untested ranges, known multiple solutions, ...)
3. Show the human the report.
