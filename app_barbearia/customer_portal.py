import reflex as rx

from app_barbearia.mock_repository import (
    AppointmentRecord,
    BarberRecord,
    ServiceRecord,
)
from app_barbearia.state import AppState
from app_barbearia.ui import (
    ACCENT,
    FOREGROUND,
    MUTED,
    SURFACE,
    SURFACE_BORDER,
    public_layout,
)


PORTAL_LINKS = [
    ("Minha Conta", "/"),
    ("Meus Agendamentos", "/agendamentos"),
    ("Histórico", "/agendamentos#historico"),
    ("Sair", "/login"),
]
CATALOG_LINKS = [
    ("Serviços", "/servicos"),
    ("Equipe", "/equipe"),
    ("Agendamentos", "/agendamentos"),
    ("Minha Conta", "/"),
    ("Sair", "/login"),
]
APPOINTMENT_LINKS = PORTAL_LINKS
BOOKING_LINKS = [
    ("Início", "/"),
    ("Serviços", "/servicos"),
    ("Equipe", "/equipe"),
    ("Agendamentos", "/agendar"),
    ("Minha Conta", "/"),
    ("Sair", "/login"),
]


def _page_header(eyebrow: str, title: str, description: str) -> rx.Component:
    return rx.vstack(
        rx.text(
            eyebrow.upper(),
            color=ACCENT,
            font_size="0.68rem",
            font_weight="700",
            letter_spacing="0.15em",
        ),
        rx.heading(
            title,
            as_="h1",
            size="7",
            color=FOREGROUND,
            line_height="1.12",
        ),
        rx.text(
            description,
            color=MUTED,
            font_size="0.94rem",
            line_height="1.7",
            max_width="720px",
        ),
        align="start",
        spacing="3",
        width="100%",
    )


def _card(title: str, content: rx.Component) -> rx.Component:
    return rx.box(
        rx.heading(title, as_="h2", size="3", color=FOREGROUND, margin_bottom="12px"),
        content,
        background_color="#10100f",
        border=f"1px solid {SURFACE_BORDER}",
        border_radius="10px",
        padding="12px",
        width="100%",
    )


def _service_card(service: ServiceRecord) -> rx.Component:
    return rx.vstack(
        rx.box(
            rx.icon(
                tag=service["icon_tag"],
                size=34,
                color=ACCENT,
                aria_hidden=True,
            ),
            display="flex",
            align_items="center",
            justify_content="center",
            height="92px",
            width="100%",
            background_image=(
                "linear-gradient(135deg, #34281b 0%, #171512 50%, #3a2a19 100%)"
            ),
            border_radius="7px",
        ),
        rx.vstack(
            rx.heading(service["title"], as_="h3", size="3", color=FOREGROUND),
            rx.text(service["price_display"], color=FOREGROUND, font_size="0.86rem"),
            rx.flex(
                rx.icon(tag="clock_3", size=14, color=MUTED, aria_hidden=True),
                rx.text(
                    service["duration_display"],
                    color=MUTED,
                    font_size="0.78rem",
                ),
                align="center",
                gap="6px",
            ),
            rx.button(
                "Agendar",
                type="button",
                on_click=AppState.start_booking(service["id"]),
                color="#17140f",
                background_color=ACCENT,
                border_radius="6px",
                padding="8px 12px",
                font_size="0.75rem",
                font_weight="700",
                text_align="center",
                width="100%",
                _focus={
                    "outline": f"2px solid {FOREGROUND}",
                    "outline_offset": "2px",
                },
            ),
            align="stretch",
            spacing="2",
            width="100%",
            padding="8px 2px 2px",
        ),
        background_color="#111110",
        border=f"1px solid {SURFACE_BORDER}",
        border_radius="9px",
        padding="8px",
        spacing="1",
        align="stretch",
        flex="1 1 170px",
        max_width="250px",
    )


def _barber_card(barber: BarberRecord) -> rx.Component:
    return rx.vstack(
        rx.box(
            rx.icon(tag="user_round", size=30, color="#d2d0cb", aria_hidden=True),
            background_image=(
                "linear-gradient(145deg, #4a3b2b 0%, #211d18 65%, #111110 100%)"
            ),
            border_radius="7px",
            width="100%",
            height="118px",
            display="flex",
            align_items="center",
            justify_content="center",
        ),
        rx.flex(
            rx.vstack(
                rx.text(
                    barber["name"],
                    color=FOREGROUND,
                    font_size="0.88rem",
                    font_weight="600",
                ),
                rx.text(
                    barber["specialty"],
                    color=MUTED,
                    font_size="0.73rem",
                ),
                align="start",
                spacing="1",
            ),
            rx.text(
                barber["initials"],
                color=ACCENT,
                font_size="0.68rem",
                font_weight="700",
            ),
            align="center",
            justify="between",
        ),
        rx.button(
            "Agendar",
            type="button",
            on_click=AppState.start_barber_booking(barber["id"]),
            color="#17140f",
            background_color=ACCENT,
            border_radius="6px",
            padding="8px 12px",
            font_size="0.75rem",
            font_weight="700",
            text_align="center",
            width="100%",
            _focus={
                "outline": f"2px solid {FOREGROUND}",
                "outline_offset": "2px",
            },
        ),
        align="stretch",
        spacing="2",
        background_color="#111110",
        border=f"1px solid {SURFACE_BORDER}",
        border_radius="9px",
        padding="8px",
        flex="1 1 210px",
        max_width="280px",
    )


