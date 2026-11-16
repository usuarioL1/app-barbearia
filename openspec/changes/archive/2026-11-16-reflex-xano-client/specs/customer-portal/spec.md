# Spec Delta

## ADDED Requirements

### Requirement: Xano authentication uses server-controlled identity
When Xano mode is active, the account screens SHALL authenticate through Xano and use only the session token and user profile returned or confirmed by the server.

#### Scenario: Login succeeds
- **WHEN** a visitor submits valid credentials and `POST /auth/login` succeeds
- **THEN** the application establishes the session from the returned token and server profile, obtaining the profile from `GET /auth/me` when it is not included in the response

#### Scenario: Public signup succeeds
- **WHEN** a visitor submits valid name, email, phone, and password and `POST /auth/signup` succeeds
- **THEN** the application establishes the returned server session and presents the account as a client without sending or selecting a role

#### Scenario: Login or signup is rejected
- **WHEN** Xano rejects login or signup
- **THEN** the application reports the failure and does not retain an authenticated session or present the operation as successful

### Requirement: Xano profile operations are limited to the authenticated user
When Xano mode is active, the profile screen SHALL load and update only the authenticated user's profile through the authenticated profile endpoints.

#### Scenario: Profile is loaded
- **WHEN** an authenticated client opens the profile screen
- **THEN** the application obtains the current profile from `GET /auth/me` and displays only the returned user's permitted profile fields

#### Scenario: Profile is updated
- **WHEN** an authenticated client submits valid editable profile fields
- **THEN** the application sends those fields to `PATCH /auth/me` and presents the returned profile only after the backend confirms the update

#### Scenario: Profile update fails
- **WHEN** Xano rejects the update or the returned profile is invalid
- **THEN** the application preserves the current profile and reports that the update did not complete

### Requirement: Password recovery uses Xano's public reset endpoints
When Xano mode is active, the recovery screens SHALL request and confirm password changes through the public Xano reset endpoints without sending the current session token.

#### Scenario: Reset is requested
- **WHEN** a visitor submits a valid email address
- **THEN** the application sends it to `POST /auth/password-reset` and displays only the response returned by the service

#### Scenario: Reset token is confirmed
- **WHEN** a visitor submits the email, one-time reset token, and a valid new password
- **THEN** the application sends them to `POST /auth/password-reset/confirm` and reports success only after Xano confirms the change

#### Scenario: Reset request or confirmation fails
- **WHEN** Xano rejects a reset request or confirmation
- **THEN** the application reports the failure without presenting a password change as completed

### Requirement: Customer catalog uses active Xano services and barbers
When Xano mode is active, the catalog SHALL load services and barbers from their public Xano endpoints and SHALL NOT offer demo records as available choices.

#### Scenario: Catalog loads
- **WHEN** a customer opens services or team in Xano mode
- **THEN** the application loads services from `GET /services` and barbers from `GET /barbers`, presenting validated active records

#### Scenario: Catalog is empty or unavailable
- **WHEN** an endpoint returns no active records or its request fails
- **THEN** the application shows an empty or error state and does not offer fictitious records for a booking
