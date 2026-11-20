from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime, time, timedelta
from decimal import Decimal, InvalidOperation
from typing import Generic, Literal, NotRequired, TypedDict, TypeVar
from zoneinfo import ZoneInfo


LOCAL_TIMEZONE = ZoneInfo("America/Sao_Paulo")
MOCK_NOW = datetime(2026, 8, 24, 16, 0, tzinfo=LOCAL_TIMEZONE)
MOCK_SUCCESS_MESSAGE = "Ação simulada; nada foi salvo."


class UserRecord(TypedDict):
    id: str
    name: str
    email: str
    phone: str
    role: str
    avatar_url: NotRequired[str]


class ServiceRecord(TypedDict):
    id: str
    title: str
    description: str
    price_cents: int
    price_display: str
    duration_minutes: int
    duration_display: str
    booking_description: str
    icon_tag: str
    active: bool


class BarberRecord(TypedDict):
    id: str
    user_id: str
    name: str
    specialty: str
    booking_description: str
    initials: str
    active: bool


class ClientRecord(TypedDict):
    id: str
    name: str
    email: str
    phone: str
    appointments: str
    last_appointment: str


class AppointmentSeed(TypedDict):
    id: str
    client_id: str
    client_name: str
    client_email: str
    barber_id: str
    barber_name: str
    service_id: str
    service_title: str
    price_cents: int
    duration_minutes: int
    date: str
    time: str
    status: str


class AppointmentRecord(AppointmentSeed):
    date_display: str
    status_label: str
    status_color: str
    price_display: str


class BarberAppointmentRecord(TypedDict):
    id: str
    client_name: str
    service_title: str
    price_cents: int
    duration_minutes: int
    date: str
    time: str
    status: str
    date_display: str
    status_label: str
    status_color: str
    price_display: str


T = TypeVar("T")


@dataclass(frozen=True)
class MockResult(Generic[T]):
    data: T
    message: str = MOCK_SUCCESS_MESSAGE
    persisted: Literal[False] = False


