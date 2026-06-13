---
name: bug-finder
description: Rigorous senior-engineer bug finding and implementation review. Use when the user asks Codex to inspect files, changes, features, integrations, APIs, external services, payment flows, auth flows, AI integrations, webhooks, or related code for bugs, broken assumptions, logic gaps, missing edge cases, invalid third-party usage, security risks, regressions, or missing tests. Trigger on requests such as /bug-finder, bug hunt, find bugs, grill this code, review hard, test the logic, audit implementation, verify integration correctness, or thoroughly inspect related files.
---

# Bug Finder

Run a hostile-but-fair engineering review of the target files and every related path needed to understand them. Treat the task as finding concrete defects, not giving broad style feedback.

## Workflow

1. Identify the review target:
   - Start from the files, diff, feature, PR, stack trace, or behavior the user named.
   - If the target is ambiguous, infer the smallest useful scope from the conversation and repository context.
   - Expand beyond mentioned files by tracing imports, callers, callees, route handlers, hooks, components, services, jobs, schemas, migrations, tests, config, generated clients, and downstream flows.
   - Do not rely only on import chains. Search for shared state names, model/table names, field names, route URLs, cache keys, event names, status values, persisted identifiers, generated types, and fallback identifiers that connect the behavior across files.

2. Build a behavior map before judging:
   - Trace where data enters, how it is validated, transformed, persisted, emitted, rendered, retried, cached, and observed.
   - Follow upstream and downstream flow: who calls this code, what this code calls next, and what happens after success, failure, retry, cancellation, or partial completion.
   - Build a behavior graph, not a nearest-file summary: entry points, state writes, state reads, alternate paths, boundaries crossed, and invariants that must remain true after the behavior completes.
   - For each state-changing operation, trace the lifecycle until the intended invariant is enforced on every later read/request/render/retry/reconnect path.
   - Identify stale state that can outlive the operation: client memory, browser tabs, tokens, caches, optimistic UI, queued jobs, background sync, open connections, third-party state, filesystem objects, and database rows.
   - Read tests to learn intended behavior, then look for missing cases and weak assertions.
   - Use `rg` first for symbols, routes, environment variables, event names, webhooks, provider IDs, config keys, and shared types.

3. Inspect aggressively:
   - Prefer concrete, reproducible findings over speculative concerns.
   - Verify suspected issues against real code paths, data contracts, and runtime assumptions before reporting them.
   - Challenge fallback and recovery paths: retries, hydration, cache refill, default creation, upserts, reconciliation, reconnects, and any branch that can reconstruct or trust old state.
   - When code deletes, revokes, expires, disables, archives, cancels, signs out, marks inactive, or otherwise invalidates something, prove no later path can revive or continue trusting it.
   - Look for off-by-one errors, stale state, race conditions, async ordering bugs, null/undefined handling, timezone and currency mistakes, partial failures, idempotency gaps, authorization bypasses, validation holes, migration drift, and test blind spots.

4. Validate external integrations generally:
   - Treat any external dependency as a contract: payment providers, AI APIs, email/SMS, auth, analytics, storage, search, maps, CRMs, webhooks, queues, SDKs, databases, and internal services.
   - When implementation correctness depends on provider behavior, consult current official docs, SDK source, API references, changelogs, and provider examples when internet access is available or the user asks for full validation.
   - Check required parameters, auth/scopes, request signing, signature verification, callback/webhook payload shape, raw-body requirements, status/state transitions, retries, idempotency, pagination, rate limits, timeout behavior, sandbox/live differences, API/model/version names, response schemas, error formats, and deprecations.
   - Clearly distinguish source-backed facts from inferences.

5. Stress the implementation:
   - Try failure paths, edge inputs, missing environment variables, duplicate requests, concurrent requests, provider retries, expired sessions/tokens, malformed payloads, slow network responses, and rollback/compensation behavior.
   - For behavior involving shared or persisted state, simulate at least two actors or attempts when relevant: actor A changes state, actor B continues with stale state, actor B refreshes/retries/reconnects, then actor A reads the result again.
   - Look for user-visible success that only updates the immediate UI while another state owner, consumer, or recovery path remains unchanged.
   - When safe and useful, run existing tests, targeted checks, type checks, lint, or small local repro commands.
   - Do not mutate production systems or perform destructive operations.

## Stop Condition

Do not stop exploring until you can answer:

- What are the core state variables or resources involved?
- Who can create, update, delete, cache, derive, reconstruct, or revive them?
- Who consumes, displays, authorizes from, syncs, or trusts them later?
- What happens on the next request, render, retry, reconnect, refresh, job run, or external callback after the change?
- What stale state can still exist outside the target files?
- What path could make the user believe the action succeeded while the system did not reach the invariant?

Only stop expanding connected files when new paths no longer read, write, reconstruct, trust, display, or enforce the same behavior state.

6. Report like a code review:
   - Lead with findings ordered by severity.
   - Include exact file and line references when possible.
   - State impact, why the current logic fails, and the smallest credible fix direction.
   - Note missing tests only when tied to a real risk or unverified behavior.
   - If no concrete defects are found, say so and list the highest-risk areas still not fully proven.

## Output Format

Use this structure by default:

```markdown
**Findings**
- `severity` [file:line] Short title
  Impact: ...
  Evidence: ...
  Fix: ...

**Open Questions**
- ...

**Checks Run**
- ...

**Residual Risk**
- ...
```

Use severity values: `critical`, `high`, `medium`, `low`.

## Reference

Read [references/audit-checklist.md](references/audit-checklist.md) when the review touches external integrations, auth, payments, webhooks, AI APIs, concurrency, persistence, background jobs, or other high-risk surfaces.