def _appointment_row(
    date: str | rx.Var[str],
    time: str | rx.Var[str],
    service: str | rx.Var[str],
    barber: str | rx.Var[str],
    status: str | rx.Var[str],
    status_color: str | rx.Var[str] = ACCENT,
    appointment_id: str | rx.Var[str] | None = None,
) -> rx.Component:
    cancel_button = rx.button(
        "Cancelar",
        color=FOREGROUND,
        background_color="transparent",
        border=f"1px solid {ACCENT}",
        border_radius="7px",
        padding="6px 10px",
        font_size="0.7rem",
        type="button",
        on_click=(
            AppState.cancel_client_appointment(appointment_id)
            if appointment_id is not None
            else None
        ),
    )
    return rx.flex(
        rx.box(
            rx.icon(tag="user_round", size=34, color="#d2d0cb", aria_hidden=True),
            background_image=(
                "linear-gradient(145deg, #4a3b2b 0%, #211d18 65%, #111110 100%)"
            ),
            border_radius="7px",
            width="90px",
            height="72px",
            display="flex",
            align_items="center",
            justify_content="center",
            flex_shrink="0",
        ),
        rx.vstack(
            rx.text(service, color=FOREGROUND, font_weight="600"),
            rx.flex(
                rx.icon(tag="calendar_days", size=14, color=MUTED, aria_hidden=True),
                rx.text(date, color=MUTED, font_size="0.77rem"),
                align="center",
                gap="6px",
            ),
            rx.flex(
                rx.icon(tag="clock_3", size=14, color=MUTED, aria_hidden=True),
                rx.text(time, color=MUTED, font_size="0.77rem"),
                align="center",
                gap="6px",
            ),
            rx.text("Com ", barber, color=MUTED, font_size="0.75rem"),
            align="start",
            spacing="2",
            flex="1",
        ),
        rx.vstack(
            rx.text(
                status,
                color=status_color,
                background_color=rx.cond(
                    status == "Confirmado",
                    "#17251c",
                    "transparent",
                ),
                border=rx.cond(
                    status == "Confirmado",
                    "1px solid #54a86b",
                    rx.cond(
                        status == "Pendente",
                        "1px solid #d6a64f",
                        "1px solid #aaa69d",
                    ),
                ),
                border_radius="999px",
                padding="5px 10px",
                font_size="0.67rem",
                font_weight="700",
                white_space="nowrap",
            ),
            rx.cond(
                status == "Confirmado",
                cancel_button,
                rx.cond(status == "Pendente", cancel_button, rx.fragment()),
            ),
            align="end",
            spacing="2",
        ),
        align="center",
        flex_wrap="wrap",
        gap="12px",
        width="100%",
        padding="12px 0",
        border_bottom=f"1px solid {SURFACE_BORDER}",
    )


def _appointment_item(item: AppointmentRecord) -> rx.Component:
    return _appointment_row(
        item["date_display"],
        item["time"],
        item["service_title"],
        item["barber_name"],
        item["status_label"],
        item["status_color"],
        appointment_id=item["id"],
    )


def _customer_page(
    *,
    content: rx.Component,
    active_path: str = "/",
    links: list[tuple[str, str]] | None = None,
    eyebrow: str = "",
    title: str = "",
    description: str = "",
    content_max_width: str = "1440px",
) -> rx.Component:
    children = []
    if title:
        children.append(_page_header(eyebrow, title, description))
    children.append(content)
    return public_layout(
        rx.vstack(
            *children,
            align="stretch",
            spacing="5",
            width="100%",
            max_width=content_max_width,
            margin="0 auto",
            padding="18px 20px 30px",
        ),
        links=links or PORTAL_LINKS,
        active_path=active_path,
    )


