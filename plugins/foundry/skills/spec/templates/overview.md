# Overview (source of the briefing page)

In the reader's order. Formulas in LaTeX (`\( … \)`, `\[ … \]`). Mark parts as new / unchanged / shared.

## 1. Conventions
<!-- units, signs, normalisations, index conventions; the one most likely to cause a factor-of-2 bug -->

## 2. Problem
<!-- physical picture in two or three sentences; the equation and boundary conditions; what is returned -->

## 3. Algorithm
```
<!-- 10–15 lines of pseudocode, each step tagged new / unchanged, with term IDs -->
```

## 4. Code structure
| Component | In → out | Terms | New / unchanged / shared |
|---|---|---|---|

## 5. Verification map
| Component / term | Typical bugs | Test kinds that catch them |
|---|---|---|
<!-- weak spots (bugs invisible in some outputs) and the tests planned for them; where reference answers come from and why they are independent; the pass bar of the level -->

## 6. Scope in layers
| Layer | Inputs | What happens |
|---|---|---|
| guaranteed | | |
| runs, not guaranteed | | |
| rejected | | |
| not built | | |
