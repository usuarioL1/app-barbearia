from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import Any, Literal, TypeVar, cast
from urllib.parse import urlparse

import reflex as rx

from app_barbearia.mock_repository import (
    LOCAL_TIMEZONE,
    MOCK_NOW,
    AppointmentRecord,
    BarberRecord,
    BarberAppointmentRecord,
    ClientRecord,
    MockFailure,
    ServiceRecord,
    UserRecord,
    RATE_LIMIT_MESSAGE,
    barber_appointment_view,
)
from app_barbearia.xano_repository import XanoRepository, repository_for, xano_enabled


_MONTH_LABELS = (
    "Jan",
    "Fev",
    "Mar",
    "Abr",
    "Mai",
    "Jun",
    "Jul",
    "Ago",
    "Set",
    "Out",
    "Nov",
    "Dez",
)
_MONTH_NAMES = (
    "Janeiro",
    "Fevereiro",
    "Março",
    "Abril",
    "Maio",
    "Junho",
    "Julho",
    "Agosto",
    "Setembro",
    "Outubro",
    "Novembro",
    "Dezembro",
)
_INITIAL_TODAY = date.today()
_AppointmentStatusRecord = TypeVar(
    "_AppointmentStatusRecord",
    AppointmentRecord,
    BarberAppointmentRecord,
)


def _format_brazilian_date(value: str) -> str:
    """Converte uma data ISO somente para apresentação em português brasileiro."""
    if not value:
        return ""
    try:
        return date.fromisoformat(value).strftime("%d/%m/%Y")
    except ValueError:
        return value


def _report_month_window(anchor_month: date) -> tuple[str, str]:
    month_index = anchor_month.year * 12 + anchor_month.month - 1
    first_month_index = month_index - 5
    first_month = date(
        first_month_index // 12,
        first_month_index % 12 + 1,
        1,
    )
    next_month = date(
        anchor_month.year + (anchor_month.month == 12),
        anchor_month.month % 12 + 1,
        1,
    )
    return first_month.isoformat(), (next_month - timedelta(days=1)).isoformat()


def _completed_appointment_revenue(
    appointments: list[AppointmentRecord],
    period: Literal["day", "month"],
    selected_date: str,
) -> int:
    return sum(
        appointment["price_cents"]
        for appointment in _completed_appointments(
            appointments,
            period,
            selected_date,
        )
    )


def _completed_appointments(
    appointments: list[AppointmentRecord],
    period: Literal["day", "month"],
    selected_date: str,
) -> list[AppointmentRecord]:
    return [
        appointment
        for appointment in appointments
        if appointment["status"] == "completed"
        and (
            appointment["date"] == selected_date
            if period == "day"
            else appointment["date"].startswith(selected_date[:7])
        )
    ]


def _attendance_rate_display(completed_count: int, cancelled_count: int) -> str:
    finished_count = completed_count + cancelled_count
    if finished_count == 0:
        return "—"
    return f"{round(completed_count / finished_count * 100)}%"


