---
name: report
description: foundry stage 5, per feature — the auditor writes the verification report after a PASS verdict, the user is briefed on it and gives the final approval, and the run moves on to the next feature. Run by the orchestrator.
argument-hint: "<code> <feature>"
---

# 5 · Report

Prerequisite: `FEAT/audit/verdict.md` is PASS, and nothing in the main code, `FEAT/method.md` or `FEAT/tests/` changed after the audit (check the commits; if something changed, audit again). Below, CODE = `foundry/<code>/`, FEAT = `CODE/features/<feature>/`.

Purpose: leave a record that answers "is this verified?" with numbers, for this exact version of the code — and get the user's final approval.

## 1. Report (🤖 auditor)
Summon `foundry:auditor` for the report. It writes `FEAT/audit/report.md`: scope, results against the level's criteria, a code walkthrough by step, limits, verified versions (commits), audit history.

## 2. Brief
Show `FEAT/pages/report.html` (artifact when available; equations in LaTeX): the feature's page from stages 1–2 with the measured results and the code walkthrough added.
Ask the user only:
- each **surviving mutant**: accept as harmless, or strengthen the tests first;
- each **limit**: accept, or go back and work on it.
The measured results are not up for decision — they are what they are.

Record each answer verbatim in `FEAT/REVIEW-report.md`. If the user wants tests strengthened, go back to stage 2 for those, then 3–4 again. Otherwise apply any wording changes through the auditor, show the result, and set `Review status: APPROVED` when the user confirms.

## 3. Close the feature
- Mark the feature **done** in `CODE/roadmap.md`, with the verified commit.
- Its public and holdout tests now run as regression for every later feature; its API is fixed.
- Commit, and tell the user in one line: the feature, the verdict, the verified commit.
- Start the next feature in `roadmap.md` at stage 1 (`method`). After the last one, tell the user the code is complete: per feature, the verdict and the verified commit.
