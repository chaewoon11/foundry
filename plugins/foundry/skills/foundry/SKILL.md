---
name: foundry
description: Entry point and orchestrator of the foundry workflow for verification-first scientific code development. Use when the user wants to develop, extend or verify scientific code with foundry (e.g. "foundry로 ~ 하자", "code develop 워크플로우", "검증 워크플로우로 개발하자", "let's use foundry to ..."), asks where a foundry run stands or what comes next, or wants to continue one.
argument-hint: "[status | <what to build> | continue <code>]"
allowed-tools: Bash(foundry-status:*), Bash(foundry-init:*)
---

# foundry

## Rules for you, the orchestrator, and the current status of this project
!`foundry-status --with-rules`

## What to do

**Status only** (`status`, or the user asks where things stand): summarise the block above in plain language and name the next step. Do nothing else.

**Continue** (a code is in progress): pick the code (ask if several and the request does not say), recap its stage in one line, and resume the next step shown above.

**Start a new code** (the user describes something to build or extend):
1. Recommend a fresh session if this one already holds unrelated context about the code (the barriers depend on you not carrying it into agents' tasks). Continue if the user prefers.
2. Agree on a short code name and where the main code lives (an existing directory to extend, or a new one). Then run
   `foundry-init <code> --source <path> [--source <path> ...]`
   and commit.
3. Run the stages below in order, each by following its skill. Move on automatically after each approval, with a one-line heads-up.

| Stage | Skill | Ends when |
|---|---|---|
| 1. Spec — content, then verification level, then criteria; briefed | `foundry:spec` | `foundry/<code>/spec/REVIEW.md` approved, scripts in place |
| 2. Tests & oracle; test rules briefed | `foundry:design-tests` | `foundry/<code>/tests/REVIEW.md` approved |
| 3. Develop | `foundry:develop` | public tests pass |
| 4. Audit | `foundry:audit` | verdict PASS (else ask the user) |
| 5. Report; briefed | `foundry:report` | `foundry/<code>/audit/REVIEW.md` approved |

Stops that need the user: every briefing; any new file in `foundry/<code>/spec/issues/` (brief it, `foundry:spec` issues mode); a failed audit (explain the verdict and the options: strengthen tests, fix code, or revisit the spec).

When the report is approved, tell the user the run is complete, with the verdict, the verified commit, and where the report is.
