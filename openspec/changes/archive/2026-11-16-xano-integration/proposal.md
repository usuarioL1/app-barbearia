# Proposal

## Why

The project needs a small, locally verifiable Xano integration slice before expanding into booking and administration workflows. This change captures the authentication, profile, and initial catalog work already represented in local XanoScript and Reflex code, without claiming that the scripts are deployed or that remote contracts have been confirmed.

## What Changes

- Keep this change limited to authentication and recovery, profile, initial service/barber catalog reads, and the base table definitions already present under `xano/`.
- Validate the local XanoScript and Reflex changes and document the remote schema and endpoint gaps.
- Keep all work local: do not run `xano push`, write through the Meta API, or otherwise alter the Xano workspace.
- Defer availability, appointment operations, barber agendas, and administration to future changes.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `customer-portal`: local authentication, profile, and initial catalog behavior.

## Impact

- Local XanoScript under `xano/` and the Reflex authentication, profile, and catalog integration.
- Local automated tests and XanoScript/Reflex validation.
- The remote Xano workspace remains unchanged; local scripts and table definitions are not evidence of deployment or runtime compatibility.
