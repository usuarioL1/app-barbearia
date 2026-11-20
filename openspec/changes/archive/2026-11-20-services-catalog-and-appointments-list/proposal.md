# Proposal

## Why

The customer catalog currently uses imagery that does not clearly distinguish the haircut-and-beard combo, and it lacks the requested services and matching visuals. On `/agendamentos`, the upcoming summary can contain several active bookings, but the main view highlights only the nearest one, leaving the remaining bookings less visible and harder to manage.

## What Changes

- Replace the combo service image with a distinct, high-quality haircut-and-beard image and map catalog and appointment imagery to services consistently.
- Add Sobrancelha (15 min, R$ 20,00), Pezinho / Acabamento (15 min, R$ 15,00), and Hidratação Capilar (30 min, R$ 40,00) to the local seed and Xano catalog without deleting existing services. Update the existing local Sobrancelha seed to the specified price and duration rather than adding a duplicate.
- Provide suitable assets for the requested services and use the eyebrow asset already present for Sobrancelha.
- Keep the featured next appointment and add a complete list of the customer's upcoming active appointments on `/agendamentos`, retaining supported cancellation controls and repository-backed data.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `customer-portal`: Require distinct service imagery and the specified catalog entries, and show all upcoming active appointments in addition to the featured next appointment.

## Impact

- Customer catalog and appointment presentation in `app_barbearia/customer_portal.py`.
- Local catalog seed in `app_barbearia/mock_repository.py` and regression coverage in `tests/`.
- New or replaced images in `assets/`.
- Xano `service` records in workspace 149139, added without deleting existing services; verify title matches first to avoid duplicates.
- No change to appointment API contracts, authorization, status transitions, or booking rules.
