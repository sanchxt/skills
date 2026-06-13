# Audit Checklist

Use this checklist selectively. Do not paste it into the final answer; use it to drive review coverage.

## Flow Tracing

- Find every import, caller, route, event subscription, scheduled job, hook, component, service wrapper, and test touching the target.
- Trace the next step after the target code runs: downstream side effects, redirects, emitted events, database writes, cache updates, notifications, and background work.
- Confirm behavior across success, validation failure, provider failure, retry, timeout, cancellation, duplicate event, and partial completion.
- Compare frontend assumptions to backend enforcement and backend assumptions to database/schema constraints.

## Code Logic

- Validate every branch that transforms user input, external payloads, database records, or cached state.
- Check defaults, optional fields, nullability, empty arrays, zero values, duplicate IDs, and unexpected enum values.
- Verify sorting, filtering, pagination, deduplication, rounding, timezone, currency, and unit conversions.
- Trace async flows for missing `await`, swallowed errors, stale closures, race conditions, and inconsistent loading/error states.
- Confirm transactions, retries, and compensating actions leave the system consistent after partial failure.

## Security And Access Control

- Confirm every privileged read/write is gated server-side, not only in UI.
- Check object ownership, tenant boundaries, role checks, resource IDs, and indirect object references.
- Review token/session expiry, refresh behavior, secret handling, logs, and environment variable fallbacks.
- Inspect input validation, output escaping, SQL/NoSQL query construction, SSRF/file path handling, and upload processing.

## External Integrations

- Identify the provider contract: endpoint, SDK method, API version, required fields, auth scheme, scopes, request signing, response shape, and error shape.
- Verify implementation against current official docs when possible, especially for recently changed SDKs/APIs.
- Check idempotency, retry safety, rate limits, pagination, cursor handling, timeouts, backoff, circuit breaking, and provider-side duplicate delivery.
- Confirm environment separation: sandbox/live, region, account/project IDs, webhook secrets, API keys, model/version names, and feature flags.
- Validate callbacks/webhooks/events with the exact payload shape, signature verification requirements, raw-body requirements, timestamp tolerance, replay protection, and state transitions.
- Ensure user-visible success is based on trusted server/provider state, not only client redirects or optimistic UI.

## Data And Persistence

- Compare application assumptions to schema constraints, migrations, indexes, cascade rules, uniqueness, and nullable columns.
- Check migration ordering, backwards compatibility, seed/default data assumptions, and rollback behavior.
- Verify cache invalidation, optimistic updates, background job replays, and eventual consistency paths.

## Tests

- Look for tests covering success paths, invalid inputs, authorization failures, provider failures, duplicate events, retries, concurrency, and boundary values.
- Prefer focused reproduction tests for concrete defects.
- Flag missing tests when a behavior is important, fragile, recently changed, or not obvious from type constraints.
