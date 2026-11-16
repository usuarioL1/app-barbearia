import unittest
from unittest.mock import AsyncMock, patch

from app_barbearia.mock_repository import MockFailure, MockRepository
from app_barbearia.state import (
    AppState,
    _appointments_for_date,
    _filter_admin_clients,
)


class ClientStateHarness:
    def __init__(self) -> None:
        self.is_loading = False
        self.error_message = ""
        self.success_message = ""
        self.services = []
        self.barbers = []
        self.available_times = []
        self.selected_time = ""
        self.selected_service_id = "corte"
        self.selected_barber_id = "rafael"
        self.selected_date = "2026-08-25"
        self.current_user_id = "client-lucas"
        self.booking_confirmed = False
        self.booking_confirmation_service = ""
        self.booking_confirmation_date = ""
        self.booking_confirmation_time = ""
        self.customer_appointments = []
        self.login_email = ""
        self.login_password = ""
        self.is_authenticated = False
        self.barber_id = "rafael"
        self.barber_date = "2026-08-24"
        self.barber_appointments = []
        self.admin_date = "2026-08-24"
        self.admin_view_mode = "week"
        self.admin_filter_barber = ""
        self.admin_filter_status = ""
        self.admin_appointments = []
        self.admin_week_days = []
        self.admin_dashboard_appointments = []
        self.clients = []
        self.admin_client_search = ""
        self.admin_client_form_open = False
        self.admin_client_form_action = "create"
        self.admin_client_form_id = ""
        self.admin_client_form_name = ""
        self.admin_client_form_phone = ""
        self.admin_service_form_open = False
        self.admin_service_form_action = "create"
        self.admin_service_form_id = ""
        self.admin_service_form_title = ""
        self.admin_service_form_description = ""
        self.admin_service_form_price = ""
        self.admin_service_form_duration = ""
        self.admin_barber_form_open = False
        self.admin_barber_form_action = "create"
        self.admin_barber_form_id = ""
        self.admin_barber_form_name = ""
        self.admin_barber_form_specialty = ""
        self.admin_revenue_cents = 0
        self.admin_revenue_series = []
        self.admin_report_period = "month"
        self.admin_report_date = "2026-08-01"
        self.admin_report_revenue_cents = 0
        self.admin_report_completed_count = 0
        self.admin_report_service_summary = []
        self.admin_report_revenue_series = []
        self.admin_report_service_gradient = "conic-gradient(#292929 0% 100%)"

    def _begin_request(self) -> None:
        self.is_loading = True
        self.error_message = ""
        self.success_message = ""

    def _end_request(self) -> None:
        self.is_loading = False

    def _set_failure(self, error: MockFailure) -> None:
        self.error_message = str(error)

    def _split_customer_appointments(self, appointments: list) -> None:
        self.customer_appointments = appointments

    async def _run_admin_mutation(
        self,
        entity: str,
        action: str,
        values: dict[str, str],
    ) -> None:
        self._begin_request()
        try:
            result = await MockRepository.admin_mutation(entity, action, values)
        except MockFailure as error:
            self._set_failure(error)
        else:
            self.success_message = result.message
        finally:
            self._end_request()


