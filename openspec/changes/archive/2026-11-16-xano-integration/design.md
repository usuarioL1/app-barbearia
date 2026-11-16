# Design

## Context

The read-only inspection report records the remote workspace's current contracts and gaps. The local repository already contains XanoScript for authentication, profile, password recovery, initial catalog reads, and table definitions. Those local files have not been applied to or verified against the remote workspace.

## Goals / Non-Goals

**Goals:**
- Keep this increment restricted to authentication/recovery, profile, initial service/barber catalog reads, and local base table definitions.
- Preserve the separation between Reflex state/UI and the Xano HTTP adapter, including explicit response validation and no fallback to mock success in Xano mode.
- Mark only locally verifiable work complete.

**Non-Goals:**
- Deploy or write to the Xano workspace.
- Treat proposed local endpoints or schemas as confirmed remote contracts.
- Implement availability, appointment lifecycle operations, booking concurrency guarantees, barber agendas, reports, or administrative CRUD in this change.

## Decisions

- Preserve the read-only inspection results as the source for statements about remote contracts; local scripts remain proposals until separately applied and verified.
- Keep the existing local table definitions under `xano/table/` in scope as schema artifacts, not as evidence that booking APIs or appointment behavior are implemented.
- Keep local Xano selection explicit and surface API or response errors rather than silently returning demo data.
- Limit the customer-portal delta to authentication/recovery, profile, and initial catalog behavior. Barber and administration integration are deferred.
- Use the already completed local checks as evidence for this slice: Python tests, XanoScript syntax validation, Reflex dry compilation, and OpenSpec validation. These checks do not prove remote runtime behavior.
- Do not execute `xano push`, Meta API writes, or other remote mutations.

## Risks / Trade-offs

- [Remote schema, role, and endpoint contracts may differ from local scripts] → Keep remote inspection findings visible and do not claim deployment or runtime compatibility.
- [The live-only workspace has `allow_push: false`] → Keep this increment local and defer deployment to a separately authorized and viable workflow.
- [Deferred routes may still be represented in the Reflex adapter] → Their existence in application code does not bring their implementation or verification into this change's scope.
- [Password recovery depends on external Xano environment configuration] → Document the required configuration; do not imply the email delivery path has been exercised.

## Migration Plan

No remote migration or deployment is part of this change. A future deployment change must first confirm the target schema, endpoint contracts, required environment settings, and an authorized write path.
