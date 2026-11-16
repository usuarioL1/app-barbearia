# Design

## Context

See `proposal.md` for the motivation and the spec deltas for the required behavior. The app already has a configurable `request_json` HTTP client, a `XanoRepository` with mappings for the requested endpoint paths, and Reflex state handlers that call the repository for authentication, profile, recovery, and catalog operations. The transport currently maps HTTP and JSON failures to explicit errors, while the repository validates response shapes. The authenticated request header and live Xano contract still need verification against the published API. Demo mode is deliberately supported and must remain distinct from Xano mode.

## Goals / Non-Goals

**Goals:**
- Keep one server-side HTTP path through the existing API client and Xano repository.
- Send server-issued credentials only to protected endpoints and retain the current user's role and identity from server responses.
- Use the configured API group URL without hard-coding environment-specific URLs.
- Preserve visible errors and prevent failed live calls from appearing as successful or falling back to demo records.
- Validate the published request and response contract before changing any field mapping.

**Non-Goals:**
- Add appointment, administration, availability, or reporting endpoints beyond the requested auth/profile/catalog calls.
- Change Xano workflows, database schema, user provisioning, or password-reset policy.
- Persist authentication credentials in browser storage or introduce a new authentication mechanism.
- Test account creation or send reset email as part of routine live smoke testing without a controlled test account.

## Decisions

1. **Reuse the existing transport and repository.** Route the requested operations through `request_json` and the current `XanoRepository` methods rather than adding parallel HTTP calls in page components. This preserves current validation and error translation. A second client or direct requests from Reflex components were considered but would duplicate configuration, authentication, and failure handling.

2. **Use `XANO_API_BASE_URL` as the only API root.** Keep the Xano API group path in the configured base URL and append only the relative endpoint path. Do not copy the deployment URL into source code. Invalid configuration remains an explicit error; it does not select demo data.

3. **Use the server-issued token for protected calls only.** Login and signup establish the session from the returned token and profile, loading `GET /auth/me` when the response omits the profile. Profile read/update requests use that token; login, signup, and password-reset requests do not. Keep the token in the existing private Reflex server-side state and clear it when authentication is rejected or expired. Do not move it to browser storage or log request payloads/headers.

4. **Keep the repository mode boundary strict.** Preserve demo behavior when demo mode is selected without an Xano URL. Once Xano mode is selected or the URL is configured, errors remain errors and are not retried through the mock repository. This avoids success-shaped fallback behavior.

5. **Confirm the live Xano contract before adjusting mappings.** Check the published endpoint definitions and response shape for token keys, profile fields, catalog list envelopes, and active-record fields. Retain strict response validation and make only the mappings required by observed responses. This avoids accepting malformed data or silently guessing at backend contracts.

6. **Test at transport, repository, and runtime levels.** Use mock HTTP transports to assert request paths, methods, payloads, Bearer behavior, and error handling; repository/state tests to verify server-profile and UI outcomes; then start Reflex in Xano mode and make non-mutating live requests to `GET /services` and `GET /barbers`. Do not create a real account or send a reset email as a smoke test without a controlled test account.

## Risks / Trade-offs

- [Published Xano response shapes differ from existing repository assumptions] → Inspect endpoint definitions and validate real catalog responses before changing mappings; add fixtures for each observed shape.
- [The API is unavailable during live verification] → Complete deterministic transport/repository tests and record the live check as blocked rather than treating a mock response as proof of connectivity.
- [A session expires while the app remains open] → Treat an authorization response as unauthenticated, clear local identity/session state, and require login again.
- [A live test could mutate user data or send email] → Restrict routine API smoke checks to the public catalog GET endpoints; use only a specifically controlled test account for mutating auth checks.

## Migration Plan

No schema migration is expected. Deploy the application with `XANO_API_BASE_URL` provided through the existing environment configuration. Rollback consists of reverting the application change; the demo repository remains available when explicitly selected and does not require data migration.

## Open Questions

None. The published endpoint contract should be verified during implementation; that verification may refine field mapping without changing the user-visible behavior defined by the specs.
