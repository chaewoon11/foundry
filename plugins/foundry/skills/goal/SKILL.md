---
name: goal
description: foundry stage 0a — agree with the user on the starting point, the input, the output, and the method in words. Writes foundry/<code>/goal.md. Run by the orchestrator.
argument-hint: "<code>"
---

# 0a · Goal

You (the orchestrator) and the user agree, in chat, on four things — no more. No equations yet: the method is said in words. Theory, equations and literature come in the next stages.

## The four things

| | Question | Example |
|---|---|---|
| **Starting point** | New code, or extending existing code? If existing: where is it, and what does it do now? | Existing code `src/tb/`: s, p tight-binding bands |
| **Input** | What goes in? | Atomic positions, lattice vectors, Slater–Koster parameters, spin–orbit strength λ |
| **Output** | What comes out, in which units? | Band energies along a k-path, in eV |
| **Method** | What will be solved numerically, in words? | Add a spin–orbit term to the existing Hamiltonian and diagonalise the doubled matrix at each k |

## How
1. Ask for what the user has not already said. Keep it short: one or two messages, not an interview.
2. If something is vague, propose a concrete wording and let the user correct it. Do not ask about details that belong to later stages (approximations, equations, numerical methods, API).
3. For existing code, ask only for its path, what it computes now, and how it is run. Do not read the code yourself.
4. Write `foundry/<code>/goal.md` (below), show it, and get a plain "yes".
5. Write `foundry/<code>/foundry.json` with the main code's path(s), relative to the project root — the plugin's hook uses it to keep agents that must not see the code away from it:
   ```json
   { "code": "<code>", "source": ["<path>"] }
   ```
   If the path changes later, update this file. That ends 0a.
6. Hand over to 0b: tell the user to put the papers and notes they want to discuss in `foundry/<code>/literature/`.

## `goal.md`
```
# Goal: <code>

## Starting point
New code at <path>   |   Existing code at <path>: <what it does now>; run with <how>

## Input
- <item> (<units>)

## Output
- <item> (<units>)

## Method
<two to four sentences, in words>
```
