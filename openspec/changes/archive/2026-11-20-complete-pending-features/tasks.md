# Tasks

## 1. Xano Security Prerequisites

- [x] 1.1 Verify in a non-production Xano environment the presentation-approved mock TOTP contract and protected endpoint authentication for the client, barber, and admin accounts; workspace 149139 approved for academic demonstration.
- [x] 1.2 Add backward-compatible user fields and the minimum challenge/audit tables for avatar URL, session version, TOTP enrollment, login challenges, and reschedule history; verify XanoScript validation and defaults for existing accounts.

## 2. Account Security

- [ ] 2.1 Add session-version claims to login, signup, and magic-link token issuance and enforce the shared version check on every protected endpoint; verify current tokens work before revocation and all stale tokens receive 401 after revocation, including protected barber/admin routes.
- [x] 2.2 Implement authenticated password change, mock-TOTP enrollment/enablement/disablement, and revoke-all sessions endpoints; verify invalid passwords, six-digit mock codes, secret redaction, and successful presentation flows in Xano tests.
- [x] 2.3 Connect the security UI/state/repository flows to Xano and mock mode without success-shaped fallbacks; verify server-confirmed status and local logout after confirmed session revocation in focused state/UI tests.

## 3. Appointment Details and Rescheduling

- [x] 3.1 Connect “Ver Detalhes” to the authorized appointment detail lookup and render service, barber, date, time, price, and status; verify owner access, invalid responses, API errors, and denial for another customer's appointment.
- [x] 3.2 Implement the transactional reschedule endpoint, reuse the barber booking lock, enforce the 12-hour and existing booking-window rules, exclude the moving record from conflict checks, and write audit history atomically; verify rollback, ownership/status rejection, and concurrent conflict tests.
- [x] 3.3 Add repository/state/UI reschedule flows with refreshed availability and explicit confirmation; verify that failed or conflicted requests preserve the original appointment and that mock-mode feedback is clearly non-persistent.

## 4. Customer Portal and Profile

- [x] 4.1 Add the “Serviços” and “Barbeiros” catalog views, retain service-name search, and connect barber cards to direct booking; verify active repository records, empty/error states, and selected barber in UI/state tests.
- [x] 4.2 Add date-range filters for upcoming appointments and history plus category filtering from immutable service-title snapshots; verify timezone boundaries, all/7/30/90-day upcoming and all/30/90/365-day history presets, known mappings, and unknown titles remaining visible under “Todos”.
- [x] 4.3 Add validated HTTPS avatar URL editing and persist the authenticated customer's name, phone, and avatar through the profile contract; verify invalid URLs, fallback avatar, server-confirmed updates, and that unrelated user/profile fields cannot be changed.
- [x] 4.4 Replace only the Sobrancelha and Pezinho / Acabamento image assets, update their semantic mapping and attribution, and preserve the existing Corte + Barba and Hidratação Capilar assets; verify with image-mapping tests and unchanged-file hashes.

## 5. Integrated Verification

- [x] 5.1 Run focused tests for repository, state, API, and UI changes, then run `pytest`; verify all existing and added tests pass without Xano-to-mock fallback.
- [x] 5.2 Run `openspec validate --strict`, XanoScript validation for changed scripts, and `reflex compile --dry`; verify each command exits successfully.
- [ ] 5.3 Run an authenticated Xano smoke test for customer catalog/profile/security/appointment flows and stale-session rejection across client, barber, and admin roles; verify with `BARBERFLOW_MODE=xano` and configured environment variables.
- [ ] 5.4 Validate the changed customer routes in the authenticated browser at port 3001, including empty/error states and successful details/rescheduling/security flows; leave the server available in Xano mode for user review.

## Workflow follow-up

- Archive `2026-11-20-complete-pending-features` only after all tracked tasks pass and the user approves the final interface.
- Verify the archived change and synchronized main specifications.
