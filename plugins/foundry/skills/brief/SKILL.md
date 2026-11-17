---
name: brief
description: Brief the human on a set of documents section by section and record a decision for each item, so the human reviews everything without reading the files. Use right after an agent has written documents that need human approval (spec, test rules, spec issues), or when the human asks to start or continue a briefing/review.
argument-hint: "[spec | tests | <path to REVIEW.md>]"
---

# Briefing: section-by-section human review

The human should not have to open the files. You walk them through every section, one item at a time, and record their decision immediately. Nothing is approved until every item has a decision.

## Files
- The review record lives next to the documents: `spec/REVIEW.md`, `tests/REVIEW.md`, ... Template: `.claude/skills/brief/template.md`.
- The review record is the single source of truth for approval. Its header line `- Review status:` is `IN REVIEW` or `APPROVED`.

## 1. Prepare (only if the review record has no items yet)
1. The authoring agent should have drafted the item list (one item per section, with a tag). If it did not, draft it yourself.
2. **Read every document in full yourself** and complete the list: add any section or choice the author did not list. In particular, any number or choice that the human did not explicitly agree to is 🟡.
3. Split large tables into groups of 3–4 rows by theme, one item per group.
4. Order: follow the documents' reading order. Put open questions (🔴) in the item where they belong, not at the end.
5. Tags: 🟢 agreed by the human already · 🟡 proposed by an agent · 🔴 open question needing a decision. An item takes the most severe tag of its contents.

## 2. Brief, one item per message
Open with one message: what was written, how many documents and items, the order. Then for each item:

```
✅ [previous n/total] Decision: <one line>          (omit on the first item)
---
### [n/total] <file> §<section> — <plain-language title>
<one or two lines: what this section decides>
<content, with 🟢/🟡/🔴 markers; use tables or small diagrams>
**My view:** <your honest assessment, including weaknesses>
👉 **[n/total] Approve?** <for 🔴: the concrete options>
```

Rules:
- **One item per message. Wait for the human's answer before moving on.** Never batch several 🟡/🔴 items.
- Explain in plain language: what is being decided, why the author chose this, the alternatives, and the consequences. Assume the human has not read the file.
- If the human asks "why?" or is confused, explain from first principles (why the thing is needed at all) before returning to the item. Then ask again.
- The human may overrule the author. Record the change; don't argue past one honest statement of the trade-off.
- Consecutive 🟢-only items may be offered together: "Items 8–10 only restate what you agreed. Approve all, or open any?" Expand on request.
- Reply in the human's language. Documents stay in English.

## 3. Record immediately after each answer
Update the item in the review record before sending the next item:
- `Status:` APPROVED · CHANGED (approved with a change) · DEFERRED (postponed; blocks approval) · PENDING
- `Human:` the human's words, verbatim, in their language
- `Decision:` one line in English
- `Edits needed:` concrete file/section changes (CHANGED only)
- `Verified:` `no` for CHANGED items until step 5; `n/a` otherwise

Do not edit the documents during the briefing. Collect the changes.

## 4. After the last item
1. If any item is DEFERRED or PENDING, list them and stop. The review stays open.
2. Send all `Edits needed` to the authoring agent in one delegation (spec → `spec-writer`, tests → `test-designer`). Quote the decisions; do not reinterpret them.

## 5. Re-brief the changes
For each CHANGED item, show the human the resulting text in plain language ("Decision X is now reflected as …"). If the human confirms, set `Verified: yes`. If not, send it back to the author.

## 6. Approve
Only when the human explicitly approves the whole review: set `- Review status: APPROVED (<date>)`. A hook blocks this while any item is PENDING or DEFERRED, or any CHANGED item is not `Verified: yes`. Never work around the hook. Then return to the calling stage skill for the next step.

## Resuming
If a review record is `IN REVIEW`, resume at the first PENDING item. Start with a one-line recap: "Resuming the spec briefing at [6/17]; 5 decided so far."