def _monthly_revenue_series(
    anchor_month: date,
    appointments: list[AppointmentRecord],
) -> list[dict[str, str]]:
    month_index = anchor_month.year * 12 + anchor_month.month - 1
    months = [
        date((month_index + offset) // 12, (month_index + offset) % 12 + 1, 1)
        for offset in range(-5, 1)
    ]
    values = [
        (
            _MONTH_LABELS[item.month - 1],
            _completed_appointment_revenue(
                appointments,
                "month",
                item.isoformat(),
            ),
        )
        for item in months
    ]
    maximum = max((value for _, value in values), default=0)
    return [
        {
            "month": label,
            "amount": str(value),
            "height": f"{max(4, round(value / maximum * 100))}px"
            if maximum
            else "4px",
        }
        for label, value in values
    ]


def _report_service_gradient(services: list[dict[str, str]]) -> str:
    counts = [int(item["count"]) for item in services]
    total = sum(counts)
    if not total:
        return "conic-gradient(#292929 0% 100%)"

    colors = ("#d5a64a", "#54789a", "#7d9872", "#a46c5b")
    segments = []
    cumulative = 0
    for index, count in enumerate(counts):
        start = round(cumulative / total * 100)
        cumulative += count
        end = 100 if index == len(counts) - 1 else round(cumulative / total * 100)
        segments.append(f"{colors[index % len(colors)]} {start}% {end}%")
    return f"conic-gradient({', '.join(segments)})"


def _appointments_for_date(
    appointments: list[AppointmentRecord],
    selected_date: str,
) -> list[AppointmentRecord]:
    return [item for item in appointments if item["date"] == selected_date]


def _reconcile_missing_appointment_statuses(
    appointments: list[_AppointmentStatusRecord],
    filtered_appointments: dict[str, list[_AppointmentStatusRecord]],
) -> list[_AppointmentStatusRecord]:
    status_presentation = {
        "pending": ("Pendente", "#d6a64f"),
        "confirmed": ("Confirmado", "#54a86b"),
        "cancelled": ("Cancelado", "#d9776b"),
        "completed": ("Concluído", "#aaa69d"),
    }
    known_statuses = {
        appointment["id"]: status
        for status, records in filtered_appointments.items()
        for appointment in records
    }
    reconciled: list[_AppointmentStatusRecord] = []
    for appointment in appointments:
        existing_status = appointment["status"]
        if existing_status not in status_presentation:
            existing_status = "pending"
        status = known_statuses.get(appointment["id"], existing_status)
        status_label, status_color = status_presentation[status]
        reconciled.append(
            cast(
                _AppointmentStatusRecord,
                {
                    **appointment,
                    "status": status,
                    "status_label": status_label,
                    "status_color": status_color,
                },
            )
        )
    return reconciled


def _filter_admin_clients(
    clients: list[ClientRecord],
    search: str,
) -> list[ClientRecord]:
    clients = [client for client in clients if client["role"] == "client"]
    query = search.strip().casefold()
    if not query:
        return clients
    return [
        client
        for client in clients
        if any(
            query in client[field].casefold()
            for field in ("name", "email", "phone")
        )
    ]


def _repository_for(state: object) -> Any:
    return repository_for(getattr(state, "_auth_token", ""))


def _clear_authenticated_session(state: Any) -> None:
    state._auth_token = ""
    state.is_authenticated = False
    state.current_user_id = ""
    state.user_name = ""
    state.greeting_name = ""
    state.user_email = ""
    state.user_phone = ""
    state.user_role = ""
    state.profile_name = ""
    state.profile_email = ""
    state.profile_phone = ""
    state.customer_appointments = []
    state.upcoming_appointments = []
    state.next_appointments = []
    state.historical_appointments = []
    state._login_password = ""
    state._signup_password = ""
    state._signup_password_confirmation = ""


async def _ensure_authenticated(
    state: Any,
    allowed_roles: set[str],
) -> tuple[bool, rx.event.EventSpec | None]:
    token = getattr(state, "_auth_token", "")
    if not xano_enabled() or not token:
        redirect = rx.redirect("/login")
        failure = MockFailure(
            "Entre para continuar.",
            code="unauthorized",
            status_code=401,
        )
    else:
        try:
            user = await XanoRepository(token).current_user()
        except MockFailure as error:
            failure = error
            redirect = rx.redirect("/login") if error.status_code == 401 else None
        else:
            AppState._present_user(state, user)
            state.is_authenticated = True
            if user["role"] in allowed_roles:
                return True, None
            failure = MockFailure(
                "Seu perfil não tem acesso a esta área.",
                code="forbidden",
                status_code=403,
            )
            routes = {
                "client": "/",
                "barber": "/barbeiro",
                "admin": "/admin",
            }
            redirect = rx.redirect(routes[user["role"]])

    state.error_message = str(failure)
    state.success_message = ""
    if failure.status_code == 401:
        _clear_authenticated_session(state)
    return False, redirect


class AppState(rx.State):
    is_loading: bool = False
    error_message: str = ""
    success_message: str = ""
    current_user_id: str = ""
    user_name: str = ""
    greeting_name: str = ""
    user_email: str = ""
    user_phone: str = ""
    user_role: str = ""
    is_authenticated: bool = False

    login_email: str = ""
    _login_password: str = ""
    signup_name: str = ""
    signup_email: str = ""
    signup_phone: str = ""
    _signup_password: str = ""
    _signup_password_confirmation: str = ""
    _auth_token: str = ""
    _reset_email: str = ""
    _reset_token: str = ""
    _reset_password: str = ""
    _reset_password_confirmation: str = ""
    is_reset_flow: bool = False
    recovery_email: str = ""

    profile_name: str = ""
    profile_email: str = ""
    profile_phone: str = ""
    profile_avatar_url: str = ""
    security_current_password: str = ""
    security_new_password: str = ""
    security_totp_code: str = ""
    totp_enabled: bool = False
    totp_setup_secret: str = ""

    services: list[ServiceRecord] = []
    barbers: list[BarberRecord] = []
    clients: list[ClientRecord] = []
    users: list[UserRecord] = []
    admin_client_search: str = ""
    admin_client_form_open: bool = False
    admin_client_form_action: Literal["create", "update"] = "create"
    admin_client_form_id: str = ""
    admin_client_form_name: str = ""
    admin_client_form_phone: str = ""
    admin_service_form_open: bool = False
    admin_service_form_action: Literal["create", "update"] = "create"
    admin_service_form_id: str = ""
    admin_service_form_title: str = ""
    admin_service_form_description: str = ""
    admin_service_form_price: str = ""
    admin_service_form_duration: str = ""
    admin_barber_form_open: bool = False
    admin_barber_form_action: Literal["create", "update"] = "create"
    admin_barber_form_id: str = ""
    admin_barber_form_name: str = ""
    admin_barber_form_specialty: str = ""
    service_search: str = ""
    customer_appointments: list[AppointmentRecord] = []
    upcoming_appointments: list[AppointmentRecord] = []
    next_appointments: list[AppointmentRecord] = []
    historical_appointments: list[AppointmentRecord] = []
    appointment_filter: str = "all"
    upcoming_period_filter: Literal["all", "7", "30", "90"] = "all"
    history_period_filter: Literal["all", "30", "90", "365"] = "all"
    history_category_filter: Literal["Todos", "Cortes", "Barba", "Combos"] = "Todos"
    selected_appointment: AppointmentRecord | None = None
    reschedule_appointment_id: str = ""
    reschedule_date: str = ""
    reschedule_time: str = ""
    reschedule_available_times: list[str] = []

    selected_service_id: str = "corte"
    selected_service_ids: list[str] = []
    selected_service_title: str = "Corte Masculino"
    selected_service_price: str = "R$ 40,00"
    selected_service_duration: str = "30 min"
    selected_barber_id: str = "rafael"
    selected_barber_name: str = "Rafael Silva"
    selected_date: str = _INITIAL_TODAY.isoformat()
    selected_day: str = _INITIAL_TODAY.strftime("%d")
    selected_date_display: str = _INITIAL_TODAY.strftime("%d/%m/%Y")
    selected_time: str = ""
    booking_month: str = _INITIAL_TODAY.strftime("%Y-%m")
    booking_month_display: str = (
        f"{_MONTH_NAMES[_INITIAL_TODAY.month - 1]} {_INITIAL_TODAY.year}"
    )
    calendar_days: list[str] = []
    available_times: list[str] = []
    booking_confirmed: bool = False
    booking_confirmation_service: str = ""
    booking_confirmation_date: str = ""
    booking_confirmation_time: str = ""

    barber_id: str = "rafael"
    barber_date: str = _INITIAL_TODAY.isoformat()
    barber_appointments: list[BarberAppointmentRecord] = []

    admin_date: str = _INITIAL_TODAY.isoformat()
    admin_view_mode: Literal["day", "week"] = "week"
    admin_filter_barber: str = ""
    admin_filter_status: str = ""
    admin_appointments: list[AppointmentRecord] = []
    admin_week_days: list[dict[str, str]] = []
    admin_dashboard_appointments: list[AppointmentRecord] = []
    admin_revenue_cents: int = 0
    admin_completed_count: int = 0
    admin_cancelled_count: int = 0
    admin_revenue_series: list[dict[str, str]] = []
    admin_report_period: Literal["day", "month"] = "month"
    admin_report_date: str = _INITIAL_TODAY.replace(day=1).isoformat()
    admin_report_revenue_cents: int = 0
    admin_report_completed_count: int = 0
    admin_report_service_summary: list[dict[str, str]] = []
    admin_report_revenue_series: list[dict[str, str]] = []
    admin_report_service_gradient: str = "conic-gradient(#292929 0% 100%)"

    @rx.var
    def barber_date_display(self) -> str:
        return date.fromisoformat(self.barber_date).strftime("%d/%m/%Y")

    @rx.var
    def barber_appointment_count(self) -> str:
        count = sum(item["status"] != "cancelled" for item in self.barber_appointments)
        return str(count)

    @rx.var
    def barber_duration_display(self) -> str:
        minutes = sum(
            item["duration_minutes"]
            for item in self.barber_appointments
            if item["status"] != "cancelled"
        )
        return f"{minutes // 60}h {minutes % 60:02d}min"

    @rx.var
    def barber_revenue_display(self) -> str:
        cents = sum(
            item["price_cents"]
            for item in self.barber_appointments
            if item["status"] == "completed"
        )
        return f"R$ {cents // 100},{cents % 100:02d}"

    def _next_barber_appointment(self) -> BarberAppointmentRecord | None:
        now_key = (MOCK_NOW.date().isoformat(), MOCK_NOW.strftime("%H:%M"))
        return next(
            (
                item
                for item in self.barber_appointments
                if item["status"] in {"pending", "confirmed"}
                and (item["date"], item["time"]) >= now_key
            ),
            None,
        )

    @rx.var
    def barber_next_client_name(self) -> str:
        appointment = self._next_barber_appointment()
        return appointment["client_name"] if appointment else "Nenhum atendimento"

    @rx.var
    def barber_next_service_title(self) -> str:
        appointment = self._next_barber_appointment()
        return appointment["service_title"] if appointment else "Programado para esta data"

    @rx.var
    def barber_next_time(self) -> str:
        appointment = self._next_barber_appointment()
        return appointment["time"] if appointment else "—"

    @rx.var
    def admin_date_display(self) -> str:
        return date.fromisoformat(self.admin_date).strftime("%d/%m/%Y")

    @rx.var
    def admin_report_date_display(self) -> str:
        return _format_brazilian_date(self.admin_report_date)

    @rx.var
    def reschedule_date_display(self) -> str:
        return _format_brazilian_date(self.reschedule_date)

    @rx.var
    def admin_day_appointments(self) -> list[AppointmentRecord]:
        return _appointments_for_date(self.admin_appointments, self.admin_date)

    @rx.var
    def admin_appointment_count(self) -> str:
        return str(len(self.admin_dashboard_appointments))

    @rx.var
    def admin_client_count(self) -> str:
        return str(len(self.filtered_admin_clients))

    @rx.var
    def filtered_admin_clients(self) -> list[ClientRecord]:
        return _filter_admin_clients(self.clients, self.admin_client_search)

    @rx.var
    def filtered_admin_client_count(self) -> str:
        return str(len(self.filtered_admin_clients))

    @rx.var
    def admin_revenue_display(self) -> str:
        return f"R$ {self.admin_revenue_cents // 100},{self.admin_revenue_cents % 100:02d}"

    @rx.var
    def admin_attendance_display(self) -> str:
        return _attendance_rate_display(
            self.admin_completed_count,
            self.admin_cancelled_count,
        )

    @rx.var
    def admin_report_revenue_display(self) -> str:
        cents = self.admin_report_revenue_cents
        return f"R$ {cents // 100},{cents % 100:02d}"

    @rx.var
    def admin_report_average_display(self) -> str:
        if self.admin_report_completed_count == 0:
            return "—"
        cents = round(
            self.admin_report_revenue_cents / self.admin_report_completed_count
        )
        return f"R$ {cents // 100},{cents % 100:02d}"

    @rx.var
    def admin_report_completed_count_display(self) -> str:
        return str(self.admin_report_completed_count)

    def _begin_request(self) -> None:
        self.is_loading = True
        self.error_message = ""
        self.success_message = ""

    def _end_request(self) -> None:
        self.is_loading = False

    def _set_failure(self, error: MockFailure) -> None:
        if error.status_code == 401:
            _clear_authenticated_session(self)
        if error.status_code == 429:
            self.error_message = RATE_LIMIT_MESSAGE
        else:
            self.error_message = str(error)

    @rx.event
    def set_login_email(self, value: str) -> None:
        self.login_email = value

    @rx.event
    def set_login_password(self, value: str) -> None:
        self._login_password = value

    @rx.event
    def set_signup_name(self, value: str) -> None:
        self.signup_name = value

    @rx.event
    def set_signup_email(self, value: str) -> None:
        self.signup_email = value

    @rx.event
    def set_signup_phone(self, value: str) -> None:
        self.signup_phone = value

    @rx.event
    def set_signup_password(self, value: str) -> None:
        self._signup_password = value

    @rx.event
    def set_signup_password_confirmation(self, value: str) -> None:
        self._signup_password_confirmation = value

    @rx.event
    def set_recovery_email(self, value: str) -> None:
        self.recovery_email = value

    @rx.event
    def set_reset_password(self, value: str) -> None:
        self._reset_password = value

    @rx.event
    def set_reset_password_confirmation(self, value: str) -> None:
        self._reset_password_confirmation = value

    @rx.event
    def load_password_reset(self) -> None:
        query = self.router.url.query_parameters
        email = query.get("email", "").strip()
        token = query.get("token", "").strip()
        self._reset_email = email
        self._reset_token = token
        self._reset_password = ""
        self._reset_password_confirmation = ""
        self.is_reset_flow = bool(email and token)

    @rx.event
    async def update_password(self) -> rx.event.EventSpec | None:
        password = self._reset_password
        confirmation = self._reset_password_confirmation
        if not self._reset_email or not self._reset_token:
            self.error_message = "O link de redefinição é inválido ou expirou."
            self.success_message = ""
            return
        if len(password) < 8:
            self.error_message = "A senha deve conter pelo menos 8 caracteres."
            self.success_message = ""
            self._reset_password = ""
            self._reset_password_confirmation = ""
            return
        if password != confirmation:
            self.error_message = "As senhas não conferem."
            self.success_message = ""
            self._reset_password = ""
            self._reset_password_confirmation = ""
            return

        self._begin_request()
        try:
            result = await _repository_for(self).update_password(
                email=self._reset_email,
                token=self._reset_token,
                password=password,
            )
        except MockFailure as error:
            self._set_failure(error)
        else:
            self.is_reset_flow = False
            self._reset_email = ""
            self._reset_token = ""
            self.success_message = result.message
            return rx.redirect("/login")
        finally:
            self._reset_password = ""
            self._reset_password_confirmation = ""
            self._end_request()

    @rx.event
    def set_profile_name(self, value: str) -> None:
        self.profile_name = value

    @rx.event
    def set_profile_email(self, value: str) -> None:
        self.profile_email = value

    @rx.event
    def set_profile_phone(self, value: str) -> None:
        self.profile_phone = value

    @rx.event
    def set_profile_avatar_url(self, value: str) -> None:
        self.profile_avatar_url = value

    @rx.event
    def set_security_current_password(self, value: str) -> None:
        self.security_current_password = value

    @rx.event
    def set_security_new_password(self, value: str) -> None:
        self.security_new_password = value

    @rx.event
    def set_security_totp_code(self, value: str) -> None:
        self.security_totp_code = value

    @rx.event
    def logout(self) -> rx.event.EventSpec:
        self._auth_token = ""
        self.is_authenticated = False
        self.current_user_id = ""
        self.user_name = ""
        self.greeting_name = ""
        self.user_email = ""
        self.user_phone = ""
        self.user_role = ""
        self.profile_name = ""
        self.profile_email = ""
        self.profile_phone = ""
        self.customer_appointments = []
        self.upcoming_appointments = []
        self.next_appointments = []
        self.historical_appointments = []
        self._login_password = ""
        self._signup_password = ""
        self._signup_password_confirmation = ""
        return rx.redirect("/login")

    @rx.event
    def set_admin_client_search(self, value: str) -> None:
        self.admin_client_search = value

    @rx.event
    def set_admin_client_form_name(self, value: str) -> None:
        self.admin_client_form_name = value

    @rx.event
    def set_admin_client_form_phone(self, value: str) -> None:
        self.admin_client_form_phone = value

    def _open_admin_client_form(self, action: str, record_id: str) -> None:
        if action not in {"create", "update"}:
            self.error_message = "Ação de cliente inválida."
            self.success_message = ""
            return

        client = next(
            (item for item in self.clients if item["id"] == record_id),
            None,
        )
        if action == "update" and client is None:
            self.error_message = "Cliente não encontrado na lista atual."
            self.success_message = ""
            return

        self.admin_client_form_action = action
        self.admin_client_form_id = record_id if action == "update" else ""
        self.admin_client_form_name = client["name"] if client else ""
        self.admin_client_form_phone = client["phone"] if client else ""
        self.admin_client_form_open = True
        self.error_message = ""
        self.success_message = ""

    @rx.event
    def open_admin_client_form(self) -> None:
        self._open_admin_client_form("create", "")

    @rx.event
    def open_admin_client_edit_form(self, record_id: str) -> None:
        self._open_admin_client_form("update", record_id)

    @rx.event
    def close_admin_client_form(self) -> None:
        self.admin_client_form_open = False

    @rx.event
    async def submit_admin_client_form(self) -> None:
        values = {
            "name": self.admin_client_form_name,
            "phone": self.admin_client_form_phone,
        }
        if self.admin_client_form_action == "update":
            values["id"] = self.admin_client_form_id

        await self._run_admin_mutation(
            "client",
            self.admin_client_form_action,
            values,
        )
        if not self.error_message:
            self.admin_client_form_open = False

    @rx.event
    def set_admin_service_form_title(self, value: str) -> None:
        self.admin_service_form_title = value

    @rx.event
    def set_admin_service_form_description(self, value: str) -> None:
        self.admin_service_form_description = value

    @rx.event
    def set_admin_service_form_price(self, value: str) -> None:
        self.admin_service_form_price = value

    @rx.event
    def set_admin_service_form_duration(self, value: str) -> None:
        self.admin_service_form_duration = value

    def _open_admin_service_form(self, action: str, record_id: str) -> None:
        if action not in {"create", "update"}:
            self.error_message = "Ação de serviço inválida."
            self.success_message = ""
            return

        service = next(
            (item for item in self.services if item["id"] == record_id),
            None,
        )
        if action == "update" and service is None:
            self.error_message = "Serviço não encontrado no catálogo atual."
            self.success_message = ""
            return

        self.admin_service_form_action = action
        self.admin_service_form_id = record_id if action == "update" else ""
        self.admin_service_form_title = service["title"] if service else ""
        self.admin_service_form_description = (
            service["description"] if service else ""
        )
        self.admin_service_form_price = (
            f"{service['price_cents'] // 100}.{service['price_cents'] % 100:02d}"
            if service
            else ""
        )
        self.admin_service_form_duration = (
            str(service["duration_minutes"]) if service else ""
        )
        self.admin_service_form_open = True
        self.error_message = ""
        self.success_message = ""

    @rx.event
    def open_admin_service_form(self) -> None:
        self._open_admin_service_form("create", "")

    @rx.event
    def open_admin_service_edit_form(self, record_id: str) -> None:
        self._open_admin_service_form("update", record_id)

    @rx.event
    def close_admin_service_form(self) -> None:
        self.admin_service_form_open = False

    @rx.event
    async def submit_admin_service_form(self) -> None:
        values = {
            "title": self.admin_service_form_title,
            "description": self.admin_service_form_description,
            "price": self.admin_service_form_price,
            "duration": self.admin_service_form_duration,
        }
        if self.admin_service_form_action == "update":
            values["id"] = self.admin_service_form_id

        await self._run_admin_mutation(
            "service",
            self.admin_service_form_action,
            values,
        )
        if not self.error_message:
            self.admin_service_form_open = False

    @rx.event
    def set_admin_barber_form_name(self, value: str) -> None:
        self.admin_barber_form_name = value

    @rx.event
    def set_admin_barber_form_specialty(self, value: str) -> None:
        self.admin_barber_form_specialty = value

    def _open_admin_barber_form(self, action: str, record_id: str) -> None:
        if action not in {"create", "update"}:
            self.error_message = "Ação de equipe inválida."
            self.success_message = ""
            return

        barber = next(
            (item for item in self.barbers if item["id"] == record_id),
            None,
        )
        if action == "update" and barber is None:
            self.error_message = "Barbeiro não encontrado na equipe atual."
            self.success_message = ""
            return

        self.admin_barber_form_action = action
        self.admin_barber_form_id = record_id if action == "update" else ""
        self.admin_barber_form_name = barber["name"] if barber else ""
        self.admin_barber_form_specialty = barber["specialty"] if barber else ""
        self.admin_barber_form_open = True
        self.error_message = ""
        self.success_message = ""

    @rx.event
    def open_admin_barber_form(self) -> None:
        self._open_admin_barber_form("create", "")

    @rx.event
    def open_admin_barber_edit_form(self, record_id: str) -> None:
        self._open_admin_barber_form("update", record_id)

    @rx.event
    def close_admin_barber_form(self) -> None:
        self.admin_barber_form_open = False

    @rx.event
    async def submit_admin_barber_form(self) -> None:
        values = {
            "name": self.admin_barber_form_name,
            "specialty": self.admin_barber_form_specialty,
        }
        if self.admin_barber_form_action == "update":
            values["id"] = self.admin_barber_form_id

        await self._run_admin_mutation(
            "barber",
            self.admin_barber_form_action,
            values,
        )
        if not self.error_message:
            self.admin_barber_form_open = False

    @rx.var
    def filtered_services(self) -> list[ServiceRecord]:
        query = self.service_search.strip().casefold()
        return [
            service
            for service in self.services
            if not query
            or query in service["title"].casefold()
            or query in service["description"].casefold()
        ]

    def _split_customer_appointments(
        self,
        appointments: list[AppointmentRecord],
    ) -> None:
        today = MOCK_NOW.date().isoformat()
        appointments = sorted(
            appointments,
            key=lambda item: (item["date"], item["time"]),
        )
        self.customer_appointments = appointments
        self.upcoming_appointments = [
            item
            for item in appointments
            if item["status"] in {"pending", "confirmed"} and item["date"] >= today
        ]
        self.next_appointments = self.upcoming_appointments[:1]
        self.historical_appointments = [
            item
            for item in appointments
            if item["status"] in {"completed", "cancelled"} or item["date"] < today
        ]

    @rx.var
    def filtered_upcoming_appointments(self) -> list[AppointmentRecord]:
        if self.upcoming_period_filter == "all":
            return self.upcoming_appointments
        cutoff = (MOCK_NOW.date() + timedelta(days=int(self.upcoming_period_filter))).isoformat()
        return [
            item
            for item in self.upcoming_appointments
            if item["date"] <= cutoff
        ]

    @rx.var
    def filtered_historical_appointments(self) -> list[AppointmentRecord]:
        items = self.historical_appointments
        if self.history_period_filter != "all":
            cutoff = (MOCK_NOW.date() - timedelta(days=int(self.history_period_filter))).isoformat()
            items = [item for item in items if item["date"] >= cutoff]
        category = self.history_category_filter
        if category == "Todos":
            return items

        def matches_category(title: str) -> bool:
            normalized = title.strip().casefold()
            if category == "Combos":
                return "combo" in normalized or "corte + barba" in normalized
            if category == "Barba":
                return "barba" in normalized
            if category == "Cortes":
                return any(
                    term in normalized
                    for term in ("corte", "pezinho", "acabamento", "sobrancelha")
                )
            return False

        return [item for item in items if matches_category(item["service_title"])]

    def _calendar_for_month(self, month: str) -> list[str]:
        year, month_number = (int(part) for part in month.split("-"))
        first_day = date(year, month_number, 1)
        next_month = (
            date(year + 1, 1, 1)
            if month_number == 12
            else date(year, month_number + 1, 1)
        )
        days_in_month = (next_month - first_day).days
        leading_blanks = first_day.weekday()
        days = [""] * leading_blanks + [
            str(day).zfill(2) for day in range(1, days_in_month + 1)
        ]
        days.extend([""] * ((7 - len(days) % 7) % 7))
        return days

    def _month_label(self, month: str) -> str:
        month_names = (
            "Janeiro",
            "Fevereiro",
            "Março",
            "Abril",
            "Maio",
            "Junho",
            "Julho",
            "Agosto",
            "Setembro",
            "Outubro",
            "Novembro",
            "Dezembro",
        )
        year, month_number = (int(part) for part in month.split("-"))
        return f"{month_names[month_number - 1]} {year}"

    def _present_user(self, user: UserRecord) -> None:
        self.current_user_id = user["id"]
        self.user_name = user["name"]
        self.greeting_name = user["name"].split()[0]
        self.user_email = user["email"]
        self.user_phone = user["phone"]
        self.user_role = user["role"]
        self.profile_name = user["name"]
        self.profile_email = user["email"]
        self.profile_phone = user["phone"]
        self.profile_avatar_url = user.get("avatar_url", "")

    @rx.event
    async def load_client_portal(self) -> rx.event.EventSpec | None:
        allowed, redirect = await _ensure_authenticated(self, {"client"})
        if not allowed:
            return redirect
        self._begin_request()
        try:
            appointments = await _repository_for(self).customer_appointments(
                self.current_user_id
            )
        except MockFailure as error:
            self._set_failure(error)
        else:
            self._split_customer_appointments(appointments)
        finally:
            self._end_request()

    @rx.event
    async def load_catalog(self) -> None:
        self._begin_request()
        try:
            services = await _repository_for(self).services()
            barbers = await _repository_for(self).barbers()
        except MockFailure as error:
            self.services = []
            self.barbers = []
            self._set_failure(error)
        else:
            self.services = services
            self.barbers = barbers
        finally:
            self._end_request()

    @rx.event
    async def load_appointments(self) -> rx.event.EventSpec | None:
        allowed, redirect = await _ensure_authenticated(self, {"client"})
        if not allowed:
            return redirect
        self._begin_request()
        try:
            appointments = await _repository_for(self).customer_appointments(
                self.current_user_id
            )
        except MockFailure as error:
            self._set_failure(error)
        else:
            self._split_customer_appointments(appointments)
        finally:
            self._end_request()

    @rx.event
    async def load_profile(self) -> rx.event.EventSpec | None:
        allowed, redirect = await _ensure_authenticated(self, {"client"})
        if not allowed:
            return redirect
        if self.current_user_id == "client-new":
            return
        self._begin_request()
        try:
            user = await _repository_for(self).user(self.current_user_id)
        except MockFailure as error:
            self._set_failure(error)
        else:
            self._present_user(user)
        finally:
            self._end_request()

    async def _load_barber_appointments(self, selected_date: str) -> None:
        allowed, _ = await _ensure_authenticated(self, {"barber"})
        if not allowed:
            return
        self._begin_request()
        try:
            repository = _repository_for(self)
            appointments = await repository.barber_appointments(
                self.barber_id,
                date=selected_date,
            )
            status_appointments = {
                known_status: await repository.barber_appointments(
                    self.barber_id,
                    date=selected_date,
                    status=known_status,
                )
                for known_status in ("completed", "confirmed", "cancelled")
            }
            appointment_ids = {item["id"] for item in appointments}
            if appointment_ids and all(
                {item["id"] for item in filtered_appointments} == appointment_ids
                for filtered_appointments in status_appointments.values()
            ):
                status_appointments = {}
            appointments = _reconcile_missing_appointment_statuses(
                appointments,
                status_appointments,
            )
        except MockFailure as error:
            self._set_failure(error)
        else:
            self.barber_date = selected_date
            self.barber_appointments = appointments
        finally:
            self._end_request()

    @rx.event
    async def load_barber_workspace(self) -> None:
        await self._load_barber_appointments(date.today().isoformat())

    @rx.event
    async def change_barber_date(self, day_delta: int) -> None:
        next_date = date.fromisoformat(self.barber_date) + timedelta(days=day_delta)
        await self._load_barber_appointments(next_date.isoformat())

    @rx.event
    async def set_barber_date(self, selected_date: str) -> None:
        await self._load_barber_appointments(selected_date)

    @rx.event
    async def update_barber_appointment_status(
        self,
        appointment_id: str,
        status: str,
    ) -> None:
        self._begin_request()
        try:
            result = await _repository_for(self).update_appointment_status(
                appointment_id,
                status,
                actor_role="barber",
                barber_id=self.barber_id,
            )
        except MockFailure as error:
            self._set_failure(error)
        else:
            barber_view = barber_appointment_view(result.data)
            barber_view = {
                **next(
                    (
                        item
                        for item in self.barber_appointments
                        if item["id"] == appointment_id
                    ),
                    {},
                ),
                **{
                    key: value
                    for key, value in barber_view.items()
                    if value != ""
                },
            }
            self.barber_appointments = [
                barber_view if item["id"] == appointment_id else item
                for item in self.barber_appointments
            ]
            self.success_message = result.message
        finally:
            self._end_request()

    async def _load_admin_agenda(
        self,
        *,
        selected_date: str,
        barber_id: str,
        status: str,
    ) -> None:
        allowed, _ = await _ensure_authenticated(self, {"admin"})
        if not allowed:
            return
        try:
            selected = date.fromisoformat(selected_date)
        except ValueError:
            self.error_message = "Informe uma data válida para a agenda."
            self.success_message = ""
            return
        week_start = selected - timedelta(days=selected.weekday())
        week_dates = [
            week_start + timedelta(days=day_number)
            for day_number in range(7)
        ]
        range_start = week_dates[0]
        range_end = week_dates[-1]
        self._begin_request()
        try:
            repository = _repository_for(self)
            appointments = await repository.admin_appointments(
                barber_id=barber_id,
                status=status,
                from_date=range_start.isoformat(),
                to_date=range_end.isoformat(),
            )
            if not status:
                status_appointments = {
                    known_status: await repository.admin_appointments(
                        barber_id=barber_id,
                        status=known_status,
                        from_date=range_start.isoformat(),
                        to_date=range_end.isoformat(),
                    )
                    for known_status in ("completed", "confirmed", "cancelled")
                }
                appointments = _reconcile_missing_appointment_statuses(
                    appointments,
                    status_appointments,
                )
            barbers = await repository.barbers()
        except MockFailure as error:
            self._set_failure(error)
        else:
            week_end = week_dates[-1]
            self.admin_date = selected_date
            self.admin_filter_barber = barber_id
            self.admin_filter_status = status
            self.admin_appointments = [
                item
                for item in appointments
                if week_start.isoformat() <= item["date"] <= week_end.isoformat()
            ]
            day_names = ("Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom")
            self.admin_week_days = [
                {
                    "date": day.isoformat(),
                    "label": (
                        f"{day_names[day.weekday()]} "
                        f"{day.strftime('%d/%m/%Y')}"
                    ),
                    "count": str(
                        sum(item["date"] == day.isoformat() for item in self.admin_appointments)
                    ),
                }
                for day in week_dates
            ]
            self.barbers = barbers
        finally:
            self._end_request()

    @rx.event
    async def load_admin_agenda(self) -> None:
        await self._load_admin_agenda(
            selected_date=date.today().isoformat(),
            barber_id=self.admin_filter_barber,
            status=self.admin_filter_status,
        )

    @rx.event
    async def set_admin_barber_filter(self, barber_id: str) -> None:
        await self._load_admin_agenda(
            selected_date=self.admin_date,
            barber_id=barber_id,
            status=self.admin_filter_status,
        )

    @rx.event
    async def set_admin_status_filter(self, status: str) -> None:
        await self._load_admin_agenda(
            selected_date=self.admin_date,
            barber_id=self.admin_filter_barber,
            status=status,
        )

    @rx.event
    async def set_admin_date(self, selected_date: str) -> None:
        await self._load_admin_agenda(
            selected_date=selected_date,
            barber_id=self.admin_filter_barber,
            status=self.admin_filter_status,
        )

    @rx.event
    async def change_admin_date(self, day_delta: int) -> None:
        next_date = date.fromisoformat(self.admin_date) + timedelta(days=day_delta)
        await self._load_admin_agenda(
            selected_date=next_date.isoformat(),
            barber_id=self.admin_filter_barber,
            status=self.admin_filter_status,
        )

    @rx.event
    def set_admin_view_mode(self, mode: str) -> None:
        if mode in {"day", "week"}:
            self.admin_view_mode = mode

    @rx.event
    async def change_admin_period(self, direction: int) -> None:
        days = direction if self.admin_view_mode == "day" else direction * 7
        next_date = date.fromisoformat(self.admin_date) + timedelta(days=days)
        await self._load_admin_agenda(
            selected_date=next_date.isoformat(),
            barber_id=self.admin_filter_barber,
            status=self.admin_filter_status,
        )

    @rx.event
    async def update_admin_appointment_status(
        self,
        appointment_id: str,
        status: str,
    ) -> None:
        self._begin_request()
        try:
            result = await _repository_for(self).update_appointment_status(
                appointment_id,
                status,
                actor_role="admin",
            )
        except MockFailure as error:
            self._set_failure(error)
        else:
            updated_appointments = [
                {
                    **item,
                    **{
                        key: value
                        for key, value in result.data.items()
                        if value != ""
                    },
                }
                if item["id"] == appointment_id
                else item
                for item in self.admin_appointments
            ]
            if (
                self.admin_filter_status
                and result.data["status"] != self.admin_filter_status
            ):
                updated_appointments = [
                    item
                    for item in updated_appointments
                    if item["id"] != appointment_id
                ]
            self.admin_appointments = updated_appointments
            self.admin_week_days = [
                {
                    **day,
                    "count": str(
                        sum(item["date"] == day["date"] for item in updated_appointments)
                    ),
                }
                for day in self.admin_week_days
            ]
            self.success_message = result.message
        finally:
            self._end_request()

    @rx.event
    async def load_admin_dashboard(self) -> None:
        allowed, _ = await _ensure_authenticated(self, {"admin"})
        if not allowed:
            return
        self.admin_date = date.today().isoformat()
        self._begin_request()
        anchor_month = date.fromisoformat(self.admin_date).replace(day=1)
        from_date, to_date = _report_month_window(anchor_month)
        next_month = date(
            anchor_month.year + (anchor_month.month == 12),
            anchor_month.month % 12 + 1,
            1,
        )
        month_end = (next_month - timedelta(days=1)).isoformat()
        try:
            repository = _repository_for(self)
            completed_appointments = await repository.admin_appointments(
                from_date=from_date,
                to_date=to_date,
                status="completed",
            )
            cancelled_appointments = await repository.admin_appointments(
                from_date=anchor_month.isoformat(),
                to_date=month_end,
                status="cancelled",
            )
            recent_appointments = _appointments_for_date(
                completed_appointments,
                self.admin_date,
            )
            for status in ("pending", "confirmed", "cancelled"):
                recent_appointments.extend(
                    await repository.admin_appointments(
                        date=self.admin_date,
                        status=status,
                    )
                )
            recent_appointments.sort(key=lambda item: (item["date"], item["time"]))
        except MockFailure as error:
            self._set_failure(error)
        else:
            self.admin_dashboard_appointments = recent_appointments
            self.admin_revenue_cents = _completed_appointment_revenue(
                completed_appointments,
                "month",
                self.admin_date,
            )
            self.admin_completed_count = len(
                _completed_appointments(
                    completed_appointments,
                    "month",
                    self.admin_date,
                )
            )
            self.admin_cancelled_count = len(cancelled_appointments)
            self.admin_revenue_series = _monthly_revenue_series(
                anchor_month,
                completed_appointments,
            )

        try:
            clients = await _repository_for(self).clients()
        except MockFailure as error:
            self._set_failure(error)
        else:
            self.clients = clients
        finally:
            self._end_request()

    @rx.event
    async def load_admin_data(self) -> None:
        allowed, _ = await _ensure_authenticated(self, {"admin"})
        if not allowed:
            return
        self._begin_request()
        try:
            clients = await _repository_for(self).clients()
        except MockFailure as error:
            self._set_failure(error)
        else:
            self.clients = clients

        try:
            appointments = await _repository_for(self).admin_appointments()
        except MockFailure as error:
            self._set_failure(error)
        else:
            client_appointments: dict[str, list[str]] = {}
            for appointment in appointments:
                client_appointments.setdefault(appointment["client_id"], []).append(
                    appointment["date"]
                )
            self.clients = [
                {
                    **client,
                    "appointments": str(
                        len(client_appointments.get(client["id"], []))
                    ),
                    "last_appointment": (
                        date.fromisoformat(
                            max(client_appointments[client["id"]])
                        ).strftime("%d/%m/%Y")
                        if client_appointments.get(client["id"])
                        else ""
                    ),
                }
                for client in self.clients
            ]

        try:
            services = await _repository_for(self).services(active_only=False)
        except MockFailure as error:
            self._set_failure(error)
        else:
            self.services = services

        try:
            barbers = await _repository_for(self).barbers(active_only=False)
        except MockFailure as error:
            self._set_failure(error)
        else:
            self.barbers = barbers

        try:
            users = await _repository_for(self).users()
        except MockFailure as error:
            self._set_failure(error)
        else:
            self.users = users
        finally:
            self._end_request()

    @rx.event
    async def load_admin_users(self) -> None:
        allowed, _ = await _ensure_authenticated(self, {"admin"})
        if not allowed:
            return
        self._begin_request()
        try:
            self.users = await _repository_for(self).users()
        except MockFailure as error:
            self._set_failure(error)
        finally:
            self._end_request()

    async def _run_admin_mutation(
        self,
        entity: str,
        action: str,
        values: dict[str, str],
    ) -> None:
        allowed, _ = await _ensure_authenticated(self, {"admin"})
        if not allowed:
            return
        self._begin_request()
        try:
            result = await _repository_for(self).admin_mutation(entity, action, values)
        except MockFailure as error:
            self._set_failure(error)
        else:
            self.success_message = result.message
        finally:
            self._end_request()

    @rx.event
    async def perform_admin_mutation(
        self,
        entity: str,
        action: str,
        values: dict[str, str],
    ) -> None:
        await self._run_admin_mutation(entity, action, values)

    @rx.event
    async def perform_admin_record_action(
        self,
        entity: str,
        action: str,
        record_id: str,
    ) -> None:
        await self._run_admin_mutation(entity, action, {"id": record_id})

    async def _load_admin_reports(
        self,
        *,
        period: Literal["day", "month"],
        selected_date: str,
    ) -> None:
        allowed, _ = await _ensure_authenticated(self, {"admin"})
        if not allowed:
            return
        try:
            date.fromisoformat(selected_date)
        except ValueError:
            self.error_message = "Informe uma data válida para o relatório."
            self.success_message = ""
            return
        self.admin_report_period = period
        self.admin_report_date = selected_date
        self._begin_request()
        try:
            anchor_month = date.fromisoformat(selected_date).replace(day=1)
            from_date, to_date = _report_month_window(anchor_month)
            appointments = await _repository_for(self).admin_appointments(
                from_date=from_date,
                to_date=to_date,
                status="completed",
            )
            revenue_series = _monthly_revenue_series(
                anchor_month,
                appointments,
            )
            completed = _completed_appointments(
                appointments,
                period,
                selected_date,
            )
            revenue = _completed_appointment_revenue(
                appointments,
                period,
                selected_date,
            )
            services = {
                item["service_title"]: sum(
                    entry["service_title"] == item["service_title"]
                    for entry in completed
                )
                for item in completed
            }
        except MockFailure as error:
            self._set_failure(error)
        else:
            self.admin_report_revenue_cents = revenue
            self.admin_report_completed_count = len(completed)
            service_summary = [
                {
                    "title": title,
                    "count": str(count),
                    "share": f"{count / len(completed):.0%}",
                }
                for title, count in services.items()
            ]
            self.admin_report_service_summary = service_summary
            self.admin_report_revenue_series = revenue_series
            self.admin_report_service_gradient = _report_service_gradient(
                service_summary
            )
        finally:
            self._end_request()

    @rx.event
    async def load_admin_reports(self) -> None:
        await self._load_admin_reports(
            period=self.admin_report_period,
            selected_date=self.admin_report_date,
        )

    @rx.event
    async def set_admin_report_period(self, period: Literal["day", "month"]) -> None:
        await self._load_admin_reports(
            period=period,
            selected_date=self.admin_report_date,
        )

    @rx.event
    async def set_admin_report_date(self, selected_date: str) -> None:
        await self._load_admin_reports(
            period=self.admin_report_period,
            selected_date=selected_date,
        )

    @rx.event
    async def load_booking(self) -> rx.event.EventSpec | None:
        allowed, redirect = await _ensure_authenticated(self, {"client"})
        if not allowed:
            return redirect
        self._begin_request()
        self.services = []
        self.barbers = []
        self.available_times = []
        self.selected_time = ""
        self.selected_date = date.today().isoformat()
        try:
            repository = _repository_for(self)
            services = await repository.services()
            barbers = await repository.barbers()
            self.services = services
            self.barbers = barbers

            selected_service = next(
                (
                    service
                    for service in services
                    if service["id"] == self.selected_service_id
                ),
                services[0] if services else None,
            )
            selected_barber = next(
                (
                    barber
                    for barber in barbers
                    if barber["id"] == self.selected_barber_id
                ),
                barbers[0] if barbers else None,
            )
            if selected_service is not None:
                self.selected_service_id = selected_service["id"]
                if not self.selected_service_ids:
                    self.selected_service_ids = [selected_service["id"]]
                elif self.selected_service_id not in self.selected_service_ids:
                    self.selected_service_ids = [selected_service["id"]]
                self._update_selected_service_summary()
            else:
                self.selected_service_id = ""
                self.selected_service_title = ""
                self.selected_service_price = ""
                self.selected_service_duration = ""
            if selected_barber is not None:
                self.selected_barber_id = selected_barber["id"]
                self.selected_barber_name = selected_barber["name"]
            else:
                self.selected_barber_id = ""
                self.selected_barber_name = ""

            self.booking_month = self.selected_date[:7]
            self.booking_month_display = self._month_label(self.booking_month)
            self.selected_day = self.selected_date[-2:]
            self.selected_date_display = date.fromisoformat(
                self.selected_date
            ).strftime("%d/%m/%Y")
            self.calendar_days = self._calendar_for_month(self.booking_month)

            available_times = (
                await repository.availability(
                    self.selected_barber_id,
                    self.selected_service_id,
                    self.selected_date,
                    service_ids=self.selected_service_ids,
                    duration_minutes=sum(
                        service["duration_minutes"]
                        for service in services
                        if service["id"] in self.selected_service_ids
                    ),
                )
                if selected_service is not None and selected_barber is not None
                else []
            )
        except MockFailure as error:
            self.available_times = []
            self.selected_time = ""
            self._set_failure(error)
        else:
            self.available_times = available_times
            if self.selected_time not in available_times:
                self.selected_time = available_times[0] if available_times else ""
        finally:
            self._end_request()

    @rx.event
    def set_service_search(self, value: str) -> None:
        self.service_search = value

    @rx.event
    def start_booking(self, service_id: str) -> rx.event.EventSpec:
        self.selected_service_id = service_id
        self.selected_service_ids = [service_id]
        self.selected_time = ""
        self.booking_confirmed = False
        self.error_message = ""
        self.success_message = ""
        self._update_selected_service_summary()
        return rx.redirect("/agendar")

    def _update_selected_service_summary(self) -> None:
        selected = [
            service
            for service in self.services
            if service["id"] in self.selected_service_ids
        ]
        if not selected:
            self.selected_service_title = ""
            self.selected_service_price = "R$ 0,00"
            self.selected_service_duration = "0 min"
            self.selected_service_id = ""
            return
        total_cents = sum(service["price_cents"] for service in selected)
        total_minutes = sum(service["duration_minutes"] for service in selected)
        self.selected_service_ids = [service["id"] for service in selected]
        self.selected_service_id = self.selected_service_ids[0]
        self.selected_service_title = " + ".join(service["title"] for service in selected)
        self.selected_service_price = (
            f"R$ {total_cents // 100},{total_cents % 100:02d}"
        )
        self.selected_service_duration = f"{total_minutes} min"

    @rx.event
    def start_barber_booking(self, barber_id: str) -> rx.event.EventSpec:
        self.selected_barber_id = barber_id
        self.selected_time = ""
        self.booking_confirmed = False
        self.error_message = ""
        self.success_message = ""
        return rx.redirect("/agendar")

    @rx.event
    async def select_booking_service(self, service_id: str) -> None:
        if service_id in self.selected_service_ids:
            if len(self.selected_service_ids) == 1:
                self.error_message = "Selecione pelo menos um serviço."
                self.success_message = ""
                return
            self.selected_service_ids = [
                item for item in self.selected_service_ids if item != service_id
            ]
        else:
            self.selected_service_ids = [*self.selected_service_ids, service_id]
        self._update_selected_service_summary()
        await self._refresh_booking_options(service_id=self.selected_service_id)

    @rx.event
    async def select_booking_barber(self, barber_id: str) -> None:
        await self._refresh_booking_options(barber_id=barber_id)

    async def _refresh_booking_options(
        self,
        *,
        service_id: str | None = None,
        barber_id: str | None = None,
        selected_date: str | None = None,
    ) -> None:
        next_service = service_id or self.selected_service_id
        next_barber = barber_id or self.selected_barber_id
        next_date = selected_date or self.selected_date
        self._begin_request()
        try:
            selected_services = [
                service
                for service in self.services
                if service["id"] in self.selected_service_ids
            ]
            combined_duration = sum(
                service["duration_minutes"] for service in selected_services
            )
            available_times = await _repository_for(self).availability(
                next_barber,
                next_service,
                next_date,
                service_ids=self.selected_service_ids,
                duration_minutes=combined_duration,
            )
        except MockFailure as error:
            self.available_times = []
            self.selected_time = ""
            self.booking_confirmed = False
            self._set_failure(error)
        else:
            self.selected_service_id = next_service
            self.selected_barber_id = next_barber
            self.selected_date = next_date
            self.selected_day = next_date[-2:]
            self.selected_date_display = date.fromisoformat(next_date).strftime(
                "%d/%m/%Y"
            )
            selected_service = next(
                (
                    service
                    for service in self.services
                    if service["id"] == next_service
                ),
                None,
            )
            selected_barber = next(
                (
                    barber
                    for barber in self.barbers
                    if barber["id"] == next_barber
                ),
                None,
            )
            if selected_service is not None:
                self._update_selected_service_summary()
            if selected_barber is not None:
                self.selected_barber_name = selected_barber["name"]
            self.available_times = available_times
            if self.selected_time not in available_times:
                self.selected_time = available_times[0] if available_times else ""
            self.booking_confirmed = False
        finally:
            self._end_request()

    @rx.event
    async def select_booking_date(self, selected_date: str) -> None:
        await self._refresh_booking_options(selected_date=selected_date)

    @rx.event
    async def change_booking_month(self, month_delta: int) -> None:
        year, month = (int(part) for part in self.booking_month.split("-"))
        month += month_delta
        if month < 1:
            year -= 1
            month = 12
        elif month > 12:
            year += 1
            month = 1
        next_month = f"{year:04d}-{month:02d}"
        next_month_date = f"{next_month}-01"
        await self._refresh_booking_options(selected_date=next_month_date)
        if not self.error_message:
            self.booking_month = next_month
            self.booking_month_display = self._month_label(next_month)
            self.calendar_days = self._calendar_for_month(next_month)

    @rx.event
    def select_booking_time(self, selected_time: str) -> None:
        if selected_time not in self.available_times:
            self.error_message = "Selecione um horário disponível."
            self.success_message = ""
            return
        self.error_message = ""
        self.success_message = ""
        self.selected_time = selected_time
        self.booking_confirmed = False

    @rx.event
    async def confirm_booking(self) -> rx.event.EventSpec | None:
        if self.selected_time not in self.available_times:
            self.error_message = "Selecione um horário disponível antes de confirmar."
            self.success_message = ""
            return None
        self._begin_request()
        try:
            result = await _repository_for(self).create_appointment(
                client_id=self.current_user_id,
                barber_id=self.selected_barber_id,
                service_id=self.selected_service_id,
                service_ids=self.selected_service_ids,
                date=self.selected_date,
                start_time=self.selected_time,
            )
        except MockFailure as error:
            self._set_failure(error)
            if error.code == "appointment_conflict":
                self.available_times = []
                self.selected_time = ""
                self.error_message = (
                    f"{error} Selecione novamente a data para atualizar os horários."
                )
        else:
            self.booking_confirmed = True
            self.booking_confirmation_service = result.data["service_title"]
            self.booking_confirmation_date = result.data["date_display"]
            self.booking_confirmation_time = result.data["time"]
            self.success_message = result.message
            self.error_message = ""
            return rx.redirect("/")
        finally:
            self._end_request()

    @rx.event
    async def cancel_client_appointment(self, appointment_id: str) -> None:
        self._begin_request()
        try:
            result = await _repository_for(self).cancel_appointment(
                appointment_id,
                client_id=self.current_user_id,
            )
        except MockFailure as error:
            self._set_failure(error)
        else:
            appointments = [
                {
                    **item,
                    **{
                        key: value
                        for key, value in result.data.items()
                        if value != ""
                    },
                }
                if item["id"] == appointment_id
                else item
                for item in self.customer_appointments
            ]
            self._split_customer_appointments(appointments)
            self.success_message = result.message
        finally:
            self._end_request()

    @rx.event
    async def open_appointment_details(self, appointment_id: str) -> None:
        self._begin_request()
        try:
            appointment = await _repository_for(self).appointment(appointment_id)
        except MockFailure as error:
            self.selected_appointment = None
            self._set_failure(error)
        else:
            self.selected_appointment = appointment
            self.error_message = ""
            self.success_message = ""
        finally:
            self._end_request()

    @rx.event
    def close_appointment_details(self) -> None:
        self.selected_appointment = None
        self.reschedule_appointment_id = ""
        self.reschedule_date = ""
        self.reschedule_time = ""
        self.reschedule_available_times = []

    @rx.event
    async def begin_reschedule(self, appointment_id: str) -> None:
        appointment = next(
            (item for item in self.customer_appointments if item["id"] == appointment_id),
            None,
        )
        if appointment is None:
            self.error_message = "Não foi possível localizar o agendamento."
            return
        if appointment["status"] not in {"pending", "confirmed"}:
            self.error_message = "Este agendamento não pode ser remarcado."
            return
        try:
            start = datetime.fromisoformat(
                f"{appointment['date']}T{appointment['time']}"
            ).replace(tzinfo=LOCAL_TIMEZONE)
        except ValueError:
            self.error_message = "Os dados do agendamento são inválidos."
            return
        if start - datetime.now(LOCAL_TIMEZONE) < timedelta(hours=12):
            self.error_message = "A remarcação deve ser feita com pelo menos 12 horas de antecedência."
            return
        self.reschedule_appointment_id = appointment_id
        self.reschedule_date = appointment["date"]
        self.reschedule_time = ""
        await self.load_reschedule_times()

    @rx.event
    async def load_reschedule_times(self) -> None:
        appointment = next(
            (item for item in self.customer_appointments if item["id"] == self.reschedule_appointment_id),
            None,
        )
        if appointment is None or not self.reschedule_date:
            self.reschedule_available_times = []
            return
        self._begin_request()
        try:
            times = await _repository_for(self).availability(
                appointment["barber_id"],
                appointment["service_id"],
                self.reschedule_date,
            )
        except MockFailure as error:
            self.reschedule_available_times = []
            self._set_failure(error)
        else:
            self.reschedule_available_times = times
            self.reschedule_time = times[0] if times else ""
        finally:
            self._end_request()

    @rx.event
    def set_reschedule_date(self, value: str) -> None:
        self.reschedule_date = value

    @rx.event
    def select_reschedule_time(self, value: str) -> None:
        if value not in self.reschedule_available_times:
            self.error_message = "Selecione um horário disponível."
            return
        self.reschedule_time = value
        self.error_message = ""

    @rx.event
    async def confirm_reschedule(self) -> None:
        if not self.reschedule_appointment_id or not self.reschedule_time:
            self.error_message = "Selecione uma nova data e horário disponíveis."
            return
        start_time = datetime.fromisoformat(
            f"{self.reschedule_date}T{self.reschedule_time}"
        ).replace(tzinfo=LOCAL_TIMEZONE).isoformat()
        self._begin_request()
        try:
            result = await _repository_for(self).reschedule_appointment(
                self.reschedule_appointment_id,
                client_id=self.current_user_id,
                start_time=start_time,
            )
        except MockFailure as error:
            self._set_failure(error)
        else:
            appointments = [
                {
                    **item,
                    **{
                        key: value
                        for key, value in result.data.items()
                        if value != ""
                    },
                }
                if item["id"] == self.reschedule_appointment_id
                else item
                for item in self.customer_appointments
            ]
            self._split_customer_appointments(appointments)
            self.selected_appointment = result.data
            self.reschedule_appointment_id = ""
            self.reschedule_available_times = []
            self.success_message = result.message
        finally:
            self._end_request()

    @rx.event
    def set_upcoming_period_filter(
        self,
        value: Literal["all", "7", "30", "90"],
    ) -> None:
        self.upcoming_period_filter = value

    @rx.event
    def set_history_period_filter(
        self,
        value: Literal["all", "30", "90", "365"],
    ) -> None:
        self.history_period_filter = value

    @rx.event
    def set_history_category_filter(
        self,
        value: Literal["Todos", "Cortes", "Barba", "Combos"],
    ) -> None:
        self.history_category_filter = value

    @rx.event
    def set_period_filter(self, value: str) -> None:
        if value == "Todos":
            if self.appointment_filter == "history":
                self.history_period_filter = "all"
            else:
                self.upcoming_period_filter = "all"
            return
        days = value.replace(" dias", "").strip()
        if self.appointment_filter == "history":
            self.history_period_filter = days if days in {"30", "90", "365"} else "all"
        else:
            self.upcoming_period_filter = days if days in {"7", "30", "90"} else "all"

    @rx.event
    def set_appointment_filter(self, value: Literal["all", "upcoming", "history"]) -> None:
        self.appointment_filter = value

    @rx.event
    async def login(self) -> rx.event.EventSpec | None:
        email = self.login_email.strip()
        password = getattr(self, "_login_password", getattr(self, "login_password", ""))
        if "@" not in email or not password:
            self.error_message = "Informe um e-mail válido e sua senha."
            self.success_message = ""
            self._login_password = ""
            return
        if not xano_enabled():
            _clear_authenticated_session(self)
            self.error_message = (
                "A API do Xano não está configurada. Verifique "
                "XANO_API_BASE_URL e BARBERFLOW_MODE."
            )
            self.success_message = ""
            self._login_password = ""
            return rx.redirect("/login")
        self._begin_request()
        try:
            result = await _repository_for(self).authenticate(email, password)
        except MockFailure as error:
            _clear_authenticated_session(self)
            if error.status_code in {401, 403}:
                self.error_message = "E-mail ou senha inválidos."
                self.success_message = ""
            else:
                self._set_failure(error)
        else:
            self._present_user(result.data)
            self._auth_token = getattr(result, "token", "")
            self.is_authenticated = True
            self.success_message = (
                result.message
                if getattr(result, "persisted", False)
                else "Acesso de demonstração autorizado; nenhuma sessão foi salva."
            )
            routes = {
                "client": "/",
                "barber": "/barbeiro",
                "admin": "/admin",
            }
            return rx.redirect(routes[result.data["role"]])
        finally:
            self._login_password = ""
            self._end_request()

    @rx.event
    async def signup(self) -> rx.event.EventSpec | None:
        password = getattr(self, "_signup_password", getattr(self, "signup_password", ""))
        password_confirmation = getattr(
            self,
            "_signup_password_confirmation",
            getattr(self, "signup_password_confirmation", ""),
        )
        if (
            not self.signup_name.strip()
            or "@" not in self.signup_email
            or len("".join(filter(str.isdigit, self.signup_phone))) < 10
            or len(password) < 8
        ):
            self.error_message = "Revise nome, e-mail, telefone e senha."
            self.success_message = ""
            self._signup_password = ""
            self._signup_password_confirmation = ""
            return
        if password != password_confirmation:
            self.error_message = "As senhas não conferem."
            self.success_message = ""
            self._signup_password = ""
            self._signup_password_confirmation = ""
            return
        if not xano_enabled():
            _clear_authenticated_session(self)
            self.error_message = "O cadastro exige uma conta real na API do Xano."
            self.success_message = ""
            self._signup_password = ""
            self._signup_password_confirmation = ""
            return rx.redirect("/login")
        self._begin_request()
        try:
            result = await _repository_for(self).signup(
                name=self.signup_name,
                email=self.signup_email,
                phone=self.signup_phone,
                password=password,
            )
        except MockFailure as error:
            _clear_authenticated_session(self)
            self._set_failure(error)
        else:
            self._present_user(result.data)
            self._auth_token = getattr(result, "token", "")
            self.is_authenticated = True
            self.success_message = result.message
            return rx.redirect("/")
        finally:
            self._signup_password = ""
            self._signup_password_confirmation = ""
            self._end_request()

    @rx.event
    async def request_password_reset(self) -> None:
        email = self.recovery_email.strip()
        if "@" not in email:
            self.error_message = "Informe um e-mail válido."
            self.success_message = ""
            return
        self._begin_request()
        try:
            result = await _repository_for(self).password_reset(email)
        except MockFailure as error:
            self._set_failure(error)
        else:
            self.success_message = (
                result.message
                if getattr(result, "persisted", False)
                else f"Solicitação simulada para {result.data['email']}; "
                "nenhum link foi enviado."
            )
        finally:
            self._end_request()

    @rx.event
    async def save_profile(self) -> None:
        if not self.profile_name.strip() or "@" not in self.profile_email:
            self.error_message = "Informe um nome e um e-mail válidos."
            self.success_message = ""
            return
        if len("".join(filter(str.isdigit, self.profile_phone))) < 10:
            self.error_message = "Informe um telefone válido."
            self.success_message = ""
            return
        if self.profile_avatar_url:
            parsed = urlparse(self.profile_avatar_url)
            if parsed.scheme != "https" or not parsed.netloc or parsed.username or parsed.password:
                self.error_message = "Informe uma URL HTTPS válida para a foto."
                self.success_message = ""
                return
        self._begin_request()
        try:
            result = await _repository_for(self).update_profile(
                self.current_user_id,
                name=self.profile_name,
                email=self.profile_email,
                phone=self.profile_phone,
                avatar_url=self.profile_avatar_url,
            )
        except MockFailure as error:
            self._set_failure(error)
        else:
            self._present_user(result.data)
            self.success_message = result.message
        finally:
            self._end_request()

    @rx.event
    async def change_account_password(self) -> None:
        if len(self.security_new_password) < 8:
            self.error_message = "A nova senha deve conter pelo menos 8 caracteres."
            return
        self._begin_request()
        try:
            result = await _repository_for(self).change_password(
                current_password=self.security_current_password,
                new_password=self.security_new_password,
                totp_code=self.security_totp_code,
            )
        except MockFailure as error:
            self._set_failure(error)
        else:
            self.security_current_password = ""
            self.security_new_password = ""
            self.security_totp_code = ""
            self.success_message = result.message
        finally:
            self._end_request()

    @rx.event
    async def start_totp_setup(self) -> None:
        self._begin_request()
        try:
            result = await _repository_for(self).totp_setup()
        except MockFailure as error:
            self._set_failure(error)
        else:
            self.totp_setup_secret = result.data["secret"]
            self.success_message = "Configure o TOTP e confirme o código atual."
        finally:
            self._end_request()

    @rx.event
    async def enable_totp(self) -> None:
        if len(self.security_totp_code) != 6:
            self.error_message = "Informe o código TOTP de 6 dígitos."
            return
        self._begin_request()
        try:
            result = await _repository_for(self).totp_enable(code=self.security_totp_code)
        except MockFailure as error:
            self._set_failure(error)
        else:
            self.totp_enabled = True
            self.totp_setup_secret = ""
            self.security_totp_code = ""
            self.success_message = result.message
        finally:
            self._end_request()

    @rx.event
    async def disable_totp(self) -> None:
        self._begin_request()
        try:
            result = await _repository_for(self).totp_disable(
                current_password=self.security_current_password,
                code=self.security_totp_code,
            )
        except MockFailure as error:
            self._set_failure(error)
        else:
            self.totp_enabled = False
            self.security_current_password = ""
            self.security_totp_code = ""
            self.success_message = result.message
        finally:
            self._end_request()

    @rx.event
    async def revoke_all_sessions(self) -> rx.event.EventSpec | None:
        self._begin_request()
        try:
            result = await _repository_for(self).revoke_all_sessions()
        except MockFailure as error:
            self._set_failure(error)
            return None
        else:
            self.success_message = result.message
            _clear_authenticated_session(self)
            return rx.redirect("/login")
        finally:
            self._end_request()
