# Design

## Context

See `proposal.md` for motivation and the three delta specs for externally visible behavior. The customer portal already has a shared Reflex state and repository boundary. Search by service title/description, service and barber loading, profile editing for name/email/phone, appointment detail lookup, and appointment lock-based creation exist in part. Rescheduling, customer detail presentation, period/category filters, avatar URL, and account-security operations are not complete.

The local XanoScript uses 24-hour JWTs; login, signup, and password-reset magic-link flows issue tokens. Protected endpoints are individually declared, and the user table is Xano's built-in table. Appointment records preserve the service title, price, duration, and timestamps, while the service schema has no category field. The `barber_booking_lock` and transaction pattern already protect appointment creation.

## Goals / Non-Goals

**Goals:**

- Reuse the current state/repository architecture and keep Xano mode fail-closed.
- Make all new writes authoritative in Xano and preserve local mock behavior as explicitly non-persistent.
- Keep account secrets and other customers' data out of UI responses, client logs, and unrelated endpoints.
- Preserve existing appointment snapshots and status transitions when rescheduling.

**Non-Goals:**

- Uploading avatar files, adding SMS/email second factors, or providing account-security controls for barber/admin profiles.
- Changing cancellation policy or allowing a customer to change the barber or service while rescheduling.
- Replacing Reflex, changing the existing Xano authentication provider, or adding a general service-category management UI.

## Decisions

### Extend the existing repository boundary

Add async repository operations for rescheduling, account security, avatar URL updates, and security settings. Keep the UI and state layer responsible for validation feedback, modal/form state, filters, and refreshes; the repository validates Xano response shapes and surfaces API errors. Mock-mode operations remain isolated and cannot report Xano persistence. Reuse the existing detail endpoint for a booking's details rather than creating a parallel read contract.

**Alternative considered:** Call the Xano API directly from page components. Rejected because it would bypass the existing repository, authentication, and error-handling conventions.

### Make rescheduling a server-side transaction

Keep the existing booking's service, barber, price snapshot, duration snapshot, and status. Recalculate the end time from the stored duration. Under the barber's existing booking lock, re-read the booking, enforce ownership/status and the 12-hour limit, validate the new start against the same operating-hours and booking-window rules as creation, and check conflicts while excluding the booking being moved. Update the record and append an immutable reschedule audit event in the same transaction. A failure at any point leaves the original record and audit history unchanged.

**Alternative considered:** Cancel the old appointment and create a replacement. Rejected because it creates a cancellation/rebooking gap, risks losing the original status and snapshots, and can leave partial records.

### Keep filters local and deterministic

Filter the authenticated customer's already-loaded appointments by their date in `America/Sao_Paulo`; do not change server records or request other customers' data. Use presets of all, 7, 30, and 90 days for upcoming appointments, and all, 30, 90, and 365 days for history. Classify history from the immutable `service_title_snapshot`: combo terms take precedence, beard terms map to “Barba”, known haircut/grooming titles map to “Cortes”, and an unrecognized title remains visible in “Todos” only. Add a test whenever a new catalog service requires an explicit category mapping.

**Alternative considered:** Add a live service-category join to history. Rejected because a service can be renamed, deactivated, or deleted after the appointment, while its snapshot must remain independently presentable.

### Use an HTTPS avatar URL, never a server-side fetch

Persist `avatar_url` on the authenticated user's profile and return it through the current-user endpoint. Accept only syntactically valid HTTPS URLs with a host and without embedded credentials; do not fetch or proxy the remote image from the application server. A missing or invalid URL uses the existing local avatar presentation.

**Alternative considered:** Upload an image to application or Xano storage. Rejected per the user's choice of URL-only editing.

### Add server-side TOTP and versioned session revocation

Store TOTP enrollment state and a protected server-side secret; expose a provisioning value only during enrollment, activate only after a valid code, and require a one-time expiring challenge before issuing a JWT at login. Use standard TOTP verification on the server; never accept client-computed verification or log the secret or code.

Add a monotonically increasing session version to the user record and include its value in every issued JWT. A shared server-side guard compares the token claim to the current user value on every protected endpoint. “Sair de todos os dispositivos” increments that value, thereby invalidating old tokens on their next request. Apply the same claim to login, signup, and magic-link token issuance. Restrict setup, disablement, password change, and session revocation to the authenticated user; require reauthentication for security-sensitive changes.

**Alternative considered:** Rely on JWT expiration or clear only the current browser token. Rejected because neither immediately revokes sessions on other devices. A token denylist was also considered; the user-version check avoids storing every individual JWT.

Before implementation enables TOTP, validate that the selected Xano-supported server-side primitive can securely generate and verify TOTP and protect recoverable secrets. If it cannot, stop and request approval for a vetted server-side option; do not move secret generation or verification into the browser or silently weaken the feature.

### Keep service photography local and attributable

Replace only the eyebrow and edge-up assets, use them through the existing semantic service-image map, and retain the current combo and hydration assets byte-for-byte. Source replacement photographs with reuse rights compatible with the repository and record attribution/license metadata.

## Risks / Trade-offs

- **A protected endpoint misses the session-version guard** → Inventory and test every protected endpoint, including barber/admin and reset-login token paths, before enabling global revocation.
- **Xano's token context or crypto primitives do not support the selected guards/TOTP safely** → Validate these primitives before rollout; block release and request a design decision rather than shipping a partial security control.
- **A new service title is not in the history category map** → Keep it visible under “Todos”; add an explicit mapping and regression test before assigning a category.
- **Remote avatar URLs can change or become unavailable** → Never treat the image as identity verification; retain a local fallback and do not proxy remote content.
- **TOTP enrollment can lock out a customer if activated prematurely** → Do not enable until a current code is verified; keep challenge expiry and single-use checks server-side.

## Migration Plan

1. Add nullable/defaulted profile and security fields (`avatar_url`, session version, disabled TOTP state) and the minimum server-side tables for one-time login challenges and reschedule audit records. Existing users start with no avatar, TOTP disabled, and session version zero.
2. Deploy and test the shared session-version guard and update every token-issuance path before enabling revocation. Tokens without a version are treated as version zero only while the stored user version remains zero.
3. Deploy the password/TOTP/session endpoints and the rescheduling endpoint; verify ownership, failed transaction rollback, and legacy-session behavior in a non-production Xano environment.
4. Update repository/state/UI contracts and tests, then replace only the two requested image assets.
5. Roll out the UI after the Xano contracts are available. Roll back UI/assets independently if needed; retain the session guard after any account-security rollout so a rollback cannot revalidate revoked tokens. Reverting the guard requires waiting out issued token lifetimes and an explicit security review.
