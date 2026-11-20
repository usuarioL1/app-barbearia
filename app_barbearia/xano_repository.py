from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from typing import Any, Generic, Literal, Mapping, TypeVar
from zoneinfo import ZoneInfo

from app_barbearia.api_client import ApiError, request_json
from app_barbearia.mock_repository import (
    AppointmentRecord,
    BarberAppointmentRecord,
    BarberRecord,
    ClientRecord,
    MockFailure,
    MockRepository,
    ServiceRecord,
    UserRecord,
    barber_appointment_view,
)


LOCAL_TIMEZONE = ZoneInfo("America/Sao_Paulo")
T = TypeVar("T")
_STATUS_LABELS = {
    "pending": "Pendente",
    "confirmed": "Confirmado",
    "cancelled": "Cancelado",
    "completed": "Concluído",
}
_STATUS_COLORS = {
    "pending": "#d6a64f",
    "confirmed": "#54a86b",
    "cancelled": "#d9776b",
    "completed": "#aaa69d",
}


@dataclass(frozen=True)
class PersistedResult(Generic[T]):
    data: T
    message: str
    persisted: Literal[True] = True


@dataclass(frozen=True)
class AuthResult:
    data: UserRecord
    token: str
    message: str = "Sessão iniciada."
    persisted: Literal[True] = True


def repository_for(token: str = "") -> Any:
    """Keep local demos explicit and never fall back after selecting Xano."""
    mode = os.environ.get(
        "BARBERFLOW_MODE",
        "xano" if os.environ.get("APP_ENV", "").casefold() == "production" else "demo",
    ).casefold()
    if "XANO_API_BASE_URL" in os.environ:
        mode = "xano"
    if mode == "demo":
        return MockRepository
    if mode == "xano":
        return XanoRepository(token)
    raise MockFailure(
        "BARBERFLOW_MODE deve ser 'demo' ou 'xano'.",
        code="invalid_repository_mode",
    )


def xano_enabled() -> bool:
    try:
        return isinstance(repository_for(), XanoRepository)
    except MockFailure:
        return False


