---
name: report
description: foundry stage 5 for one code — brief the verification report after a PASS verdict and get the user's approval. Usually run from the foundry skill.
argument-hint: "<code>"
---

# Stage 5: report (folder `foundry/<code>/` = CODE)

1. Check `CODE/audit/verdict.md` is PASS and that nothing in the spec, tests or main code changed after the audit (`foundry-status` says so). Otherwise go back to the audit.
2. If `CODE/audit/report.md` is missing or incomplete, hand to `foundry:auditor` to write it (sections listed in its definition, including the verified versions).
3. Brief it (`foundry:brief`, record in `CODE/audit/REVIEW.md`): scope and results; remaining limitations (with the option to fix test-set problems first); anything the report does not yet record. Apply changes through `foundry:auditor`, re-brief, approve when the user confirms.
4. Tell the user the run is complete: verdict, verified commit, report location.
