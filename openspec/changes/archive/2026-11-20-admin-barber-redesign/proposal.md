# Proposal

## Why

In Xano mode, unpublished endpoints can return the technical message `Unable to locate request.` and expose it in the shared feedback area, while parts of the administration and barber workspaces still describe or present mock-only behavior. These portals need a polished, consistent interface that remains honest about live data and available operations.

## What Changes

- Handle the specific unpublished-endpoint 404 gracefully in the administration and barber workspaces, keeping affected data views clean and avoiding stale or demonstrative records.
- Refine administration and barber layouts with the established black `#090909` and gold `#F2A900` identity, preserving responsive layouts, routes, and existing workflows.
- Show or enable only actions backed by an available Xano endpoint; do not simulate unsupported operations or report them as successful.
- Preserve `BARBERFLOW_MODE=xano`, current authentication and authorization boundaries, domain rules, and the existing state/repository integration.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `admin-console`: Handle unpublished Xano endpoints cleanly, use real Xano-backed data and operations without mock fallbacks, and refine the administration interface.
- `barber-workspace`: Keep agenda and status workflows Xano-backed, avoid simulated operations, and refine the barber interface.

## Impact

- Affected UI and feedback surfaces in `app_barbearia/ui.py` and `app_barbearia/workspace_pages.py`, with state-level error handling as needed.
- Existing Xano operations and mode selection in `app_barbearia/state.py` and `app_barbearia/xano_repository.py` must continue to work; this change does not add Xano endpoints.
- No change to customer routes, appointment business rules, authentication contracts, dependencies, or the Xano API.
