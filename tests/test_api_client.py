import unittest
from unittest.mock import patch

import httpx

from app_barbearia.api_client import ApiError, request_json


class ApiClientTests(unittest.IsolatedAsyncioTestCase):
    async def test_missing_base_url_fails_explicitly(self) -> None:
        with patch.dict("os.environ", {"XANO_API_BASE_URL": ""}):
            with self.assertRaises(ApiError) as raised:
                await request_json("GET", "services")

        self.assertEqual(raised.exception.code, "api_not_configured")

    async def test_network_failure_does_not_expose_exception_details(self) -> None:
        secret = "sensitive-token-value"

        def fail_request(request: httpx.Request) -> httpx.Response:
            raise httpx.ConnectError(secret, request=request)

        with patch.dict(
            "os.environ", {"XANO_API_BASE_URL": "https://xano.example.test"}
        ):
            with self.assertRaises(ApiError) as raised:
                await request_json(
                    "GET",
                    "services",
                    transport=httpx.MockTransport(fail_request),
                )

        self.assertEqual(raised.exception.code, "network_error")
        self.assertNotIn(secret, str(raised.exception))

    async def test_request_sends_bearer_token_and_query_parameters(self) -> None:
        observed: dict[str, str] = {}

        def respond(request: httpx.Request) -> httpx.Response:
            observed["authorization"] = request.headers["Authorization"]
            observed["query"] = request.url.query.decode()
            return httpx.Response(200, json={"items": []})

        with patch.dict(
            "os.environ", {"XANO_API_BASE_URL": "https://xano.example.test"}
        ):
            result = await request_json(
                "GET",
                "availability",
                token="access-token",
                params={"date": "2026-11-11"},
                transport=httpx.MockTransport(respond),
            )

        self.assertEqual(result, {"items": []})
        self.assertEqual(observed["authorization"], "Bearer access-token")
        self.assertEqual(observed["query"], "date=2026-11-11")

    async def test_public_request_omits_authentication_and_preserves_api_group(self) -> None:
        observed: dict[str, str | None] = {}

        def respond(request: httpx.Request) -> httpx.Response:
            observed["authorization"] = request.headers.get("Authorization")
            observed["url"] = str(request.url)
            return httpx.Response(200, json={"items": []})

        with patch.dict(
            "os.environ",
            {"XANO_API_BASE_URL": "https://xano.example.test/api:auth"},
        ):
            await request_json(
                "GET",
                "services",
                token="",
                transport=httpx.MockTransport(respond),
            )

        self.assertIsNone(observed["authorization"])
        self.assertEqual(
            observed["url"],
            "https://xano.example.test/api:auth/services",
        )

    async def test_error_envelope_preserves_code_and_safe_message(self) -> None:
        def respond(request: httpx.Request) -> httpx.Response:
            return httpx.Response(
                409,
                json={
                    "error": {
                        "code": "appointment_conflict",
                        "message": "Horário não disponível.",
                        "details": {"token": "must-not-be-shown"},
                    }
                },
            )

        with patch.dict(
            "os.environ", {"XANO_API_BASE_URL": "https://xano.example.test"}
        ):
            with self.assertRaises(ApiError) as raised:
                await request_json(
                    "POST",
                    "appointments",
                    payload={"start_time": "2026-11-12T10:00:00-03:00"},
                    transport=httpx.MockTransport(respond),
                )

        self.assertEqual(raised.exception.code, "appointment_conflict")
        self.assertEqual(raised.exception.status_code, 409)
        self.assertEqual(
            raised.exception.response_json,
            {
                "error": {
                    "code": "appointment_conflict",
                    "message": "Horário não disponível.",
                    "details": {"token": "must-not-be-shown"},
                }
            },
        )
        self.assertEqual(
            raised.exception.request_url,
            "https://xano.example.test/appointments",
        )
        self.assertNotIn("must-not-be-shown", str(raised.exception))

    async def test_invalid_success_response_is_not_treated_as_success(self) -> None:
        def respond(request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, text="not-json")

        with patch.dict(
            "os.environ", {"XANO_API_BASE_URL": "https://xano.example.test"}
        ):
            with self.assertRaises(ApiError) as raised:
                await request_json(
                    "GET",
                    "services",
                    transport=httpx.MockTransport(respond),
                )

        self.assertEqual(raised.exception.code, "invalid_response")
        self.assertEqual(raised.exception.status_code, 200)


if __name__ == "__main__":
    unittest.main()
