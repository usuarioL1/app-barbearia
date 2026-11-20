# Design

## Context

See `proposal.md` for motivation and `specs/admin-console/spec.md` and `specs/barber-workspace/spec.md` for the behavior contract. The administration and barber pages share a role layout whose global feedback area displays `AppState.error_message`. Xano errors retain their HTTP status and message through the repository boundary, so an unpublished route currently exposes `Unable to locate request.` as a global error. Several loaders populate the same page state from multiple requests, and controls exist for operations that the Xano repository does not support. The existing theme already defines near-black and gold tokens; some workspace components also use local style values.

## Goals / Non-Goals

**Goals:**

- Contain the exact unpublished-endpoint 404 behavior to administrative and barber workspace reads.
- Keep unavailable data views free of stale or demonstrative records while preserving the existing empty-state presentation.
- Make unsupported operations unavailable in the UI and preserve backend-confirmed results for supported actions.
- Polish the admin and barber pages with a consistent, responsive `#090909` / `#F2A900` theme.
- Keep the existing Xano mode, authentication, authorization, endpoint paths, and domain rules intact.

**Non-Goals:**

- Add, publish, or remap Xano endpoints.
- Change customer portal behavior, authentication contracts, appointment rules, database schema, or permissions.
- Treat arbitrary 404 responses or non-404 failures as empty results.
- Introduce mock data or fallback behavior in Xano mode.

## Decisions

### Handle only the known read-endpoint 404 in workspace state

The user explicitly chose UI-only suppression while requiring `state.py` and `xano_repository.py` to remain intact. Those constraints mean the shared state exposes only the error text to the UI, not the HTTP status. Therefore, recognize only the exact message `Unable to locate request.` in the admin/barber role layout, suppress it from global feedback, and replace the affected page content with a neutral unavailable-data state so stale records are not rendered. Other error messages retain the normal feedback path. This choice intentionally cannot distinguish the same exact text returned with a different HTTP status.

For mutations, never convert a failed request into an empty or successful result. Unsupported controls should be hidden or disabled; if an attempted supported action receives an error, preserve displayed data and report a concise user-facing failure without optimistic updates.

**Alternative considered:** Modify API/state boundaries to retain and classify the HTTP status, or map every 404 to an empty list. Rejected to honor the user's request to leave state/repository behavior intact and because broader status mapping could misclassify unrelated errors.

### Preserve Xano as the source of truth

Keep `BARBERFLOW_MODE=xano` selection and current repository/API contracts. Use only successful Xano responses for operational records and metrics; do not fall back to `mock_repository` when an endpoint is missing. Do not add an endpoint in anticipation of a UI action. Keep user-role provisioning manual and settings read-only unless a permitted Xano operation is added separately.

**Alternative considered:** Make unsupported actions appear to succeed locally until endpoints are published. Rejected because it would misrepresent persistence and diverge from the backend.

### Refine shared workspace presentation using existing theme tokens

Apply the exact black and gold values consistently across the role layout and workspace components. Prioritize readable hierarchy, spacing, filters, status badges, data tables, and narrow-screen reflow; retain existing routes, data bindings, supported controls, and empty/loading/error states.

**Alternative considered:** Replace screens with static reference images or create new operations to match them. Rejected because the existing views must remain functional and visuals must not imply unsupported data or behavior.

## Risks / Trade-offs

- [Risk] UI-only matching cannot verify the HTTP status and could suppress an identical message from another response. → Match only the exact text, limit it to the admin/barber layout, and document the limitation; the approved scope preserves `state.py` and `xano_repository.py`.
- [Risk] Hiding an action can reduce visible functionality while an endpoint is unpublished. → Prefer an honest disabled/omitted control over a simulated operation and retain all currently supported backend operations.
- [Risk] Shared layout edits could unintentionally affect other roles. → Keep error classification scoped to admin/barber state flows and verify customer routes remain unchanged.

## Migration Plan

No database migration or Xano deployment is required. Implement and validate the scoped UI/state behavior while running with `BARBERFLOW_MODE=xano`; verify real endpoint responses, the exact unpublished-endpoint 404, and supported mutations before release. Rollback consists of reverting the UI/state change; no persisted data format changes need reversal.
