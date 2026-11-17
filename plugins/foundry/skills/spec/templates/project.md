# Project contract

## Languages and tools
| Component | Language / libraries |
|---|---|
| Main code (path from foundry.json `source`) | |
| Reference implementation (`reference/`, if any) | <!-- preferably a different method and library --> |
| Tests (`tests/`) | |

## Main code: public API
<!-- What the tests call: module/function signatures, inputs, outputs, units, errors. For an extension of existing code: what is new, and which existing behaviour must stay unchanged. -->

## Entry points (`scripts/` in this folder; written by the orchestrator, not by agents)
All scripts run from the project root as `foundry/<code>/scripts/<name>` and exit non-zero on failure.
**`FOUNDRY_SRC`**: if set, it names a directory holding a copy of the main code (same layout as the `source` paths); every script that builds or runs the main code must use it instead of the original. `mutate` relies on this.

| Script | Who runs it | What it does | Output |
|---|---|---|---|
| `build` | developer | build / import-check the main code | exit status |
| `run-public-tests` | developer, auditor | run tests/anchor, public, external, regression (missing directories skipped) | per-test results |
| `run-holdout` | auditor | run tests/holdout | stdout: only `kind=<k> pass=<p> fail=<f>` lines and a total; details to audit/private/ |
| `run-oracle` | test designer, auditor | run the reference implementation on an input | see oracle contract |
| `mutate` | auditor | `--baseline`, or apply one patch to a copy of the main code and run public + holdout with `FOUNDRY_SRC` pointing at the copy | `<id> KILLED / SURVIVED / INVALID` |

## Oracle contract (if there is an oracle)
<!-- Input format, output format, units, error estimates and a converged flag for every output tests may use, how to call. The test designer sees only this, never reference/. Tests never call the oracle at run time: answers are frozen into case files at generation. -->

## Test metadata format
<!-- How each test declares: kind (1–6), activated term IDs, tolerance + reference to acceptance.md, expected order (kind 4), rule ID, justification. -->

## Term activity measurement
<!-- How the auditor can measure each term's size from inputs/outputs (or instrumentation) to confirm it was active. -->
