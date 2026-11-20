# Design

## Context

See `proposal.md` for motivation and `specs/customer-portal/spec.md` for the required behavior. The customer catalog uses a local tuple in `mock_repository.py`; the customer portal maps images in separate catalog and appointment helpers. The Xano service endpoint returns active `service` rows with title, description, price, duration, and active state, but no image field. The local seed already contains Sobrancelha at 20 minutes and R$ 25,00; the active Xano catalog currently has Corte Masculino, Barba, and `corte + Barba`, but no Sobrancelha.

The client state already derives `upcoming_appointments` and `next_appointments`; the `/agendamentos` view currently renders only the highlighted subset.

## Goals / Non-Goals

**Goals:**
- Keep service imagery consistent between catalog and appointment views without changing the Xano response contract.
- Make the requested services available in both data sources while preserving unrelated services and avoiding duplicate titles.
- Render the existing customer-owned upcoming appointment records with the same supported actions as before.

**Non-Goals:**
- Change appointment authorization, booking rules, snapshots, status lifecycle, or Xano endpoint contracts.
- Add an image field to the service table or manage catalog images in Xano.
- Reconcile unrelated existing service prices or descriptions.

## Decisions

### Use one normalized service-image mapping

Use a shared title-to-asset mapping for catalog cards and appointment imagery. Normalize title case and map known aliases, including `Combo` and the Xano title `corte + Barba`, to a dedicated combo image. Give Sobrancelha, Pezinho / Acabamento, and Hidratação Capilar semantically appropriate images; reuse the existing eyebrow asset and add dedicated assets for the two new services. Replace the current combo asset with a clearly distinct haircut-and-beard image.

This avoids changing the Xano service schema or requiring image URLs in API records. A shared resolver prevents the catalog and appointment views from drifting apart; adding a backend image field was considered but would create an unnecessary contract and data migration.

### Keep catalog updates additive and idempotent

Update the existing local Sobrancelha seed to 15 minutes and R$ 20,00, then append Pezinho / Acabamento and Hidratação Capilar with the requested values. Keep all other local services unchanged.

For Xano, inspect existing service records before writing. Add each requested title only when absent, preserving every unrelated record; if a title already exists, avoid duplication and reconcile only the requested fields. Do not run a workspace-wide destructive sync, delete, or truncate. Preview the exact record changes before applying them. If a matching remote service is intentionally inactive or otherwise conflicts with the request, stop and ask before reactivating or duplicating it.

The local source of truth remains the selected repository: Xano mode must continue using Xano-returned records and must not fall back to mock catalog entries.

### Reuse existing upcoming-appointment state and actions

Retain the highlighted next appointment and add a separate complete upcoming list sourced from `upcoming_appointments`. Preserve each appointment's existing status and cancel control; do not create client-side or success-shaped state changes. Render the list in chronological order, including the highlighted appointment, so the complete list itself is sufficient to manage all upcoming active records.

Sorting the existing records before deriving the highlighted appointment and list was preferred over maintaining a second derived collection, which could become inconsistent.

## Risks / Trade-offs

- [An existing Xano title may be inactive or have a conflicting price/duration] → Inspect all matching records before writing; do not duplicate or silently reactivate a conflicting service.
- [External photos may have incompatible licensing or visual quality] → Use appropriately licensed, high-quality assets and verify each asset against its service before adding it.
- [Adding another full list increases page length and repeats the highlighted appointment] → Keep the featured card distinct and label the complete list clearly; inclusion of the nearest appointment in both is intentional.
- [Service titles may vary in case between seed, API, and snapshots] → Normalize case and explicitly support known title aliases in the shared image mapping.

## Migration Plan

1. Add or replace local image assets and update the shared mapping and local seed.
2. Read and verify Xano service records; preview and apply only the requested additive service-record changes.
3. Add the complete upcoming list and regression tests; run the test suite and Reflex compile.
4. Inspect the catalog and appointment list in the running UI in both relevant repository modes when available.
5. Archive this change only after all implementation tasks and acceptance checks pass.

Rollback consists of reverting the focused UI, seed, and asset changes and, if needed, deactivating only the newly added Xano service records after explicit confirmation; existing service records must not be deleted.
