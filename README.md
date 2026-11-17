# foundry

A scientific code development plugin, verification-first.

Built for scientific codes (especially for materials science and condensed matter physics).
The user describes the code they want; agents write the spec, the test set, a reference implementation and the code; the user approves each step through short briefings. When it is done, "is it verified?" is answered by one table and one number, not by opinion.

## Install

```
/plugin install foundry --marketplace chaewoon11/foundry
```

or, in two steps:

```
/plugin marketplace add chaewoon11/foundry
/plugin install foundry@sci-workflows
```

Requires `python3` (hooks and helper scripts). The bundled script templates assume Python + pytest projects; other languages adapt them during the spec stage.

## Use

```
/foundry:start                             # or just say: "let's use foundry to …"
"Extend my solver in src/solver/ with periodic boundaries and Bloch k."
```

Start a new code in a fresh session. From there the run proceeds on its own. The user does three things:

1. **Describe** what they want, settle the spec together, then pick a verification level (L1 light · L2 standard · L3 strict). Claude recommends one with reasons once the spec shows what is at stake.
2. **Answer briefings.** Each document that needs the user's approval is explained one item at a time in plain language: what was decided, why, the alternatives, and Claude's view. The user approves, changes, or asks.
3. **Decide when asked.** Apart from briefings, the run stops in only two cases: an agent finds a problem in the spec, or the audit fails. Either way the user is told what happened and what the options are, and decides.

A new session picks up a run where the user left off: "let's continue", or `/foundry:start status`.

## How a run goes

```
 user: describe ─▶ 1. Spec ─────────▶ 2. Tests & oracle ──▶ 3. Develop ──▶ 4. Audit ──▶ 5. Report
                   spec-writer        test-designer ∥        developer      auditor       briefing
                   ▲ level, briefing  oracle                                  │
                   │                  ▲ briefing                              ├─ PASS ─▶ report
                   │                  │                                       └─ FAIL ─▶ user decides:
                   └── spec issue ◀───┴──── raised by any agent                  more tests / fix code
```

| Stage | What happens | User |
|---|---|---|
| 1. Spec | Equations, units and conventions, scope, the "terms" of the model; then the verification level and the numeric exit criteria that follow from it — all fixed **before** any code is written or changed | pick the level, briefed, approve |
| 2. Tests & oracle | Test-generation rules and (L2 optional, L3 required) a slow, obviously-correct reference implementation, each written from the spec alone | briefed on the rules, approve |
| 3. Develop | The developer iterates against the public tests. It cannot edit tests; spec doubts become spec issues | — |
| 4. Audit | Coverage, mutation testing, holdout (as the level requires) → verdict | decide on failure |
| 5. Report | What was verified, against which criteria, for which commit | briefed, approve |

## Verification levels

| | L1 light | L2 standard | L3 strict |
|---|---|---|---|
| Use for | one-off scripts, analysis tools | general research code | core methods in papers, long-lived code |
| Test kinds | ① + ② | ①②③ + ④ or ⑤ | ①–⑥ as available |
| Holdout | none | some rules | all rules |
| Oracle | none | optional | required |
| Mutation testing | none | key terms, ≥ 70 % | all terms, ≥ 90 % |
| Briefing | summary + open questions | agent choices and open questions | every item |

## Agents and information barriers

If one model writes both the code and its tests, the same misunderstanding ends up in both and they agree. So each role sees only what it must:

| Agent | Writes | Cannot see |
|---|---|---|
| `foundry:spec-writer` | the spec | main code, oracle |
| `foundry:test-designer` | test rules and cases | main code, oracle |
| `foundry:oracle` | brute-force reference implementation | main code, tests |
| `foundry:developer` | the main code | holdout tests, test generators, oracle, audit details |
| `foundry:auditor` | audit results and the report | — (sees everything, changes nothing) |

The orchestrator is the main session, the Claude Code session the user works in: it hands each task to the right agent, briefs the user, and records the user's decisions. The barriers are **enforced by hooks**, not just requested in prompts.

