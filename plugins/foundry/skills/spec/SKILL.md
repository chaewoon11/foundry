---
name: spec
description: Stage 1 — write or revise the specification with the human (model, terms, acceptance criteria, project contract), then brief it for approval. Also resolves open issues in spec/issues/.
argument-hint: "[new | issues]"
disable-model-invocation: true
---

# Stage 1: Specification and agreement

Goal: fix **what is solved, how it is judged, and when we are done** — before any code exists. Tests chosen after the code tend to lean toward what already passes.

## Mode: `new` (default when `spec/` is empty)
1. Discuss the problem with the human until the main choices are clear (equation, units, boundary conditions, method, oracle method, language, acceptance numbers). Offer defaults; let the human pick.
2. Copy the templates from `.claude/skills/spec/templates/` into `spec/` if they are not there yet.
3. Delegate to the `spec-writer` agent, quoting the agreed decisions. It writes the four spec files and drafts the item list in `spec/REVIEW.md`.
4. **Immediately start the briefing** (`brief` skill on `spec/`): "The spec is written. I'll brief you starting with model.md. Item 1: …". Do not ask the human to read the files.
5. After all items are decided: delegate the collected edits to `spec-writer`, re-brief the changed items, and approve `spec/REVIEW.md` once the human confirms.
6. Create the `scripts/` entry points described in `spec/project.md` (main session only — no agent role may write `scripts/`):
   `scripts/build`, `scripts/run-public-tests`, `scripts/run-holdout`, `scripts/run-oracle`, `scripts/mutate`. Show the human what each does in one line each.
7. If the developer needs extra Bash commands, add regexes to `developer.bash_allow` in `.claude/hooks/policy.json` (human approval required).

## Mode: `issues`
1. List open files in `spec/issues/` (no `## Resolution` section).
2. Brief each issue as one item (`brief` skill, review record `spec/issues/REVIEW.md`): what was found, where, the possible interpretations, your view. Record the human's decision.
3. Delegate to `spec-writer` to update the spec and append `## Resolution` to each issue; re-brief the changes.
4. Report which downstream artifacts must be redone (tests → `/design-tests tests`, oracle → `/design-tests oracle`, code → `/develop`).

## Exit condition
`spec/REVIEW.md` is APPROVED and the `scripts/` entry points exist. Next: `/design-tests`.