def customer_portal() -> rx.Component:
    return _customer_page(
        content_max_width="960px",
        content=rx.vstack(
            rx.flex(
                rx.box(
                    rx.icon(tag="user_round", size=28, color="#d2d0cb", aria_hidden=True),
                    background_color="#596270",
                    border_radius="50%",
                    width="48px",
                    height="48px",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    flex_shrink="0",
                ),
                rx.vstack(
                    rx.heading(
                        "Olá, ",
                        AppState.greeting_name,
                        "!",
                        as_="h1",
                        size="5",
                        color=FOREGROUND,
                    ),
                    rx.text("Cliente desde 2026", color=MUTED, font_size="0.76rem"),
                    align="start",
                    spacing="1",
                ),
                rx.link(
                    rx.icon(tag="square_pen", size=14, aria_hidden=True),
                    "Editar Perfil",
                    href="/perfil",
                    color=ACCENT,
                    border=f"1px solid {ACCENT}",
                    border_radius="7px",
                    padding="8px 11px",
                    font_size="0.73rem",
                    font_weight="600",
                    text_decoration="none",
                    display="flex",
                    align_items="center",
                    gap="5px",
                    _focus={
                        "outline": f"2px solid {FOREGROUND}",
                        "outline_offset": "2px",
                    },
                ),
                align="center",
                gap="12px",
                width="100%",
                padding="2px 2px 12px",
            ),
            rx.flex(
                rx.box(
                    rx.flex(
                        rx.heading(
                            "Meus Próximos Agendamentos",
                            as_="h2",
                            size="3",
                            color=FOREGROUND,
                        ),
                        rx.link(
                            "Ver todos →",
                            href="/agendamentos",
                            color=ACCENT,
                            font_size="0.67rem",
                            text_decoration="none",
                        ),
                        align="center",
                        justify="between",
                        gap="10px",
                    ),
                    rx.cond(
                        AppState.next_appointments.length() == 0,
                        rx.cond(
                            AppState.is_loading,
                            rx.text(
                                "Carregando agendamentos...",
                                color=MUTED,
                                font_size="0.75rem",
                            ),
                            rx.text(
                                "Você ainda não tem próximos agendamentos.",
                                color=MUTED,
                                font_size="0.75rem",
                            ),
                        ),
                        rx.foreach(
                            AppState.next_appointments,
                            _appointment_item,
                        ),
                    ),
                    background_color="#10100f",
                    border=f"1px solid {SURFACE_BORDER}",
                    border_radius="10px",
                    padding="12px",
                    flex="2.4 1 430px",
                    min_width="0",
                ),
                rx.box(
                    rx.heading(
                        "Seu Histórico",
                        as_="h2",
                        size="3",
                        color=FOREGROUND,
                        margin_bottom="16px",
                    ),
                    rx.text("Total de atendimentos", color=MUTED, font_size="0.73rem"),
                    rx.flex(
                        rx.text(
                            "12",
                            color=FOREGROUND,
                            font_size="1.8rem",
                            font_weight="700",
                        ),
                        rx.flex(
                            *[
                                rx.box(
                                    width="7px",
                                    height=height,
                                    background_color=ACCENT,
                                    border_radius="2px 2px 0 0",
                                )
                                for height in ("17px", "24px", "30px", "21px", "36px")
                            ],
                            align="end",
                            gap="3px",
                            height="40px",
                            padding_bottom="2px",
                        ),
                        align="end",
                        justify="between",
                        width="100%",
                    ),
                    background_color="#10100f",
                    border=f"1px solid {SURFACE_BORDER}",
                    border_radius="10px",
                    padding="14px",
                    flex="1 1 180px",
                    max_width="280px",
                    min_width="0",
                ),
                align="start",
                flex_wrap="wrap",
                gap="12px",
                width="100%",
            ),
            rx.flex(
                rx.icon(tag="crown", size=26, color=ACCENT, aria_hidden=True),
                rx.vstack(
                    rx.text(
                        "Obrigado por escolher a BarberFlow!",
                        color=FOREGROUND,
                        font_size="0.84rem",
                        font_weight="700",
                    ),
                    rx.text(
                        "Cuide do seu estilo, sempre.",
                        color=MUTED,
                        font_size="0.73rem",
                    ),
                    align="start",
                    spacing="1",
                ),
                align="center",
                gap="14px",
                width="100%",
                background_image=(
                    "linear-gradient(110deg, #12110f, #19150f 72%, #4c3618)"
                ),
                border=f"1px solid {SURFACE_BORDER}",
                border_radius="10px",
                padding="16px 20px",
            ),
            align="stretch",
            spacing="4",
            width="100%",
        ),
    )


