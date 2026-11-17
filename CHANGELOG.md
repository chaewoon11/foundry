# Changelog

## Unreleased (dev)

First version of the foundry plugin, packaged from the workflow used in the 1D Schrödinger example run (chaewoon11/foundry-test).

- Entry skill `start` (`/foundry:start`): one call starts or continues a run; the orchestrator rules and the current status are loaded when it is invoked; stages advance automatically after each approval.
- Stage skills `spec`, `design-tests`, `develop`, `audit`, `report`, and `brief` (section-by-section briefings with decisions recorded in `REVIEW.md`).
- Verification levels L1 / L2 / L3, recommended after the spec content is settled; briefing depth, test kinds, holdout, oracle and mutation testing scale with the level.
- Per-code layout `foundry/<code>/` with `foundry.json`; the main code stays where the project keeps it; several codes per project; projects without `foundry/` are left alone.
- Agents `spec-writer`, `test-designer`, `oracle`, `developer`, `auditor` with progress notes and resumption.
- Hooks: information barriers per role and per code (plugin-prefixed agent names handled; developer limited to an allowlist incl. restricted git), approval gate for `REVIEW.md` (also against shell edits), session-start status.
- `bin/foundry-init`, `bin/foundry-status` (stage inferred from files; audit staleness by git commit order).
- Script templates with `FOUNDRY_SRC`, so mutation testing runs the tests against a copy of the main code.
- Automated tests (pytest) and CI.
- Fix: the entry skill loads the orchestrator rules and status through `foundry-status --with-rules` (on PATH from `bin/`, allowed in the skill's `allowed-tools`) instead of `cat`-ing a plugin file, which Claude Code blocks outside the working directory. Verified in a live headless session: `/foundry status` worked (the entry skill was then named `foundry`), and a real `foundry:developer` agent is blocked from reading holdout tests by the plugin's guard hook.
- Fix: `mutate` removes bytecode caches from the copy and disables writing them. A cache copied with the main code could look valid for a same-size edit made within the same second, so the unmutated code ran and the mutant was wrongly reported as SURVIVED (found by the test suite; it can only under-report kills).
- Entry skill renamed from `foundry` to `start`: the cloud UI listed it only as `/foundry:foundry`; it is now `/foundry:start`.
