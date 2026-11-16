# xano-runtime-client Specification

## Purpose

Define a integração de runtime entre o frontend e a API Xano configurada, incluindo autenticação HTTP, tratamento explícito de falhas e separação da fonte demonstrativa.

## Requirements

### Requirement: Xano uses the configured API base URL
When Xano mode is selected, the application SHALL send API requests to the base URL supplied by `XANO_API_BASE_URL` and SHALL NOT embed an environment-specific API URL in frontend code.

#### Scenario: Configured Xano API
- **WHEN** a runtime operation is selected in Xano mode with a valid base URL
- **THEN** the request targets that configured host and preserves any API group path in the base URL

#### Scenario: Invalid or missing Xano configuration
- **WHEN** an operation requires Xano but the configured base URL is missing or invalid
- **THEN** the application reports a configuration error and does not present demo data as an Xano result

### Requirement: Protected Xano requests use the server-issued session
The application SHALL send the server-issued JWT with the `Bearer` authorization scheme only for protected requests and SHALL NOT expose passwords or tokens in user-visible messages or logs.

#### Scenario: Authenticated request
- **WHEN** an authenticated operation calls a protected endpoint
- **THEN** the request includes the current session token as a Bearer credential

#### Scenario: Public authentication or recovery request
- **WHEN** signup, login, or password recovery calls a public endpoint
- **THEN** the request does not include an existing session token

### Requirement: Xano failures are explicit and never fall back to demo data
The application SHALL distinguish successful JSON responses from HTTP, network, configuration, and invalid-response failures and SHALL preserve the failure outcome in the UI.

#### Scenario: Xano request fails
- **WHEN** Xano returns an error or the request cannot be completed
- **THEN** the application reports the failure and does not substitute mock records or indicate that the operation was persisted

#### Scenario: Xano returns an invalid response
- **WHEN** a successful HTTP response has an invalid JSON body or an unexpected data shape
- **THEN** the application reports an invalid-response failure and does not present the response as loaded data

### Requirement: Demo data remains isolated from configured Xano operations
The application SHALL use demonstrative records only when demo mode is selected without a configured Xano API and SHALL label demo operations as simulated and non-persistent.

#### Scenario: Explicit demo mode
- **WHEN** the application runs in demo mode without `XANO_API_BASE_URL`
- **THEN** it uses the demo repository and identifies its operations as simulated

#### Scenario: Xano mode is selected
- **WHEN** Xano mode is selected or an Xano base URL is configured
- **THEN** requests use the Xano repository and a failed request is not retried against the demo repository
