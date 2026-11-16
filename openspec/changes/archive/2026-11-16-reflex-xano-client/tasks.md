# Tasks

## 1. Verify and repair the HTTP transport

- [x] 1.1 Confirm the published Xano definitions for the requested endpoints, request fields, token/profile response keys, and catalog response envelopes; record the verified contract in tests or existing integration documentation without copying credentials, and verify each mapping against the published API.
- [x] 1.2 Update the shared HTTP client to send the supplied token as a Bearer credential only when present and preserve explicit configuration, network, HTTP, and invalid-JSON errors; verify with `python -m unittest discover -s tests -p test_api_client.py`.

## 2. Connect repository and Reflex account/catalog flows

- [x] 2.1 Verify and adjust the Xano repository mappings for signup, login, current profile, profile update, both password-reset endpoints, services, and barbers; retain server-controlled identity and strict response validation, then verify with `python -m unittest discover -s tests -p test_xano_repository.py`.
- [x] 2.2 Verify Reflex state and account/catalog pages retain server session and profile results only after confirmed responses, keep reset calls unauthenticated, clear invalid/expired sessions, and never fall back to mock data in Xano mode; verify with `python -m unittest discover -s tests -p test_client_state.py`.

## 3. Verify end-to-end runtime behavior

- [x] 3.1 Start the Reflex app with the configured Xano base URL and verify the app responds and the services/team pages load only the live results from `GET /services` and `GET /barbers`, including clear empty/error states; do not create an account or send a reset email during this smoke test.
- [x] 3.2 Run `python -m unittest discover -s tests` and verify all existing tests pass alongside the live catalog smoke test; report live API unavailability as a blocked integration check, not as a successful mock-backed test.
