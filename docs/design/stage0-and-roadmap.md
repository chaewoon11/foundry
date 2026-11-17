# Design: stage 0 (goal → theory → features) and the roadmap layer

Status: **draft for review** · 2026-11-17 · source: lab feedback BACKLOG §11, §12 (chaewoon11/foundry-test)

## 1. Why

Two gaps showed up in the lab runs.

1. **One code, many features.** `schrodinger1d` (Dirichlet box) and `schrodinger1d-bloch` (periodic BC, Bloch k, band structure) were two "codes" to the plugin but are features 1 and 2 of one code with one source. Run 2 had to pull run 1's tests in as regression by hand, and a rename (`n` → `nbands`) changed run 1's API without any record that a verified feature had changed.
2. **A wrong theory passes every test.** The information barriers stop code and tests from sharing a misunderstanding — but both read the same spec. If the equations in the spec are wrong (a sign rule, a missing factor, a wrong symmetry), the code and the tests implement the same wrong equations, every test passes and mutation scores look good. Nothing in today's pipeline catches this common-mode error.

## 2. The idea in one picture

```
request
  │
  ▼  stage 0 — once per code (later features append to it)
  0a goal ........ chat → goal.md                          user agrees
  0b theory ...... theorist writes theory.md + page        user decides approximations
                   theory-checker re-derives independently  disagreements briefed
  0c features .... chat → roadmap.md (order, deps, level)  user agrees
  │
  ▼  one run per feature, in roadmap order
  feature 1: spec → tests & oracle → develop → audit → report     (today's pipeline)
  feature 2: spec → …   earlier features' tests run as regression; their API is frozen
  …
```

## 3. Concepts

| Term | Meaning |
|---|---|
| **code** | one piece of software with one main-code location; `foundry/<code>/` |
| **feature** | one verifiable increment of that code (e.g. "Dirichlet eigenstates", "periodic BC + Bloch k", "band structure"); one run of the pipeline |
| **theory** | the physics and mathematics the code implements, down to the numerical problem; shared by all features; contains no code content, so every agent may read it |
| **roadmap** | the ordered list of features with dependencies and a verification level each |

## 4. Layout

```
<project>/
  <main code>                         developed in place (unchanged rule)
  foundry/<code>/
    foundry.json                      code name, source paths, features (name, level, depends_on)
    goal.md                           0a: what the user wants to compute and why; inputs, outputs, conventions
    roadmap.md                        0c: features, order, dependencies, levels, one-line scope each
    theory/
      theory.md                       0b: conventions, physical picture, approximations, derivation down to the
                                          numerical problem, solvable limits, symmetries, references
      claims.md                       the numbered equations/statements the code will rely on (checker's input)
      checks/                         theory-checker's independent derivations and symbolic checks + report
      REVIEW.md                       user decisions on the theory (approximations; disputed claims)
    reference/                        the oracle, shared by all features and extended per feature
    scripts/                          shared; take --feature
    pages/                            code-level pages: theory.html, roadmap.html
    features/<feature>/
      spec/ tests/ audit/ progress/ pages/      as today, per feature
```

