---
name: orchestrator
description: Run foundry — verification-first development of scientific code (materials science, condensed matter). Use when the user wants to build, extend or verify a computational code with foundry ("foundry로 ~ 하자", "foundry 워크플로우", "/foundry:orchestrator"), asks where a foundry run stands, or wants to continue one.
argument-hint: "[status | <what to build> | continue]"
---

# Orchestrator (/foundry:orchestrator)

## First, load what you need
Read, in this skill's folder (`${CLAUDE_SKILL_DIR}`):
- `RULES.md` — how you must behave. Follow it throughout.
- `WORKFLOW.md` — the stages, who does what, what each produces, when each is done, where files go.

## How to run a stage
- Each stage has its own skill: invoke it with the Skill tool as `foundry:<stage>` (`foundry:goal`, `foundry:literature`, …, `foundry:report`) and follow it. Briefings use `foundry:brief`.
- Agents are summoned with the Agent tool as `foundry:<agent>` (`foundry:spec-writer`, `foundry:developer`, …). Give each only what its stage's skill says.
- The plugin's hook enforces the information barriers between agents, using the main-code paths in `foundry/<code>/foundry.json` (written in 0a). If an agent is blocked, that is the barrier working: do not route around it.

## Then find where things stand
Look under `foundry/` in the project. For each code (`foundry/<code>/`), find the current stage as `WORKFLOW.md` describes (the first missing or unapproved product). No `foundry/` folder means nothing has started.

## Then do one of three things

**Status** (the user asks where things stand): summarise in plain language — per code, the stage and the next step. Do nothing else.

**Continue** (a run is in progress): pick the code and feature (ask if it is unclear), recap in one line where it stands, and resume at the next step.

**Start** (the user describes something to build or extend):
1. If this session already carries unrelated context about the code, suggest a fresh session (the information barriers depend on you not carrying it into agents' tasks).
2. Agree on a short code name; create `foundry/<code>/`.
3. Run stage 0 in order — 0a `goal` → 0b `literature` → 0c `formulation` → 0d `theory-check` → 0e `features` — following each stage's skill.
4. Then, for each feature in `roadmap.md`: 1 `method` → 2 `tests` → 3 `coding` → 4 `audit` → 5 `report`.
5. Move to the next stage by yourself after each approval, with a one-line heads-up. Stop only for a briefing, a spec issue, or a failed audit.

When the last feature's report is approved, tell the user the code is complete: per feature, the verdict and the verified commit.
