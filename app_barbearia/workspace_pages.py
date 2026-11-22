import reflex as rx

from app_barbearia.mock_repository import (
    AppointmentRecord,
    BarberAppointmentRecord,
    BarberRecord,
    ClientRecord,
    ServiceRecord,
    UserRecord,
)
from app_barbearia.state import AppState
from app_barbearia.ui import (
    ACCENT,
    DANGER,
    FOREGROUND,
    INFO,
    MUTED,
    SUCCESS,
    SURFACE,
    SURFACE_RAISED,
    SURFACE_BORDER,
    WARNING,
    role_layout,
)


BARBER_LINKS = [
    ("Minha agenda", "/barbeiro"),
    ("Atendimentos", "/barbeiro/atendimentos"),
    ("Perfil", "/barbeiro/perfil"),
    ("Sair", "/login"),
]

ADMIN_LINKS = [
    ("Dashboard", "/admin"),
    ("Agenda", "/admin/agenda"),
    ("Clientes", "/admin/clientes"),
    ("Serviços", "/admin/servicos"),
    ("Equipe", "/admin/equipe"),
    ("Relatórios", "/admin/relatorios"),
    ("Usuários", "/admin/usuarios"),
    ("Configurações", "/admin/configuracoes"),
    ("Sair", "/login"),
]


def _panel(
    title: str,
    content: rx.Component,
    min_height: str | None = None,
) -> rx.Component:
    return rx.box(
        rx.heading(title, as_="h2", size="4", color=ACCENT, margin_bottom="16px"),
        content,
        background_color="#111111ee",
        border="1px solid #3a3327",
        border_radius="16px",
        padding="22px",
        width="100%",
        min_height=min_height,
        box_shadow="0 18px 42px #00000066, inset 0 1px 0 #ffffff08",
    )


def _badge(status: str | rx.Var[str]) -> rx.Component:
    colors = {
        "Confirmado": (SUCCESS, "#173823"),
        "Pendente": (WARNING, "#3b2c14"),
        "Em Atendimento": (INFO, "#172b40"),
        "Aguardando": (INFO, "#172b40"),
        "Concluído": (FOREGROUND, "#292929"),
        "Cancelado": (DANGER, "#3b1e1d"),
        "Ativo": (SUCCESS, "#173823"),
    }
    if isinstance(status, str):
        color, background = colors.get(status, (MUTED, "#252521"))
    else:
        color = rx.cond(
            status == "Confirmado",
            SUCCESS,
            rx.cond(
                status == "Pendente",
                WARNING,
                rx.cond(status == "Cancelado", DANGER, FOREGROUND),
            ),
        )
        background = rx.cond(
            status == "Confirmado",
            "#173823",
            rx.cond(
                status == "Pendente",
                "#3b2c14",
                rx.cond(status == "Cancelado", "#3b1e1d", "#292929"),
            ),
        )
    return rx.text(
        status,
        color=color,
        background_color=background,
        border_radius="999px",
        padding="4px 9px",
        font_size="0.72rem",
        font_weight="700",
        white_space="nowrap",
    )


def _action(
    label: str | rx.Var[str],
    primary: bool = False,
    aria_label: str | rx.Var[str] | None = None,
    on_click: rx.event.EventSpec | None = None,
) -> rx.Component:
    return rx.button(
        label,
        type="button",
        aria_label=aria_label or label,
        on_click=on_click,
        color="#17140f" if primary else FOREGROUND,
        background_color=ACCENT if primary else "transparent",
        border=f"1px solid {ACCENT if not primary else ACCENT}",
        border_radius="9px",
        padding="9px 12px",
        font_size="0.75rem",
        font_weight="700" if primary else "500",
        cursor="pointer",
        min_height="40px",
        _hover={"background_color": ACCENT, "color": "#17140f"},
        _focus={"outline": f"2px solid {FOREGROUND}", "outline_offset": "2px"},
    )


def _metric(
    label: str,
    value: str | int | rx.Var[str] | rx.Var[int],
    icon: str,
    detail: str = "",
) -> rx.Component:
    return rx.box(
        rx.icon(tag=icon, size=21, color=ACCENT, aria_hidden=True),
        rx.text(
            value,
            color=FOREGROUND,
            font_size="1.5rem",
            font_weight="700",
            margin_top="8px",
        ),
        rx.text(label, color=MUTED, font_size="0.8rem"),
        rx.cond(
            bool(detail),
            rx.text(detail, color=SUCCESS, font_size="0.72rem", margin_top="5px"),
            rx.fragment(),
        ),
        background_color=SURFACE_RAISED,
        border=f"1px solid {SURFACE_BORDER}",
        border_radius="12px",
        padding="16px",
        flex="1 1 170px",
        min_width="145px",
    )


def _barber_empty_state(
    title: str,
    description: str,
    icon: str,
) -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.icon(tag=icon, size=34, color=ACCENT, aria_hidden=True),
            rx.heading(
                title,
                as_="h3",
                size="3",
                color=FOREGROUND,
                text_align="center",
            ),
            rx.text(
                description,
                color=MUTED,
                font_size="0.8rem",
                text_align="center",
                max_width="360px",
            ),
            align="center",
            spacing="2",
        ),
        min_height="220px",
        width="100%",
        role="status",
    )


def _barber_row(
    item: AppointmentRecord | BarberAppointmentRecord,
) -> rx.Component:
    return rx.flex(
        rx.text(
            item["time"],
            color=FOREGROUND,
            font_size="0.79rem",
            font_weight="700",
            width="48px",
        ),
        rx.box(
            rx.icon(tag="user_round", size=16, color=FOREGROUND, aria_hidden=True),
            background_color=SURFACE_RAISED,
            border_radius="50%",
            width="28px",
            height="28px",
            display="flex",
            align_items="center",
            justify_content="center",
            flex_shrink="0",
        ),
        rx.vstack(
            rx.text(
                item["service_title"],
                color=FOREGROUND,
                font_size="0.71rem",
                font_weight="600",
            ),
            rx.text(item["client_name"], color=MUTED, font_size="0.63rem"),
            align="start",
            spacing="0",
            flex="1",
            min_width="90px",
        ),
        _badge(item["status_label"]),
        align="center",
        flex_wrap="wrap",
        gap="8px",
        width="100%",
        padding="14px 0",
        border_bottom=f"1px solid {SURFACE_BORDER}",
    )


