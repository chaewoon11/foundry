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
- README: cloud-session install via the environment setup script (with update lines, since `/plugin` is unavailable there and environments may be cached).
- Briefings show the big picture first (lab-feedback §10): `foundry:brief` builds a page `foundry/<code>/pages/<stage>.html` from the new `spec/overview.md` (conventions, problem, algorithm as pseudocode, code structure, verification map, scope in layers, decisions), published as an artifact when available, else shown as the HTML file; formulas in LaTeX via MathJax 3. The test and report briefings extend the same page. Template: `skills/brief/page-template.html`.
- Who decides what (lab-feedback §9): only the user's decisions are briefing items (questions without a correct answer: purpose, values, risk, scope, API, the definition of verified); agent-domain choices (derivations, derived tolerances, conventions, plumbing) are one grouped "Agent decisions" item approved as a list. Spec writer, test designer, review template, orchestrator rules and the acceptance template follow this. In the second lab run this cut a 61-item spec review to a few questions plus one list.
- `pages/` is written by the orchestrator only (guard); `foundry-init` creates it and the `overview.md` template.
