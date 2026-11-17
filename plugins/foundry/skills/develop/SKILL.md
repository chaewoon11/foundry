---
name: develop
description: Stages 2–3 — the developer agent implements src/ and iterates on public tests. Stops and routes back to /spec when a spec issue is filed.
argument-hint: "[optional focus, e.g. a failing test kind]"
disable-model-invocation: true
---

# Stages 2–3: Implementation and fixing

Prerequisite: approved test set (`/design-tests`).

1. Delegate to the `developer` agent with: "Implement / fix `src/` until `./scripts/run-public-tests` passes. Follow your escalation rules." Add `$ARGUMENTS` as focus if given.
   - If the last audit verdict was **FAIL-HOLDOUT**, pass only the failing test *kinds* from `audit/holdout.md` — never anything from `audit/private/`.
2. When the developer returns, check:
   - **New files in `spec/issues/`** → stop. Tell the human, and run `/spec issues`. Do not let the developer continue on its own interpretation.
   - **Public tests all pass** → report and suggest `/audit`.
   - **Still failing** → report progress (pass count, what changed, new regression tests) and ask the human whether to continue.
3. Report briefly after each developer round: tests passing / total, files changed, regression tests added, issues filed.

## Never
- Edit tests, tolerances or the spec to make things pass.
- Change the solution method (algorithms, mixing scheme, ...) inside this loop — that is a spec issue.
- Show the developer holdout cases, generators, the oracle code or `audit/private/`.
