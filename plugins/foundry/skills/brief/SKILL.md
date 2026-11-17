---
name: brief
description: foundry's common briefing procedure — show the page, ask the user only their decisions one at a time, approve the agents' decisions as one list, record every answer verbatim, re-brief changes, approve. Used by stages 0d, 1, 2 and 5; each stage's skill says what to show and what to ask. Run by the orchestrator.
argument-hint: "<code> [<feature>] <stage>"
disable-model-invocation: true
---

# Briefing

The user should leave a briefing understanding what was built and having decided only what is theirs. Each stage's skill says **what** to show and **which** questions to ask; this skill says **how**.

## Who decides what
- **The user**: what has no correct answer — goals, approximations, method choices, the API, trade-offs between rigour and cost, whether a limit or a surviving mutant is acceptable.
- **The agents**: what is derivable or does not change results — derivations, derived tolerances, default values, conventions, plumbing. These come as one list.

## 1. Show the page
- Build the page from the stage's markdown record (the record is the source; the page is generated from it).
- Formulas in LaTeX, rendered with MathJax; pseudocode as code blocks; diagrams where they help.
- Publish it as an artifact when an Artifact tool is available; otherwise send the HTML file, or tell the user to open it in a browser.
- Keep the same page through the briefing and update it as decisions are made.

Then ask one question first: **"Anything odd or missing here?"** Deal with it before the decisions.

## 2. The user's decisions, one per message
```
✅ [previous n/N] <decision in one line>        (omit for the first)
---
### [n/N] <question in plain words>   (page: <section>)
<what is being decided and why it is the user's call>
<the options and what each leads to>
**My view:** <your honest assessment>
👉 <the question>
```
- Wait for the answer before the next question.
- If the user asks "why?", explain from the beginning, then ask again.
- The user may overrule; record it. State a trade-off once; do not argue.
- Reply in the user's language; records and pages stay in English.

## 3. The agents' decisions, as one list
Show them grouped by section, one line each with its reason. The user approves the list at once, or vetoes single lines (each veto becomes a change).

## 4. Record at once
After every answer, before the next question, update the stage's review record:

```
# Review: <stage>
- Page: <path>
- Review status: IN REVIEW            (→ APPROVED (<date>) at the end)

## [n/N] <question>
- Status: PENDING | APPROVED | CHANGED | DEFERRED
- Human: "<the user's words, verbatim>"
- Decision: <one line>
- Edits needed: <what must change; CHANGED only>
- Verified: n/a | no | yes            (CHANGED items: no until re-briefed)

## [N/N] Agent decisions
- Items: <one line each>
- Status / Human / Decision / Edits needed / Verified as above
```
Do not change the documents during the briefing; collect the changes.

## 5. Apply and re-brief
If anything is DEFERRED, stop: the review stays open. Otherwise send all changes to the agent that wrote the documents, in one message, quoting the decisions. Show each change in plain words and update the page; when the user confirms, set `Verified: yes`.

## 6. Approve
Only when the user explicitly approves the whole review, and every item is APPROVED or CHANGED with `Verified: yes`: set `Review status: APPROVED (<date>)`. Commit the record and the page, and return to the stage, which moves on.

## Resuming
If a record says `IN REVIEW`, reopen the page, recap in one line ("2 of 4 decided; next: …"), and continue at the first open item.