def _barber_action_row(
    item: AppointmentRecord | BarberAppointmentRecord,
) -> rx.Component:
    return rx.flex(
        rx.box(
            rx.icon(
                tag="user_round",
                size=22,
                color=FOREGROUND,
                aria_hidden=True,
            ),
            background_color=SURFACE_RAISED,
            border_radius="50%",
            width="38px",
            height="38px",
            display="flex",
            align_items="center",
            justify_content="center",
            flex_shrink="0",
        ),
        rx.vstack(
            rx.text(
                item["client_name"],
                color=FOREGROUND,
                font_size="0.73rem",
                font_weight="600",
            ),
            rx.text(
                item["service_title"] + " · " + item["time"],
                color=MUTED,
                font_size="0.64rem",
            ),
            align="start",
            spacing="1",
            flex="1",
        ),
        _badge(item["status_label"]),
        rx.box(
            _appointment_actions(item, actor_role="barber"),
            width="132px",
            margin_left="auto",
            flex_shrink="0",
        ),
        align="center",
        flex_wrap="wrap",
        gap="9px",
        width="100%",
        padding="12px 0",
        border_bottom=f"1px solid {SURFACE_BORDER}",
    )


def _table_row(
    values: tuple[str | rx.Var[str] | rx.Component, ...],
    header: bool = False,
) -> rx.Component:
    return rx.flex(
        *[
            value
            if isinstance(value, rx.Component)
            else rx.text(
                value,
                color=ACCENT if header else FOREGROUND,
                font_size="0.72rem" if header else "0.78rem",
                font_weight="700" if header else "400",
                flex="1 1 85px",
                min_width="75px",
            )
            for value in values
        ],
        align="center",
        flex_wrap="wrap",
        gap="8px",
        width="100%",
        padding="10px 0",
        border_bottom=f"1px solid {SURFACE_BORDER}",
    )


def _appointment_actions(
    item: AppointmentRecord | BarberAppointmentRecord,
    *,
    actor_role: str,
) -> rx.Component:
    if actor_role == "barber":
        confirm = AppState.update_barber_appointment_status(
            item["id"],
            "confirmed",
        )
        complete = AppState.update_barber_appointment_status(
            item["id"],
            "completed",
        )
        cancel = AppState.update_barber_appointment_status(
            item["id"],
            "cancelled",
        )
    else:
        confirm = AppState.update_admin_appointment_status(
            item["id"],
            "confirmed",
        )
        complete = AppState.update_admin_appointment_status(
            item["id"],
            "completed",
        )
        cancel = AppState.update_admin_appointment_status(
            item["id"],
            "cancelled",
        )
    return rx.cond(
        item["status"] == "pending",
        rx.vstack(
            _action("Confirmar", primary=True, on_click=confirm),
            _action("Cancelar", on_click=cancel),
            align="stretch",
            spacing="1",
            width="100%",
        ),
        rx.cond(
            item["status"] == "confirmed",
            rx.vstack(
                _action("Concluir", primary=True, on_click=complete),
                _action("Cancelar", on_click=cancel),
                align="stretch",
                spacing="1",
                width="100%",
            ),
            rx.fragment(),
        ),
    )


def _admin_week_appointment(item: AppointmentRecord) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.text(item["time"], color=ACCENT, font_size="0.62rem", font_weight="700"),
            rx.text(
                item["client_name"],
                color=FOREGROUND,
                font_size="0.61rem",
                font_weight="600",
            ),
            rx.text(
                item["service_title"] + " · " + item["barber_name"],
                color=MUTED,
                font_size="0.56rem",
            ),
            _badge(item["status_label"]),
            _appointment_actions(item, actor_role="admin"),
            align="start",
            spacing="2",
            width="100%",
        ),
        background_color="#302718",
        border=f"1px solid {ACCENT}",
        border_radius="5px",
        padding="6px",
        margin="2px 0",
    )


def _admin_week_column(day: dict[str, str]) -> rx.Component:
    return rx.box(
        rx.text(
            day["label"],
            color=FOREGROUND,
            font_size="0.62rem",
            text_align="center",
            background_color=SURFACE_RAISED,
            padding="8px 2px",
            border_bottom=f"1px solid {SURFACE_BORDER}",
            width="100%",
        ),
        rx.cond(
            day["count"] == "0",
            rx.text("—", color=MUTED, font_size="0.6rem", text_align="center"),
            rx.foreach(
                AppState.admin_appointments,
                lambda item: rx.cond(
                    item["date"] == day["date"],
                    _admin_week_appointment(item),
                    rx.fragment(),
                ),
            ),
        ),
        min_height="105px",
        border=f"1px solid {SURFACE_BORDER}",
        border_radius="5px",
        padding="3px",
    )


def _admin_day_appointment(item: AppointmentRecord) -> rx.Component:
    return rx.box(
        rx.flex(
            rx.vstack(
                rx.text(
                    item["time"],
                    color=ACCENT,
                    font_size="0.82rem",
                    font_weight="700",
                ),
                rx.text(item["client_name"], color=FOREGROUND, font_weight="600"),
                rx.text(
                    item["service_title"] + " · " + item["barber_name"],
                    color=MUTED,
                    font_size="0.76rem",
                ),
                align="start",
                spacing="1",
                flex="1",
            ),
            _badge(item["status_label"]),
            align="center",
            justify="between",
            flex_wrap="wrap",
            gap="10px",
            width="100%",
        ),
        _appointment_actions(item, actor_role="admin"),
        background_color="#302718",
        border=f"1px solid {ACCENT}",
        border_radius="7px",
        padding="10px",
        width="100%",
    )


def _admin_agenda_view_button(label: str, mode: str) -> rx.Component:
    selected = AppState.admin_view_mode == mode
    return rx.button(
        label,
        type="button",
        aria_label=f"Visualização {label.lower()}",
        aria_pressed=selected,
        on_click=AppState.set_admin_view_mode(mode),
        color=rx.cond(selected, "#17140f", FOREGROUND),
        background_color=rx.cond(selected, ACCENT, "transparent"),
        border=f"1px solid {ACCENT}",
        border_radius="6px",
        padding="7px 10px",
        font_size="0.68rem",
        font_weight="700",
        cursor="pointer",
        _focus={"outline": f"2px solid {FOREGROUND}", "outline_offset": "2px"},
    )


def _admin_recent_appointment(item: AppointmentRecord) -> rx.Component:
    return rx.flex(
        rx.box(
            rx.icon(
                tag="user_round",
                size=15,
                color=FOREGROUND,
                aria_hidden=True,
            ),
            background_color="#42474d",
            border_radius="50%",
            width="28px",
            height="28px",
            display="flex",
            align_items="center",
            justify_content="center",
        ),
        rx.vstack(
            rx.text(item["client_name"], color=FOREGROUND, font_size="0.67rem"),
            rx.text(
                item["time"] + " · " + item["service_title"],
                color=MUTED,
                font_size="0.6rem",
            ),
            align="start",
            spacing="0",
            flex="1",
        ),
        _badge(item["status_label"]),
        align="center",
        gap="8px",
        width="100%",
        padding="8px 0",
        border_bottom=f"1px solid {SURFACE_BORDER}",
    )


