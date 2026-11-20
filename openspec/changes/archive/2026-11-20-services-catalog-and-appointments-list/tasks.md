# Tasks

## 1. Service imagery

- [x] 1.1 Add or replace the licensed, high-quality combo image and suitable Pezinho / Acabamento and Hidratação Capilar assets; verify each file exists, opens, and depicts its mapped service.
- [x] 1.2 Unify catalog and appointment image selection, including title-case aliases for `Combo` and Xano's `corte + Barba`; add focused tests proving the combo is distinct from Corte Masculino and each requested service maps to an appropriate image.

## 2. Service catalog data

- [x] 2.1 Update the local Sobrancelha seed to 15 minutes and R$ 20,00 and add Pezinho / Acabamento (15 minutes, R$ 15,00) and Hidratação Capilar (30 minutes, R$ 40,00); add repository tests asserting exact titles, prices, durations, and preservation of existing services.
- [x] 2.2 Inspect all matching Xano `service` records and add or reconcile only the three requested entries without deleting or changing unrelated services; preview the scoped write first and verify `GET /services` returns the expected active titles, prices, and durations without duplicates.

## 3. Complete upcoming appointment list

- [x] 3.1 Keep the featured next appointment and render a separate chronological list of every upcoming active appointment, including the featured one, with existing per-record cancellation and status behavior; add UI/state tests for multiple records, ordering, and empty/loading states.

## 4. Integration verification

- [x] 4.1 Run `pytest` and `reflex compile --dry`; verify both pass with `BARBERFLOW_MODE=xano` and no mock fallback.
- [x] 4.2 Inspect `/servicos` and `/agendamentos` in the running app with multiple upcoming bookings; verify all requested service details and images and that every eligible appointment remains manageable.

## Workflow follow-up

- Archive the change only after all implementation tasks and visual acceptance checks are complete.
- Verify the archived change and resulting customer-portal spec.