## The test set

Rules (generators), not hand-picked cases.

| Layer | Kind | Checks | Needs an answer |
|---|---|---|---|
| Anchor | ① analytic / textbook | basic sanity | yes, by hand |
| Net | ② transformation relations | symmetry, invariance | no |
| Net | ③ consistency relations | two routes, same answer | no |
| Net | ④ convergence order | converges at the predicted rate | no |
| Scale | ⑤ machine-made answers | matches the oracle / a manufactured solution | from the oracle |
| Scale | ⑥ external references | matches community data | yes |

Holdout cases come from different seeds and a different input region than the public ones.

## When is it "verified"?

> Within the stated scope, every term of the model is active in tests of at least two independent kinds, the test set catches at least 90 % of bugs planted term by term, and every holdout test passes. (L3; L1 and L2 use lighter numbers.)

The audit checks the **test set**, not the code: coverage (was every term exercised?), mutation testing (do the tests catch planted bugs?), holdout (did the code pass by fitting the public tests?).

## What a run leaves in the project

```
<project>/
  <main code>                  ← developed in place, where the project keeps it
  foundry/<code>/
    foundry.json               ← code name, main-code paths, verification level
    spec/                      ← model, terms, acceptance, project contract, REVIEW.md (the user's decisions)
    tests/                     ← anchor, generators, public, holdout, regression, REVIEW.md
    reference/                 ← the oracle
    audit/                     ← coverage, mutation, holdout, verdict, report
    scripts/                   ← build, run-public-tests, run-holdout, run-oracle, mutate
    progress/                  ← agents' progress notes (for resuming)
```

One project can hold several codes. A project without `foundry/` is left alone: no status, no rules, no restrictions.

## Known limits

- Bash commands are only partly checkable by a hook: the developer is limited to an allowlist, other roles to a forbidden-path check.
- Hidden files (holdout tests, audit details) are committed to git; the developer's git access is restricted, not removed.
- Briefings are where human trust enters. They can be shortened (L1), never skipped.

## Plugin layout

```
.claude-plugin/marketplace.json      marketplace "sci-workflows"
plugins/foundry/
  .claude-plugin/plugin.json
  agents/        spec-writer, test-designer, oracle, developer, auditor
  skills/        start (entry + orchestrator rules), spec, design-tests, develop, audit, report, brief
  hooks/         hooks.json, guard.py + policy.json (barriers), review_gate.py (approval gate)
  bin/           foundry-status, foundry-init
  templates/     script templates
tests/           automated tests of the plugin itself (pytest; run in CI)
CHANGELOG.md
```

## Developing the plugin

- Change the plugin only in this repository, on `dev`. Run `python -m pytest tests -q` (also runs in CI on every push).
- Try changes in a separate test project: `/plugin marketplace add chaewoon11/foundry#dev`, `/plugin install foundry@sci-workflows`; after pushing, `/plugin marketplace update sci-workflows` and `/plugin update foundry@sci-workflows`, then `/reload-plugins`. Locally, `claude --plugin-dir ./plugins/foundry` loads the files directly.
- `plugin.json` carries no `version` while on `dev`, so every push is picked up. A release sets the version, adds a CHANGELOG entry, and merges `dev` into `main`.

## References

- W. L. Oberkampf, C. J. Roy, *Verification and Validation in Scientific Computing*, CUP (2010); 2nd ed. 2025.
- K. Salari, P. Knupp, "Code Verification by the Method of Manufactured Solutions," SAND2000-1444 (2000).
- E. Bosoni et al., "How to verify the precision of density-functional-theory implementations via reproducible and universal workflows," *Nat. Rev. Phys.* 6, 45 (2024).
- K. Lejaeghere et al., "Reproducibility in density functional theory calculations of solids," *Science* 351 (2016).
- P. J. Roache, *Verification and Validation in Computational Science and Engineering*, Hermosa (1998).
- Y. Jia, M. Harman, "An Analysis and Survey of the Development of Mutation Testing," *IEEE TSE* (2011).

## License

MIT