def _admin_client_row(item: ClientRecord) -> rx.Component:
    return _table_row(
        (
            item["name"],
            item["phone"],
            item["appointments"],
            item["last_appointment"],
            rx.flex(
                _action(
                    "Editar",
                    aria_label=f"Editar {item['name']}",
                    on_click=AppState.open_admin_client_edit_form(item["id"]),
                ),
                _action(
                    "Desativar",
                    aria_label=f"Desativar {item['name']}",
                    on_click=AppState.perform_admin_record_action(
                        "client",
                        "deactivate",
                        item["id"],
                    ),
                ),
                gap="4px",
            ),
        )
    )


def _admin_service_row(item: ServiceRecord) -> rx.Component:
    return _table_row(
        (
            item["title"],
            item["description"],
            item["price_display"],
            item["duration_display"],
            rx.cond(item["active"], "Ativo", "Inativo"),
            rx.flex(
                _action(
                    "Editar",
                    aria_label=f"Editar {item['title']}",
                    on_click=AppState.open_admin_service_edit_form(item["id"]),
                ),
                _action(
                    "Desativar",
                    aria_label=f"Desativar {item['title']}",
                    on_click=AppState.perform_admin_record_action(
                        "service",
                        "deactivate",
                        item["id"],
                    ),
                ),
                gap="4px",
            ),
        )
    )


def _admin_barber_row(item: BarberRecord) -> rx.Component:
    return _table_row(
        (
            item["name"],
            item["specialty"],
            rx.cond(item["active"], "Ativo", "Inativo"),
            rx.flex(
                _action(
                    "Editar",
                    aria_label=f"Editar {item['name']}",
                    on_click=AppState.open_admin_barber_edit_form(item["id"]),
                ),
                _action(
                    "Desativar",
                    aria_label=f"Desativar {item['name']}",
                    on_click=AppState.perform_admin_record_action(
                        "barber",
                        "deactivate",
                        item["id"],
                    ),
                ),
                gap="4px",
            ),
        )
    )


def _admin_user_row(item: UserRecord) -> rx.Component:
    role = rx.cond(
        item["role"] == "client",
        "Cliente",
        rx.cond(item["role"] == "barber", "Barbeiro", "Administrador"),
    )
    return _table_row(
        (
            item["name"],
            item["email"],
            role,
        )
    )


def _revenue_bar(item: dict[str, str]) -> rx.Component:
    return rx.vstack(
        rx.box(
            height=item["height"],
            width="100%",
            background_color=ACCENT,
            border_radius="5px 5px 0 0",
        ),
        rx.text(item["month"], color=MUTED, font_size="0.6rem"),
        align="center",
        justify="end",
        spacing="2",
        height="150px",
        flex="1",
    )


def _report_service_row(item: dict[str, str]) -> rx.Component:
    return rx.flex(
        rx.text(item["title"], color=FOREGROUND, font_size="0.66rem"),
        rx.text(
            item["count"] + " · " + item["share"],
            color=MUTED,
            font_size="0.78rem",
        ),
        justify="between",
        width="100%",
    )


def _admin_page(
    title: str,
    description: str,
    active_path: str,
    content: rx.Component,
) -> rx.Component:
    return role_layout(
        role_title="Administração",
        title=title,
        description=description,
        active_path=active_path,
        links=ADMIN_LINKS,
        content=content,
    )


def _barber_page(
    title: str,
    description: str,
    active_path: str,
    content: rx.Component,
) -> rx.Component:
    return role_layout(
        role_title="Painel do Barbeiro",
        title=title,
        description=description,
        active_path=active_path,
        links=BARBER_LINKS,
        content=content,
    )


def barber_workspace() -> rx.Component:
    return _barber_page(
        title="Painel do Barbeiro",
        description="Sua agenda e atendimentos de hoje",
        active_path="/barbeiro",
        content=rx.vstack(
            rx.flex(
                rx.heading(
                    "Sua Agenda de Hoje",
                    as_="h2",
                    size="3",
                    color=ACCENT,
                ),
                rx.flex(
                    rx.icon(
                        tag="calendar_days",
                        size=16,
                        color=ACCENT,
                        aria_hidden=True,
                    ),
                    rx.text(
                        AppState.barber_date_display,
                        color=FOREGROUND,
                        font_size="0.7rem",
                    ),
                    rx.el.input(
                        type="date",
                        lang="pt-BR",
                        value=AppState.barber_date,
                        on_change=AppState.set_barber_date,
                        aria_label="Selecionar data da agenda",
                        background_color=SURFACE,
                        color=FOREGROUND,
                        border=f"1px solid {SURFACE_BORDER}",
                        border_radius="7px",
                        padding="6px 8px",
                    ),
                    _action(
                        "‹",
                        aria_label="Dia anterior",
                        on_click=AppState.change_barber_date(-1),
                    ),
                    _action(
                        "›",
                        aria_label="Dia seguinte",
                        on_click=AppState.change_barber_date(1),
                    ),
                    align="center",
                    gap="8px",
                    background_color=SURFACE,
                    border=f"1px solid {SURFACE_BORDER}",
                    border_radius="7px",
                    padding="8px 10px",
                ),
                align="center",
                justify="between",
                flex_wrap="wrap",
                gap="10px",
                width="100%",
            ),
            rx.flex(
                rx.box(
                    _panel(
                        "Agenda do Dia",
                        rx.vstack(
                            rx.cond(
                                AppState.barber_appointments.length() == 0,
                                rx.cond(
                                    AppState.is_loading,
                                    rx.center(
                                        rx.text("Carregando agenda...", color=MUTED),
                                        min_height="220px",
                                        width="100%",
                                    ),
                                    _barber_empty_state(
                                        "Seu dia está livre",
                                        "Nenhum atendimento agendado para esta data.",
                                        "calendar_days",
                                    ),
                                ),
                                rx.foreach(AppState.barber_appointments, _barber_row),
                            ),
                            align="stretch",
                            spacing="0",
                        ),
                        min_height="340px",
                    ),
                    flex="2 1 540px",
                    min_width="280px",
                ),
                rx.vstack(
                    rx.flex(
                        _metric(
                            "Atendimentos",
                            AppState.barber_appointment_count,
                            "scissors",
                        ),
                        _metric(
                            "Tempo Total",
                            AppState.barber_duration_display,
                            "clock_3",
                        ),
                        _metric(
                            "Faturamento Concluído",
                            AppState.barber_revenue_display,
                            "star",
                        ),
                        flex_wrap="wrap",
                        gap="8px",
                        width="100%",
                    ),
                    _panel(
                        "Próximo Atendimento",
                        rx.cond(
                            AppState.barber_next_time == "",
                            rx.text(
                                "Nenhum próximo atendimento nesta data.",
                                color=MUTED,
                            ),
                            rx.flex(
                                rx.box(
                                    rx.icon(
                                        tag="user_round",
                                        size=28,
                                        color=FOREGROUND,
                                        aria_hidden=True,
                                    ),
                                    background_image=(
                                        "linear-gradient(145deg, #30210a, #181614)"
                                    ),
                                    border_radius="9px",
                                    width="68px",
                                    height="74px",
                                    display="flex",
                                    align_items="center",
                                    justify_content="center",
                                    flex_shrink="0",
                                ),
                                rx.vstack(
                                    rx.text(
                                        AppState.barber_next_client_name,
                                        color=FOREGROUND,
                                        font_size="0.85rem",
                                        font_weight="600",
                                    ),
                                    rx.text(
                                        AppState.barber_next_service_title,
                                        color=MUTED,
                                        font_size="0.78rem",
                                    ),
                                    rx.flex(
                                        rx.icon(tag="clock_3", size=13, color=ACCENT),
                                        rx.text(
                                            AppState.barber_next_time,
                                            color=FOREGROUND,
                                            font_size="0.78rem",
                                        ),
                                        align="center",
                                        gap="5px",
                                        margin_top="5px",
                                    ),
                                    align="start",
                                    spacing="1",
                                    flex="1",
                                ),
                                align="center",
                                gap="10px",
                                width="100%",
                            ),
                        ),
                    ),
                    flex="1 1 300px",
                    spacing="3",
                ),
                align="start",
                flex_wrap="wrap",
                gap="12px",
                width="100%",
            ),
            align="stretch",
            spacing="4",
            width="100%",
        ),
    )


