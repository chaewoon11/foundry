# Project contract

## Languages and tools
| Component | Language / libraries |
|---|---|
| Main code (`src/`) | |
| Reference implementation (`reference/`) | <!-- preferably different from the main code --> |
| Tests (`tests/`) | |

## Entry points (`scripts/`, written in the main session only)
| Script | Who runs it | What it does | Output |
|---|---|---|---|
| `scripts/build` | developer | build the main code | |
| `scripts/run-public-tests` | developer, auditor | run `tests/anchor`, `tests/public`, `tests/external`, `tests/regression` | per-test pass/fail with messages |
| `scripts/run-holdout` | auditor | run `tests/holdout` | full detail to `audit/private/`, summary counts per kind to stdout |
| `scripts/run-oracle` | test designer | run the reference implementation on an input | see oracle contract |
| `scripts/mutate` | auditor | copy `src/` to `audit/private/work/`, apply one mutation, run tests against the copy | killed / survived |

## Oracle contract
<!-- Input format, output format, units, how to call. The test designer sees only this, never reference/. -->

## Test metadata format
<!-- How each generator/test declares: kind (①–⑥), activated term IDs, tolerance, expected convergence order. e.g. a decorator, a YAML header, a sidecar JSON. -->

## Term instrumentation (optional)
<!-- How the auditor can record the magnitude of each term at runtime to confirm it was active. -->
