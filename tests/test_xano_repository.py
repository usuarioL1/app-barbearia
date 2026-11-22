import os
from contextlib import redirect_stdout
from io import StringIO
import unittest
from unittest.mock import AsyncMock, patch

from app_barbearia.api_client import ApiError
from app_barbearia.mock_repository import MockFailure, MockRepository
from app_barbearia.xano_repository import (
    XanoRepository,
    _appointment,
    repository_for,
)


class XanoRepositoryTests(unittest.IsolatedAsyncioTestCase):
    async def test_unconfigured_environment_uses_the_demo_repository(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            self.assertIs(repository_for(), MockRepository)

    async def test_configured_environment_never_falls_back_to_demo_data(self) -> None:
        with patch.dict(
            os.environ,
            {"XANO_API_BASE_URL": "https://xano.example.test/api:auth"},
            clear=True,
        ):
            repository = repository_for()

        self.assertIsInstance(repository, XanoRepository)

    async def test_login_uses_bearer_session_and_signup_does_not_send_a_role(self) -> None:
        user = {
            "id": 42,
            "name": "Cliente",
            "email": "cliente@example.test",
            "phone": "11999999999",
            "role": "client",
        }
        request = AsyncMock(return_value={"authToken": "session-token", "user": user})
        with patch("app_barbearia.xano_repository.request_json", new=request):
            result = await XanoRepository().signup(
                name=" Cliente ",
                email="CLIENTE@example.test",
                phone="11999999999",
                password="a-strong-password",
            )

        self.assertEqual(result.data["role"], "client")
        self.assertEqual(result.token, "session-token")
        self.assertEqual(request.await_args.args[:2], ("POST", "auth/signup"))
        self.assertEqual(
            request.await_args.kwargs["payload"],
            {
                "name": "Cliente",
                "email": "cliente@example.test",
                "phone": "11999999999",
                "password": "a-strong-password",
            },
        )
        self.assertNotIn("role", request.await_args.kwargs["payload"])
        self.assertEqual(request.await_args.kwargs["token"], "")

    async def test_authentication_loads_profile_with_new_token_if_needed(self) -> None:
        user = {
            "id": 42,
            "name": "Cliente",
            "email": "cliente@example.test",
            "phone": "",
            "role": "client",
        }
        request = AsyncMock(
            side_effect=[
                {"auth_token": "session-token"},
                user,
            ]
        )
        with patch("app_barbearia.xano_repository.request_json", new=request):
            result = await XanoRepository().authenticate(
                "cliente@example.test",
                "a-strong-password",
            )

        self.assertEqual(result.data["id"], "42")
        self.assertEqual(request.await_args_list[1].args[:2], ("GET", "auth/me"))
        self.assertEqual(request.await_args_list[1].kwargs["token"], "session-token")

    async def test_login_sends_expected_xano_fields(self) -> None:
        request = AsyncMock(
            return_value={
                "authToken": "session-token",
                "user": {
                    "id": 42,
                    "name": "Cliente",
                    "email": "cliente@example.test",
                    "phone": "",
                    "role": "client",
                },
            }
        )
        with patch("app_barbearia.xano_repository.request_json", new=request):
            result = await XanoRepository().authenticate(
                " CLIENTE@example.test ",
                "secret-password",
            )

        self.assertEqual(result.token, "session-token")
        self.assertEqual(request.await_args.args[:2], ("POST", "auth/login"))
        self.assertEqual(
            request.await_args.kwargs["payload"],
            {"email": "cliente@example.test", "password": "secret-password"},
        )
        self.assertEqual(request.await_args.kwargs["token"], "")

    async def test_login_failure_prints_status_and_redacted_json(self) -> None:
        request = AsyncMock(
            side_effect=ApiError(
                "E-mail ou senha inválidos.",
                code="unauthorized",
                status_code=401,
                response_json={
                    "error": {
                        "message": "E-mail ou senha inválidos.",
                        "password": "secret-password",
                        "authToken": "secret-token",
                    }
                },
                request_url="https://xano.example.test/api:auth/auth/login",
            )
        )
        output = StringIO()
        expected_error = (
            'Falha no login: HTTP 401. Resposta JSON do Xano: '
            '{"error": {"message": "E-mail ou senha inválidos.", '
            '"password": "[REDACTED]", "authToken": "[REDACTED]"}}'
        )
        with (
            patch("app_barbearia.xano_repository.request_json", new=request),
            redirect_stdout(output),
            self.assertRaisesRegex(MockFailure, "Falha no login: HTTP 401") as raised,
        ):
            await XanoRepository().authenticate(
                "cliente@example.test",
                "secret-password",
            )

        diagnostic = output.getvalue()
        self.assertIn("HTTP 401", diagnostic)
        self.assertIn("https://xano.example.test/api:auth/auth/login", diagnostic)
        self.assertIn("E-mail ou senha inválidos.", diagnostic)
        self.assertNotIn("secret-password", diagnostic)
        self.assertNotIn("secret-token", diagnostic)
        self.assertEqual(str(raised.exception), expected_error)

    async def test_backend_errors_keep_conflict_status_and_do_not_fake_success(self) -> None:
        request = AsyncMock(
            side_effect=ApiError(
                "Este horário não está mais disponível.",
                code="appointment_conflict",
                status_code=409,
            )
        )
        repository = XanoRepository("session-token")
        with patch("app_barbearia.xano_repository.request_json", new=request):
            with self.assertRaises(MockFailure) as raised:
                await repository.services()

        self.assertEqual(raised.exception.code, "appointment_conflict")
        self.assertEqual(raised.exception.status_code, 409)

    async def test_rate_limit_error_is_localized_for_all_repository_calls(self) -> None:
        request = AsyncMock(
            side_effect=ApiError(
                "Too many requests",
                code="rate_limit",
                status_code=429,
            )
        )
        with patch("app_barbearia.xano_repository.request_json", new=request):
            with self.assertRaises(MockFailure) as raised:
                await XanoRepository().services()

        self.assertEqual(raised.exception.status_code, 429)
        self.assertEqual(
            str(raised.exception),
            "Muitas consultas seguidas. Aguarde alguns segundos e tente novamente.",
        )

    async def test_profile_update_does_not_send_identity_or_role(self) -> None:
        current_user = {
            "id": 42,
            "name": "Cliente",
            "email": "cliente@example.test",
            "phone": "11999999999",
            "role": "client",
        }
        updated_user = {
            **current_user,
            "name": "Cliente Atualizado",
            "phone": "11888888888",
        }
        request = AsyncMock(side_effect=[current_user, updated_user])
        with patch("app_barbearia.xano_repository.request_json", new=request):
            result = await XanoRepository("session-token").update_profile(
                "42",
                name="Cliente Atualizado",
                email="cliente@example.test",
                phone="11888888888",
            )

        self.assertEqual(result.data["name"], "Cliente Atualizado")
        self.assertEqual(
            request.await_args_list[0].args[:2],
            ("GET", "auth/me"),
        )
        self.assertEqual(request.await_args_list[0].kwargs["token"], "session-token")
        self.assertEqual(request.await_args_list[1].args[:2], ("PATCH", "auth/me"))
        self.assertEqual(request.await_args_list[1].kwargs["token"], "session-token")
        self.assertEqual(
            request.await_args_list[1].kwargs["payload"],
            {
                "name": "Cliente Atualizado",
                "email": "cliente@example.test",
                "phone": "11888888888",
            },
        )

    async def test_password_reset_request_uses_public_endpoint(self) -> None:
        request = AsyncMock(
            return_value={
                "message": "Se o e-mail estiver cadastrado, enviaremos um link."
            }
        )
        with patch("app_barbearia.xano_repository.request_json", new=request):
            result = await XanoRepository("existing-session").password_reset(
                " CLIENTE@example.test "
            )

        self.assertTrue(result.persisted)
        self.assertEqual(request.await_args.args[:2], ("POST", "auth/password-reset"))
        self.assertEqual(request.await_args.kwargs["token"], "")
        self.assertEqual(
            request.await_args.kwargs["payload"],
            {"email": "cliente@example.test"},
        )

    async def test_password_reset_uses_one_time_token_without_auth_header(self) -> None:
        request = AsyncMock(return_value={"message": "Senha atualizada. Entre novamente."})
        with patch("app_barbearia.xano_repository.request_json", new=request):
            result = await XanoRepository("existing-session").update_password(
                email="cliente@example.test",
                token="one-time-reset-token",
                password="new-strong-password",
            )

        self.assertTrue(result.persisted)
        self.assertEqual(request.await_args.args[:2], ("POST", "auth/password-reset/confirm"))
        self.assertEqual(request.await_args.kwargs["token"], "")
        self.assertEqual(
            request.await_args.kwargs["payload"],
            {
                "email": "cliente@example.test",
                "token": "one-time-reset-token",
                "password": "new-strong-password",
            },
        )

    async def test_catalog_uses_published_xano_items_and_record_fields(self) -> None:
        request = AsyncMock(
            side_effect=[
                {
                    "items": [
                        {
                            "id": 8,
                            "title": "Corte",
                            "description": "Corte tradicional",
                            "price": "40.00",
                            "duration_minutes": 30,
                            "active": True,
                        }
                    ]
                },
                {
                    "items": [
                        {
                            "id": 3,
                            "user_id": 12,
                            "name": "Barbeiro",
                            "specialty": "Corte clássico",
                            "active": True,
                        }
                    ]
                },
            ]
        )
        with patch("app_barbearia.xano_repository.request_json", new=request):
            services = await XanoRepository().services()
            barbers = await XanoRepository().barbers()

        self.assertEqual(services[0]["id"], "8")
        self.assertEqual(services[0]["title"], "Corte")
        self.assertEqual(services[0]["price_cents"], 4000)
        self.assertEqual(services[0]["duration_minutes"], 30)
        self.assertEqual(barbers[0]["id"], "3")
        self.assertEqual(barbers[0]["name"], "Barbeiro")
        self.assertEqual(barbers[0]["specialty"], "Corte clássico")
        self.assertEqual(request.await_args_list[0].args[:2], ("GET", "services"))
        self.assertEqual(request.await_args_list[1].args[:2], ("GET", "barbers"))

    async def test_admin_clients_and_users_use_admin_collections(self) -> None:
        request = AsyncMock(
            side_effect=[
                {
                    "items": [
                        {
                            "id": 14,
                            "name": "Cliente",
                            "email": "cliente@example.test",
                            "phone": "11999999999",
                            "role": "client",
                        },
                        {
                            "id": 16,
                            "name": "Administrador",
                            "email": "admin@example.test",
                            "phone": "",
                            "role": "admin",
                        }
                    ]
                },
                {
                    "items": [
                        {
                            "id": 15,
                            "name": "Administrador",
                            "email": "admin@example.test",
                            "phone": "",
                            "role": "admin",
                        }
                    ]
                },
            ]
        )
        repository = XanoRepository("admin-session")
        with patch("app_barbearia.xano_repository.request_json", new=request):
            clients = await repository.clients()
            users = await repository.users()

        self.assertEqual(clients[0]["id"], "14")
        self.assertEqual(clients[0]["name"], "Cliente")
        self.assertEqual([client["role"] for client in clients], ["client"])
        self.assertEqual(users[0]["id"], "15")
        self.assertEqual(users[0]["role"], "admin")
        self.assertEqual(
            [call.args[1] for call in request.await_args_list],
            ["admin/clients", "admin/users"],
        )
        self.assertTrue(
            all(call.kwargs["token"] == "admin-session" for call in request.await_args_list)
        )

    def test_appointment_timestamps_are_presented_in_sao_paulo_time(self) -> None:
        appointment = _appointment(
            {
                "id": 13,
                "client_id": 4,
                "barber_id": 2,
                "service_id": 5,
                "service_title_snapshot": "Corte",
                "price_snapshot": "40.00",
                "duration_minutes_snapshot": 30,
                "start_time": "2026-08-25T12:00:00Z",
                "status": "pending",
            }
        )

        self.assertEqual(appointment["date"], "2026-08-25")
        self.assertEqual(appointment["time"], "09:00")
        self.assertEqual(appointment["price_cents"], 4000)

    async def test_successful_booking_defaults_missing_status_to_pending(self) -> None:
        response = {
            "id": 13,
            "client_id": 4,
            "barber_id": 2,
            "service_id": 5,
            "service_title_snapshot": "Corte",
            "price_snapshot": "40.00",
            "duration_minutes_snapshot": 30,
            "start_time": "2026-08-25T09:00:00-03:00",
            "end_time": "2026-08-25T09:30:00-03:00",
        }
        request = AsyncMock(return_value=response)

        with patch("app_barbearia.xano_repository.request_json", new=request):
            result = await XanoRepository("session-token").create_appointment(
                client_id="4",
                barber_id="2",
                service_id="5",
                date="2026-08-25",
                start_time="09:00",
            )

        self.assertEqual(result.data["status"], "pending")
        self.assertEqual(result.data["status_label"], "Pendente")
        self.assertTrue(result.persisted)
        self.assertEqual(request.await_args.args[:2], ("POST", "appointments"))

    async def test_successful_multi_service_booking_sends_service_ids(self) -> None:
        response = {
            "id": 14,
            "client_id": 4,
            "barber_id": 2,
            "service_id": 5,
            "service_title_snapshot": "Corte + Barba",
            "price_snapshot": "75.00",
            "duration_minutes_snapshot": 60,
            "start_time": "2026-08-25T09:45:00-03:00",
            "end_time": "2026-08-25T10:45:00-03:00",
        }
        request = AsyncMock(return_value=response)

        with patch("app_barbearia.xano_repository.request_json", new=request):
            await XanoRepository("session-token").create_appointment(
                client_id="4",
                barber_id="2",
                service_id="5",
                service_ids=["5", "6"],
                date="2026-08-25",
                start_time="09:45",
            )

        payload = request.await_args.kwargs["payload"]
        self.assertEqual(payload["service_id"], "5")
        self.assertEqual(payload["service_ids"], [5, 6])

    def test_appointment_reads_default_missing_status_to_pending(self) -> None:
        with self.assertLogs("app_barbearia.xano_repository", level="WARNING"):
            appointment = _appointment(self._appointment_payload())
        self.assertEqual(appointment["status"], "pending")
        self.assertEqual(appointment["status_label"], "Pendente")

    def test_appointment_statuses_are_normalized(self) -> None:
        statuses = {
            "pending": "pending",
            "pendente": "pending",
            "PENDING": "pending",
            "PENDENTE": "pending",
            "confirmed": "confirmed",
            "confirmado": "confirmed",
            "CONFIRMED": "confirmed",
            "CONFIRMADO": "confirmed",
            "cancelled": "cancelled",
            "cancelado": "cancelled",
            "CANCELLED": "cancelled",
            "CANCELADO": "cancelled",
            "completed": "completed",
            "concluido": "completed",
            "concluído": "completed",
            "COMPLETED": "completed",
            "CONCLUÍDO": "completed",
        }

        for raw_status, expected in statuses.items():
            with self.subTest(raw_status=raw_status):
                appointment = _appointment(
                    self._appointment_payload(status=raw_status)
                )
                self.assertEqual(appointment["status"], expected)

    def test_completed_appointment_uses_snapshot_price_and_sao_paulo_start_date(
        self,
    ) -> None:
        appointment = _appointment(
            {
                **self._appointment_payload(status="completed"),
                "price_snapshot": "125.50",
                "start_time": "2026-11-01T03:00:00Z",
            }
        )

        self.assertEqual(appointment["date"], "2026-11-01")
        self.assertEqual(appointment["time"], "00:00")
        self.assertEqual(appointment["status"], "completed")
        self.assertEqual(appointment["price_cents"], 12550)
        self.assertEqual(appointment["price_display"], "R$ 125,50")

    async def test_admin_appointments_requests_local_date_range_and_maps_snapshots(
        self,
    ) -> None:
        response = {
            "items": [
                {
                    **self._appointment_payload(),
                    "price_snapshot": "125.50",
                    "start_time": "2026-11-01T03:00:00-03:00",
                }
            ]
        }
        request = AsyncMock(return_value=response)

        with patch("app_barbearia.xano_repository.request_json", new=request):
            appointments = await XanoRepository("session-token").admin_appointments(
                from_date="2026-11-01",
                to_date="2026-11-30",
                status="completed",
            )

        self.assertEqual(
            request.await_args.args[:2],
            ("GET", "admin/appointments"),
        )
        self.assertEqual(
            request.await_args.kwargs["params"],
            {
                "status": "completed",
                "from": "2026-11-01",
                "to": "2026-11-30",
            },
        )
        self.assertEqual(appointments[0]["date"], "2026-11-01")
        self.assertEqual(appointments[0]["price_cents"], 12550)
        self.assertEqual(appointments[0]["service_title"], "Corte")
        self.assertEqual(appointments[0]["status"], "completed")

    async def test_admin_appointments_with_no_status_filter_omits_status_param(
        self,
    ) -> None:
        request = AsyncMock(
            return_value={"items": [self._appointment_payload()]}
        )

        with (
            patch("app_barbearia.xano_repository.request_json", new=request),
            self.assertNoLogs("app_barbearia.xano_repository", level="WARNING"),
        ):
            appointments = await XanoRepository().admin_appointments(status=None)

        self.assertEqual(request.await_args.kwargs["params"], {})
        self.assertEqual(appointments[0]["status"], "pending")

    async def test_barber_appointments_preserve_status_returned_by_role_endpoint(
        self,
    ) -> None:
        record = {
            **self._appointment_payload(status="completed"),
            "client_name": "Cliente",
        }
        request = AsyncMock(return_value={"items": [record]})

        with patch("app_barbearia.xano_repository.request_json", new=request):
            appointments = await XanoRepository("session-token").barber_appointments(
                "2",
                date="2026-08-25",
            )

        self.assertEqual(request.await_args.args[:2], ("GET", "barber/appointments"))
        self.assertEqual(appointments[0]["status"], "completed")

    async def test_barber_appointments_pass_status_filter_and_infer_omitted_status(
        self,
    ) -> None:
        record = self._appointment_payload()
        request = AsyncMock(return_value={"items": [record]})

        with (
            patch("app_barbearia.xano_repository.request_json", new=request),
            self.assertNoLogs("app_barbearia.xano_repository", level="WARNING"),
        ):
            appointments = await XanoRepository("session-token").barber_appointments(
                "2",
                date="2026-11-20",
                status="completed",
            )

        self.assertEqual(
            request.await_args.kwargs["params"],
            {"date": "2026-11-20", "status": "completed"},
        )
        self.assertEqual(appointments[0]["status"], "completed")
        self.assertEqual(appointments[0]["status_label"], "Concluído")

    def test_nested_appointment_statuses_are_normalized(self) -> None:
        statuses = (
            ({"value": "COMPLETED"}, "completed"),
            ({"status": {"label": "Concluído"}}, "completed"),
            ({"STATUS": {"VALUE": "CONCLUÍDO"}}, "completed"),
            ({"name": "CONFIRMADO"}, "confirmed"),
            ({"value": "Pendente"}, "pending"),
            ({"status": {"value": "CANCELADO"}}, "cancelled"),
            ([{"name": "completed"}], "completed"),
        )

        for raw_status, expected in statuses:
            with self.subTest(raw_status=raw_status):
                appointment = _appointment(
                    self._appointment_payload(status=raw_status)
                )
                self.assertEqual(appointment["status"], expected)
                self.assertEqual(
                    appointment["status_label"],
                    {
                        "pending": "Pendente",
                        "confirmed": "Confirmado",
                        "cancelled": "Cancelado",
                        "completed": "Concluído",
                    }[expected],
                )

    def test_appointment_statuses_that_are_not_supported_default_to_pending(self) -> None:
        for raw_status in ("reserved", "", None, [], 123):
            with self.subTest(raw_status=raw_status):
                with self.assertLogs(
                    "app_barbearia.xano_repository",
                    level="WARNING",
                ):
                    appointment = _appointment(
                        self._appointment_payload(status=raw_status)
                    )

                self.assertEqual(appointment["status"], "pending")

    @staticmethod
    def _appointment_payload(*, status: object = None) -> dict[str, object]:
        payload: dict[str, object] = {
            "id": 13,
            "client_id": 4,
            "barber_id": 2,
            "service_id": 5,
            "service_title_snapshot": "Corte",
            "price_snapshot": "40.00",
            "duration_minutes_snapshot": 30,
            "start_time": "2026-08-25T12:00:00Z",
        }
        if status is not None:
            payload["status"] = status
        return payload


if __name__ == "__main__":
    unittest.main()