def barber_appointments_page() -> rx.Component:
    return _barber_page(
        title="Atendimentos",
        description="Atualize os estados permitidos para cada atendimento.",
        active_path="/barbeiro/atendimentos",
        content=rx.flex(
            rx.box(
                _panel(
                    "Atendimentos do Dia",
                    rx.vstack(
                        rx.cond(
                            AppState.barber_appointments.length() == 0,
                            rx.cond(
                                AppState.is_loading,
                                rx.center(
                                    rx.text("Carregando atendimentos...", color=MUTED),
                                    min_height="220px",
                                    width="100%",
                                ),
                                _barber_empty_state(
                                    "Agenda tranquila",
                                    "Nenhum atendimento previsto para esta data.",
                                    "scissors",
                                ),
                            ),
                            rx.foreach(
                                AppState.barber_appointments,
                                _barber_action_row,
                            ),
                        ),
                        align="stretch",
                        spacing="0",
                    ),
                    min_height="340px",
                ),
                flex="2 1 560px",
                min_width="280px",
            ),
            rx.box(
                _panel(
                    "Status Disponíveis",
                    rx.vstack(
                    *[
                        rx.flex(
                            rx.icon(tag=icon, size=18, color=color),
                            rx.text(label, color=FOREGROUND, font_size="0.7rem"),
                            align="center",
                            gap="10px",
                            width="100%",
                            background_color=SURFACE_RAISED,
                            border=f"1px solid {SURFACE_BORDER}",
                            border_radius="7px",
                            padding="10px",
                        )
                        for label, icon, color in (
                            ("Pendente", "clock_3", WARNING),
                            ("Confirmado", "circle_check", SUCCESS),
                            ("Concluído", "circle_check", FOREGROUND),
                            ("Cancelado", "circle_x", DANGER),
                        )
                    ],
                        align="stretch",
                        spacing="2",
                    ),
                ),
                flex="1 1 240px",
                min_width="210px",
            ),
            align="start",
            flex_wrap="wrap",
            gap="12px",
            width="100%",
        ),
    )


def barber_profile_page() -> rx.Component:
    return _barber_page(
        title="Perfil",
        description="Informações do profissional",
        active_path="/barbeiro/perfil",
        content=_panel(
            "Perfil profissional",
            rx.grid(
                rx.flex(
                    rx.box(
                        rx.icon(
                            tag="user_round",
                            size=34,
                            color=ACCENT,
                            aria_hidden=True,
                        ),
                        background_image=(
                            "radial-gradient(circle at 30% 25%, #f2a90035, transparent 70%), "
                            "linear-gradient(145deg, #30210a, #181614)"
                        ),
                        border="1px solid #6a4b0d",
                        border_radius="50%",
                        width="84px",
                        height="84px",
                        display="flex",
                        align_items="center",
                        justify_content="center",
                        flex_shrink="0",
                    ),
                    rx.vstack(
                        rx.text(
                            AppState.user_name,
                            color=FOREGROUND,
                            font_size="1.1rem",
                            font_weight="700",
                        ),
                        rx.text(
                            rx.cond(
                                AppState.user_role == "barber",
                                "Barbeiro",
                                "Função não informada",
                            ),
                            color=MUTED,
                            font_size="0.8rem",
                        ),
                        rx.text(
                            "Especialidade não informada no perfil atual",
                            color=MUTED,
                            font_size="0.72rem",
                        ),
                        align="start",
                        spacing="2",
                    ),
                    align="center",
                    gap="18px",
                    width="100%",
                    background_color=SURFACE_RAISED,
                    border=f"1px solid {SURFACE_BORDER}",
                    border_radius="14px",
                    padding="20px",
                ),
                rx.vstack(
                    rx.text(
                        "Status da sessão",
                        color=MUTED,
                        font_size="0.72rem",
                        font_weight="600",
                    ),
                    rx.text(
                        rx.cond(
                            AppState.is_authenticated,
                            "Ativo",
                            "Sessão não autenticada",
                        ),
                        color=rx.cond(AppState.is_authenticated, SUCCESS, MUTED),
                        background_color=rx.cond(
                            AppState.is_authenticated,
                            "#173823",
                            "#252521",
                        ),
                        border=rx.cond(
                            AppState.is_authenticated,
                            "1px solid #2f7042",
                            f"1px solid {SURFACE_BORDER}",
                        ),
                        border_radius="999px",
                        padding="6px 12px",
                        font_size="0.75rem",
                        font_weight="700",
                        white_space="nowrap",
                    ),
                    rx.text(
                        "Disponibilidade da unidade",
                        color=ACCENT,
                        font_size="0.72rem",
                        font_weight="700",
                        margin_top="10px",
                    ),
                    rx.text(
                        "Segunda a sábado · 09:00 às 18:00",
                        color=FOREGROUND,
                        font_size="0.8rem",
                    ),
                    rx.text(
                        "America/Sao_Paulo",
                        color=MUTED,
                        font_size="0.72rem",
                    ),
                    align="start",
                    spacing="2",
                    background_color=SURFACE_RAISED,
                    border=f"1px solid {SURFACE_BORDER}",
                    border_radius="14px",
                    padding="20px",
                    width="100%",
                ),
                grid_template_columns="repeat(auto-fit, minmax(240px, 1fr))",
                spacing="4",
                width="100%",
            ),
            min_height="260px",
        ),
    )


