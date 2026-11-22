import unittest
from datetime import date
from unittest.mock import AsyncMock, patch

from app_barbearia.mock_repository import MockFailure, MockRepository
from app_barbearia.state import (
    AppState,
    _attendance_rate_display,
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
        self.selected_service_ids = ["corte"]
        self.selected_barber_id = "rafael"
        self.selected_date = "2026-08-25"
        self.current_user_id = "client-lucas"
        self.booking_confirmed = False
        self.booking_confirmation_service = ""
        self.booking_confirmation_date = ""
        self.booking_confirmation_time = ""
        self.customer_appointments = []
        self.upcoming_appointments = []
        self.next_appointments = []
        self.historical_appointments = []
        self.upcoming_period_filter = "all"
        self.history_period_filter = "all"
        self.history_category_filter = "Todos"
        self.appointment_filter = "all"
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
        self.admin_completed_count = 0
        self.admin_cancelled_count = 0
        self.users = []
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

    def _calendar_for_month(self, month: str) -> list[str]:
        return AppState._calendar_for_month(self, month)

    def _month_label(self, month: str) -> str:
        return AppState._month_label(self, month)

    def _update_selected_service_summary(self) -> None:
        AppState._update_selected_service_summary(self)

    def _begin_request(self) -> None:
        self.is_loading = True
        self.error_message = ""
        self.success_message = ""

    def _end_request(self) -> None:
        self.is_loading = False

    def _set_failure(self, error: MockFailure) -> None:
        AppState._set_failure(self, error)

    async def _load_admin_reports(self, **kwargs) -> None:
        await AppState._load_admin_reports(self, **kwargs)

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
    def setUp(self) -> None:
        environment = patch.dict(
            "os.environ",
            {"BARBERFLOW_MODE": "demo"},
            clear=True,
        )
        environment.start()
        self.addCleanup(environment.stop)

    def _allow_authenticated_test_state(self):
        return patch(
            "app_barbearia.state._ensure_authenticated",
            new=AsyncMock(return_value=(True, None)),
        )

    async def test_barber_workspace_loads_machine_today(self) -> None:
        class MachineDate(date):
            @classmethod
            def today(cls) -> date:
                return cls(2026, 11, 22)

        state = ClientStateHarness()
        state._load_barber_appointments = AsyncMock()
        with (
            self._allow_authenticated_test_state(),
            patch("app_barbearia.state.date", MachineDate),
        ):
            await AppState.load_barber_workspace.fn(state)

        state._load_barber_appointments.assert_awaited_once_with("2026-11-22")

    async def test_admin_agenda_loads_machine_today(self) -> None:
        class MachineDate(date):
            @classmethod
            def today(cls) -> date:
                return cls(2026, 11, 22)

        state = ClientStateHarness()
        state._load_admin_agenda = AsyncMock()
        with (
            self._allow_authenticated_test_state(),
            patch("app_barbearia.state.date", MachineDate),
        ):
            await AppState.load_admin_agenda.fn(state)

        state._load_admin_agenda.assert_awaited_once_with(
            selected_date="2026-11-22",
            barber_id="",
            status="",
        )

    async def test_booking_load_selects_machine_today(self) -> None:
        class MachineDate(date):
            @classmethod
            def today(cls) -> date:
                return cls(2026, 11, 22)

        state = ClientStateHarness()
        with (
            self._allow_authenticated_test_state(),
            patch("app_barbearia.state.date", MachineDate),
            patch.object(
                MockRepository,
                "availability",
                new=AsyncMock(return_value=[]),
            ),
        ):
            await AppState.load_booking.fn(state)

        self.assertEqual(state.selected_date, "2026-11-22")
        self.assertEqual(state.selected_day, "22")
        self.assertEqual(state.booking_month, "2026-11")
        self.assertEqual(state.selected_date_display, "22/11/2026")

    async def test_customer_appointments_are_sorted_and_split_by_active_status(self) -> None:
        state = ClientStateHarness()
        appointments = [
            {"id": "later", "date": "2026-08-25", "time": "11:00", "status": "confirmed"},
            {"id": "earlier", "date": "2026-08-25", "time": "09:00", "status": "pending"},
            {"id": "cancelled", "date": "2026-08-25", "time": "10:00", "status": "cancelled"},
            {"id": "past", "date": "2026-08-23", "time": "10:00", "status": "pending"},
        ]

        AppState._split_customer_appointments(state, appointments)

        self.assertEqual(
            [item["id"] for item in state.upcoming_appointments],
            ["earlier", "later"],
        )
        self.assertEqual([item["id"] for item in state.next_appointments], ["earlier"])
        self.assertEqual(
            [item["id"] for item in state.historical_appointments],
            ["past", "cancelled"],
        )

    async def test_customer_appointments_empty_state_clears_all_lists(self) -> None:
        state = ClientStateHarness()

        AppState._split_customer_appointments(state, [])

        self.assertEqual(state.upcoming_appointments, [])
        self.assertEqual(state.next_appointments, [])
        self.assertEqual(state.historical_appointments, [])

    async def test_xano_customer_history_uses_real_reference_date(self) -> None:
        state = ClientStateHarness()
        appointments = [
            {
                "id": "past-with-omitted-status",
                "date": "2026-11-20",
                "time": "09:00",
                "status": "pending",
            },
            {
                "id": "future",
                "date": "2026-11-23",
                "time": "09:00",
                "status": "pending",
            },
        ]

        with patch(
            "app_barbearia.state._appointments_reference_date",
            return_value=date(2026, 11, 22),
        ):
            AppState._split_customer_appointments(state, appointments)

        self.assertEqual(
            [item["id"] for item in state.historical_appointments],
            ["past-with-omitted-status"],
        )
        self.assertEqual(
            [item["id"] for item in state.upcoming_appointments],
            ["future"],
        )

    async def test_history_category_and_period_filters_are_operational(self) -> None:
        state = ClientStateHarness()
        state.historical_appointments = [
            {
                "id": "haircut",
                "date": "2026-11-10",
                "service_title": "Corte Masculino",
            },
            {
                "id": "beard",
                "date": "2026-11-11",
                "service_title": "Barba",
            },
            {
                "id": "combo",
                "date": "2026-11-12",
                "service_title": "Corte + Barba",
            },
            {
                "id": "old-haircut",
                "date": "2026-09-01",
                "service_title": "Corte Masculino",
            },
        ]

        with patch(
            "app_barbearia.state._appointments_reference_date",
            return_value=date(2026, 11, 22),
        ):
            AppState.set_history_category_filter.fn(state, "Barba")
            AppState.set_history_period_filter.fn(state, "30 dias")
            filtered = AppState.filtered_historical_appointments.fget(state)

        self.assertEqual(
            [item["id"] for item in filtered],
            ["beard"],
        )
        self.assertEqual(state.history_period_filter, "30")

        AppState.set_history_category_filter.fn(state, "Combos")
        with patch(
            "app_barbearia.state._appointments_reference_date",
            return_value=date(2026, 11, 22),
        ):
            filtered_combos = AppState.filtered_historical_appointments.fget(state)
        self.assertEqual([item["id"] for item in filtered_combos], ["combo"])

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

    async def test_demo_mode_does_not_authenticate_the_mock_user(self) -> None:
        state = ClientStateHarness()

        with (
            patch.object(
                MockRepository,
                "customer_appointments",
                new=AsyncMock(),
            ) as appointments,
            patch.object(
                MockRepository,
                "authenticate",
                new=AsyncMock(),
            ) as authenticate,
        ):
            redirect = await AppState.load_client_portal.fn(state)
            state.login_email = "lucas@email.com"
            state._login_password = "demo-password"
            await AppState.login.fn(state)

        appointments.assert_not_awaited()
        authenticate.assert_not_awaited()
        self.assertFalse(state.is_authenticated)
        self.assertEqual(state.current_user_id, "")
        self.assertEqual(state.user_email, "")
        self.assertIn("Xano", state.error_message)
        self.assertNotIn(
            "A autenticação exige uma conta real na API do Xano.",
            state.error_message,
        )
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
        state.services = [{"id": "demo-service"}]
        state.barbers = [{"id": "demo-barber"}]
        failure = MockFailure("Catálogo indisponível.")
        repository = type("Repository", (), {})()
        repository.services = AsyncMock(side_effect=failure)
        repository.barbers = AsyncMock()
        with (
            patch.dict("os.environ", {"XANO_API_BASE_URL": "https://xano.example.test"}),
            patch("app_barbearia.state._repository_for", return_value=repository),
        ):
            await AppState.load_catalog.fn(state)

        self.assertEqual(state.error_message, "Catálogo indisponível.")
        self.assertEqual(state.success_message, "")
        self.assertEqual(state.services, [])
        self.assertEqual(state.barbers, [])
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
            redirect = await AppState.confirm_booking.fn(state)

        request.assert_not_awaited()
        self.assertTrue(state.booking_confirmed)
        self.assertIn("nada foi salvo", state.success_message)
        self.assertEqual(state.booking_confirmation_time, "09:45")
        self.assertIsNotNone(redirect)

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

    async def test_rejected_authentication_clears_an_existing_session(self) -> None:
        state = ClientStateHarness()
        state.login_email = "cliente@example.test"
        state._login_password = "wrong-password"
        state._auth_token = "old-session"
        state.current_user_id = "42"
        state.is_authenticated = True
        failure = MockFailure(
            'Falha no login: HTTP 401. Resposta JSON do Xano: '
            '{"error": {"message": "E-mail ou senha inválidos."}}',
            code="unauthorized",
            status_code=401,
        )
        repository = type("Repository", (), {})()
        repository.authenticate = AsyncMock(side_effect=failure)
        repository.signup = AsyncMock(side_effect=failure)

        with (
            patch("app_barbearia.state.xano_enabled", return_value=True),
            patch("app_barbearia.state._repository_for", return_value=repository),
        ):
            await AppState.login.fn(state)

        self.assertEqual(state._auth_token, "")
        self.assertFalse(state.is_authenticated)
        self.assertEqual(state.current_user_id, "")
        self.assertEqual(state._login_password, "")
        self.assertEqual(state.error_message, "E-mail ou senha inválidos.")

        state.signup_name = "Cliente"
        state.signup_email = "cliente@example.test"
        state.signup_phone = "11999999999"
        state._signup_password = "wrong-password"
        state._signup_password_confirmation = "wrong-password"
        state._auth_token = "old-session"
        state.current_user_id = "42"
        state.is_authenticated = True

        with (
            patch("app_barbearia.state.xano_enabled", return_value=True),
            patch("app_barbearia.state._repository_for", return_value=repository),
        ):
            await AppState.signup.fn(state)

        self.assertEqual(state._auth_token, "")
        self.assertFalse(state.is_authenticated)
        self.assertEqual(state.current_user_id, "")
        self.assertEqual(state._signup_password, "")

    async def test_login_401_and_403_use_generic_message_and_always_end_loading(self) -> None:
        for status_code in (401, 403):
            with self.subTest(status_code=status_code):
                state = ClientStateHarness()
                state.login_email = "admin@example.test"
                state._login_password = "wrong-password"
                repository = type("Repository", (), {})()
                repository.authenticate = AsyncMock(
                    side_effect=MockFailure(
                        "technical response containing HTTP details",
                        status_code=status_code,
                    )
                )
                with (
                    patch("app_barbearia.state.xano_enabled", return_value=True),
                    patch("app_barbearia.state._repository_for", return_value=repository),
                ):
                    await AppState.login.fn(state)

                self.assertEqual(state.error_message, "E-mail ou senha inválidos.")
                self.assertFalse(state.is_loading)

    async def test_login_429_uses_friendly_message_and_always_ends_loading(self) -> None:
        state = ClientStateHarness()
        state.login_email = "admin@example.test"
        state._login_password = "valid-looking-password"
        repository = type("Repository", (), {})()
        repository.authenticate = AsyncMock(
            side_effect=MockFailure("Too many requests", status_code=429)
        )

        with (
            patch("app_barbearia.state.xano_enabled", return_value=True),
            patch("app_barbearia.state._repository_for", return_value=repository),
        ):
            await AppState.login.fn(state)

        self.assertEqual(
            state.error_message,
            "Muitas consultas seguidas. Aguarde alguns segundos e tente novamente.",
        )
        self.assertFalse(state.is_loading)

    async def test_429_error_is_friendly_for_other_state_requests(self) -> None:
        state = ClientStateHarness()

        AppState._set_failure(
            state,
            MockFailure("Too many requests", status_code=429),
        )

        self.assertEqual(
            state.error_message,
            "Muitas consultas seguidas. Aguarde alguns segundos e tente novamente.",
        )

    async def test_expired_session_is_cleared_when_profile_check_returns_401(self) -> None:
        state = ClientStateHarness()
        state._auth_token = "expired-session"
        state.current_user_id = "42"
        state.user_name = "Cliente"
        state.is_authenticated = True
        failure = MockFailure(
            "Sessão inválida ou expirada.",
            code="unauthorized",
            status_code=401,
        )

        with (
            patch.dict("os.environ", {"XANO_API_BASE_URL": "https://xano.example.test"}),
            patch(
                "app_barbearia.state.XanoRepository.current_user",
                new=AsyncMock(side_effect=failure),
            ),
        ):
            redirect = await AppState.load_profile.fn(state)

        self.assertIsNotNone(redirect)
        self.assertEqual(state._auth_token, "")
        self.assertFalse(state.is_authenticated)
        self.assertEqual(state.current_user_id, "")
        self.assertEqual(state.user_name, "")
        self.assertEqual(state.error_message, "Sessão inválida ou expirada.")

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

        with self._allow_authenticated_test_state():
            await AppState._load_barber_appointments(state, "2026-08-24")

        self.assertEqual(state.barber_date, "2026-08-24")
        self.assertTrue(state.barber_appointments)
        self.assertEqual(
            {item["status"] for item in state.barber_appointments},
            {"pending", "confirmed"},
        )
        self.assertTrue(
            all(
                "client_id" not in item and "client_email" not in item
                for item in state.barber_appointments
            )
        )
        self.assertFalse(state.is_loading)

    async def test_barber_agenda_reconciles_completed_status_and_revenue(self) -> None:
        state = ClientStateHarness()
        all_appointments = [
            {
                "id": "completed-1",
                "client_name": "Cliente",
                "service_title": "Corte",
                "price_cents": 4500,
                "duration_minutes": 30,
                "date": "2026-11-20",
                "time": "09:00",
                "status": "pending",
                "date_display": "20/11/2026",
                "status_label": "Pendente",
                "status_color": "#d6a64f",
                "price_display": "R$ 45,00",
            },
            {
                "id": "pending-1",
                "client_name": "Outro Cliente",
                "service_title": "Barba",
                "price_cents": 3000,
                "duration_minutes": 30,
                "date": "2026-11-20",
                "time": "10:00",
                "status": "pending",
                "date_display": "20/11/2026",
                "status_label": "Pendente",
                "status_color": "#d6a64f",
                "price_display": "R$ 30,00",
            },
        ]
        filtered_by_status = {
            "completed": [dict(all_appointments[0], status="completed")],
            "confirmed": [],
            "cancelled": [],
        }

        async def appointments_for_query(barber_id, *, date=None, status=None):
            if status:
                return filtered_by_status[status]
            return all_appointments

        with (
            self._allow_authenticated_test_state(),
            patch.object(
                MockRepository,
                "barber_appointments",
                new=AsyncMock(side_effect=appointments_for_query),
            ) as load_appointments,
        ):
            await AppState._load_barber_appointments(state, "2026-11-20")

        self.assertEqual(
            {item["id"]: item["status"] for item in state.barber_appointments},
            {"completed-1": "completed", "pending-1": "pending"},
        )
        self.assertEqual(
            {item["id"]: item["status_label"] for item in state.barber_appointments},
            {"completed-1": "Concluído", "pending-1": "Pendente"},
        )
        self.assertEqual(
            {item["id"]: item["status_color"] for item in state.barber_appointments},
            {"completed-1": "#aaa69d", "pending-1": "#d6a64f"},
        )
        self.assertEqual(
            AppState.barber_revenue_display.fget(state),
            "R$ 45,00",
        )
        self.assertEqual(load_appointments.await_count, 4)

    async def test_barber_agenda_does_not_trust_ignored_status_filters(self) -> None:
        state = ClientStateHarness()
        appointment = {
            "id": "appointment-1",
            "client_name": "Cliente",
            "service_title": "Corte",
            "price_cents": 4500,
            "duration_minutes": 30,
            "date": "2026-11-20",
            "time": "09:00",
            "status": "pending",
            "date_display": "20/11/2026",
            "status_label": "Pendente",
            "status_color": "#d6a64f",
            "price_display": "R$ 45,00",
        }

        with (
            self._allow_authenticated_test_state(),
            patch.object(
                MockRepository,
                "barber_appointments",
                new=AsyncMock(return_value=[appointment]),
            ),
        ):
            await AppState._load_barber_appointments(state, "2026-11-20")

        self.assertEqual(state.barber_appointments[0]["status"], "pending")
        self.assertEqual(state.barber_appointments[0]["status_label"], "Pendente")
        self.assertEqual(
            AppState.barber_revenue_display.fget(state),
            "R$ 0,00",
        )

    async def test_barber_set_date_loads_selected_date(self) -> None:
        state = ClientStateHarness()
        state._load_barber_appointments = AsyncMock()

        await AppState.set_barber_date.fn(state, "2026-08-28")

        state._load_barber_appointments.assert_awaited_once_with("2026-08-28")

    async def test_admin_filter_success_updates_period_filter_and_results_together(self) -> None:
        state = ClientStateHarness()
        appointment = {
            "id": "appointment-filtered",
            "date": "2026-08-24",
            "status": "pending",
        }

        with (
            self._allow_authenticated_test_state(),
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

    async def test_admin_all_statuses_reconciles_missing_status_without_detail_calls(
        self,
    ) -> None:
        state = ClientStateHarness()
        all_appointments = [
            {"id": "completed-1", "date": "2026-08-24", "time": "09:00", "status": "pending"},
            {"id": "confirmed-1", "date": "2026-08-24", "time": "10:00", "status": "pending"},
            {"id": "cancelled-1", "date": "2026-08-24", "time": "11:00", "status": "pending"},
            {"id": "pending-1", "date": "2026-08-24", "time": "12:00", "status": "pending"},
        ]
        filtered_by_status = {
            "completed": [dict(all_appointments[0], status="completed")],
            "confirmed": [dict(all_appointments[1], status="confirmed")],
            "cancelled": [dict(all_appointments[2], status="cancelled")],
        }

        async def appointments_for_query(**filters):
            requested_status = filters["status"]
            if requested_status:
                return filtered_by_status[requested_status]
            return all_appointments

        with (
            self._allow_authenticated_test_state(),
            patch.object(
                MockRepository,
                "admin_appointments",
                new=AsyncMock(side_effect=appointments_for_query),
            ) as load_appointments,
            patch.object(MockRepository, "barbers", new=AsyncMock(return_value=[])),
        ):
            await AppState._load_admin_agenda(
                state,
                selected_date="2026-08-24",
                barber_id="",
                status="",
            )

        self.assertEqual(
            {item["id"]: item["status"] for item in state.admin_appointments},
            {
                "completed-1": "completed",
                "confirmed-1": "confirmed",
                "cancelled-1": "cancelled",
                "pending-1": "pending",
            },
        )
        self.assertEqual(
            {item["id"]: item["status_label"] for item in state.admin_appointments},
            {
                "completed-1": "Concluído",
                "confirmed-1": "Confirmado",
                "cancelled-1": "Cancelado",
                "pending-1": "Pendente",
            },
        )
        self.assertEqual(
            {item["id"]: item["status_color"] for item in state.admin_appointments},
            {
                "completed-1": "#aaa69d",
                "confirmed-1": "#54a86b",
                "cancelled-1": "#d9776b",
                "pending-1": "#d6a64f",
            },
        )
        self.assertEqual(load_appointments.await_count, 4)
        self.assertEqual(
            [call.kwargs["status"] for call in load_appointments.await_args_list],
            ["", "completed", "confirmed", "cancelled"],
        )

    async def test_admin_filter_failure_keeps_previous_filter_and_results(self) -> None:
        state = ClientStateHarness()
        appointment = {"id": "appointment-old", "status": "confirmed"}
        state.admin_appointments = [appointment]
        failure = MockFailure("Agenda indisponível.")

        with (
            self._allow_authenticated_test_state(),
            patch.object(
                MockRepository,
                "admin_appointments",
                new=AsyncMock(side_effect=failure),
            ),
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

    async def test_admin_dashboard_calculates_revenue_from_appointment_snapshots(self) -> None:
        class MachineDate(date):
            @classmethod
            def today(cls) -> date:
                return cls(2026, 8, 24)

        state = ClientStateHarness()
        with (
            self._allow_authenticated_test_state(),
            patch("app_barbearia.state.date", MachineDate),
            patch.object(MockRepository, "clients", new=AsyncMock(return_value=[])),
            patch.object(
                MockRepository,
                "admin_appointments",
                new=AsyncMock(wraps=MockRepository.admin_appointments),
            ) as load_appointments,
        ):
            await AppState.load_admin_dashboard.fn(state)

        self.assertEqual(
            [call.kwargs for call in load_appointments.await_args_list],
            [
                {
                    "from_date": "2026-03-01",
                    "to_date": "2026-08-31",
                    "status": "completed",
                },
                {
                    "from_date": "2026-08-01",
                    "to_date": "2026-08-31",
                    "status": "cancelled",
                },
                {"date": "2026-08-24", "status": "pending"},
                {"date": "2026-08-24", "status": "confirmed"},
                {"date": "2026-08-24", "status": "cancelled"},
            ],
        )
        self.assertEqual(state.admin_revenue_cents, 11000)
        self.assertEqual(state.admin_completed_count, 2)
        self.assertEqual(state.admin_cancelled_count, 0)
        self.assertTrue(state.admin_dashboard_appointments)
        self.assertTrue(
            all(item["date"] == "2026-08-24" for item in state.admin_dashboard_appointments)
        )
        self.assertEqual(state.admin_revenue_series[-1]["amount"], "11000")

    def test_attendance_rate_uses_monthly_completed_and_cancelled_counts(self) -> None:
        self.assertEqual(_attendance_rate_display(7, 3), "70%")
        self.assertEqual(_attendance_rate_display(2, 1), "67%")
        self.assertEqual(_attendance_rate_display(0, 0), "—")

    async def test_admin_dashboard_uses_monthly_cancelled_appointments_for_attendance(
        self,
    ) -> None:
        class MachineDate(date):
            @classmethod
            def today(cls) -> date:
                return cls(2026, 8, 24)

        completed = await MockRepository.admin_appointments(
            from_date="2026-03-01",
            to_date="2026-08-31",
            status="completed",
        )
        original_admin_appointments = MockRepository.admin_appointments
        cancelled = [{**completed[0], "date": "2026-08-20", "status": "cancelled"}]

        async def appointments_for_query(**filters):
            if filters["status"] == "cancelled":
                return cancelled
            return await original_admin_appointments(**filters)

        state = ClientStateHarness()
        with (
            self._allow_authenticated_test_state(),
            patch("app_barbearia.state.date", MachineDate),
            patch.object(MockRepository, "clients", new=AsyncMock(return_value=[])),
            patch.object(
                MockRepository,
                "admin_appointments",
                new=AsyncMock(side_effect=appointments_for_query),
            ) as load_appointments,
        ):
            await AppState.load_admin_dashboard.fn(state)

        self.assertEqual(state.admin_completed_count, 2)
        self.assertEqual(state.admin_cancelled_count, 1)
        self.assertEqual(
            _attendance_rate_display(
                state.admin_completed_count,
                state.admin_cancelled_count,
            ),
            "67%",
        )
        self.assertEqual(load_appointments.await_count, 5)

    async def test_admin_users_loader_fetches_only_users_and_finalizes_loading(self) -> None:
        state = ClientStateHarness()
        users = [
            {
                "id": "admin-1",
                "name": "Admin",
                "email": "admin@example.test",
                "phone": "",
                "role": "admin",
            }
        ]
        with (
            self._allow_authenticated_test_state(),
            patch.object(MockRepository, "users", new=AsyncMock(return_value=users)) as load_users,
            patch.object(MockRepository, "clients", new=AsyncMock()) as load_clients,
            patch.object(
                MockRepository,
                "admin_appointments",
                new=AsyncMock(),
            ) as load_appointments,
            patch.object(MockRepository, "services", new=AsyncMock()) as load_services,
            patch.object(MockRepository, "barbers", new=AsyncMock()) as load_barbers,
        ):
            await AppState.load_admin_users.fn(state)

        load_users.assert_awaited_once()
        load_clients.assert_not_awaited()
        load_appointments.assert_not_awaited()
        load_services.assert_not_awaited()
        load_barbers.assert_not_awaited()
        self.assertEqual(state.users, users)
        self.assertFalse(state.is_loading)

    async def test_admin_users_loader_finalizes_loading_after_rate_limit(self) -> None:
        state = ClientStateHarness()
        with (
            self._allow_authenticated_test_state(),
            patch.object(
                MockRepository,
                "users",
                new=AsyncMock(
                    side_effect=MockFailure("Too many requests", status_code=429)
                ),
            ),
        ):
            await AppState.load_admin_users.fn(state)

        self.assertEqual(
            state.error_message,
            "Muitas consultas seguidas. Aguarde alguns segundos e tente novamente.",
        )
        self.assertFalse(state.is_loading)

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
            with self._allow_authenticated_test_state():
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

    async def test_admin_client_filter_excludes_other_user_roles(self) -> None:
        clients = await MockRepository.clients()
        clients.extend(
            [
                {**clients[0], "id": "admin-1", "role": "admin"},
                {**clients[1], "id": "barber-1", "role": "barber"},
            ]
        )

        filtered = _filter_admin_clients(clients, "")

        self.assertEqual(
            [client["id"] for client in filtered],
            [client["id"] for client in await MockRepository.clients()],
        )

    async def test_admin_week_agenda_labels_use_brazilian_full_date(self) -> None:
        state = ClientStateHarness()

        with (
            self._allow_authenticated_test_state(),
            patch.object(
                MockRepository,
                "admin_appointments",
                new=AsyncMock(return_value=[]),
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
                barber_id="",
                status="",
            )

        self.assertEqual(state.admin_week_days[0]["label"], "Seg 24/08/2026")

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
            "admin_appointments",
            new=AsyncMock(side_effect=failure),
        ):
            with self._allow_authenticated_test_state():
                await AppState._load_admin_reports(
                    state,
                    period="day",
                    selected_date="2026-08-12",
                )

        self.assertEqual(state.admin_report_period, "day")
        self.assertEqual(state.admin_report_date, "2026-08-12")
        self.assertEqual(state.admin_report_revenue_cents, 11000)
        self.assertEqual(state.admin_report_completed_count, 2)
        self.assertEqual(
            state.admin_report_revenue_series,
            [{"month": "Ago", "amount": "11000"}],
        )
        self.assertEqual(state.error_message, "Relatório indisponível.")

    async def test_admin_report_uses_only_completed_demo_appointments(self) -> None:
        state = ClientStateHarness()

        with self._allow_authenticated_test_state():
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

    async def test_admin_report_date_change_recalculates_daily_metrics(self) -> None:
        state = ClientStateHarness()
        state.admin_report_period = "day"

        with self._allow_authenticated_test_state():
            await AppState.set_admin_report_date.fn(state, "2026-08-12")

        self.assertEqual(state.admin_report_date, "2026-08-12")
        self.assertEqual(state.admin_report_revenue_cents, 7000)
        self.assertEqual(state.admin_report_completed_count, 1)
        self.assertEqual(
            state.admin_report_service_summary,
            [{"title": "Combo", "count": "1", "share": "100%"}],
        )
        self.assertEqual(len(state.admin_report_revenue_series), 6)
        self.assertEqual(state.admin_report_revenue_series[-1]["amount"], "11000")

    async def test_admin_report_accepts_date_after_previous_calendar_cutoff(self) -> None:
        state = ClientStateHarness()

        with self._allow_authenticated_test_state():
            await AppState.set_admin_report_date.fn(state, "2026-11-22")

        self.assertEqual(state.admin_report_date, "2026-11-22")
        self.assertEqual(state.error_message, "")

    async def test_admin_report_period_change_recalculates_monthly_metrics(self) -> None:
        state = ClientStateHarness()
        state.admin_report_date = "2026-08-12"
        state.admin_report_period = "day"

        with self._allow_authenticated_test_state():
            await AppState.set_admin_report_period.fn(state, "month")

        self.assertEqual(state.admin_report_period, "month")
        self.assertEqual(state.admin_report_revenue_cents, 11000)
        self.assertEqual(state.admin_report_completed_count, 2)
        self.assertEqual(
            {item["title"] for item in state.admin_report_service_summary},
            {"Corte Masculino", "Combo"},
        )


if __name__ == "__main__":
    unittest.main()