def services_page() -> rx.Component:
    return _customer_page(
        active_path="/servicos",
        links=CATALOG_LINKS,
        content=rx.vstack(
            rx.flex(
                rx.flex(
                    rx.link(
                        "Serviços",
                        href="/servicos",
                        color="#17140f",
                        background_color=ACCENT,
                        border_radius="7px",
                        padding="8px 15px",
                        font_size="0.75rem",
                        font_weight="700",
                        text_decoration="none",
                        aria_current="page",
                        _focus={
                            "outline": f"2px solid {FOREGROUND}",
                            "outline_offset": "2px",
                        },
                    ),
                    rx.link(
                        "Barbeiros",
                        href="/equipe",
                        color=FOREGROUND,
                        background_color="#171715",
                        border=f"1px solid {SURFACE_BORDER}",
                        border_radius="7px",
                        padding="8px 15px",
                        font_size="0.75rem",
                        text_decoration="none",
                        _focus={
                            "outline": f"2px solid {FOREGROUND}",
                            "outline_offset": "2px",
                        },
                    ),
                    align="center",
                    gap="4px",
                    background_color="#171715",
                    border=f"1px solid {SURFACE_BORDER}",
                    border_radius="9px",
                    padding="4px",
                ),
                rx.el.input(
                    type="search",
                    placeholder="Buscar serviço...",
                    aria_label="Buscar serviço",
                    value=AppState.service_search,
                    on_change=AppState.set_service_search,
                    background_color="#111110",
                    color=FOREGROUND,
                    border=f"1px solid {SURFACE_BORDER}",
                    border_radius="8px",
                    padding="9px 12px",
                    font_size="0.77rem",
                    width="200px",
                    max_width="100%",
                ),
                justify="between",
                align="center",
                flex_wrap="wrap",
                gap="12px",
                width="100%",
            ),
            rx.vstack(
                rx.heading("Nossos Serviços", as_="h1", size="4", color=FOREGROUND),
                rx.text(
                    "Qualidade e estilo em cada detalhe.",
                    color=MUTED,
                    font_size="0.75rem",
                ),
                align="start",
                spacing="1",
                width="100%",
            ),
            rx.flex(
                rx.cond(
                    AppState.filtered_services.length() == 0,
                    rx.cond(
                        AppState.is_loading,
                        rx.text("Carregando serviços...", color=MUTED),
                        rx.text(
                            "Nenhum serviço disponível para esta busca.",
                            color=MUTED,
                        ),
                    ),
                    rx.foreach(AppState.filtered_services, _service_card),
                ),
                flex_wrap="wrap",
                gap="10px",
                width="100%",
            ),
            align="stretch",
            spacing="4",
            width="100%",
        ),
    )


def team_page() -> rx.Component:
    return _customer_page(
        active_path="/equipe",
        links=CATALOG_LINKS,
        content=rx.vstack(
            rx.flex(
                rx.link(
                    "Serviços",
                    href="/servicos",
                    color=FOREGROUND,
                    background_color="#171715",
                    border=f"1px solid {SURFACE_BORDER}",
                    border_radius="7px",
                    padding="8px 15px",
                    font_size="0.75rem",
                    text_decoration="none",
                    _focus={
                        "outline": f"2px solid {FOREGROUND}",
                        "outline_offset": "2px",
                    },
                ),
                rx.link(
                    "Barbeiros",
                    href="/equipe",
                    color="#17140f",
                    background_color=ACCENT,
                    border_radius="7px",
                    padding="8px 15px",
                    font_size="0.75rem",
                    font_weight="700",
                    text_decoration="none",
                    aria_current="page",
                    _focus={
                        "outline": f"2px solid {FOREGROUND}",
                        "outline_offset": "2px",
                    },
                ),
                align="center",
                gap="4px",
                background_color="#171715",
                border=f"1px solid {SURFACE_BORDER}",
                border_radius="9px",
                padding="4px",
            ),
            rx.vstack(
                rx.heading("Nossa Equipe", as_="h1", size="4", color=FOREGROUND),
                rx.text(
                    "Profissionais especializados para cuidar do seu estilo.",
                    color=MUTED,
                    font_size="0.75rem",
                ),
                align="start",
                spacing="1",
                width="100%",
            ),
            rx.flex(
                rx.cond(
                    AppState.barbers.length() == 0,
                    rx.cond(
                        AppState.is_loading,
                        rx.text("Carregando equipe...", color=MUTED),
                        rx.text("Nenhum profissional disponível.", color=MUTED),
                    ),
                    rx.foreach(AppState.barbers, _barber_card),
                ),
                flex_wrap="wrap",
                gap="12px",
                width="100%",
            ),
            align="stretch",
            spacing="4",
            width="100%",
        ),
    )


