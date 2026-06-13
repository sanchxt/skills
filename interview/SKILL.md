---
name: interview
description: Ask the user clarifying questions freely and persistently before or during work. Use when the user invokes /interview or $interview, asks Codex to ask questions, requests collaborative requirement gathering, or wants Codex to clarify tradeoffs, UI/UX, plans, implementation details, status, assumptions, constraints, or requirements until enough information is available.
---

# Interview

Treat the user as an always-available collaborator. If any information would materially improve the work, ask the user directly instead of guessing.

## Core Behavior

- Ask questions about anything relevant: requirements, tradeoffs, product intent, UI/UX preferences, architecture, implementation details, status, constraints, data, edge cases, testing, deployment, or priorities.
- Continue asking follow-up questions until the task has enough information to proceed confidently.
- Prefer a small number of high-signal questions at a time.
- State why an answer matters when the tradeoff is not obvious.
- Offer a sensible default when possible, but make clear what assumption would be used if the user does not care.
- Resume work after the user answers; do not turn clarification into an open-ended interview when enough context exists.

## Question Style

- Ask direct, concrete questions.
- Group related questions together when it reduces back-and-forth.
- Use short option lists only when the choices are genuinely constrained.
- Ask about priorities when multiple valid approaches exist.
- Ask for examples, references, screenshots, or acceptance criteria when they would materially reduce ambiguity.

## Stop Condition

Proceed once the remaining unknowns are low-risk, reversible, or can be handled with clearly stated assumptions.