class MockFailure(Exception):
    def __init__(
        self,
        message: str,
        *,
        code: str = "mock_operation_failed",
        status_code: int | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.status_code = status_code


_USERS: tuple[UserRecord, ...] = (
    {
        "id": "client-lucas",
        "name": "Lucas Ferreira",
        "email": "lucas@email.com",
        "phone": "(11) 98765-4321",
        "role": "client",
    },
    {
        "id": "barber-rafael",
        "name": "Rafael Silva",
        "email": "rafael@email.com",
        "phone": "(11) 97654-3210",
        "role": "barber",
    },
    {
        "id": "barber-carlos",
        "name": "Carlos Souza",
        "email": "carlos@email.com",
        "phone": "(11) 96543-2109",
        "role": "barber",
    },
    {
        "id": "barber-diego",
        "name": "Diego Alves",
        "email": "diego@email.com",
        "phone": "(11) 95432-1098",
        "role": "barber",
    },
    {
        "id": "admin-demo",
        "name": "Administrador",
        "email": "admin@email.com",
        "phone": "",
        "role": "admin",
    },
)

_SERVICES: tuple[ServiceRecord, ...] = (
    {
        "id": "corte",
        "title": "Corte Masculino",
        "description": "Corte moderno e personalizado",
        "price_cents": 4000,
        "price_display": "R$ 40,00",
        "duration_minutes": 30,
        "duration_display": "30 min",
        "booking_description": "30 min · R$ 40,00",
        "icon_tag": "scissors",
        "active": True,
    },
    {
        "id": "barba",
        "title": "Barba",
        "description": "Barba completa com acabamento",
        "price_cents": 3500,
        "price_display": "R$ 35,00",
        "duration_minutes": 30,
        "duration_display": "30 min",
        "booking_description": "30 min · R$ 35,00",
        "icon_tag": "sparkles",
        "active": True,
    },
    {
        "id": "sobrancelha",
        "title": "Sobrancelha",
        "description": "Design de sobrancelhas",
        "price_cents": 2000,
        "price_display": "R$ 20,00",
        "duration_minutes": 15,
        "duration_display": "15 min",
        "booking_description": "15 min · R$ 20,00",
        "icon_tag": "eye",
        "active": True,
    },
    {
        "id": "combo",
        "title": "Combo",
        "description": "Corte + Barba",
        "price_cents": 7000,
        "price_display": "R$ 70,00",
        "duration_minutes": 60,
        "duration_display": "60 min",
        "booking_description": "60 min · R$ 70,00",
        "icon_tag": "scissors",
        "active": True,
    },
    {
        "id": "pezinho-acabamento",
        "title": "Pezinho / Acabamento",
        "description": "Acabamento de contorno e costeletas",
        "price_cents": 1500,
        "price_display": "R$ 15,00",
        "duration_minutes": 15,
        "duration_display": "15 min",
        "booking_description": "15 min · R$ 15,00",
        "icon_tag": "scissors",
        "active": True,
    },
    {
        "id": "hidratacao-capilar",
        "title": "Hidratação Capilar",
        "description": "Tratamento hidratante para os fios",
        "price_cents": 4000,
        "price_display": "R$ 40,00",
        "duration_minutes": 30,
        "duration_display": "30 min",
        "booking_description": "30 min · R$ 40,00",
        "icon_tag": "sparkles",
        "active": True,
    },
)

_BARBERS: tuple[BarberRecord, ...] = (
    {
        "id": "rafael",
        "user_id": "barber-rafael",
        "name": "Rafael Silva",
        "specialty": "Corte Clássico",
        "booking_description": "Especialidade: Corte Clássico",
        "initials": "RS",
        "active": True,
    },
    {
        "id": "carlos",
        "user_id": "barber-carlos",
        "name": "Carlos Souza",
        "specialty": "Degradê",
        "booking_description": "Especialidade: Degradê",
        "initials": "CS",
        "active": True,
    },
    {
        "id": "diego",
        "user_id": "barber-diego",
        "name": "Diego Alves",
        "specialty": "Barba",
        "booking_description": "Especialidade: Barba",
        "initials": "DA",
        "active": True,
    },
)

_APPOINTMENTS: tuple[AppointmentSeed, ...] = (
    {
        "id": "customer-upcoming-1",
        "client_id": "client-lucas",
        "client_name": "Lucas Ferreira",
        "client_email": "lucas@email.com",
        "barber_id": "rafael",
        "barber_name": "Rafael Silva",
        "service_id": "corte",
        "service_title": "Corte Masculino",
        "price_cents": 4000,
        "duration_minutes": 30,
        "date": "2026-08-25",
        "time": "14:00",
        "status": "confirmed",
    },
    {
        "id": "customer-upcoming-2",
        "client_id": "client-lucas",
        "client_name": "Lucas Ferreira",
        "client_email": "lucas@email.com",
        "barber_id": "carlos",
        "barber_name": "Carlos Souza",
        "service_id": "barba",
        "service_title": "Barba",
        "price_cents": 3500,
        "duration_minutes": 30,
        "date": "2026-08-29",
        "time": "10:30",
        "status": "confirmed",
    },
    {
        "id": "customer-history-1",
        "client_id": "client-lucas",
        "client_name": "Lucas Ferreira",
        "client_email": "lucas@email.com",
        "barber_id": "rafael",
        "barber_name": "Rafael Silva",
        "service_id": "combo",
        "service_title": "Combo",
        "price_cents": 7000,
        "duration_minutes": 60,
        "date": "2026-08-12",
        "time": "11:00",
        "status": "completed",
    },
    {
        "id": "customer-history-2",
        "client_id": "client-lucas",
        "client_name": "Lucas Ferreira",
        "client_email": "lucas@email.com",
        "barber_id": "diego",
        "barber_name": "Diego Alves",
        "service_id": "corte",
        "service_title": "Corte Masculino",
        "price_cents": 4000,
        "duration_minutes": 30,
        "date": "2026-08-05",
        "time": "16:15",
        "status": "completed",
    },
    {
        "id": "barber-today-1",
        "client_id": "client-barber-lucas",
        "client_name": "Lucas Ferreira",
        "client_email": "lucas.ferreira@email.com",
        "barber_id": "rafael",
        "barber_name": "Rafael Silva",
        "service_id": "corte",
        "service_title": "Corte Masculino",
        "price_cents": 4000,
        "duration_minutes": 45,
        "date": "2026-08-24",
        "time": "09:00",
        "status": "confirmed",
    },
    {
        "id": "barber-today-2",
        "client_id": "client-matheus",
        "client_name": "Matheus Lima",
        "client_email": "matheus@email.com",
        "barber_id": "rafael",
        "barber_name": "Rafael Silva",
        "service_id": "barba",
        "service_title": "Barba",
        "price_cents": 3500,
        "duration_minutes": 30,
        "date": "2026-08-24",
        "time": "10:30",
        "status": "confirmed",
    },
    {
        "id": "barber-today-3",
        "client_id": "client-gabriel",
        "client_name": "Gabriel Santos",
        "client_email": "gabriel@email.com",
        "barber_id": "rafael",
        "barber_name": "Rafael Silva",
        "service_id": "corte",
        "service_title": "Corte Masculino",
        "price_cents": 4000,
        "duration_minutes": 30,
        "date": "2026-08-24",
        "time": "13:00",
        "status": "pending",
    },
    {
        "id": "barber-today-4",
        "client_id": "client-ana",
        "client_name": "Ana Oliveira",
        "client_email": "ana@email.com",
        "barber_id": "rafael",
        "barber_name": "Rafael Silva",
        "service_id": "sobrancelha",
        "service_title": "Sobrancelha",
        "price_cents": 2500,
        "duration_minutes": 20,
        "date": "2026-08-24",
        "time": "15:00",
        "status": "confirmed",
    },
    {
        "id": "availability-conflict",
        "client_id": "client-joao",
        "client_name": "João Silva",
        "client_email": "joao@email.com",
        "barber_id": "rafael",
        "barber_name": "Rafael Silva",
        "service_id": "corte",
        "service_title": "Corte Masculino",
        "price_cents": 4000,
        "duration_minutes": 30,
        "date": "2026-08-25",
        "time": "09:00",
        "status": "confirmed",
    },
)

_CLIENTS: tuple[ClientRecord, ...] = (
    {
        "id": "client-joao",
        "name": "João Silva",
        "email": "joao@email.com",
        "phone": "(11) 98765-4321",
        "appointments": "12",
        "last_appointment": "10/08/2026",
    },
    {
        "id": "client-maria",
        "name": "Maria Oliveira",
        "email": "maria@email.com",
        "phone": "(11) 97654-3210",
        "appointments": "8",
        "last_appointment": "05/08/2026",
    },
    {
        "id": "client-pedro",
        "name": "Pedro Santos",
        "email": "pedro@email.com",
        "phone": "(11) 96543-2109",
        "appointments": "15",
        "last_appointment": "12/08/2026",
    },
    {
        "id": "client-lucas",
        "name": "Lucas Souza",
        "email": "lucas.souza@email.com",
        "phone": "(11) 95432-1098",
        "appointments": "6",
        "last_appointment": "01/08/2026",
    },
    {
        "id": "client-rafael",
        "name": "Rafael Costa",
        "email": "rafael.costa@email.com",
        "phone": "(11) 94321-0987",
        "appointments": "9",
        "last_appointment": "08/08/2026",
    },
)

_DEMO_EMAIL = "lucas@email.com"
_DEMO_PASSWORD = "BarberFlow123!"


def _copy_records(records: tuple[T, ...]) -> list[T]:
    return deepcopy(list(records))


def _local_start(appointment: AppointmentSeed) -> datetime:
    return datetime.fromisoformat(
        f"{appointment['date']}T{appointment['time']}"
    ).replace(tzinfo=LOCAL_TIMEZONE)


def _price_display(price_cents: int) -> str:
    return f"R$ {price_cents // 100},{price_cents % 100:02d}"


def _present_appointment(appointment: AppointmentSeed) -> AppointmentRecord:
    status_labels = {
        "pending": "Pendente",
        "confirmed": "Confirmado",
        "cancelled": "Cancelado",
        "completed": "Concluído",
    }
    status_colors = {
        "pending": "#d6a64f",
        "confirmed": "#54a86b",
        "cancelled": "#d9776b",
        "completed": "#aaa69d",
    }
    return {
        **deepcopy(appointment),
        "date_display": datetime.strptime(appointment["date"], "%Y-%m-%d").strftime(
            "%d/%m/%Y"
        ),
        "status_label": status_labels[appointment["status"]],
        "status_color": status_colors[appointment["status"]],
        "price_display": _price_display(appointment["price_cents"]),
    }


def _present_appointments(
    appointments: tuple[AppointmentSeed, ...] | list[AppointmentSeed],
) -> list[AppointmentRecord]:
    return [_present_appointment(appointment) for appointment in appointments]


def barber_appointment_view(
    appointment: AppointmentRecord,
) -> BarberAppointmentRecord:
    return {
        "id": appointment["id"],
        "client_name": appointment["client_name"],
        "service_title": appointment["service_title"],
        "price_cents": appointment["price_cents"],
        "duration_minutes": appointment["duration_minutes"],
        "date": appointment["date"],
        "time": appointment["time"],
        "status": appointment["status"],
        "date_display": appointment["date_display"],
        "status_label": appointment["status_label"],
        "status_color": appointment["status_color"],
        "price_display": appointment["price_display"],
    }


class MockRepository:
    """Isolated, non-persistent data source for the visual-flow phase."""

    @classmethod
    async def services(cls, *, active_only: bool = True) -> list[ServiceRecord]:
        records = [service for service in _SERVICES if service["active"] or not active_only]
        return _copy_records(tuple(records))

    @classmethod
    async def barbers(cls, *, active_only: bool = True) -> list[BarberRecord]:
        records = [barber for barber in _BARBERS if barber["active"] or not active_only]
        return _copy_records(tuple(records))

    @classmethod
    async def user(cls, user_id: str) -> UserRecord:
        user = next((user for user in _USERS if user["id"] == user_id), None)
        if user is None:
            raise MockFailure("Usuário não encontrado.", code="not_found", status_code=404)
        return deepcopy(user)

    @classmethod
    async def customer_appointments(
        cls,
        client_id: str,
    ) -> list[AppointmentRecord]:
        records = [item for item in _APPOINTMENTS if item["client_id"] == client_id]
        return _present_appointments(sorted(records, key=lambda item: (item["date"], item["time"])))

    @classmethod
    async def barber_appointments(
        cls,
        barber_id: str,
        *,
        date: str | None = None,
    ) -> list[BarberAppointmentRecord]:
        records = [
            item
            for item in _APPOINTMENTS
            if item["barber_id"] == barber_id
            and (date is None or item["date"] == date)
        ]
        return [
            barber_appointment_view(item)
            for item in _present_appointments(
                sorted(records, key=lambda item: (item["date"], item["time"]))
            )
        ]

    @classmethod
    async def admin_appointments(
        cls,
        *,
        barber_id: str = "",
        status: str = "",
        date: str = "",
        from_date: str = "",
        to_date: str = "",
    ) -> list[AppointmentRecord]:
        records = [
            item
            for item in _APPOINTMENTS
            if (not barber_id or item["barber_id"] == barber_id)
            and (not status or item["status"] == status)
            and (not date or item["date"] == date)
            and (not from_date or item["date"] >= from_date)
            and (not to_date or item["date"] <= to_date)
        ]
        return _present_appointments(sorted(records, key=lambda item: (item["date"], item["time"])))

    @classmethod
    async def clients(cls) -> list[ClientRecord]:
        return _copy_records(_CLIENTS)

    @classmethod
    async def users(cls) -> list[UserRecord]:
        return _copy_records(_USERS)

    @classmethod
    async def authenticate(
        cls,
        email: str,
        password: str,
    ) -> MockResult[UserRecord]:
        if email.casefold() != _DEMO_EMAIL or password != _DEMO_PASSWORD:
            raise MockFailure(
                "E-mail ou senha inválidos.",
                code="invalid_credentials",
                status_code=401,
            )
        user = await cls.user("client-lucas")
        return MockResult(user)

    @classmethod
    async def signup(
        cls,
        *,
        name: str,
        email: str,
        phone: str,
        password: str,
    ) -> MockResult[UserRecord]:
        if any(user["email"].casefold() == email.casefold() for user in _USERS):
            raise MockFailure("Este e-mail já está cadastrado.", code="email_conflict", status_code=409)
        user: UserRecord = {
            "id": "client-new",
            "name": name.strip(),
            "email": email.strip().casefold(),
            "phone": phone.strip(),
            "role": "client",
        }
        if not password:
            raise MockFailure("Informe uma senha.", code="validation_error", status_code=400)
        return MockResult(user)

    @classmethod
    async def password_reset(cls, email: str) -> MockResult[dict[str, str]]:
        known_email = any(user["email"].casefold() == email.casefold() for user in _USERS)
        if not known_email:
            raise MockFailure(
                "Não encontramos uma conta com este e-mail.",
                code="user_not_found",
                status_code=404,
            )
        return MockResult({"email": email.strip().casefold()})

    @classmethod
    async def update_password(
        cls,
        *,
        email: str,
        token: str,
        password: str,
    ) -> MockResult[dict[str, str]]:
        del email, token, password
        raise MockFailure(
            "A redefinição de senha não está disponível no modo de demonstração.",
            code="unsupported_operation",
        )

    @classmethod
    async def update_profile(
        cls,
        user_id: str,
        *,
        name: str,
        email: str,
        phone: str,
        avatar_url: str = "",
    ) -> MockResult[UserRecord]:
        current = await cls.user(user_id)
        if any(
            user["id"] != user_id and user["email"].casefold() == email.casefold()
            for user in _USERS
        ):
            raise MockFailure("Este e-mail já está em uso.", code="email_conflict", status_code=409)
        updated = {
            **current,
            "name": name.strip(),
            "email": email.strip().casefold(),
            "phone": phone.strip(),
            "avatar_url": avatar_url,
        }
        return MockResult(updated)

    @classmethod
    async def change_password(
        cls,
        *,
        current_password: str,
        new_password: str,
        totp_code: str = "",
    ) -> MockResult[dict[str, bool]]:
        del current_password, new_password, totp_code
        raise MockFailure(
            "A alteração autenticada de senha não está disponível no modo de demonstração.",
            code="unsupported_operation",
        )

    @classmethod
    async def totp_setup(cls) -> MockResult[dict[str, str]]:
        raise MockFailure(
            "O TOTP não está disponível no modo de demonstração.",
            code="unsupported_operation",
        )

    @classmethod
    async def totp_enable(cls, *, code: str) -> MockResult[dict[str, bool]]:
        del code
        raise MockFailure(
            "O TOTP não está disponível no modo de demonstração.",
            code="unsupported_operation",
        )

    @classmethod
    async def totp_disable(cls, *, current_password: str, code: str) -> MockResult[dict[str, bool]]:
        del current_password, code
        raise MockFailure(
            "O TOTP não está disponível no modo de demonstração.",
            code="unsupported_operation",
        )

    @classmethod
    async def revoke_all_sessions(cls) -> MockResult[dict[str, bool]]:
        raise MockFailure(
            "A revogação de sessões não está disponível no modo de demonstração.",
            code="unsupported_operation",
        )

    @classmethod
    async def availability(
        cls,
        barber_id: str,
        service_id: str,
        date: str,
    ) -> list[str]:
        barber = next((item for item in _BARBERS if item["id"] == barber_id and item["active"]), None)
        service = next((item for item in _SERVICES if item["id"] == service_id and item["active"]), None)
        if barber is None or service is None:
            raise MockFailure("Selecione um serviço e barbeiro ativos.", code="invalid_selection")

        try:
            selected_date = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError as error:
            raise MockFailure(
                "A data selecionada é inválida.",
                code="invalid_date",
                status_code=400,
            ) from error
        if (
            selected_date < MOCK_NOW.date()
            or selected_date > MOCK_NOW.date() + timedelta(days=30)
            or selected_date.weekday() == 6
        ):
            return []

        duration = timedelta(minutes=service["duration_minutes"])
        preparation = timedelta(minutes=15)
        closing_time = datetime.combine(selected_date, time(18, 0), LOCAL_TIMEZONE)
        earliest_start = MOCK_NOW + timedelta(hours=2)
        busy = [
            (
                _local_start(appointment),
                _local_start(appointment)
                + timedelta(minutes=appointment["duration_minutes"])
                + preparation,
            )
            for appointment in _APPOINTMENTS
            if appointment["barber_id"] == barber_id
            and appointment["date"] == date
            and appointment["status"] != "cancelled"
        ]
        valid: list[str] = []
        opening_time = datetime.combine(selected_date, time(9, 0), LOCAL_TIMEZONE)
        start = max(opening_time, earliest_start)
        if start.second or start.microsecond:
            start = start.replace(second=0, microsecond=0) + timedelta(minutes=1)
        while start + duration + preparation <= closing_time:
            conflicting_ends = [
                busy_end
                for busy_start, busy_end in busy
                if start < busy_end
                and start + duration + preparation > busy_start
            ]
            if conflicting_ends:
                start = max(conflicting_ends)
                continue
            valid.append(start.strftime("%H:%M"))
            start += duration + preparation
        return valid

    @classmethod
    async def create_appointment(
        cls,
        *,
        client_id: str,
        barber_id: str,
        service_id: str,
        date: str,
        start_time: str,
    ) -> MockResult[AppointmentRecord]:
        times = await cls.availability(barber_id, service_id, date)
        if start_time not in times:
            raise MockFailure(
                "Este horário não está mais disponível.",
                code="appointment_conflict",
                status_code=400,
            )
        client = await cls.user(client_id)
        barber = next(item for item in _BARBERS if item["id"] == barber_id)
        service = next(item for item in _SERVICES if item["id"] == service_id)
        appointment: AppointmentSeed = {
            "id": "appointment-simulated",
            "client_id": client_id,
            "client_name": client["name"],
            "client_email": client["email"],
            "barber_id": barber_id,
            "barber_name": barber["name"],
            "service_id": service_id,
            "service_title": service["title"],
            "price_cents": service["price_cents"],
            "duration_minutes": service["duration_minutes"],
            "date": date,
            "time": start_time,
            "status": "pending",
        }
        return MockResult(_present_appointment(appointment))

    @classmethod
    async def cancel_appointment(
        cls,
        appointment_id: str,
        *,
        client_id: str,
    ) -> MockResult[AppointmentRecord]:
        appointment = next(
            (item for item in _APPOINTMENTS if item["id"] == appointment_id),
            None,
        )
        if appointment is None or appointment["client_id"] != client_id:
            raise MockFailure("Agendamento não encontrado.", code="not_found", status_code=404)
        if appointment["status"] not in {"pending", "confirmed"}:
            raise MockFailure("Este agendamento não pode ser cancelado.", code="invalid_transition")
        if _local_start(appointment) - MOCK_NOW < timedelta(hours=12):
            raise MockFailure(
                "O cancelamento deve ser feito com pelo menos 12 horas de antecedência.",
                code="cancellation_deadline",
                status_code=400,
            )
        return MockResult(_present_appointment({**appointment, "status": "cancelled"}))

    @classmethod
    async def appointment(cls, appointment_id: str) -> AppointmentRecord:
        appointment = next(
            (item for item in _APPOINTMENTS if item["id"] == appointment_id),
            None,
        )
        if appointment is None:
            raise MockFailure("Agendamento não encontrado.", code="not_found", status_code=404)
        return _present_appointment(appointment)

    @classmethod
    async def reschedule_appointment(
        cls,
        appointment_id: str,
        *,
        client_id: str,
        start_time: str,
    ) -> MockResult[AppointmentRecord]:
        appointment = next(
            (item for item in _APPOINTMENTS if item["id"] == appointment_id),
            None,
        )
        if appointment is None or appointment["client_id"] != client_id:
            raise MockFailure("Agendamento não encontrado.", code="not_found", status_code=404)
        if appointment["status"] not in {"pending", "confirmed"}:
            raise MockFailure("Este agendamento não pode ser remarcado.", code="invalid_transition", status_code=400)
        if _local_start(appointment) - MOCK_NOW < timedelta(hours=12):
            raise MockFailure(
                "A remarcação deve ser feita com pelo menos 12 horas de antecedência.",
                code="reschedule_deadline",
                status_code=400,
            )
        try:
            new_start = datetime.fromisoformat(start_time)
            if new_start.tzinfo is None:
                new_start = new_start.replace(tzinfo=LOCAL_TIMEZONE)
        except ValueError as error:
            raise MockFailure("O novo horário é inválido.", code="invalid_date", status_code=400) from error
        if new_start < MOCK_NOW + timedelta(hours=2) or new_start > MOCK_NOW + timedelta(days=30):
            raise MockFailure("O novo horário está fora da janela permitida.", code="invalid_date", status_code=400)
        if new_start.weekday() == 6:
            raise MockFailure("O expediente não atende aos domingos.", code="invalid_date", status_code=400)
        closing = datetime.combine(new_start.date(), time(18, 0), LOCAL_TIMEZONE)
        busy_end = new_start + timedelta(
            minutes=appointment["duration_minutes"] + 15
        )
        if new_start < datetime.combine(new_start.date(), time(9, 0), LOCAL_TIMEZONE) or busy_end > closing:
            raise MockFailure("O novo horário está fora do expediente.", code="invalid_date", status_code=400)
        for existing in _APPOINTMENTS:
            if (
                existing["id"] != appointment_id
                and existing["barber_id"] == appointment["barber_id"]
                and existing["status"] != "cancelled"
            ):
                existing_start = _local_start(existing)
                existing_end = existing_start + timedelta(
                    minutes=existing["duration_minutes"] + 15
                )
                if new_start < existing_end and busy_end > existing_start:
                    raise MockFailure(
                        "Este horário não está mais disponível.",
                        code="appointment_conflict",
                        status_code=400,
                    )
        updated = {
            **appointment,
            "date": new_start.date().isoformat(),
            "time": new_start.strftime("%H:%M"),
        }
        return MockResult(_present_appointment(updated))

    @classmethod
    async def update_appointment_status(
        cls,
        appointment_id: str,
        status: str,
        *,
        actor_role: str,
        barber_id: str = "",
    ) -> MockResult[AppointmentRecord]:
        appointment = next(
            (item for item in _APPOINTMENTS if item["id"] == appointment_id),
            None,
        )
        if appointment is None:
            raise MockFailure("Agendamento não encontrado.", code="not_found", status_code=404)
        if actor_role == "barber" and appointment["barber_id"] != barber_id:
            raise MockFailure("Este atendimento não pertence à sua agenda.", code="forbidden", status_code=403)
        allowed = {
            "pending": {"confirmed", "cancelled"},
            "confirmed": {"completed", "cancelled"},
        }
        if status not in allowed.get(appointment["status"], set()):
            raise MockFailure("Esta transição de status não é permitida.", code="invalid_transition", status_code=400)
        end = _local_start(appointment) + timedelta(minutes=appointment["duration_minutes"])
        if status == "completed" and MOCK_NOW < end:
            raise MockFailure(
                "O atendimento só pode ser concluído após o horário de término.",
                code="appointment_in_progress",
                status_code=400,
            )
        return MockResult(_present_appointment({**appointment, "status": status}))

    @classmethod
    async def admin_mutation(
        cls,
        entity: str,
        action: str,
        values: dict[str, str],
    ) -> MockResult[dict[str, str]]:
        if entity not in {"client", "service", "barber", "user", "settings"}:
            raise MockFailure("Tipo de cadastro inválido.", code="invalid_entity")
        if action not in {"create", "update", "deactivate", "save"}:
            raise MockFailure("Ação administrativa inválida.", code="invalid_action")
        required = {
            "client": ("name", "phone"),
            "service": ("title", "price", "duration"),
            "barber": ("name", "specialty"),
            "user": ("name", "email", "role"),
        }.get(entity, ())
        validate_record = action == "create" or (
            action == "update" and entity in {"client", "service", "barber"}
        )
        if validate_record and any(
            not values.get(field, "").strip() for field in required
        ):
            raise MockFailure(
                "Preencha os campos obrigatórios.",
                code="validation_error",
                status_code=400,
            )
        if (
            entity in {"client", "service", "barber"}
            and action == "update"
            and not values.get("id", "").strip()
        ):
            raise MockFailure(
                "Registro não informado para edição.",
                code="validation_error",
                status_code=400,
            )
        if entity == "client" and validate_record:
            digits = "".join(filter(str.isdigit, values["phone"]))
            if len(digits) < 10:
                raise MockFailure("Informe um telefone válido.", code="validation_error", status_code=400)
        if entity == "service" and validate_record:
            try:
                price = Decimal(values["price"].replace(",", "."))
                duration = int(values["duration"])
            except (InvalidOperation, ValueError) as error:
                raise MockFailure(
                    "Preço e duração devem ser numéricos.",
                    code="validation_error",
                    status_code=400,
                ) from error
            if price <= 0 or duration <= 0:
                raise MockFailure(
                    "Preço e duração devem ser maiores que zero.",
                    code="validation_error",
                    status_code=400,
                )
        if entity == "user" and action == "create" and "@" not in values["email"]:
            raise MockFailure(
                "Informe um e-mail válido.",
                code="validation_error",
                status_code=400,
            )
        if entity == "user" and values.get("role") not in {"client", "barber", "admin"}:
            raise MockFailure("Papel de usuário inválido.", code="validation_error", status_code=400)
        return MockResult({"entity": entity, "action": action, **values})

    @classmethod
    async def revenue(
        cls,
        period: Literal["day", "month"],
        selected_date: str,
    ) -> int:
        if period not in {"day", "month"}:
            raise MockFailure("Período inválido.", code="validation_error")
        completed = [
            item
            for item in _APPOINTMENTS
            if item["status"] == "completed"
            and (
                item["date"] == selected_date
                if period == "day"
                else item["date"].startswith(selected_date[:7])
            )
        ]
        return sum(item["price_cents"] for item in completed)