def appointments_page() -> rx.Component:
    upcoming_card = _card(
        "Próximos Agendamentos",
        rx.cond(
            AppState.upcoming_appointments.length() == 0,
            rx.cond(
                AppState.is_loading,
                rx.text("Carregando agendamentos...", color=MUTED),
                rx.vstack(
                    rx.text(
                        "Você ainda não tem próximos agendamentos.",
                        color=MUTED,
                        font_size="0.75rem",
                    ),
                    rx.link(
                        "Agendar um horário",
                        href="/agendar",
                        color=ACCENT,
                        font_size="0.75rem",
                    ),
                    align="start",
                    spacing="2",
                ),
            ),
            rx.vstack(
                rx.foreach(AppState.upcoming_appointments, _appointment_item),
                align="stretch",
                spacing="0",
            ),
        ),
    )
    history_card = rx.box(
        _card(
            "Histórico",
            rx.cond(
                AppState.historical_appointments.length() == 0,
                rx.cond(
                    AppState.is_loading,
                    rx.text("Carregando histórico...", color=MUTED),
                    rx.text(
                        "Nenhum atendimento no histórico.",
                        color=MUTED,
                        font_size="0.75rem",
                    ),
                ),
                rx.vstack(
                    rx.foreach(AppState.historical_appointments, _appointment_item),
                    align="stretch",
                    spacing="0",
                ),
            ),
        ),
        id="historico",
        width="100%",
    )
    return _customer_page(
        active_path="/agendamentos",
        links=APPOINTMENT_LINKS,
        content=rx.vstack(
            rx.heading("Meus Agendamentos", as_="h1", size="5", color=FOREGROUND),
            rx.flex(
                rx.button(
                    "Todos",
                    on_click=AppState.set_appointment_filter("all"),
                    type="button",
                    aria_pressed=AppState.appointment_filter == "all",
                ),
                rx.button(
                    "Próximos",
                    on_click=AppState.set_appointment_filter("upcoming"),
                    type="button",
                    aria_pressed=AppState.appointment_filter == "upcoming",
                ),
                rx.button(
                    "Histórico",
                    on_click=AppState.set_appointment_filter("history"),
                    type="button",
                    aria_pressed=AppState.appointment_filter == "history",
                ),
                align="center",
                flex_wrap="wrap",
                gap="8px",
            ),
            rx.cond(
                AppState.appointment_filter == "all",
                rx.vstack(upcoming_card, history_card, align="stretch", spacing="4"),
                rx.cond(
                    AppState.appointment_filter == "upcoming",
                    upcoming_card,
                    history_card,
                ),
            ),
            align="stretch",
            spacing="4",
            width="100%",
        ),
    )


def _booking_step(number: str, label: str, active: bool = False) -> rx.Component:
    return rx.flex(
        rx.box(
            rx.text(
                number,
                color="#17140f" if active else MUTED,
                font_size="0.74rem",
                font_weight="700",
            ),
            background_color=ACCENT if active else "#262521",
            border_radius="50%",
            width="28px",
            height="28px",
            display="flex",
            align_items="center",
            justify_content="center",
            flex_shrink="0",
        ),
        rx.text(
            label,
            color=FOREGROUND if active else MUTED,
            font_size="0.8rem",
            font_weight="600" if active else "400",
        ),
        align="center",
        gap="9px",
        padding="10px 12px",
        background_color="#211e18" if active else "transparent",
        border_radius="999px",
    )


def _booking_option(
    title: str | rx.Var[str],
    description: str | rx.Var[str],
    selected: bool | rx.Var[bool] = False,
    icon_tag: str | rx.Var[str] = "user_round",
    on_click: rx.EventHandler | None = None,
) -> rx.Component:
    return rx.button(
        rx.box(
            rx.icon(tag=icon_tag, size=17, color=ACCENT, aria_hidden=True),
            background_color="#211e18",
            border_radius="7px",
            width="36px",
            height="36px",
            display="flex",
            align_items="center",
            justify_content="center",
            flex_shrink="0",
        ),
        rx.flex(
            rx.vstack(
                rx.text(title, color=FOREGROUND, font_size="0.78rem", font_weight="600"),
                rx.text(description, color=MUTED, font_size="0.66rem"),
                align="start",
                spacing="1",
                flex="1",
            ),
            rx.icon(
                tag=rx.cond(selected, "circle_check", "circle"),
                size=16,
                color=rx.cond(selected, ACCENT, MUTED),
                aria_hidden=True,
            ),
            align="center",
            justify="between",
            gap="8px",
            width="100%",
        ),
        type="button",
        aria_pressed=selected,
        on_click=on_click,
        background_color=rx.cond(selected, "#211e18", "#111110"),
        border=rx.cond(
            selected,
            f"1px solid {ACCENT}",
            f"1px solid {SURFACE_BORDER}",
        ),
        border_radius="8px",
        padding="8px",
        width="100%",
        display="flex",
        align_items="center",
        gap="8px",
        text_align="left",
        cursor="pointer",
        _focus={
            "outline": f"2px solid {FOREGROUND}",
            "outline_offset": "2px",
        },
    )


