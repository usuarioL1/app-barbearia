import os
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


if __name__ == "__main__":
    unittest.main()
