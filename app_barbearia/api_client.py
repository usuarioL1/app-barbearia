import os
from collections.abc import Mapping
from typing import Any
from urllib.parse import urlparse

import httpx


class ApiError(Exception):
    def __init__(
        self,
        message: str,
        *,
        code: str = "api_error",
        status_code: int | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.status_code = status_code


def _api_base_url() -> str:
    base_url = os.environ.get("XANO_API_BASE_URL", "").strip().rstrip("/")
    parsed = urlparse(base_url)
    if (
        parsed.scheme not in {"http", "https"}
        or not parsed.netloc
        or parsed.username is not None
        or parsed.password is not None
        or parsed.query
        or parsed.fragment
    ):
        raise ApiError(
            "A conexão com o sistema ainda não está configurada.",
            code="api_not_configured",
        )
    return base_url


def _error_details(response: httpx.Response) -> tuple[str, str]:
    try:
        payload = response.json()
    except ValueError:
        return "request_failed", "Não foi possível concluir a solicitação."

    if not isinstance(payload, dict):
        return "request_failed", "Não foi possível concluir a solicitação."

    error = payload.get("error", payload)
    if not isinstance(error, dict):
        return "request_failed", "Não foi possível concluir a solicitação."

    code = error.get("code")
    message = error.get("message")
    if (
        response.status_code == 400
        and isinstance(message, str)
        and message.startswith("appointment_conflict:")
    ):
        return "appointment_conflict", message.partition(":")[2].strip()
    return (
        code if isinstance(code, str) and code else "request_failed",
        message
        if isinstance(message, str) and message
        else "Não foi possível concluir a solicitação.",
    )


async def request_json(
    method: str,
    path: str,
    *,
    token: str | None = None,
    params: Mapping[str, str] | None = None,
    payload: Mapping[str, Any] | None = None,
    transport: httpx.AsyncBaseTransport | None = None,
) -> Any:
    if not path or path.startswith("//") or "://" in path:
        raise ApiError("A rota solicitada é inválida.", code="invalid_api_path")

    url = f"{_api_base_url()}/{path.lstrip('/')}"
    headers = {"Accept": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        async with httpx.AsyncClient(
            timeout=15.0,
            transport=transport,
        ) as client:
            response = await client.request(
                method,
                url,
                headers=headers,
                params=params,
                json=payload,
            )
    except httpx.RequestError as exc:
        raise ApiError(
            "Não foi possível conectar ao sistema. Tente novamente.",
            code="network_error",
        ) from exc

    if response.is_error:
        code, message = _error_details(response)
        raise ApiError(message, code=code, status_code=response.status_code)

    if response.status_code == 204:
        return None

    try:
        return response.json()
    except ValueError as exc:
        raise ApiError(
            "O sistema retornou uma resposta inválida.",
            code="invalid_response",
            status_code=response.status_code,
        ) from exc