def _booking_service_option(service: ServiceRecord) -> rx.Component:
    return _booking_option(
        service["title"],
        service["booking_description"],
        selected=AppState.selected_service_id == service["id"],
        icon_tag=service["icon_tag"],
        on_click=AppState.select_booking_service(service["id"]),
    )


def _booking_barber_option(barber: BarberRecord) -> rx.Component:
    return _booking_option(
        barber["name"],
        barber["booking_description"],
        selected=AppState.selected_barber_id == barber["id"],
        on_click=AppState.select_booking_barber(barber["id"]),
    )


def _booking_calendar_cell(day: str) -> rx.Component:
    return rx.cond(
        day == "",
        rx.box(width="24px", height="24px"),
        rx.button(
            rx.text(
                day,
                color=rx.cond(
                    AppState.selected_day == day,
                    "#17140f",
                    FOREGROUND,
                ),
                font_size="0.66rem",
                font_weight=rx.cond(
                    AppState.selected_day == day,
                    "700",
                    "400",
                ),
                text_align="center",
            ),
            type="button",
            aria_pressed=AppState.selected_day == day,
            on_click=AppState.select_booking_date(
                AppState.booking_month + "-" + day
            ),
            background_color=rx.cond(
                AppState.selected_day == day,
                ACCENT,
                "transparent",
            ),
            border="0",
            border_radius="5px",
            width="24px",
            height="24px",
            display="flex",
            align_items="center",
            justify_content="center",
            padding="0",
            _focus={
                "outline": f"2px solid {FOREGROUND}",
                "outline_offset": "1px",
            },
        ),
    )


def _booking_time_option(time_value: str) -> rx.Component:
    selected = AppState.selected_time == time_value
    return rx.button(
        rx.text(
            time_value,
            color=rx.cond(selected, "#17140f", FOREGROUND),
            font_size="0.68rem",
            font_weight=rx.cond(selected, "700", "400"),
        ),
        type="button",
        aria_pressed=selected,
        on_click=AppState.select_booking_time(time_value),
        background_color=rx.cond(selected, ACCENT, "#111110"),
        border=rx.cond(
            selected,
            f"1px solid {ACCENT}",
            f"1px solid {SURFACE_BORDER}",
        ),
        border_radius="7px",
        padding="8px 4px",
        text_align="center",
        flex="1 1 70px",
        cursor="pointer",
        _focus={
            "outline": f"2px solid {FOREGROUND}",
            "outline_offset": "1px",
        },
    )


