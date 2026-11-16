# Spec Delta

## ADDED Requirements

### Requirement: Authentication and recovery use server-controlled identity
The client SHALL use the server-issued session and role, and SHALL NOT submit or choose a business role during public signup.

#### Scenario: Public signup
- **WHEN** a visitor submits valid registration details
- **THEN** the local signup contract creates a client account and the UI presents the server result without accepting a role from the request

#### Scenario: Invalid login
- **WHEN** the authentication service rejects credentials
- **THEN** the UI reports the failure and does not create or retain an authenticated session

#### Scenario: Password recovery
- **WHEN** a user requests and completes password recovery using a valid reset token
- **THEN** the reset token is single-use and expires according to the local XanoScript contract

### Requirement: Profile and initial catalog use validated service responses
The client SHALL obtain the authenticated profile and initial service/barber catalog through the local Xano integration contracts, validate response shapes, and report failures without substituting mock results in Xano mode.

#### Scenario: Load profile and catalog
- **WHEN** a user loads their profile or the initial service/barber catalog
- **THEN** the UI presents the validated data returned by the selected repository

#### Scenario: Invalid or failed response
- **WHEN** an Xano request fails or returns an invalid response
- **THEN** the UI reports the error and does not present demo data as a successful Xano result
