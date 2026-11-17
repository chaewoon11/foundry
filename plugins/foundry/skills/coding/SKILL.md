---
name: coding
description: foundry stage 3, per feature — the developer agent writes the main code in place until the public tests pass. The user only hears progress, unless something in the method or the tests is unclear. Run by the orchestrator.
argument-hint: "<code> <feature>"
disable-model-invocation: true
---

# 3 · Coding

Prerequisite: `FEAT/REVIEW-tests.md` approved (stage 2). Below, CODE = `foundry/<code>/`, FEAT = `CODE/features/<feature>/`.

## Why a separate agent
You (the orchestrator) have seen the holdout tests, the test rules and the oracle in stage 2. Code written by you would be written with the exam in view. A fresh agent that sees only the public tests writes code that has to be right, not code that fits the exam.

## 1. Summon 🤖 developer
Give it:
- `FEAT/method.md` — numerical method, API, pseudocode;
- where the main code lives (`CODE/goal.md`);
- the public tests: `FEAT/tests/public/`, the public tests of completed features, and `FEAT/tests/existing/` for existing code;
- the command that runs them.

Never give it holdout tests, test generators or rules, the oracle's code, or audit details — not even in a summary.

## 2. Watch
Tell the user it has started. Check `FEAT/progress/developer.md` now and then; if it stops changing for a long time, ask the developer, and tell the user if it does not answer.

## 3. When it returns
- **All public tests pass** → report briefly (tests passed, files changed, regression tests added) and move on to stage 4 (`audit`).
- **It reports that the method, the API or a test seems wrong** → stop. Explain it to the user with the options; the answer may send the run back to stage 1 or 2.
- **Still failing** → report what passes and what does not, and ask the user whether to continue.

## After a failed audit
If the audit's holdout check fails, send the developer back with **only which kinds of holdout tests failed** — never the cases themselves.