def _object(value: Any, *, context: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise MockFailure(
            f"O sistema retornou dados inválidos para {context}.",
            code="invalid_response",
        )
    return value


def _items(value: Any, *, context: str) -> list[dict[str, Any]]:
    if isinstance(value, dict):
        value = value.get("items")
    if not isinstance(value, list) or any(not isinstance(item, dict) for item in value):
        raise MockFailure(
            f"O sistema retornou uma lista inválida para {context}.",
            code="invalid_response",
        )
    return value


def _text(record: Mapping[str, Any], key: str, *, context: str) -> str:
    value = record.get(key)
    if isinstance(value, (str, int)) and not isinstance(value, bool):
        return str(value)
    raise MockFailure(
        f"O sistema retornou um campo inválido ({key}) em {context}.",
        code="invalid_response",
    )


def _optional_text(record: Mapping[str, Any], key: str) -> str:
    value = record.get(key)
    if value is None:
        return ""
    if isinstance(value, (str, int)) and not isinstance(value, bool):
        return str(value)
    raise MockFailure(
        f"O sistema retornou um campo inválido ({key}).",
        code="invalid_response",
    )


def _boolean(record: Mapping[str, Any], key: str, *, default: bool = True) -> bool:
    value = record.get(key, default)
    if not isinstance(value, bool):
        raise MockFailure(
            f"O sistema retornou um campo inválido ({key}).",
            code="invalid_response",
        )
    return value


def _integer(record: Mapping[str, Any], key: str) -> int:
    value = record.get(key)
    if isinstance(value, bool):
        raise MockFailure(
            f"O sistema retornou um campo inválido ({key}).",
            code="invalid_response",
        )
    try:
        return int(value)
    except (TypeError, ValueError) as error:
        raise MockFailure(
            f"O sistema retornou um campo inválido ({key}).",
            code="invalid_response",
        ) from error


def _price_cents(record: Mapping[str, Any]) -> int:
    if "price_cents" in record:
        return _integer(record, "price_cents")
    try:
        value = record["price"] if "price" in record else record["price_snapshot"]
        amount = Decimal(str(value))
    except (KeyError, InvalidOperation, ValueError) as error:
        raise MockFailure(
            "O sistema retornou um preço inválido.",
            code="invalid_response",
        ) from error
    return int((amount * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def _user(record: Mapping[str, Any]) -> UserRecord:
    role = _text(record, "role", context="usuário")
    if role not in {"client", "barber", "admin"}:
        raise MockFailure("O sistema retornou um papel inválido.", code="invalid_response")
    return {
        "id": _text(record, "id", context="usuário"),
        "name": _text(record, "name", context="usuário"),
        "email": _text(record, "email", context="usuário"),
        "phone": _optional_text(record, "phone"),
        "role": role,
    }


def _service(record: Mapping[str, Any]) -> ServiceRecord:
    cents = _price_cents(record)
    duration = _integer(record, "duration_minutes")
    title = _text(record, "title", context="serviço")
    return {
        "id": _text(record, "id", context="serviço"),
        "title": title,
        "description": _optional_text(record, "description"),
        "price_cents": cents,
        "price_display": f"R$ {cents // 100},{cents % 100:02d}",
        "duration_minutes": duration,
        "duration_display": f"{duration} min",
        "booking_description": f"{duration} min · R$ {cents // 100},{cents % 100:02d}",
        "icon_tag": "scissors",
        "active": _boolean(record, "active"),
    }


def _barber(record: Mapping[str, Any]) -> BarberRecord:
    name = _text(record, "name", context="barbeiro")
    specialty = _optional_text(record, "specialty")
    initials = "".join(part[0] for part in name.split()[:2]).upper()
    return {
        "id": _text(record, "id", context="barbeiro"),
        "user_id": _optional_text(record, "user_id"),
        "name": name,
        "specialty": specialty,
        "booking_description": f"Especialidade: {specialty}" if specialty else "",
        "initials": initials,
        "active": _boolean(record, "active"),
    }


def _local_start(record: Mapping[str, Any]) -> datetime:
    value = record.get("start_time_iso", record.get("start_time"))
    if not isinstance(value, str):
        date_value = record.get("date")
        time_value = record.get("time")
        if isinstance(date_value, str) and isinstance(time_value, str):
            value = f"{date_value}T{time_value}"
        else:
            raise MockFailure(
                "O sistema retornou um horário inválido.",
                code="invalid_response",
            )
    try:
        start = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise MockFailure(
            "O sistema retornou um horário inválido.",
            code="invalid_response",
        ) from error
    if start.tzinfo is None:
        raise MockFailure(
            "O horário retornado não contém fuso horário.",
            code="invalid_response",
        )
    return start.astimezone(LOCAL_TIMEZONE)


def _appointment(record: Mapping[str, Any]) -> AppointmentRecord:
    start = _local_start(record)
    status = _text(record, "status", context="agendamento")
    if status not in _STATUS_LABELS:
        raise MockFailure(
            "O sistema retornou um status inválido.",
            code="invalid_response",
        )
    cents = _price_cents(record)
    duration = _integer(record, "duration_minutes_snapshot")
    return {
        "id": _text(record, "id", context="agendamento"),
        "client_id": _optional_text(record, "client_id"),
        "client_name": _optional_text(record, "client_name"),
        "client_email": _optional_text(record, "client_email"),
        "barber_id": _text(record, "barber_id", context="agendamento"),
        "barber_name": _optional_text(record, "barber_name"),
        "service_id": _text(record, "service_id", context="agendamento"),
        "service_title": _text(
            record,
            "service_title_snapshot",
            context="agendamento",
        ),
        "price_cents": cents,
        "duration_minutes": duration,
        "date": start.date().isoformat(),
        "time": start.strftime("%H:%M"),
        "status": status,
        "date_display": start.strftime("%d/%m/%Y"),
        "status_label": _STATUS_LABELS[status],
        "status_color": _STATUS_COLORS[status],
        "price_display": f"R$ {cents // 100},{cents % 100:02d}",
    }


class XanoRepository:
    def __init__(self, token: str = "") -> None:
        self._token = token

    async def _request(
        self,
        method: str,
        path: str,
        *,
        params: Mapping[str, str] | None = None,
        payload: Mapping[str, Any] | None = None,
        token: str | None = None,
    ) -> Any:
        try:
            return await request_json(
                method,
                path,
                token=self._token if token is None else token,
                params=params,
                payload=payload,
            )
        except ApiError as error:
            raise MockFailure(
                str(error),
                code=error.code,
                status_code=error.status_code,
            ) from error

    async def _authenticate(
        self,
        path: str,
        payload: Mapping[str, Any],
    ) -> AuthResult:
        response = _object(
            await self._request("POST", path, payload=payload, token=""),
            context="autenticação",
        )
        token = response.get("authToken", response.get("auth_token"))
        user_data = response.get("user")
        if not isinstance(token, str) or not token:
            raise MockFailure(
                "A resposta de autenticação não contém uma sessão válida.",
                code="invalid_response",
            )
        if not isinstance(user_data, dict):
            user_data = await self._request("GET", "auth/me", token=token)
        return AuthResult(
            data=_user(_object(user_data, context="perfil")),
            token=token,
            message="Sessão iniciada.",
        )

    async def authenticate(self, email: str, password: str) -> AuthResult:
        return await self._authenticate(
            "auth/login",
            {"email": email.strip().casefold(), "password": password},
        )

    async def signup(
        self,
        *,
        name: str,
        email: str,
        phone: str,
        password: str,
    ) -> AuthResult:
        return await self._authenticate(
            "auth/signup",
            {
                "name": name.strip(),
                "email": email.strip().casefold(),
                "phone": phone.strip(),
                "password": password,
            },
        )

    async def password_reset(self, email: str) -> PersistedResult[dict[str, str]]:
        response = _object(
            await self._request(
                "POST",
                "auth/password-reset",
                payload={"email": email.strip().casefold()},
                token="",
            ),
            context="recuperação de senha",
        )
        message = response.get("message")
        if not isinstance(message, str) or not message:
            raise MockFailure(
                "O sistema não confirmou a solicitação de recuperação.",
                code="invalid_response",
            )
        return PersistedResult({"email": email.strip().casefold()}, message)

    async def update_password(
        self,
        *,
        email: str,
        token: str,
        password: str,
    ) -> PersistedResult[dict[str, str]]:
        response = _object(
            await self._request(
                "POST",
                "auth/password-reset/confirm",
                payload={
                    "email": email.strip().casefold(),
                    "token": token,
                    "password": password,
                },
                token="",
            ),
            context="atualização de senha",
        )
        message = response.get("message")
        if not isinstance(message, str) or not message:
            raise MockFailure(
                "O sistema não confirmou a atualização de senha.",
                code="invalid_response",
            )
        return PersistedResult({"email": email.strip().casefold()}, message)

    async def user(self, user_id: str) -> UserRecord:
        user = await self.current_user()
        if user["id"] != user_id:
            raise MockFailure(
                "O perfil solicitado não corresponde à sessão atual.",
                code="forbidden",
                status_code=403,
            )
        return user

    async def current_user(self) -> UserRecord:
        return _user(
            _object(
                await self._request("GET", "auth/me"),
                context="perfil",
            )
        )

    async def update_profile(
        self,
        user_id: str,
        *,
        name: str,
        email: str,
        phone: str,
    ) -> PersistedResult[UserRecord]:
        current = await self.user(user_id)
        updated = _user(
            _object(
                await self._request(
                    "PATCH",
                    "auth/me",
                    payload={
                        "name": name.strip(),
                        "email": email.strip().casefold(),
                        "phone": phone.strip(),
                    },
                ),
                context="perfil",
            )
        )
        if updated["id"] != current["id"] or updated["role"] != current["role"]:
            raise MockFailure(
                "A resposta de perfil alterou campos protegidos.",
                code="invalid_response",
            )
        return PersistedResult(updated, "Perfil atualizado.")

    async def services(self, *, active_only: bool = True) -> list[ServiceRecord]:
        path = "services" if active_only else "admin/services"
        records = _items(
            await self._request("GET", path),
            context="serviços",
        )
        return [_service(record) for record in records]

    async def barbers(self, *, active_only: bool = True) -> list[BarberRecord]:
        path = "barbers" if active_only else "admin/barbers"
        records = _items(
            await self._request("GET", path),
            context="barbeiros",
        )
        return [_barber(record) for record in records]

    async def customer_appointments(
        self,
        client_id: str,
    ) -> list[AppointmentRecord]:
        del client_id
        records = _items(
            await self._request("GET", "appointments/me"),
            context="agendamentos",
        )
        return [_appointment(record) for record in records]

    async def barber_appointments(
        self,
        barber_id: str,
        *,
        date: str | None = None,
    ) -> list[BarberAppointmentRecord]:
        del barber_id
        records = _items(
            await self._request(
                "GET",
                "barber/appointments",
                params={"date": date} if date else None,
            ),
            context="agenda do barbeiro",
        )
        return [barber_appointment_view(_appointment(record)) for record in records]

    async def admin_appointments(
        self,
        *,
        barber_id: str = "",
        status: str = "",
        date: str = "",
        from_date: str = "",
        to_date: str = "",
    ) -> list[AppointmentRecord]:
        if date and not (from_date or to_date):
            from_date = date
            to_date = date
        params = {
            key: value
            for key, value in {
                "barber_id": barber_id,
                "status": status,
                "from": from_date,
                "to": to_date,
            }.items()
            if value
        }
        records = _items(
            await self._request("GET", "admin/appointments", params=params),
            context="agenda administrativa",
        )
        return [_appointment(record) for record in records]

    async def appointment(self, appointment_id: str) -> AppointmentRecord:
        return _appointment(
            _object(
                await self._request("GET", f"appointments/{appointment_id}"),
                context="agendamento",
            )
        )

    async def clients(self) -> list[ClientRecord]:
        records = _items(
            await self._request("GET", "admin/clients"),
            context="clientes",
        )
        return [
            {
                "id": _text(record, "id", context="cliente"),
                "name": _text(record, "name", context="cliente"),
                "email": _text(record, "email", context="cliente"),
                "phone": _optional_text(record, "phone"),
                "appointments": _optional_text(record, "appointments"),
                "last_appointment": _optional_text(record, "last_appointment"),
            }
            for record in records
        ]

    async def users(self) -> list[UserRecord]:
        records = _items(
            await self._request("GET", "admin/users"),
            context="usuários",
        )
        return [_user(record) for record in records]

    async def availability(
        self,
        barber_id: str,
        service_id: str,
        date: str,
    ) -> list[str]:
        response = await self._request(
            "GET",
            "availability",
            params={
                "barber_id": barber_id,
                "service_id": service_id,
                "date": date,
            },
        )
        if isinstance(response, dict):
            response = response.get("items")
        if not isinstance(response, list) or any(
            not isinstance(value, str) for value in response
        ):
            raise MockFailure(
                "O sistema retornou horários disponíveis inválidos.",
                code="invalid_response",
            )
        return response

    async def create_appointment(
        self,
        *,
        client_id: str,
        barber_id: str,
        service_id: str,
        date: str,
        start_time: str,
    ) -> PersistedResult[AppointmentRecord]:
        del client_id
        start = datetime.fromisoformat(f"{date}T{start_time}").replace(
            tzinfo=LOCAL_TIMEZONE
        )
        record = _appointment(
            _object(
                await self._request(
                    "POST",
                    "appointments",
                    payload={
                        "barber_id": barber_id,
                        "service_id": service_id,
                        "start_time": start.isoformat(),
                    },
                ),
                context="novo agendamento",
            )
        )
        return PersistedResult(record, "Agendamento solicitado.")

    async def cancel_appointment(
        self,
        appointment_id: str,
        *,
        client_id: str,
    ) -> PersistedResult[AppointmentRecord]:
        del client_id
        record = _appointment(
            _object(
                await self._request(
                    "POST",
                    f"appointments/{appointment_id}/cancel",
                    payload={},
                ),
                context="cancelamento",
            )
        )
        return PersistedResult(record, "Agendamento cancelado.")

    async def update_appointment_status(
        self,
        appointment_id: str,
        status: str,
        *,
        actor_role: str,
        barber_id: str = "",
    ) -> PersistedResult[AppointmentRecord]:
        del actor_role, barber_id
        record = _appointment(
            _object(
                await self._request(
                    "PATCH",
                    f"appointments/{appointment_id}/status",
                    payload={"status": status},
                ),
                context="atualização do agendamento",
            )
        )
        return PersistedResult(record, "Status do agendamento atualizado.")

    async def admin_mutation(
        self,
        entity: str,
        action: str,
        values: dict[str, str],
    ) -> PersistedResult[dict[str, str]]:
        if entity == "user":
            raise MockFailure(
                "Usuários barbeiro e administrador devem ser provisionados no Xano.",
                code="manual_provisioning_required",
                status_code=403,
            )
        if entity == "settings":
            raise MockFailure(
                "A configuração solicitada ainda não possui endpoint no Xano.",
                code="unsupported_operation",
            )
        routes = {
            "client": ("admin/clients", "admin/clients"),
            "service": ("admin/services", "admin/services"),
            "barber": ("admin/barbers", "admin/barbers"),
        }
        if entity not in routes:
            raise MockFailure("Tipo de cadastro inválido.", code="invalid_entity")
        collection, _ = routes[entity]
        record_id = values.get("id", "")
        payload: dict[str, Any] = dict(values)
        payload.pop("id", None)
        if action == "create":
            method, path = "POST", collection
        elif action == "update" and record_id:
            method, path = "PATCH", f"{collection}/{record_id}"
        elif action == "deactivate" and record_id:
            method, path = "PATCH", f"{collection}/{record_id}/deactivate"
            payload = {}
        else:
            raise MockFailure(
                "Ação administrativa inválida.",
                code="invalid_action",
                status_code=400,
            )
        result = _object(
            await self._request(method, path, payload=payload),
            context="cadastro administrativo",
        )
        return PersistedResult(
            {key: str(value) for key, value in result.items()},
            "Alterações salvas.",
        )

    async def revenue(
        self,
        period: Literal["day", "month"],
        selected_date: str,
    ) -> int:
        response = _object(
            await self._request(
                "GET",
                "admin/reports/revenue",
                params={"period": period, "date": selected_date},
            ),
            context="relatório",
        )
        if "revenue_cents" in response:
            return _integer(response, "revenue_cents")
        return _price_cents(response)
