# Design

## Context

See [proposal.md](./proposal.md) for motivation and scope. The five customer references in `design_refs/projt ux barbearia/tela usario/` are complete screen compositions with photographs embedded in them, not standalone assets. The existing app routes are registered in `app_barbearia/app_barbearia.py`; page data and operations remain supplied by the current state and repository. `assets/` currently contains only the favicon.

Existing requirements constrain privacy, authorization, mock-vs-Xano behavior, booking states, and the 12-hour cancellation policy. This extension refines the client experience without changing those contracts. Reference-only actions and values do not become real operations or data.

## Goals / Non-Goals

**Goals:**
- Establish one documented visual system and an explicit reference-to-route map before UI implementation.
- Recompose the five customer screens and shared customer shell while retaining existing event bindings, data, loading/empty/error states, and accessible names.
- Add `/historico` as a client route over the client's already-loaded appointment history.
- Make layouts adapt to narrow viewports while leaving `state.py` and `xano_repository.py` unchanged.

**Non-Goals:**
- Add unsupported operations such as rescheduling, appointment-detail views, profile-photo upload, two-factor authentication, or logout-all-devices.
- Add fabricated appointment data, unverified user portraits, or summary values that cannot be derived from the client's loaded records.
- Change role permissions, API or repository behavior, the state model, appointment transitions, time-zone rules, or cancellation eligibility.
- Use a full reference screenshot as a page background or replace functional components with a screenshot.

## Decisions

### Visual system

The following hex values are the initial implementation tokens, sampled approximately from the supplied images and to be checked for readable contrast during UI verification:

| Token | Value | Use |
|---|---|---|
| `background` | `#090909` | App canvas |
| `surface` | `#121212` | Primary cards and forms |
| `surface-raised` | `#1B1B1B` | Nested panels and selected rows |
| `border` | `#302C26` | Card, field, and divider outlines |
| `gold` | `#F2A900` | Primary actions, active navigation, icons, emphasis |
| `gold-light` | `#FFD36A` | Hover/focus and highlighted values |
| `foreground` | `#F5F3EF` | Primary text |
| `muted` | `#B8B4AC` | Supporting text and labels |
| `success` | `#16A34A` | Confirmed/completed/active indicators where applicable |
| `warning` | `#D99A16` | Pending indicators |
| `danger` | `#DC3B35` | Cancelled and destructive-action indicators |
| `info` | `#2878C7` | In-progress information where applicable |

Use a bold sans-serif hierarchy (`Inter, Arial, sans-serif`, falling back locally without adding a package); large page titles around 30–36 px, section headings 20–24 px, body text 14–16 px, and metadata 12–14 px. Keep headings white, emphasize only key controls and short accents in gold, and reserve spaced uppercase tracking for small brand/eyebrow labels. The existing stylized brand mark may retain a Georgia serif face.

### Shared composition and navigation

- Customer desktop shell: persistent left navigation with exactly `Início` (`/`), `Meus Agendamentos` (`/agendamentos`), `Serviços` (`/servicos`), `Meu Perfil` (`/perfil`), `Histórico` (`/historico`) and `Sair`. Keep the gold (`#F2A900`) divider between sidebar and content. The active item uses a gold background and bold black (`#090909`) label and icon. The main header places the authenticated user's circular avatar/placeholder, name and existing account/logout menu at the upper right.
- Customer background: use the `#090909` canvas, a darkened local barbershop photo near the top, and restrained gold diagonal corner accents. The full-screen reference compositions must never be used as backgrounds.
- Narrow screens: collapse the rail into a compact header and horizontally scrollable route links; stack cards and form fields, and keep actions reachable. Use layout changes and existing links; do not add a menu-toggle event.
- Cards use near-black surfaces, thin warm borders, 12–16 px corner radii and restrained shadow. Inputs use dark inset surfaces, clear labels and gold focus treatment. Primary actions are filled gold with dark text; secondary actions are transparent with a gold outline.
- Statuses retain their current labels and canonical values; use text plus a colored badge/icon so meaning is not conveyed by color alone. Loading, empty, error, success, and mock-mode feedback remain visible in their existing positions.
- Extract individual photographic regions from the user-provided references into local `assets/` files for service and banner decoration. Do not treat a reference crop as a verified photograph of a named customer or barber; use a neutral avatar when a real profile photo is unavailable.

### Screen-by-screen visual mapping

The reference filename is included for traceability. Where a reference depicts unavailable functionality, the mapping explicitly limits implementation to the closest existing route and current data.