def _revenue_chart() -> rx.Component:
    return rx.box(
        rx.flex(
            rx.heading("Faturamento Mensal", as_="h2", size="3", color=ACCENT),
            rx.text(
                AppState.admin_revenue_display,
                color=FOREGROUND,
                font_weight="700",
                font_size="0.8rem",
            ),
            justify="between",
            align="center",
        ),
        rx.flex(
            rx.cond(
                AppState.admin_revenue_series.length() == 0,
                rx.text("Sem dados de faturamento no período.", color=MUTED),
                rx.foreach(AppState.admin_revenue_series, _revenue_bar),
            ),
            align="end",
            gap="10px",
            width="100%",
            height="170px",
        ),
        background_color=SURFACE,
        border=f"1px solid {SURFACE_BORDER}",
        border_radius="14px",
        padding="20px",
        box_shadow="0 12px 32px #00000033",
        flex="2 1 350px",
    )


def admin_console() -> rx.Component:
    return _admin_page(
        title="Dashboard",
        description="Visão geral da sua barbearia",
        active_path="/admin",
        content=rx.vstack(
            rx.text(
                "Período: " + AppState.admin_date_display,
                color=MUTED,
                font_size="0.66rem",
            ),
            rx.flex(
                _metric(
                    "Agendamentos",
                    AppState.admin_appointment_count,
                    "calendar_days",
                ),
                _metric(
                    "Faturamento do Mês",
                    AppState.admin_revenue_display,
                    "circle_dollar_sign",
                ),
                _metric("Clientes", AppState.admin_client_count, "users_round"),
                _metric(
                    "Comparecimento",
                    AppState.admin_attendance_display,
                    "circle_check",
                ),
                flex_wrap="wrap",
                gap="10px",
                width="100%",
            ),
            rx.flex(
                _revenue_chart(),
                rx.box(
                    _panel(
                        "Agendamentos Recentes",
                        rx.vstack(
                            rx.cond(
                                AppState.admin_dashboard_appointments.length() == 0,
                                rx.cond(
                                    AppState.is_loading,
                                    rx.text("Carregando agendamentos...", color=MUTED),
                                    rx.text(
                                        "Nenhum agendamento neste período.",
                                        color=MUTED,
                                    ),
                                ),
                                rx.foreach(
                                    AppState.admin_dashboard_appointments,
                                    _admin_recent_appointment,
                                ),
                            ),
                            align="stretch",
                            spacing="0",
                        ),
                    ),
                    flex="1 1 270px",
                    min_width="240px",
                ),
                align="stretch",
                flex_wrap="wrap",
                gap="12px",
                width="100%",
            ),
        ),
    )


def admin_agenda_page() -> rx.Component:
    return _admin_page(
        title="Agenda",
        description="Gerencie os agendamentos da barbearia",
        active_path="/admin/agenda",
        content=rx.vstack(
            rx.flex(
                rx.el.select(
                    rx.el.option("Todos os barbeiros", value=""),
                    rx.foreach(
                        AppState.barbers,
                        lambda barber: rx.el.option(
                            barber["name"],
                            value=barber["id"],
                        ),
                    ),
                    value=AppState.admin_filter_barber,
                    on_change=AppState.set_admin_barber_filter,
                    aria_label="Filtrar por barbeiro",
                    background_color=SURFACE,
                    color=FOREGROUND,
                    border=f"1px solid {SURFACE_BORDER}",
                    border_radius="7px",
                    padding="8px 10px",
                ),
                rx.el.select(
                    rx.el.option("Todos os status", value=""),
                    rx.el.option("Pendente", value="pending"),
                    rx.el.option("Confirmado", value="confirmed"),
                    rx.el.option("Cancelado", value="cancelled"),
                    rx.el.option("Concluído", value="completed"),
                    value=AppState.admin_filter_status,
                    on_change=AppState.set_admin_status_filter,
                    aria_label="Filtrar por status",
                    background_color=SURFACE,
                    color=FOREGROUND,
                    border=f"1px solid {SURFACE_BORDER}",
                    border_radius="7px",
                    padding="8px 10px",
                ),
                rx.spacer(),
                rx.flex(
                    rx.icon(
                        tag="calendar_days",
                        size=15,
                        color=ACCENT,
                        aria_hidden=True,
                    ),
                    rx.el.input(
                        type="date",
                        lang="pt-BR",
                        value=AppState.admin_date,
                        on_change=AppState.set_admin_date,
                        aria_label="Data da agenda administrativa",
                        background_color=SURFACE,
                        color=FOREGROUND,
                        border=f"1px solid {SURFACE_BORDER}",
                        border_radius="7px",
                        padding="6px 8px",
                    ),
                    _action(
                        "‹",
                        aria_label="Período anterior",
                        on_click=AppState.change_admin_period(-1),
                    ),
                    _action(
                        "›",
                        aria_label="Próximo período",
                        on_click=AppState.change_admin_period(1),
                    ),
                    _admin_agenda_view_button("Dia", "day"),
                    _admin_agenda_view_button("Semana", "week"),
                    align="center",
                    gap="7px",
                ),
                align="center",
                flex_wrap="wrap",
                gap="8px",
                width="100%",
            ),
            rx.cond(
                AppState.admin_view_mode == "day",
                _panel(
                    "Agenda Diária",
                    rx.vstack(
                        rx.text(
                            AppState.admin_date_display,
                            color=ACCENT,
                            font_size="0.82rem",
                            font_weight="600",
                        ),
                        rx.cond(
                            AppState.admin_day_appointments.length() == 0,
                            rx.cond(
                                AppState.is_loading,
                                rx.text("Carregando agenda...", color=MUTED),
                                rx.text(
                                    "Nenhum agendamento corresponde aos filtros para esta data.",
                                    color=MUTED,
                                ),
                            ),
                            rx.foreach(
                                AppState.admin_day_appointments,
                                _admin_day_appointment,
                            ),
                        ),
                        align="stretch",
                        spacing="3",
                    ),
                ),
                _panel(
                    "Agenda Semanal",
                    rx.vstack(
                        rx.cond(
                            AppState.admin_appointments.length() == 0,
                            rx.cond(
                                AppState.is_loading,
                                rx.text("Carregando agenda...", color=MUTED),
                                rx.text(
                                    "Nenhum agendamento corresponde aos filtros.",
                                    color=MUTED,
                                ),
                            ),
                            rx.fragment(),
                        ),
                        rx.grid(
                            rx.foreach(AppState.admin_week_days, _admin_week_column),
                            grid_template_columns=(
                                "repeat(auto-fit, minmax(min(100%, 150px), 1fr))"
                            ),
                            width="100%",
                            gap="4px",
                        ),
                        align="stretch",
                        spacing="2",
                    ),
                ),
            ),
        ),
    )


