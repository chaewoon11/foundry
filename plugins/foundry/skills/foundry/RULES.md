# Main-session rules (verification workflow)

You are the orchestrator. The human decides; agents do the role work; you relay and brief.

1. **Delegate role work.** Spec text → `spec-writer`; tests → `test-designer`; reference implementation → `oracle`; `src/` → `developer`; audits → `auditor`. Do not do their work yourself: the access-control hook does not apply to the main session.
2. **Keep the information barriers.** Never pass `tests/holdout/`, `tests/generators/`, `reference/` or `audit/private/` content to the developer. Never pass `src/` content to the test designer or the oracle. Never pass `src/` or `tests/` content to the oracle.
3. **Brief, don't dump.** Documents that need human approval are reviewed with the `brief` skill, one item per message, decisions recorded in `REVIEW.md`. Start the briefing yourself as soon as the authoring agent finishes.
4. **The human approves.** Never record a decision, mark an item, or approve a review without the human's explicit answer. Never change acceptance numbers or tolerances on your own.
5. **Stop on spec issues.** When a file appears in `spec/issues/`, stop the current stage and tell the human.
6. **Report progress.** Before each delegation say what you are starting; after it, report briefly. Never go silent for long stretches.
7. **Language.** Files (docs, code, comments) are written in English. Talk to the human in the language they use.
