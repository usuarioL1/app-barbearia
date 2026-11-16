# Proposal

## Why

The Reflex app already has an Xano repository and endpoint mappings, but the live HTTP path is not yet a trustworthy runtime integration: authenticated requests do not send the supplied JWT as a Bearer token, and the UI has both demonstrative and persisted paths that must remain clearly separated. Completing the integration lets the configured Xano API—not demo data—serve the requested account, recovery, and catalog operations while preserving the explicit demo mode.

## What Changes

- Connect the Reflex account and catalog flows to the configured Xano endpoints: signup, login, current profile, profile update, password reset request and confirmation, active barbers, and active services.
- Correct runtime HTTP authentication and response/error handling so protected calls use the server-issued Bearer token, malformed or failed responses remain visible as failures, and credentials/tokens are not logged or exposed.
- Preserve the demo repository only when demo mode is selected; never replace a failed Xano request with mock results or report a failed operation as persisted.
- Validate the implementation with focused tests and a live, non-mutating catalog request to the configured Xano API while running the Reflex app. Test account-changing or email-sending flows against a controlled test account only when one is available.

## Capabilities

### New Capabilities
- `xano-runtime-client`: Runtime HTTP integration with Xano, including environment-based configuration, authenticated requests, response validation, and explicit error behavior.

### Modified Capabilities
- `customer-portal`: Define live Xano behavior for account authentication, profile maintenance, password recovery, and the barber/service catalog while retaining explicit demo-mode behavior.

## Impact

- Affected frontend/runtime code: `app_barbearia/api_client.py`, `app_barbearia/xano_repository.py`, `app_barbearia/state.py`, and the account/catalog pages in `app_barbearia/`.
- Affected tests: API-client, Xano repository, and Reflex state tests.
- External system: the Xano API configured by `XANO_API_BASE_URL`; no endpoint URL should be hard-coded in frontend code.
- No new dependency is expected; the project already uses `httpx` through its Reflex environment.