def booking_page() -> rx.Component:
    return _customer_page(
        active_path="/agendar",
        links=BOOKING_LINKS,
        content=rx.vstack(
            rx.flex(
                rx.box(
                    rx.icon(tag="calendar_days", size=32, color=ACCENT, aria_hidden=True),
                    background_color="#211e18",
                    border_radius="9px",
                    width="64px",
                    height="64px",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    flex_shrink="0",
                ),
                rx.vstack(
                    rx.heading(
                        "Agendar Horário",
                        as_="h1",
                        size="5",
                        color=FOREGROUND,
                    ),
                    rx.text(
                        "Escolha o serviço, barbeiro e horário ideal pra você.",
                        color=MUTED,
                        font_size="0.78rem",
                    ),
                    align="start",
                    spacing="1",
                ),
                align="center",
                gap="12px",
                width="100%",
            ),
            rx.flex(
                _booking_step("1", "Serviço", active=True),
                rx.box(
                    width="60px",
                    height="1px",
                    background_color=ACCENT,
                    flex_shrink="0",
                ),
                _booking_step("2", "Profissional"),
                rx.box(
                    width="60px",
                    height="1px",
                    background_color=SURFACE_BORDER,
                    flex_shrink="0",
                ),
                _booking_step("3", "Data e Horário"),
                flex_wrap="wrap",
                gap="8px",
                align="center",
                justify="end",
                width="100%",
            ),
            rx.flex(
                rx.box(
                    _card(
                        "Selecione o Serviço",
                        rx.vstack(
                            rx.cond(
                                AppState.services.length() == 0,
                                rx.cond(
                                    AppState.is_loading,
                                    rx.text("Carregando serviços...", color=MUTED),
                                    rx.text(
                                        "Nenhum serviço disponível.",
                                        color=MUTED,
                                    ),
                                ),
                                rx.foreach(
                                    AppState.services,
                                    _booking_service_option,
                                ),
                            ),
                            align="stretch",
                            spacing="2",
                        ),
                    ),
                    flex="1 1 190px",
                    min_width="190px",
                ),
                rx.box(
                    _card(
                        "Selecione o Barbeiro",
                        rx.vstack(
                            rx.cond(
                                AppState.barbers.length() == 0,
                                rx.cond(
                                    AppState.is_loading,
                                    rx.text("Carregando equipe...", color=MUTED),
                                    rx.text(
                                        "Nenhum profissional disponível.",
                                        color=MUTED,
                                    ),
                                ),
                                rx.foreach(
                                    AppState.barbers,
                                    _booking_barber_option,
                                ),
                            ),
                            align="stretch",
                            spacing="2",
                        ),
                    ),
                    flex="1 1 190px",
                    min_width="190px",
                ),
                rx.box(
                    _card(
                        "Escolha a Data",
                        rx.vstack(
                            rx.flex(
                                rx.button(
                                    rx.icon(
                                        tag="chevron_left",
                                        size=15,
                                        color=FOREGROUND,
                                        aria_hidden=True,
                                    ),
                                    type="button",
                                    aria_label="Mês anterior",
                                    on_click=AppState.change_booking_month(-1),
                                    variant="ghost",
                                    size="1",
                                ),
                                rx.text(
                                    AppState.booking_month_display,
                                    color=FOREGROUND,
                                    font_size="0.74rem",
                                    font_weight="600",
                                ),
                                rx.button(
                                    rx.icon(
                                        tag="chevron_right",
                                        size=15,
                                        color=FOREGROUND,
                                        aria_hidden=True,
                                    ),
                                    type="button",
                                    aria_label="Próximo mês",
                                    on_click=AppState.change_booking_month(1),
                                    variant="ghost",
                                    size="1",
                                ),
                                align="center",
                                justify="between",
                                width="100%",
                                padding="4px 0 8px",
                            ),
                            rx.grid(
                                *[
                                    rx.text(
                                        day,
                                        color=MUTED,
                                        font_size="0.58rem",
                                        text_align="center",
                                    )
                                    for day in ("Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom")
                                ],
                                columns="7",
                                width="100%",
                                gap="5px",
                            ),
                            rx.grid(
                                rx.foreach(
                                    AppState.calendar_days,
                                    _booking_calendar_cell,
                                ),
                                columns="7",
                                width="100%",
                                gap="3px",
                                justify_items="center",
                            ),
                            align="stretch",
                            spacing="2",
                        ),
                    ),
                    flex="1 1 210px",
                    min_width="200px",
                ),
                rx.box(
                    _card(
                        "Horários Disponíveis",
                        rx.flex(
                            rx.cond(
                                AppState.available_times.length() == 0,
                                rx.cond(
                                    AppState.is_loading,
                                    rx.text(
                                        "Consultando horários...",
                                        color=MUTED,
                                    ),
                                    rx.text(
                                        "Nenhum horário disponível para esta data.",
                                        color=MUTED,
                                        font_size="0.7rem",
                                    ),
                                ),
                                rx.foreach(
                                    AppState.available_times,
                                    _booking_time_option,
                                )
                            ),
                            flex_wrap="wrap",
                            gap="6px",
                        ),
                    ),
                    flex="1 1 190px",
                    min_width="190px",
                ),
                rx.box(
                    _card(
                        "Resumo do Agendamento",
                        rx.vstack(
                            rx.flex(
                                rx.box(
                                    rx.icon(
                                        tag="user_round",
                                        size=25,
                                        color="#d2d0cb",
                                        aria_hidden=True,
                                    ),
                                    background_image=(
                                        "linear-gradient(145deg, #4a3b2b, #171512)"
                                    ),
                                    border_radius="7px",
                                    width="54px",
                                    height="58px",
                                    display="flex",
                                    align_items="center",
                                    justify_content="center",
                                ),
                                rx.vstack(
                                    rx.text(
                                        AppState.selected_service_title,
                                        color=FOREGROUND,
                                        font_size="0.74rem",
                                        font_weight="600",
                                    ),
                                    rx.text(
                                        AppState.selected_service_price
                                        + " · "
                                        + AppState.selected_service_duration,
                                        color=MUTED,
                                        font_size="0.64rem",
                                    ),
                                    rx.text(
                                        AppState.selected_barber_name,
                                        color=MUTED,
                                        font_size="0.66rem",
                                    ),
                                    align="start",
                                    spacing="1",
                                ),
                                align="center",
                                gap="8px",
                                width="100%",
                            ),
                            rx.flex(
                                rx.icon(tag="calendar_days", size=15, color=MUTED),
                                rx.text(
                                    AppState.selected_date_display,
                                    color=FOREGROUND,
                                    font_size="0.7rem",
                                ),
                                align="center",
                                gap="8px",
                            ),
                            rx.flex(
                                rx.icon(tag="clock_3", size=15, color=MUTED),
                                rx.text(
                                    AppState.selected_time,
                                    color=FOREGROUND,
                                    font_size="0.7rem",
                                ),
                                align="center",
                                gap="8px",
                            ),
                            rx.button(
                                rx.icon(tag="check", size=15, aria_hidden=True),
                                "Confirmar Agendamento",
                                type="button",
                                on_click=AppState.confirm_booking,
                                disabled=AppState.is_loading
                                | (AppState.selected_time == ""),
                                width="100%",
                                background_color=ACCENT,
                                color="#17140f",
                                font_size="0.68rem",
                                font_weight="700",
                                border_radius="7px",
                                margin_top="5px",
                            ),
                            align="stretch",
                            spacing="4",
                        ),
                    ),
                    flex="1 1 190px",
                    min_width="190px",
                ),
                align="start",
                flex_wrap="wrap",
                gap="8px",
                width="100%",
            ),
            align="stretch",
            spacing="4",
            width="100%",
        ),
    )


