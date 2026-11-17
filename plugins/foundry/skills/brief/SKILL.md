---
name: brief
description: foundry briefing — show the user the big picture as a page, then take only the decisions that are theirs, anchored to that picture, and record each answer. Used for the spec, the test rules, spec issues and the verification report. Usually run from the stage skills.
argument-hint: "<code> [spec | tests | issues | report]"
---

# Briefing: big picture first, then the user's decisions

The user should not have to open the files, and should come out of a briefing with a **mental model** — what is solved, by which algorithm, what the code contains, how it is verified — not just a list of approvals. And the user decides only what is theirs to decide.

## Who decides what
Ask of every choice: **is there a correct answer, or is it a preference?**
- **The user decides** (no correct answer; depends on their purpose, values, risk): what is solved and returned (API, outputs, scope as the user experiences it); trade-offs between values (rigor vs cost, compatibility vs cleanliness, scope vs simplicity); the definition of "verified" (level, key terms); irreversible or outward-facing changes (e.g. changing an existing API); modelling approximations.
- **The agent decides** (derivable from what was agreed, or invisible in the result): derivations; tolerance numbers derived from error or round-off analysis — the user approves the *policy* (derived, justification recorded, mutation testing must bite), not each number; conventions (exception types, internal thresholds); plumbing (scripts, logs, metadata, term lists, oracle fields).
- **The agent decides and reports**: judgment calls with small impact are listed together in one "agent decisions" item; the user may veto any, otherwise approves the list at once.
A user can always challenge an agent decision later through a spec issue.

## Files
- Review records live in the code folder `foundry/<code>/`: `spec/REVIEW.md`, `tests/REVIEW.md`, `spec/issues/REVIEW.md`, `audit/REVIEW.md`. Template: `${CLAUDE_SKILL_DIR}/template.md`. A record is the single source of truth for approval (`- Review status: IN REVIEW | APPROVED`).
- The briefing page is `foundry/<code>/pages/<stage>.html` (`spec.html`, `tests.html`, `report.html`), built from `${CLAUDE_SKILL_DIR}/page-template.html`. It is committed with the run.

## 0. The page (understanding only, no approval)
Build the page from the author's overview (`spec/overview.md` for the spec; the rules for tests; the report for the report) and the documents, **in the reader's order, not the documents' order**. Write it like a lab-meeting deck: one idea per slide, each with a one-line takeaway; conventions first; the physical picture (with a figure where it helps) before formulas; a small worked example where cheap; then structure, verification, decisions.

Slides for a spec briefing:
1. **Conventions** — units, signs, normalisations, index conventions.
2. **Problem** — the equation and boundary conditions in a few lines; what is returned.
3. **Algorithm** — 10–15 lines of pseudocode; mark new vs unchanged parts.
4. **Code structure** — required components and data flow (public functions, inputs/outputs, pipeline steps tagged with term IDs; new / unchanged / shared). File layout stays the developer's choice.
5. **Verification map** — per component: typical bugs → which test kinds catch them; weak spots (bugs invisible in some outputs) and the tests planned for them; where reference answers come from and why they are independent; the pass bar of the level.
6. **Scope in layers** — not built / rejected with an error / runs but not guaranteed / guaranteed, with what happens for each kind of input.
7. **Decisions** — decided by the user so far; the questions still open, each pointing to the slide it belongs to; the agent-decision list.

Test briefing: reuse the page and fill the verification map with the actual rules. Report briefing: add the measured results to the map and a code walkthrough on the same structure.

Formulas are written in LaTeX (`\( … \)` inline, `\[ … \]` display); the template renders them with MathJax. Pseudocode stays in code blocks; give key equations separately as display math. Figures are inline SVG.

**Show it:** if an Artifact tool is available, publish the page as a private artifact and open it (republish the same file to update it); otherwise send the file so the app can render it, or tell the user to open `foundry/<code>/pages/<stage>.html` in a browser. Keep the page open through the briefing and update it as decisions are made.

Then ask one question: **"Anything odd or missing in this picture?"** Address it before any decision.

## 1. Prepare the items (only if the record has no items yet)
1. The author drafts the items; read every document yourself and complete the list.
2. **User-domain items only**, each tagged 🔴 (open question, with the options) or 🟡 (a user-domain choice the author proposes). Each names the slide it belongs to.
3. **One item "Agent decisions"**: every agent-domain choice worth knowing, one line each with a short reason, grouped by slide. It is approved as a whole; the user may veto single lines (record them as CHANGED edits).
4. 🟢 items (restating what the user already agreed) are listed on the decisions slide, not briefed.

## 2. Brief the decisions
Depth by verification level (`foundry/<code>/foundry.json`): **L1** — the 🔴 items one by one, everything else approved at once from the page; **L2** — 🔴 and 🟡 one by one, then the agent-decision list; **L3** — as L2, and the agent-decision list is walked through slide by slide. With no level yet (first spec briefing), use L2.

One item per message:

```
✅ [previous n/total] Decision: <one line>          (omit on the first item)
---
### [n/total] <plain-language title>   (page: slide <k>)
<what is being decided and why it is the user's call>
<options with consequences; tables or a small diagram>
**My view:** <your honest assessment, including weaknesses>
👉 **[n/total]** <the concrete question>
```

- Wait for the answer before the next item. Explain from first principles when asked "why?". The user may overrule; record it, do not argue past one honest statement of the trade-off.
- Reply in the user's language. Documents and pages stay in English.

## 3. Record immediately after each answer
In the review record, before the next item: `Status:` (APPROVED · CHANGED · DEFERRED · PENDING), `Human:` (verbatim), `Decision:` (one line, English), `Edits needed:` (CHANGED only), `Verified:` (`no` for CHANGED until re-briefed, else `n/a`). Update the decisions slide. Do not edit the documents during the briefing.

## 4. After the last item
If anything is DEFERRED or PENDING, list it and stop. Otherwise send all `Edits needed` to the author in one delegation (spec → `foundry:spec-writer`, tests → `foundry:test-designer`, report → `foundry:auditor`), quoting the decisions.

## 5. Re-brief the changes
Show each CHANGED item's resulting text in plain language, and update the page. On confirmation set `Verified: yes`; otherwise send it back.

## 6. Approve
Only when the user explicitly approves the whole review: set `- Review status: APPROVED (<date>)` with the Edit or Write tool. A hook blocks this while anything is open or unverified. Commit (record and page), then return to the calling stage skill, which continues.

## Resuming
If a record is `IN REVIEW`, reopen the page, give a one-line recap ("Spec briefing: 2 of 4 decided; next: …"), and continue at the first PENDING item.