| Reference image | Existing screen / visual mapping |
|---|---|
| `Login BarberFlow_ Gestão Premium de Barbearia.png` | `/login` — keep the two-column promotional panel and centered login card; apply the shared black/gold tokens, strong brand lockup, labeled email/password fields, remember/recovery row, primary sign-in and outlined signup action. |
| `tela usario/Dashboard BarberFlow em Preto e Dourado(user).png` | `/` — two-column next-appointment and booking-hero row, then service and history previews, followed by the lower brand banner. Show at most four actual active services; every appointment and metric comes from the authenticated client's loaded data. |
| `tela usario/Serviços Premium no BarberFlow(user).png` | `/servicos` — photo hero, responsive three-column desktop grid of horizontal service cards, and three trust badges. Render only returned active services and connect `Selecionar` to the existing preselection action. |
| `tela usario/Painel BarberFlow_ Agendamentos em Preto e Dourado(user).png` | `/agendamentos` — upcoming/history tabs backed by existing filters, a featured appointment and prior rows, plus a side summary derived from loaded records. Keep cancellation governed by the unchanged 12-hour rule; omit or disable period selection, rescheduling and details when unsupported. |
| `tela usario/Histórico de Cortes BarberFlow(user).png` | `/historico` — a dedicated list of the authenticated client's completed appointments with service, barber, local date/time, status and returned price. Show category and period controls only as disabled/omitted until an existing handler supports them; any total must be derived from loaded history, never hardcoded. |
| `tela usario/Painel de Perfil BarberFlow em Preto e Dourado(user).png` | `/perfil` — 2x2 desktop grid with authenticated profile identity, existing editable name/email/phone fields, security panel, and a compact history summary. Save through the existing handler; omit or disable photo upload, two-factor and logout-all-devices controls. |
| Customer reference set | `/agendar` — improve vertical spacing in service/barber choices, calendar legibility and the summary confirmation affordance while retaining existing selection and `confirm_booking` wiring. |
| `tela barbeio/Dashboard BarberFlow em Preto e Dourado(Barbeiro).png` | `/barbeiro` — dashboard layout with daily date controls, appointments, next appointment and the current summary metrics. Do not add notification counts, ratings or monthly trends. |
| `tela barbeio/Painel Minha Agenda BarberFlow(barbeiro).png` | `/barbeiro` — agenda-focused arrangement: date navigation, readable time/client/service rows, visible status badges and current quick context. Preserve the existing date navigation and own-agenda scope; do not introduce day/week/month modes. |
| `tela barbeio/Painel Premium de Gestão para Barbearia(Barbeiro).png` | No barber-client route exists. Use only its dark list/detail treatment as a visual reference for `/barbeiro/atendimentos`; do not add a client directory, search, client detail, messaging or rescheduling actions. |
| `tela barbeio/Dashboard de Desempenho BarberFlow(barbeiro).png` | No performance route exists. Apply its restrained metric-card style only to metrics already shown on `/barbeiro`; do not add ratings, growth indicators, reviews, charts or top-service rankings. |
| `tela barbeio/Painel Premium de Configurações do Barbeiro(configuração).png` | `/barbeiro/perfil` — adapt the profile presentation to the dark profile-card treatment. Keep the existing name/role/specialty read-only; omit password, preferences, notification toggles, account deletion and editable profile actions. |
| `tela ADM/Painel BarberFlow em Preto e Dourado(adm).png` | `/admin` — admin overview with existing count/revenue/attendance cards, revenue series and recent appointments, arranged in a dense desktop grid that stacks on mobile. No sample-only values or unsupported trend comparisons. |
| `tela ADM/Painel BarberFlow em Ouro e Preto(ADM).png` | `/admin/configuracoes` — grouped read-only panels for hours, `America/Sao_Paulo` and the 12-hour cancellation policy. Do not show functional edit/save controls because those settings are not editable here. |
| `tela ADM/Agenda BarberFlow em Preto e Dourado(adm).png` | `/admin/agenda` — day/week selector, date navigation, barber and status filters, then the existing daily list or weekly columns. Keep all filters and local-time presentation intact. |
| `tela ADM/Painel de Clientes BarberFlow(adm).png` | `/admin/clientes` — search and existing client form/table, with selected information visually prioritized only where current state provides it. Do not add fake KPIs, avatars, new-client persistence or messaging actions. |
| `tela ADM/Painel Serviços BarberFlow em Preto e Dourado(Adm).png` | `/admin/servicos` — existing service form and catalog, using compact rows/cards for description, BRL price, duration, status and actions. No image upload or unsupported catalog metrics. |
| `tela ADM/Painel Elegante de Gestão da Equipe(adm).png` | `/admin/equipe` — existing team form and barber list, with specialty, active status and current actions. No fabricated photos, ratings or individual schedules. |
| `tela ADM/Painel de Relatórios da Barbearia(adm).png` | `/admin/relatorios` — existing day/month and date controls, completed-revenue metrics, revenue visualization and service summary. Respect the current backend values and omit export or comparisons not implemented. |

Signup and password-reset pages have no separate reference image; they follow the existing split-auth layout and field hierarchy from the login reference, without changing their form fields or submit events. Routes `/admin/usuarios` and `/barbeiro/atendimentos` are also retained even where a one-to-one screenshot is absent; the existing forms, tables, feedback, and state remain authoritative.

### Implementation boundaries

Retain existing event bindings and `AppState` calls at each functional control; move or wrap components without changing their event arguments or sequencing. Shared customer layout belongs in `ui.py`; client routes remain in `customer_portal.py`; `/historico` is registered in `app_barbearia.py`. Do not edit `state.py` or `xano_repository.py`. Do not replace the 12-hour eligibility rule with UI-only logic or hide backend errors behind mock content.

## Risks / Trade-offs

- [The screenshots contain fabricated records and unsupported actions] → use each only as a layout/style reference; bind every value and functional action to existing data/state and disable or omit unsupported controls.
- [Reference photography is embedded in full-screen screenshots] → crop only individual photographic regions into local assets and use them decoratively, without implying they depict named users or staff.
- [A narrower viewport can make the side navigation and tables dense] → stack panels and use compact/scrollable table treatments while retaining labels, keyboard focus, and all actions.
- [Shared tokens can make login, public, and role pages inconsistent if changed independently] → centralize common values and validate representative routes from all three roles at desktop and mobile widths.
- [Recomposition may accidentally drop existing event bindings] → compare every interactive control before and after the visual change and verify the binding contract without changing state/repository files.

## Migration Plan

1. Review this client screen map and the `customer-portal` capability delta before implementation.
2. Implement customer assets and shell, then the five route compositions and booking layout, preserving event wiring and data sources.
3. Compile the Reflex app and visually inspect all customer routes at desktop and narrow widths; confirm Xano mode and the existing state/repository files remain unchanged.
4. If a screen loses behavior or state during review, restore its existing composition/binding rather than altering the handler, state, repository, or API contract.