A code without `features/` (today's layout) keeps working as a single implicit feature, so existing runs need no migration.

## 5. Stage 0

### 0a. Goal (chat, orchestrator only)
What the user wants to compute and why; inputs and outputs; units and conventions; what exists already. The orchestrator writes `goal.md` and confirms it in one message. No briefing items.

### 0b. Theory (two agents + one briefing)
- **`foundry:theorist`** (new agent) writes `theory.md` and `claims.md` from `goal.md` and the literature: conventions first, the physical picture, the approximations and why, the derivation down to the linear-algebra (or other numerical) problem, exactly solvable limits and analytic cases, symmetries, references. Every equation the code will rely on becomes a numbered claim.
- **`foundry:theory-checker`** (new agent) sees `goal.md` and `claims.md` — **not** the theorist's derivations — re-derives each claim from the literature, and checks symbolically where possible (sympy): sign rules, symmetry properties, analytic cases against the matrix formulas. Output in `theory/checks/`: per claim `agrees` / `disagrees` / `not checkable`, with the derivation.
- **Briefing** (`foundry:brief`, page `pages/theory.html` in lab-meeting style): the picture and derivation first; then the user's decisions only — the modelling approximations (e.g. two-centre, orthogonal basis) and every claim the checker disputed. Agent-domain items (derivable steps) go in the grouped list.
- Barriers: theory files contain no code content; all agents may read them. Only the theorist writes `theory.md`/`claims.md`; only the checker writes `checks/`.

### 0c. Features (chat, orchestrator only)
The orchestrator proposes a split (order, dependencies, a level per feature, one-line scope each) and agrees it with the user in chat; `roadmap.md` records it. Rule of thumb: a feature is the smallest increment with its own exactly solvable checks (run 2 would have been lighter as "periodic BC + Bloch k" and "band structure" separately).

### When stage 0 is light
For L1 work (scripts, small tools) 0b shrinks to a short `theory.md` (the formulas and conventions used) with no checker, and 0c to a single feature. The user can skip 0b entirely for code with no theory (pure plumbing).

## 6. Feature runs

Today's pipeline, per feature, with four changes:
1. **Spec from theory.** `model.md` cites the sections and claims of `theory.md` the feature implements instead of re-deriving them; it adds only feature-specific choices (API, scope, numerical method parameters).
2. **Frozen earlier features.** The spec lists what earlier features guarantee (API, behaviour) as "must stay unchanged". The test designer takes test ideas (limits, symmetries, analytic cases) from `theory.md`.
3. **Regression accumulates.** `run-public-tests --feature F` runs F's public tests and the public tests of every completed feature it depends on. `run-holdout --feature F` (auditor) runs F's holdout and the holdout of completed features. Earlier holdout stays hidden from the developer exactly as today.
4. **Amendments.** If feature F needs an earlier feature E to change (e.g. an API rename), F's developer or spec writer files a spec issue on **E** (`features/E/spec/issues/`, tagged amendment). After the user decides, E's spec is amended and E's audit is marked stale: E is re-audited before F is reported.

Mutation testing per feature targets the terms F adds or changes; at L3 a sample of earlier terms is re-checked so a change in shared code (e.g. the kinetic term) cannot silently weaken earlier verification.

## 7. Status and pages

- `foundry-status` shows the code first, then features:
  ```
  sktb  stage 0: theory briefing 1/3
    features: 1 two-centre s,p bands [L2] not started · 2 d orbitals [L2] · 3 SOC [L3]
  ```
- `pages/roadmap.html`: features × stage, level, verified commit per feature, and a cumulative term × feature verification map.
- Feature pages (`features/<f>/pages/spec.html`, …) link back to the theory page for every equation they use.

## 8. Plugin changes (summary)

| Area | Change |
|---|---|
| agents | new `theorist`, `theory-checker`; spec-writer, test-designer, oracle read `theory/`; per-feature paths |
| skills | `start`: stage 0 (0a, 0b, 0c) before feature runs; new `theory` skill; stage skills take `<code> <feature>` |
| hooks | guard expands rules per feature folder; `theory/` readable by all, written only by its agents; `reference/` at code level |
| bin | `foundry-init` creates code-level folders; new `foundry-feature-add`; `foundry-status` shows code → features; staleness per feature incl. amendments |
| scripts | shared, `--feature`; regression across completed features |
| tests | guard/status/init for features; regression and amendment flow |

## 9. Decisions for the user

1. **Theory checker independence.** Proposed: the checker sees `goal.md` and `claims.md` only, not the theorist's derivation. Stricter alternative: it sees only `goal.md` and writes its own claims, compared afterwards (more independent, more work, harder to compare).
2. **Format of the checker's work.** Proposed: plain Python scripts with sympy (`theory/checks/*.py`) plus a markdown report — easy to re-run and diff. Alternative: Jupyter notebooks (readable with derivations inline; needs Jupyter to re-run).
3. **Oracle per code or per feature.** Proposed: one oracle per code (`reference/`), extended feature by feature, since later features reuse earlier physics.
4. **Mutation testing of earlier terms** when a later feature touches shared code: proposed only at L3 (sample); L2 relies on the accumulated regression tests.
5. **Stage 0 for small work.** Proposed: L1 gets a light 0b without checker; the user can skip 0b for code without theory.
6. **Resuming run 2.** Proposed: not resumed; it stays archived. The next lab run is `sktb` (Slater–Koster tight binding), which exercises stage 0 fully.