def admin_clients_page() -> rx.Component:
    return _admin_page(
        title="Clientes",
        description="Gerencie seus clientes",
        active_path="/admin/clientes",
        content=rx.vstack(
            rx.flex(
                rx.el.input(
                    type="search",
                    placeholder="Buscar por nome, e-mail ou telefone...",
                    aria_label="Buscar clientes",
                    value=AppState.admin_client_search,
                    on_change=AppState.set_admin_client_search,
                    background_color=SURFACE,
                    color=FOREGROUND,
                    border=f"1px solid {SURFACE_BORDER}",
                    border_radius="7px",
                    padding="9px 11px",
                    width="100%",
                    max_width="420px",
                ),
                _action(
                    "+ Novo Cliente",
                    primary=True,
                    on_click=AppState.open_admin_client_form,
                ),
                justify="between",
                flex_wrap="wrap",
                gap="10px",
                width="100%",
            ),
            rx.cond(
                AppState.admin_client_form_open,
                _panel(
                    "Dados do Cliente",
                    rx.vstack(
                        rx.text(
                            rx.cond(
                                AppState.admin_client_form_action == "create",
                                "Novo cliente",
                                "Editar cliente",
                            ),
                            color=ACCENT,
                            font_size="0.82rem",
                            font_weight="600",
                        ),
                        rx.el.input(
                            type="text",
                            value=AppState.admin_client_form_name,
                            on_change=AppState.set_admin_client_form_name,
                            placeholder="Nome completo",
                            aria_label="Nome do cliente",
                            auto_complete="name",
                            required=True,
                            background_color=SURFACE,
                            color=FOREGROUND,
                            border=f"1px solid {SURFACE_BORDER}",
                            border_radius="7px",
                            padding="9px 11px",
                            width="100%",
                        ),
                        rx.el.input(
                            type="tel",
                            value=AppState.admin_client_form_phone,
                            on_change=AppState.set_admin_client_form_phone,
                            placeholder="Telefone / WhatsApp",
                            aria_label="Telefone do cliente",
                            auto_complete="tel",
                            required=True,
                            background_color=SURFACE,
                            color=FOREGROUND,
                            border=f"1px solid {SURFACE_BORDER}",
                            border_radius="7px",
                            padding="9px 11px",
                            width="100%",
                        ),
                        rx.flex(
                            _action(
                                "Cancelar",
                                on_click=AppState.close_admin_client_form,
                            ),
                            _action(
                                rx.cond(
                                    AppState.admin_client_form_action == "create",
                                    "Criar cliente",
                                    "Salvar alterações",
                                ),
                                primary=True,
                                on_click=AppState.submit_admin_client_form,
                            ),
                            gap="8px",
                            flex_wrap="wrap",
                        ),
                        align="stretch",
                        spacing="3",
                    ),
                ),
                rx.fragment(),
            ),
            _panel(
                "Lista de Clientes",
                rx.vstack(
                    _table_row(("Nome", "Telefone", "Total de Agendamentos", "Último Atendimento", "Ações"), True),
                    rx.cond(
                        AppState.filtered_admin_clients.length() == 0,
                        rx.cond(
                            AppState.is_loading,
                            rx.text("Carregando clientes...", color=MUTED),
                            rx.text(
                                rx.cond(
                                    AppState.admin_client_search != "",
                                    "Nenhum cliente corresponde à busca.",
                                    "Nenhum cliente encontrado.",
                                ),
                                color=MUTED,
                            ),
                        ),
                        rx.foreach(AppState.filtered_admin_clients, _admin_client_row),
                    ),
                    align="stretch",
                    spacing="0",
                ),
            ),
            rx.text(
                "Mostrando " + AppState.filtered_admin_client_count + " clientes",
                color=MUTED,
                font_size="0.64rem",
            ),
        ),
    )


def admin_services_page() -> rx.Component:
    return _admin_page(
        title="Serviços",
        description="Gerencie os serviços oferecidos",
        active_path="/admin/servicos",
        content=rx.vstack(
            rx.flex(
                rx.spacer(),
                _action(
                    "+ Novo Serviço",
                    primary=True,
                    on_click=AppState.open_admin_service_form,
                ),
                width="100%",
            ),
            rx.cond(
                AppState.admin_service_form_open,
                _panel(
                    "Dados do Serviço",
                    rx.vstack(
                        rx.text(
                            rx.cond(
                                AppState.admin_service_form_action == "create",
                                "Novo serviço",
                                "Editar serviço",
                            ),
                            color=ACCENT,
                            font_size="0.82rem",
                            font_weight="600",
                        ),
                        rx.el.input(
                            type="text",
                            value=AppState.admin_service_form_title,
                            on_change=AppState.set_admin_service_form_title,
                            placeholder="Título",
                            aria_label="Título do serviço",
                            required=True,
                            background_color=SURFACE,
                            color=FOREGROUND,
                            border=f"1px solid {SURFACE_BORDER}",
                            border_radius="7px",
                            padding="9px 11px",
                            width="100%",
                        ),
                        rx.el.input(
                            type="text",
                            value=AppState.admin_service_form_description,
                            on_change=AppState.set_admin_service_form_description,
                            placeholder="Descrição",
                            aria_label="Descrição do serviço",
                            background_color=SURFACE,
                            color=FOREGROUND,
                            border=f"1px solid {SURFACE_BORDER}",
                            border_radius="7px",
                            padding="9px 11px",
                            width="100%",
                        ),
                        rx.flex(
                            rx.el.input(
                                type="text",
                                input_mode="decimal",
                                value=AppState.admin_service_form_price,
                                on_change=AppState.set_admin_service_form_price,
                                placeholder="Preço em BRL",
                                aria_label="Preço do serviço em reais",
                                min="0.01",
                                step="0.01",
                                required=True,
                                background_color=SURFACE,
                                color=FOREGROUND,
                                border=f"1px solid {SURFACE_BORDER}",
                                border_radius="7px",
                                padding="9px 11px",
                                flex="1",
                            ),
                            rx.el.input(
                                type="text",
                                input_mode="numeric",
                                value=AppState.admin_service_form_duration,
                                on_change=AppState.set_admin_service_form_duration,
                                placeholder="Duração em minutos",
                                aria_label="Duração do serviço em minutos",
                                min="1",
                                step="1",
                                required=True,
                                background_color=SURFACE,
                                color=FOREGROUND,
                                border=f"1px solid {SURFACE_BORDER}",
                                border_radius="7px",
                                padding="9px 11px",
                                flex="1",
                            ),
                            flex_wrap="wrap",
                            gap="8px",
                            width="100%",
                        ),
                        rx.flex(
                            _action(
                                "Cancelar",
                                on_click=AppState.close_admin_service_form,
                            ),
                            _action(
                                rx.cond(
                                    AppState.admin_service_form_action == "create",
                                    "Criar serviço",
                                    "Salvar alterações",
                                ),
                                primary=True,
                                on_click=AppState.submit_admin_service_form,
                            ),
                            gap="8px",
                            flex_wrap="wrap",
                        ),
                        align="stretch",
                        spacing="3",
                    ),
                ),
                rx.fragment(),
            ),
            _panel(
                "Catálogo de Serviços",
                rx.vstack(
                    _table_row(("Serviço", "Descrição", "Preço", "Duração", "Status", "Ações"), True),
                    rx.cond(
                        AppState.services.length() == 0,
                        rx.cond(
                            AppState.is_loading,
                            rx.text("Carregando serviços...", color=MUTED),
                            rx.text("Nenhum serviço encontrado.", color=MUTED),
                        ),
                        rx.foreach(AppState.services, _admin_service_row),
                    ),
                    align="stretch",
                    spacing="0",
                ),
            ),
        ),
    )