def profile_page() -> rx.Component:
    return _customer_page(
        active_path="/",
        links=PORTAL_LINKS,
        content=rx.vstack(
            rx.heading("Minha Conta", as_="h1", size="5", color=FOREGROUND),
            rx.flex(
                rx.box(
                    rx.icon(tag="user_round", size=34, color="#d2d0cb", aria_hidden=True),
                    background_color="#596270",
                    border_radius="50%",
                    width="64px",
                    height="64px",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                ),
                rx.vstack(
                    rx.text(
                        AppState.user_name,
                        color=FOREGROUND,
                        font_size="1.05rem",
                        font_weight="700",
                    ),
                    rx.text("Cliente desde 2026", color=MUTED, font_size="0.77rem"),
                    align="start",
                    spacing="1",
                ),
                align="center",
                gap="14px",
                background_color="#10100f",
                border=f"1px solid {SURFACE_BORDER}",
                border_radius="10px",
                padding="16px",
                width="100%",
            ),
            rx.box(
                _card(
                    "Informações Pessoais",
                    rx.vstack(
                        rx.vstack(
                            rx.el.label(
                                "Nome completo",
                                color=MUTED,
                                font_size="0.75rem",
                                html_for="profile-name",
                            ),
                            rx.el.input(
                                id="profile-name",
                                type="text",
                                value=AppState.profile_name,
                                on_change=AppState.set_profile_name,
                                aria_label="Nome completo",
                                background_color="#111110",
                                color=FOREGROUND,
                                border=f"1px solid {SURFACE_BORDER}",
                                border_radius="7px",
                                padding="10px 12px",
                                width="100%",
                            ),
                            align="stretch",
                            spacing="1",
                            width="100%",
                        ),
                        rx.vstack(
                            rx.el.label(
                                "E-mail",
                                color=MUTED,
                                font_size="0.75rem",
                                html_for="profile-email",
                            ),
                            rx.el.input(
                                id="profile-email",
                                type="email",
                                value=AppState.profile_email,
                                on_change=AppState.set_profile_email,
                                aria_label="E-mail",
                                background_color="#111110",
                                color=FOREGROUND,
                                border=f"1px solid {SURFACE_BORDER}",
                                border_radius="7px",
                                padding="10px 12px",
                                width="100%",
                            ),
                            align="stretch",
                            spacing="1",
                            width="100%",
                        ),
                        rx.vstack(
                            rx.el.label(
                                "Telefone / WhatsApp",
                                color=MUTED,
                                font_size="0.75rem",
                                html_for="profile-phone",
                            ),
                            rx.el.input(
                                id="profile-phone",
                                type="tel",
                                value=AppState.profile_phone,
                                on_change=AppState.set_profile_phone,
                                aria_label="Telefone / WhatsApp",
                                background_color="#111110",
                                color=FOREGROUND,
                                border=f"1px solid {SURFACE_BORDER}",
                                border_radius="7px",
                                padding="10px 12px",
                                width="100%",
                            ),
                            align="stretch",
                            spacing="1",
                            width="100%",
                        ),
                        rx.button(
                            "Salvar Alterações",
                            type="button",
                            on_click=AppState.save_profile,
                            color="#17140f",
                            background_color=ACCENT,
                            border_radius="7px",
                            padding="10px 16px",
                            font_weight="700",
                            align_self="start",
                            margin_top="4px",
                        ),
                        align="stretch",
                        spacing="4",
                    ),
                ),
                flex="1 1 420px",
            ),
            align="stretch",
            spacing="4",
            width="100%",
        ),
    )