class ClientStateTests(unittest.IsolatedAsyncioTestCase):
    async def test_real_backend_requires_a_session_without_using_mock_data(self) -> None:
        state = ClientStateHarness()

        with (
            patch.dict("os.environ", {"XANO_API_BASE_URL": "https://xano.example.test"}),
            patch.object(
                MockRepository,
                "customer_appointments",
                new=AsyncMock(),
            ) as appointments,
        ):
            redirect = await AppState.load_client_portal.fn(state)

        appointments.assert_not_awaited()
        self.assertEqual(state.error_message, "Entre para continuar.")
        self.assertEqual(state.current_user_id, "")
        self.assertIsNotNone(redirect)

    async def test_authenticated_portal_load_uses_xano_with_private_session(self) -> None:
        state = ClientStateHarness()
        state._auth_token = "server-side-session"
        request = AsyncMock(
            side_effect=[
                {
                    "id": 42,
                    "name": "Cliente",
                    "email": "cliente@example.test",
                    "phone": "11999999999",
                    "role": "client",
                },
                {"items": []},
            ]
        )
        with (
            patch.dict("os.environ", {"XANO_API_BASE_URL": "https://xano.example.test"}),
            patch("app_barbearia.xano_repository.request_json", new=request),
            patch.object(
                MockRepository,
                "customer_appointments",
                new=AsyncMock(),
            ) as mock_appointments,
        ):
            await AppState.load_client_portal.fn(state)

        mock_appointments.assert_not_awaited()
        self.assertEqual(state.current_user_id, "42")
        self.assertEqual(state.user_role, "client")
        self.assertEqual(request.await_args_list[0].args[:2], ("GET", "auth/me"))
        self.assertEqual(request.await_args_list[0].kwargs["token"], "server-side-session")
        self.assertEqual(
            request.await_args_list[1].args[:2],
            ("GET", "appointments/me"),
        )
        self.assertEqual(request.await_args_list[1].kwargs["token"], "server-side-session")

    def test_password_and_token_state_is_private(self) -> None:
        public_fields = AppState.__annotations__

        self.assertNotIn("login_password", public_fields)
        self.assertNotIn("signup_password", public_fields)
        self.assertNotIn("signup_password_confirmation", public_fields)
        self.assertIn("_login_password", public_fields)
        self.assertIn("_signup_password", public_fields)
        self.assertIn("_auth_token", public_fields)

    async def test_catalog_load_exposes_loading_and_empty_results(self) -> None:
        state = ClientStateHarness()
        loading_states: list[bool] = []

        async def load_empty_services() -> list:
            loading_states.append(state.is_loading)
            return []

        async def load_empty_barbers() -> list:
            loading_states.append(state.is_loading)
            return []

        with (
            patch.object(
                MockRepository,
                "services",
                new=AsyncMock(side_effect=load_empty_services),
            ),
            patch.object(
                MockRepository,
                "barbers",
                new=AsyncMock(side_effect=load_empty_barbers),
            ),
        ):
            await AppState.load_catalog.fn(state)

        self.assertEqual(loading_states, [True, True])
        self.assertEqual(state.services, [])
        self.assertEqual(state.barbers, [])
        self.assertFalse(state.is_loading)
        self.assertEqual(state.error_message, "")

    async def test_catalog_failure_is_reported_without_success(self) -> None:
        state = ClientStateHarness()
        failure = MockFailure("Catálogo indisponível.")
        with patch.object(
            MockRepository,
            "services",
            new=AsyncMock(side_effect=failure),
        ):
            await AppState.load_catalog.fn(state)

        self.assertEqual(state.error_message, "Catálogo indisponível.")
        self.assertEqual(state.success_message, "")
        self.assertFalse(state.is_loading)

    async def test_booking_availability_failure_discards_stale_slots(self) -> None:
        state = ClientStateHarness()
        state.available_times = ["09:00"]
        state.selected_time = "09:00"
        failure = MockFailure("Disponibilidade indisponível.")

        with patch.object(
            MockRepository,
            "availability",
            new=AsyncMock(side_effect=failure),
        ):
            await AppState._refresh_booking_options(
                state,
                selected_date="2026-08-26",
            )

        self.assertEqual(state.available_times, [])
        self.assertEqual(state.selected_time, "")
        self.assertEqual(state.selected_date, "2026-08-25")
        self.assertEqual(state.error_message, "Disponibilidade indisponível.")
        self.assertFalse(state.is_loading)

    async def test_booking_conflict_is_not_reported_as_success(self) -> None:
        state = ClientStateHarness()
        state.available_times = ["09:45"]
        state.selected_time = "09:45"
        failure = MockFailure(
            "Este horário não está mais disponível.",
            code="appointment_conflict",
            status_code=409,
        )

        with patch.object(
            MockRepository,
            "create_appointment",
            new=AsyncMock(side_effect=failure),
        ):
            await AppState.confirm_booking.fn(state)

        self.assertFalse(state.booking_confirmed)
        self.assertEqual(state.available_times, [])
        self.assertEqual(state.selected_time, "")
        self.assertEqual(state.success_message, "")
        self.assertIn("não está mais disponível", state.error_message)
        self.assertFalse(state.is_loading)

    async def test_booking_success_is_explicitly_non_persistent(self) -> None:
        state = ClientStateHarness()
        state.available_times = ["09:45"]
        state.selected_time = "09:45"

        with patch("app_barbearia.api_client.request_json", new=AsyncMock()) as request:
            await AppState.confirm_booking.fn(state)

        request.assert_not_awaited()
        self.assertTrue(state.booking_confirmed)
        self.assertIn("nada foi salvo", state.success_message)
        self.assertEqual(state.booking_confirmation_time, "09:45")

    async def test_login_validation_does_not_call_repository(self) -> None:
        state = ClientStateHarness()
        state.login_email = "email-inválido"
        state.login_password = ""

        with patch.object(
            MockRepository,
            "authenticate",
            new=AsyncMock(),
        ) as authenticate:
            await AppState.login.fn(state)

        authenticate.assert_not_awaited()
        self.assertIn("e-mail válido", state.error_message)
        self.assertFalse(state.is_authenticated)
        self.assertFalse(state.is_loading)

    async def test_cancel_failure_preserves_displayed_appointments(self) -> None:
        state = ClientStateHarness()
        appointment = {"id": "appointment-1", "status": "confirmed"}
        state.customer_appointments = [appointment]
        failure = MockFailure("Cancelamento não permitido.")

        with patch.object(
            MockRepository,
            "cancel_appointment",
            new=AsyncMock(side_effect=failure),
        ):
            await AppState.cancel_client_appointment.fn(state, "appointment-1")

        self.assertEqual(state.customer_appointments, [appointment])
        self.assertEqual(state.success_message, "")
        self.assertEqual(state.error_message, "Cancelamento não permitido.")
        self.assertFalse(state.is_loading)

    async def test_barber_agenda_is_scoped_and_failed_transition_preserves_state(self) -> None:
        state = ClientStateHarness()
        appointment = {"id": "barber-today-3", "status": "pending"}
        state.barber_appointments = [appointment]
        failure = MockFailure("Transição não permitida.")

        with patch.object(
            MockRepository,
            "update_appointment_status",
            new=AsyncMock(side_effect=failure),
        ) as update:
            await AppState.update_barber_appointment_status.fn(
                state,
                "barber-today-3",
                "confirmed",
            )

        update.assert_awaited_once_with(
            "barber-today-3",
            "confirmed",
            actor_role="barber",
            barber_id="rafael",
        )
        self.assertEqual(state.barber_appointments, [appointment])
        self.assertEqual(state.success_message, "")
        self.assertEqual(state.error_message, "Transição não permitida.")

    async def test_barber_agenda_load_uses_the_current_barber_and_date(self) -> None:
        state = ClientStateHarness()

        await AppState._load_barber_appointments(state, "2026-08-24")

        self.assertEqual(state.barber_date, "2026-08-24")
        self.assertTrue(state.barber_appointments)
        self.assertTrue(
            all(
                "client_id" not in item and "client_email" not in item
                for item in state.barber_appointments
            )
        )
        self.assertFalse(state.is_loading)

    async def test_admin_filter_success_updates_period_filter_and_results_together(self) -> None:
        state = ClientStateHarness()
        appointment = {
            "id": "appointment-filtered",
            "date": "2026-08-24",
            "status": "pending",
        }

        with (
            patch.object(
                MockRepository,
                "admin_appointments",
                new=AsyncMock(return_value=[appointment]),
            ),
            patch.object(
                MockRepository,
                "barbers",
                new=AsyncMock(return_value=[]),
            ),
        ):
            await AppState._load_admin_agenda(
                state,
                selected_date="2026-08-24",
                barber_id="rafael",
                status="pending",
            )

        self.assertEqual(state.admin_appointments, [appointment])
        self.assertEqual(state.admin_date, "2026-08-24")
        self.assertEqual(state.admin_filter_barber, "rafael")
        self.assertEqual(state.admin_filter_status, "pending")
        self.assertFalse(state.is_loading)

    async def test_admin_filter_failure_keeps_previous_filter_and_results(self) -> None:
        state = ClientStateHarness()
        appointment = {"id": "appointment-old", "status": "confirmed"}
        state.admin_appointments = [appointment]
        failure = MockFailure("Agenda indisponível.")

        with patch.object(
            MockRepository,
            "admin_appointments",
            new=AsyncMock(side_effect=failure),
        ):
            await AppState._load_admin_agenda(
                state,
                selected_date="2026-08-25",
                barber_id="carlos",
                status="pending",
            )

        self.assertEqual(state.admin_appointments, [appointment])
        self.assertEqual(state.admin_date, "2026-08-24")
        self.assertEqual(state.admin_filter_barber, "")
        self.assertEqual(state.admin_filter_status, "")
        self.assertEqual(state.error_message, "Agenda indisponível.")

    async def test_admin_day_view_uses_selected_date_and_preserves_filters(self) -> None:
        state = ClientStateHarness()
        selected_appointment = {
            "id": "appointment-selected-day",
            "date": "2026-08-24",
            "status": "pending",
        }
        state.admin_date = "2026-08-24"
        state.admin_filter_barber = "rafael"
        state.admin_filter_status = "pending"
        state.admin_appointments = [
            selected_appointment,
            {
                "id": "appointment-next-day",
                "date": "2026-08-25",
                "status": "pending",
            },
        ]

        AppState.set_admin_view_mode.fn(state, "day")

        self.assertEqual(state.admin_view_mode, "day")
        self.assertEqual(
            _appointments_for_date(state.admin_appointments, state.admin_date),
            [selected_appointment],
        )
        self.assertEqual(state.admin_filter_barber, "rafael")
        self.assertEqual(state.admin_filter_status, "pending")

    async def test_admin_day_view_shows_empty_for_selected_date(self) -> None:
        appointments = [
            {
                "id": "appointment-other-day",
                "date": "2026-08-25",
                "status": "confirmed",
            }
        ]

        self.assertEqual(_appointments_for_date(appointments, "2026-08-24"), [])

    async def test_admin_day_navigation_moves_one_day_and_keeps_filters(self) -> None:
        state = ClientStateHarness()
        state.admin_date = "2026-08-24"
        state.admin_view_mode = "day"
        state.admin_filter_barber = "rafael"
        state.admin_filter_status = "pending"
        state._load_admin_agenda = AsyncMock()

        await AppState.change_admin_period.fn(state, 1)

        state._load_admin_agenda.assert_awaited_once_with(
            selected_date="2026-08-25",
            barber_id="rafael",
            status="pending",
        )

    async def test_admin_week_navigation_moves_seven_days_and_keeps_filters(self) -> None:
        state = ClientStateHarness()
        state.admin_date = "2026-08-24"
        state.admin_view_mode = "week"
        state.admin_filter_barber = "rafael"
        state.admin_filter_status = "pending"
        state._load_admin_agenda = AsyncMock()

        await AppState.change_admin_period.fn(state, -1)

        state._load_admin_agenda.assert_awaited_once_with(
            selected_date="2026-08-17",
            barber_id="rafael",
            status="pending",
        )

    async def test_admin_transition_removes_appointment_outside_active_filter(self) -> None:
        state = ClientStateHarness()
        appointment = next(
            item
            for item in await MockRepository.admin_appointments(
                barber_id="rafael",
                status="pending",
                date="2026-08-24",
            )
        )
        state.admin_filter_barber = "rafael"
        state.admin_filter_status = "pending"
        state.admin_appointments = [appointment]
        state.admin_week_days = [
            {"date": "2026-08-24", "label": "Seg 24/08", "count": "1"}
        ]

        await AppState.update_admin_appointment_status.fn(
            state,
            appointment["id"],
            "confirmed",
        )

        self.assertEqual(state.admin_appointments, [])
        self.assertEqual(state.admin_week_days[0]["count"], "0")
        self.assertEqual(state.admin_filter_status, "pending")
        self.assertIn("simulada", state.success_message)
        self.assertFalse(state.is_loading)

    async def test_admin_mutation_failure_is_not_reported_as_persisted(self) -> None:
        state = ClientStateHarness()
        appointment = {"id": "appointment-old", "status": "confirmed"}
        state.admin_appointments = [appointment]
        failure = MockFailure("Operação recusada.")

        with patch.object(
            MockRepository,
            "admin_mutation",
            new=AsyncMock(side_effect=failure),
        ):
            await AppState._run_admin_mutation(
                state,
                "service",
                "deactivate",
                {"id": "corte"},
            )

        self.assertEqual(state.admin_appointments, [appointment])
        self.assertEqual(state.success_message, "")
        self.assertEqual(state.error_message, "Operação recusada.")
        self.assertFalse(state.is_loading)

    async def test_admin_client_search_matches_name_email_and_phone_without_mutation(
        self,
    ) -> None:
        state = ClientStateHarness()
        state.clients = await MockRepository.clients()
        original_clients = [dict(client) for client in state.clients]

        AppState.set_admin_client_search.fn(state, "joao@email.com")
        by_email = _filter_admin_clients(state.clients, state.admin_client_search)
        AppState.set_admin_client_search.fn(state, "maria oliveira")
        by_name = _filter_admin_clients(state.clients, state.admin_client_search)
        AppState.set_admin_client_search.fn(state, "96543")
        by_phone = _filter_admin_clients(state.clients, state.admin_client_search)
        AppState.set_admin_client_search.fn(state, "inexistente")
        no_matches = _filter_admin_clients(state.clients, state.admin_client_search)

        self.assertEqual([client["id"] for client in by_email], ["client-joao"])
        self.assertEqual([client["id"] for client in by_name], ["client-maria"])
        self.assertEqual([client["id"] for client in by_phone], ["client-pedro"])
        self.assertEqual(no_matches, [])
        self.assertEqual(state.clients, original_clients)

    async def test_admin_client_form_prefills_edit_and_sends_nonpersistent_payload(
        self,
    ) -> None:
        state = ClientStateHarness()
        state.clients = await MockRepository.clients()
        AppState._open_admin_client_form(state, "update", "client-joao")

        self.assertTrue(state.admin_client_form_open)
        self.assertEqual(state.admin_client_form_name, "João Silva")
        self.assertEqual(state.admin_client_form_phone, "(11) 98765-4321")

        original_clients = [dict(client) for client in state.clients]
        await AppState.submit_admin_client_form.fn(state)

        self.assertFalse(state.admin_client_form_open)
        self.assertIn("nada foi salvo", state.success_message)
        self.assertEqual(state.clients, original_clients)

    async def test_admin_client_form_keeps_invalid_data_visible(self) -> None:
        state = ClientStateHarness()
        state.admin_client_form_open = True
        state.admin_client_form_name = "Novo Cliente"
        state.admin_client_form_phone = "123"

        await AppState.submit_admin_client_form.fn(state)

        self.assertTrue(state.admin_client_form_open)
        self.assertEqual(state.admin_client_form_name, "Novo Cliente")
        self.assertEqual(state.admin_client_form_phone, "123")
        self.assertEqual(state.success_message, "")
        self.assertIn("telefone válido", state.error_message)

    async def test_admin_service_form_prefills_edit_and_submits_demo_values(
        self,
    ) -> None:
        state = ClientStateHarness()
        state.services = await MockRepository.services(active_only=False)
        AppState._open_admin_service_form(state, "update", "corte")

        self.assertTrue(state.admin_service_form_open)
        self.assertEqual(state.admin_service_form_title, "Corte Masculino")
        self.assertEqual(state.admin_service_form_description, "Corte moderno e personalizado")
        self.assertEqual(state.admin_service_form_price, "40.00")
        self.assertEqual(state.admin_service_form_duration, "30")

        original_services = [dict(service) for service in state.services]
        await AppState.submit_admin_service_form.fn(state)

        self.assertFalse(state.admin_service_form_open)
        self.assertIn("nada foi salvo", state.success_message)
        self.assertEqual(state.services, original_services)

    async def test_admin_service_form_preserves_invalid_values(self) -> None:
        state = ClientStateHarness()
        state.admin_service_form_open = True
        state.admin_service_form_title = "Serviço"
        state.admin_service_form_description = ""
        state.admin_service_form_price = "0"
        state.admin_service_form_duration = "30"

        await AppState.submit_admin_service_form.fn(state)

        self.assertTrue(state.admin_service_form_open)
        self.assertEqual(state.admin_service_form_price, "0")
        self.assertEqual(state.success_message, "")
        self.assertIn("maiores que zero", state.error_message)

    async def test_admin_barber_form_prefills_edit_and_submits_nonpersistent_payload(
        self,
    ) -> None:
        state = ClientStateHarness()
        state.barbers = await MockRepository.barbers(active_only=False)
        AppState._open_admin_barber_form(state, "update", "rafael")
        original_barbers = [dict(barber) for barber in state.barbers]

        self.assertTrue(state.admin_barber_form_open)
        self.assertEqual(state.admin_barber_form_name, "Rafael Silva")
        self.assertEqual(state.admin_barber_form_specialty, "Corte Clássico")

        await AppState.submit_admin_barber_form.fn(state)

        self.assertFalse(state.admin_barber_form_open)
        self.assertIn("nada foi salvo", state.success_message)
        self.assertEqual(state.barbers, original_barbers)

    async def test_admin_barber_form_keeps_missing_required_values(self) -> None:
        state = ClientStateHarness()
        state.admin_barber_form_open = True
        state.admin_barber_form_name = "Novo barbeiro"
        state.admin_barber_form_specialty = ""

        await AppState.submit_admin_barber_form.fn(state)

        self.assertTrue(state.admin_barber_form_open)
        self.assertEqual(state.admin_barber_form_name, "Novo barbeiro")
        self.assertEqual(state.success_message, "")
        self.assertIn("obrigatórios", state.error_message)

    async def test_admin_report_failure_preserves_previous_totals(self) -> None:
        state = ClientStateHarness()
        state.admin_report_revenue_cents = 11000
        state.admin_report_completed_count = 2
        state.admin_report_revenue_series = [{"month": "Ago", "amount": "11000"}]
        failure = MockFailure("Relatório indisponível.")

        with patch.object(
            MockRepository,
            "revenue",
            new=AsyncMock(side_effect=failure),
        ):
            await AppState._load_admin_reports(
                state,
                period="day",
                selected_date="2026-08-12",
            )

        self.assertEqual(state.admin_report_period, "month")
        self.assertEqual(state.admin_report_date, "2026-08-01")
        self.assertEqual(state.admin_report_revenue_cents, 11000)
        self.assertEqual(state.admin_report_completed_count, 2)
        self.assertEqual(
            state.admin_report_revenue_series,
            [{"month": "Ago", "amount": "11000"}],
        )
        self.assertEqual(state.error_message, "Relatório indisponível.")

    async def test_admin_report_uses_only_completed_demo_appointments(self) -> None:
        state = ClientStateHarness()

        await AppState._load_admin_reports(
            state,
            period="month",
            selected_date="2026-08-01",
        )

        self.assertEqual(state.admin_report_revenue_cents, 11000)
        self.assertEqual(state.admin_report_completed_count, 2)
        self.assertEqual(
            {item["title"] for item in state.admin_report_service_summary},
            {"Corte Masculino", "Combo"},
        )
        self.assertTrue(
            all(item["share"] == "50%" for item in state.admin_report_service_summary)
        )
        self.assertEqual(len(state.admin_report_revenue_series), 6)
        self.assertEqual(state.admin_report_revenue_series[-1]["amount"], "11000")
        self.assertIn("conic-gradient(", state.admin_report_service_gradient)


if __name__ == "__main__":
    unittest.main()