def admin_team_page() -> rx.Component:
    return _admin_page(
        title="Equipe",
        description="Gerencie sua equipe de barbeiros",
        active_path="/admin/equipe",
        content=rx.vstack(
            rx.flex(
                rx.spacer(),
                _action(
                    "+ Novo Membro",
                    primary=True,
                    on_click=AppState.open_admin_barber_form,
                ),
                width="100%",
            ),
            rx.cond(
                AppState.admin_barber_form_open,
                _panel(
                    "Dados do Profissional",
                    rx.vstack(
                        rx.text(
                            rx.cond(
                                AppState.admin_barber_form_action == "create",
                                "Novo profissional",
                                "Editar profissional",
                            ),
                            color=ACCENT,
                            font_size="0.82rem",
                            font_weight="600",
                        ),
                        rx.el.input(
                            type="text",
                            value=AppState.admin_barber_form_name,
                            on_change=AppState.set_admin_barber_form_name,
                            placeholder="Nome completo",
                            aria_label="Nome do profissional",
                            required=True,
                            auto_complete="name",
                            background_color=SURFACE,
                            color=FOREGROUND,
                            border=f"1px solid {SURFACE_BORDER}",
                            border_radius="7px",
                            padding="9px 11px",
                            width="100%",
                        ),
                        rx.el.input(
                            type="text",
                            value=AppState.admin_barber_form_specialty,
                            on_change=AppState.set_admin_barber_form_specialty,
                            placeholder="Especialidade",
                            aria_label="Especialidade do profissional",
                            required=True,
                            background_color=SURFACE,
                            color=FOREGROUND,
                            border=f"1px solid {SURFACE_BORDER}",
                            border_radius="7px",
                            padding="9px 11px",
                            width="100%",
                        ),
                        rx.flex(
                            _action(
                                "Cancelar",
                                on_click=AppState.close_admin_barber_form,
                            ),
                            _action(
                                rx.cond(
                                    AppState.admin_barber_form_action == "create",
                                    "Criar profissional",
                                    "Salvar alterações",
                                ),
                                primary=True,
                                on_click=AppState.submit_admin_barber_form,
                            ),
                            gap="8px",
                            flex_wrap="wrap",
                        ),
                        align="stretch",
                        spacing="3",
                    ),
                ),
                rx.fragment(),
            ),
            _panel(
                "Equipe de Barbeiros",
                rx.vstack(
                    _table_row(("Nome", "Especialidade", "Status", "Ações"), True),
                    rx.cond(
                        AppState.barbers.length() == 0,
                        rx.cond(
                            AppState.is_loading,
                            rx.text("Carregando equipe...", color=MUTED),
                            rx.text("Nenhum barbeiro encontrado.", color=MUTED),
                        ),
                        rx.foreach(AppState.barbers, _admin_barber_row),
                    ),
                    align="stretch",
                    spacing="0",
                ),
            ),
        ),
    )


def admin_reports_page() -> rx.Component:
    return _admin_page(
        title="Relatórios de Faturamento",
        description="Acompanhe o desempenho da sua barbearia",
        active_path="/admin/relatorios",
        content=rx.vstack(
            rx.flex(
                rx.el.select(
                    rx.el.option("Diário", value="day"),
                    rx.el.option("Mensal", value="month"),
                    value=AppState.admin_report_period,
                    on_change=AppState.set_admin_report_period,
                    aria_label="Período do relatório",
                    background_color=SURFACE,
                    color=FOREGROUND,
                    border=f"1px solid {SURFACE_BORDER}",
                    border_radius="7px",
                    padding="8px 10px",
                ),
                rx.el.input(
                    type="date",
                    lang="pt-BR",
                    value=AppState.admin_report_date,
                    on_change=AppState.set_admin_report_date,
                    aria_label="Data do relatório",
                    background_color=SURFACE,
                    color=FOREGROUND,
                    border=f"1px solid {SURFACE_BORDER}",
                    border_radius="7px",
                    padding="6px 8px",
                ),
                rx.text(
                    AppState.admin_report_date_display,
                    color=MUTED,
                    font_size="0.7rem",
                ),
                align="center",
                flex_wrap="wrap",
                gap="8px",
                width="100%",
            ),
            rx.flex(
                _metric(
                    "Faturamento Total",
                    AppState.admin_report_revenue_display,
                    "circle_dollar_sign",
                ),
                _metric(
                    "Atendimentos Concluídos",
                    AppState.admin_report_completed_count,
                    "calendar_days",
                ),
                _metric(
                    "Ticket Médio",
                    AppState.admin_report_average_display,
                    "bar_chart_3",
                ),
                flex_wrap="wrap",
                gap="9px",
                width="100%",
            ),
            rx.flex(
                rx.box(
                    _panel(
                        "Faturamento do Período",
                        rx.vstack(
                            rx.text(
                                AppState.admin_report_date_display,
                                color=MUTED,
                                font_size="0.7rem",
                            ),
                            rx.heading(
                                AppState.admin_report_revenue_display,
                                as_="h3",
                                size="5",
                                color=FOREGROUND,
                            ),
                            rx.cond(
                                AppState.admin_report_completed_count == 0,
                                rx.text(
                                    "Nenhum atendimento concluído neste período.",
                                    color=MUTED,
                                    font_size="0.7rem",
                                ),
                                rx.text(
                                    AppState.admin_report_completed_count_display
                                    + " atendimentos concluídos",
                                    color=MUTED,
                                    font_size="0.7rem",
                                ),
                            ),
                            rx.text(
                                "Faturamento no período",
                                color=FOREGROUND,
                                font_size="0.68rem",
                                font_weight="600",
                                margin_top="10px",
                            ),
                            rx.flex(
                                rx.foreach(
                                    AppState.admin_report_revenue_series,
                                    _revenue_bar,
                                ),
                                align="end",
                                gap="8px",
                                width="100%",
                                height="150px",
                            ),
                            align="start",
                            spacing="3",
                        ),
                    ),
                    flex="2 1 540px",
                    min_width="280px",
                ),
                rx.box(
                    _panel(
                        "Serviços Concluídos",
                        rx.cond(
                            AppState.admin_report_service_summary.length() == 0,
                            rx.text(
                                "Sem serviços concluídos no período.",
                                color=MUTED,
                                font_size="0.7rem",
                            ),
                            rx.flex(
                                rx.box(
                                    rx.box(
                                        rx.vstack(
                                            rx.text(
                                                AppState.admin_report_completed_count_display,
                                                color=FOREGROUND,
                                                font_size="0.9rem",
                                                font_weight="700",
                                            ),
                                            rx.text(
                                                "concluídos",
                                                color=MUTED,
                                                font_size="0.48rem",
                                            ),
                                            align="center",
                                            spacing="0",
                                        ),
                                        width="68px",
                                        height="68px",
                                        background_color=SURFACE,
                                        border_radius="50%",
                                        display="flex",
                                        align_items="center",
                                        justify_content="center",
                                    ),
                                    width="112px",
                                    height="112px",
                                    padding="4px",
                                    background_image=AppState.admin_report_service_gradient,
                                    border_radius="50%",
                                    display="flex",
                                    align_items="center",
                                    justify_content="center",
                                    flex_shrink="0",
                                ),
                                rx.vstack(
                                    rx.foreach(
                                        AppState.admin_report_service_summary,
                                        _report_service_row,
                                    ),
                                    align="stretch",
                                    spacing="2",
                                    width="100%",
                                ),
                                align="center",
                                gap="12px",
                                width="100%",
                                flex_wrap="wrap",
                            ),
                        ),
                    ),
                    flex="1 1 270px",
                    min_width="240px",
                ),
                align="stretch",
                flex_wrap="wrap",
                gap="12px",
                width="100%",
            ),
        ),
    )


def admin_users_page() -> rx.Component:
    return _admin_page(
        title="Gerenciamento de Usuários",
        description="Gerencie os usuários do sistema",
        active_path="/admin/usuarios",
        content=rx.flex(
            rx.box(
                rx.text(
                    "Usuários administrativos e barbeiros são provisionados "
                    "manualmente no Xano. Esta tela é somente para consulta.",
                    color=MUTED,
                    font_size="0.82rem",
                    line_height="1.6",
                    margin_bottom="14px",
                ),
                _table_row(("Nome", "E-mail", "Função"), True),
                rx.cond(
                    AppState.users.length() == 0,
                    rx.cond(
                        AppState.is_loading,
                        rx.text("Carregando usuários...", color=MUTED),
                        rx.text("Nenhum usuário encontrado.", color=MUTED),
                    ),
                    rx.foreach(AppState.users, _admin_user_row),
                ),
                background_color=SURFACE,
                border=f"1px solid {SURFACE_BORDER}",
                border_radius="10px",
                padding="12px",
                flex="3 1 600px",
                min_width="0",
            ),
            rx.box(
                _panel(
                    "Permissões e Acessos",
                    rx.vstack(
                        *[
                            rx.flex(
                                rx.icon(tag="circle_check", size=16, color="#53b46a"),
                                rx.text(
                                    permission,
                                    color=FOREGROUND,
                                    font_size="0.68rem",
                                ),
                                align="center",
                                gap="8px",
                            )
                            for permission in (
                                "Clientes podem agendar e gerenciar seus dados",
                                "Barbeiros acessam apenas sua agenda",
                                "Administradores têm acesso total ao sistema",
                            )
                        ],
                        align="stretch",
                        spacing="3",
                    ),
                ),
                flex="1 1 240px",
                min_width="220px",
            ),
            align="start",
            flex_wrap="wrap",
            gap="12px",
            width="100%",
        ),
    )


def admin_settings_page() -> rx.Component:
    return _admin_page(
        title="Configurações",
        description="Configurações da barbearia",
        active_path="/admin/configuracoes",
        content=rx.flex(
            rx.box(
                _panel(
                    "Horário de Funcionamento",
                    rx.vstack(
                        rx.text("Segunda a sábado", color=FOREGROUND, font_size="0.78rem"),
                        rx.text("09:00 às 18:00", color=MUTED, font_size="0.7rem"),
                        rx.text(
                            "Expediente global da unidade; não editável nesta tela.",
                            color=MUTED,
                            font_size="0.8rem",
                            line_height="1.5",
                        ),
                        align="start",
                        spacing="3",
                    ),
                ),
                flex="1 1 270px",
            ),
            rx.box(
                _panel(
                    "Fuso Horário",
                    rx.vstack(
                        rx.text("America/Sao_Paulo", color=FOREGROUND, font_size="0.78rem"),
                        rx.text("Exibição local de todos os horários", color=MUTED, font_size="0.7rem"),
                        rx.text(
                            "Os horários são exibidos no fuso local da barbearia.",
                            color=MUTED,
                            font_size="0.8rem",
                            line_height="1.5",
                        ),
                        align="start",
                        spacing="3",
                    ),
                ),
                flex="1 1 270px",
            ),
            rx.box(
                _panel(
                    "Política de Cancelamento",
                    rx.vstack(
                        rx.text("Cancelamento permitido até 12 horas antes", color=FOREGROUND, font_size="0.78rem"),
                        rx.text(
                            "Configuração somente para consulta.",
                            color=MUTED,
                            font_size="0.8rem",
                            line_height="1.5",
                        ),
                        align="start",
                        spacing="3",
                    ),
                ),
                flex="1 1 270px",
            ),
            flex_wrap="wrap",
            align="start",
            gap="12px",
            width="100%",
        ),
    )
