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
    SUCCESS,
    SURFACE,
    SURFACE_RAISED,
    SURFACE_BORDER,
    public_layout,
)


PORTAL_LINKS = [
    ("Início", "/"),
    ("Meus Agendamentos", "/agendamentos"),
    ("Serviços", "/servicos"),
    ("Meu Perfil", "/perfil"),
    ("Histórico", "/historico"),
    ("Sair", "/login"),
]
CATALOG_LINKS = PORTAL_LINKS
APPOINTMENT_LINKS = PORTAL_LINKS
BOOKING_LINKS = PORTAL_LINKS

_SERVICE_IMAGE_ALIASES = (
    ("Corte Masculino", "service_haircut.jpg"),
    ("Barba", "service_beard.jpg"),
    ("Combo", "service_combo.jpg"),
    ("corte + Barba", "service_combo.jpg"),
    ("Corte + Barba", "service_combo.jpg"),
    ("Sobrancelha", "service_eyebrow.jpg"),
    ("Pezinho / Acabamento", "service_edgeup.jpg"),
    ("Hidratação Capilar", "service_hydration.jpg"),
)
_SERVICE_IMAGE_BY_TITLE = {
    title.strip().casefold(): image for title, image in _SERVICE_IMAGE_ALIASES
}


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
        rx.heading(title, as_="h2", size="4", color=FOREGROUND, margin_bottom="16px"),
        content,
        background_color=SURFACE,
        border=f"1px solid {SURFACE_BORDER}",
        border_radius="14px",
        padding="20px",
        width="100%",
        box_shadow="0 12px 32px #00000033",
    )


def _service_image_name(title: str) -> str:
    return _SERVICE_IMAGE_BY_TITLE.get(
        title.strip().casefold(),
        "service_haircut.jpg",
    )


def _service_image_source(title: str | rx.Var[str]) -> rx.Var[str]:
    if isinstance(title, str):
        return rx.asset(_service_image_name(title))

    source = rx.asset("service_haircut.jpg")
    for alias, image in reversed(_SERVICE_IMAGE_ALIASES):
        source = rx.cond(title == alias, rx.asset(image), source)
    return source


def _service_photo(service: ServiceRecord) -> rx.Component:
    return rx.image(
        src=_service_image_source(service["title"]),
        alt="Imagem ilustrativa do serviço",
        object_fit="cover",
        object_position="center",
        width="100%",
        height="100%",
        loading="lazy",
    )


def _coming_soon_button(label: str) -> rx.Component:
    return rx.button(
        label,
        rx.text(
            "Em breve",
            font_size="0.62rem",
            font_weight="700",
            white_space="nowrap",
        ),
        type="button",
        disabled=True,
        aria_label=f"{label}, Em breve",
        color=MUTED,
        background_color=SURFACE_RAISED,
        border=f"1px solid {SURFACE_BORDER}",
        border_radius="8px",
        padding="8px 10px",
        display="inline-flex",
        align_items="center",
        justify_content="center",
        gap="7px",
        opacity="0.8",
        cursor="not-allowed",
    )


def _service_card(service: ServiceRecord) -> rx.Component:
    return rx.vstack(
        rx.box(
            _service_photo(service),
            height="112px",
            width="100%",
            border_radius="10px",
            overflow="hidden",
            background_color=SURFACE_RAISED,
        ),
        rx.vstack(
            rx.heading(service["title"], as_="h3", size="3", color=FOREGROUND),
            rx.text(
                service["duration_display"],
                color=MUTED,
                font_size="0.78rem",
            ),
            rx.text(
                service["price_display"],
                color=ACCENT,
                font_size="0.9rem",
                font_weight="700",
            ),
            rx.button(
                "Agendar",
                type="button",
                on_click=AppState.start_booking(service["id"]),
                color="#090909",
                background_color=ACCENT,
                border_radius="9px",
                padding="9px 12px",
                font_size="0.78rem",
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
        background_color=SURFACE_RAISED,
        border=f"1px solid {SURFACE_BORDER}",
        border_radius="12px",
        padding="14px",
        spacing="1",
        align="stretch",
        flex="1 1 220px",
        max_width="320px",
    )


def _catalog_service_card(service: ServiceRecord) -> rx.Component:
    return rx.vstack(
        rx.flex(
            rx.box(
                _service_photo(service),
                width="104px",
                height="104px",
                flex_shrink="0",
                border_radius="10px",
                overflow="hidden",
            ),
            rx.vstack(
                rx.heading(
                    service["title"],
                    as_="h2",
                    size="3",
                    color=FOREGROUND,
                ),
                rx.text(
                    service["description"],
                    color=MUTED,
                    font_size="0.8rem",
                    line_height="1.5",
                ),
                align="start",
                spacing="2",
                flex="1",
                min_width="0",
            ),
            align="start",
            gap="14px",
            width="100%",
        ),
        rx.flex(
            rx.flex(
                rx.icon(tag="clock_3", size=14, color=MUTED, aria_hidden=True),
                rx.text(service["duration_display"], color=MUTED, font_size="0.76rem"),
                rx.text("·", color=MUTED),
                rx.text(
                    service["price_display"],
                    color=ACCENT,
                    font_size="0.84rem",
                    font_weight="700",
                ),
                align="center",
                gap="6px",
                flex_wrap="wrap",
            ),
            rx.button(
                "Selecionar",
                rx.icon(tag="chevron_right", size=14, aria_hidden=True),
                type="button",
                on_click=AppState.start_booking(service["id"]),
                color=ACCENT,
                background_color="transparent",
                border=f"1px solid {ACCENT}",
                border_radius="8px",
                padding="8px 10px",
                font_size="0.72rem",
                font_weight="700",
                display="inline-flex",
                align_items="center",
                gap="4px",
                _focus={
                    "outline": f"2px solid {FOREGROUND}",
                    "outline_offset": "2px",
                },
            ),
            align="center",
            justify="between",
            flex_wrap="wrap",
            gap="10px",
            width="100%",
            border_top=f"1px solid {SURFACE_BORDER}",
            padding_top="12px",
        ),
        align="stretch",
        spacing="3",
        background_color=SURFACE,
        border=f"1px solid {SURFACE_BORDER}",
        border_radius="12px",
        padding="14px",
        min_width="0",
        width="100%",
        _hover={"border_color": ACCENT},
    )


def _barber_card(barber: BarberRecord) -> rx.Component:
    return rx.vstack(
        rx.box(
            rx.icon(tag="user_round", size=30, color="#d2d0cb", aria_hidden=True),
            background_image=(
                "linear-gradient(145deg, #30210a 0%, #211d18 65%, #121212 100%)"
            ),
            border_radius="10px",
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
            color="#090909",
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
        background_color=SURFACE_RAISED,
        border=f"1px solid {SURFACE_BORDER}",
        border_radius="12px",
        padding="14px",
        flex="1 1 240px",
        max_width="340px",
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
            _appointment_photo(service),
            border_radius="10px",
            width="76px",
            height="76px",
            overflow="hidden",
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
                color=rx.cond(status == "Concluído", "#d9ffe7", status_color),
                background_color=rx.cond(
                    status == "Concluído",
                    SUCCESS,
                    SURFACE_RAISED,
                ),
                border=f"1px solid {SURFACE_BORDER}",
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
        padding="16px 0",
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


def _appointment_photo(service_title: str | rx.Var[str]) -> rx.Component:
    return rx.image(
        src=_service_image_source(service_title),
        alt="Imagem ilustrativa do serviço",
        object_fit="cover",
        object_position="center",
        width="100%",
        height="100%",
        loading="lazy",
    )


def _featured_appointment(item: AppointmentRecord) -> rx.Component:
    return rx.flex(
        rx.box(
            _appointment_photo(item["service_title"]),
            width="112px",
            height="112px",
            flex_shrink="0",
            border_radius="10px",
            overflow="hidden",
        ),
        rx.vstack(
            rx.flex(
                rx.heading(
                    item["service_title"],
                    as_="h3",
                    size="3",
                    color=FOREGROUND,
                ),
                rx.text(
                    item["status_label"],
                    color=rx.cond(
                        item["status"] == "confirmed",
                        "#d9ffe7",
                        FOREGROUND,
                    ),
                    background_color=rx.cond(
                        item["status"] == "confirmed",
                        SUCCESS,
                        SURFACE_RAISED,
                    ),
                    border_radius="999px",
                    padding="5px 10px",
                    font_size="0.68rem",
                    font_weight="700",
                ),
                align="center",
                justify="between",
                flex_wrap="wrap",
                gap="8px",
                width="100%",
            ),
            rx.text("Barbeiro: ", item["barber_name"], color=MUTED, font_size="0.8rem"),
            rx.flex(
                rx.icon(tag="calendar_days", size=14, color=ACCENT, aria_hidden=True),
                rx.text(item["date_display"], color=FOREGROUND, font_size="0.78rem"),
                rx.icon(tag="clock_3", size=14, color=ACCENT, aria_hidden=True),
                rx.text(item["time"], color=FOREGROUND, font_size="0.78rem"),
                align="center",
                flex_wrap="wrap",
                gap="7px",
            ),
            rx.text(
                item["price_display"],
                color=ACCENT,
                font_size="0.92rem",
                font_weight="700",
            ),
            align="stretch",
            spacing="2",
            flex="1",
            min_width="0",
        ),
        rx.vstack(
            rx.button(
                "Remarcar",
                type="button",
                on_click=AppState.begin_reschedule(item["id"]),
                color="#090909",
                background_color=ACCENT,
                border_radius="8px",
                padding="9px 12px",
                font_size="0.74rem",
                font_weight="700",
                width="100%",
            ),
            rx.cond(
                (item["status"] == "confirmed") | (item["status"] == "pending"),
                rx.button(
                    "Cancelar Agendamento",
                    type="button",
                    on_click=AppState.cancel_client_appointment(item["id"]),
                    color=ACCENT,
                    background_color="transparent",
                    border=f"1px solid {ACCENT}",
                    border_radius="8px",
                    padding="9px 12px",
                    font_size="0.74rem",
                    font_weight="700",
                    width="100%",
                    _focus={
                        "outline": f"2px solid {FOREGROUND}",
                        "outline_offset": "2px",
                    },
                ),
                rx.fragment(),
            ),
            rx.button(
                "Ver Detalhes",
                type="button",
                on_click=AppState.open_appointment_details(item["id"]),
                color=ACCENT,
                background_color="transparent",
                border=f"1px solid {ACCENT}",
                border_radius="8px",
                padding="9px 12px",
                font_size="0.74rem",
                font_weight="700",
                width="100%",
            ),
            align="stretch",
            justify="center",
            width="100%",
            max_width="220px",
        ),
        align="center",
        flex_wrap="wrap",
        gap="14px",
        width="100%",
        background_color=SURFACE_RAISED,
        border=f"1px solid {SURFACE_BORDER}",
        border_radius="12px",
        padding="14px",
    )


def _mini_history_item(item: AppointmentRecord) -> rx.Component:
    return rx.flex(
        rx.box(
            _appointment_photo(item["service_title"]),
            width="54px",
            height="54px",
            flex_shrink="0",
            border_radius="8px",
            overflow="hidden",
        ),
        rx.vstack(
            rx.text(
                item["service_title"],
                color=FOREGROUND,
                font_size="0.78rem",
                font_weight="600",
            ),
            rx.text(
                item["date_display"],
                " · ",
                item["time"],
                color=MUTED,
                font_size="0.7rem",
            ),
            align="start",
            spacing="1",
            flex="1",
            min_width="0",
        ),
        rx.text(
            item["status_label"],
            color=rx.cond(item["status"] == "completed", "#d9ffe7", FOREGROUND),
            background_color=rx.cond(
                item["status"] == "completed",
                SUCCESS,
                SURFACE_RAISED,
            ),
            border_radius="999px",
            padding="4px 8px",
            font_size="0.62rem",
            font_weight="700",
            white_space="nowrap",
        ),
        align="center",
        gap="9px",
        width="100%",
        padding="9px 0",
        border_bottom=f"1px solid {SURFACE_BORDER}",
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
            padding="24px",
            class_name="px-4 md:px-8",
        ),
        links=links or PORTAL_LINKS,
        active_path=active_path,
    )


def customer_portal() -> rx.Component:
    return _customer_page(
        content_max_width="1180px",
        content=rx.vstack(
            rx.flex(
                rx.vstack(
                    rx.heading(
                        "Olá, ",
                        AppState.greeting_name,
                        "!",
                        as_="h1",
                        size="5",
                        color=FOREGROUND,
                    ),
                    rx.text(
                        "Bem-vindo de volta ao BarberFlow.",
                        color=MUTED,
                        font_size="0.82rem",
                    ),
                    align="start",
                    spacing="1",
                ),
                rx.link(
                    rx.icon(tag="calendar_plus", size=15, aria_hidden=True),
                    "Agendar Agora",
                    href="/agendar",
                    color="#090909",
                    background_color=ACCENT,
                    border_radius="9px",
                    padding="11px 16px",
                    font_size="0.8rem",
                    font_weight="700",
                    text_decoration="none",
                    display="flex",
                    align_items="center",
                    gap="7px",
                    _focus={
                        "outline": f"2px solid {FOREGROUND}",
                        "outline_offset": "2px",
                    },
                ),
                align="center",
                justify="between",
                flex_wrap="wrap",
                gap="12px",
                width="100%",
            ),
            rx.flex(
                rx.box(
                    _card(
                        "Seu próximo agendamento",
                        rx.vstack(
                            rx.flex(
                                rx.link(
                                    "Ver todos",
                                    href="/agendamentos",
                                    color=ACCENT,
                                    font_weight="700",
                                    text_decoration="none",
                                ),
                                align="center",
                                justify="end",
                                flex_wrap="wrap",
                                gap="10px",
                                width="100%",
                            ),
                            rx.cond(
                                AppState.next_appointments.length() == 0,
                                rx.cond(
                                    AppState.is_loading,
                                    rx.text(
                                        "Carregando agendamentos...",
                                        color=MUTED,
                                        role="status",
                                    ),
                                    rx.text(
                                        "Você ainda não tem próximos agendamentos.",
                                        color=MUTED,
                                    ),
                                ),
                                rx.foreach(
                                    AppState.next_appointments,
                                    _featured_appointment,
                                ),
                            ),
                            align="stretch",
                            spacing="3",
                        ),
                    ),
                    flex="1 1 480px",
                    min_width="0",
                ),
                rx.box(
                    rx.vstack(
                        rx.icon(
                            tag="calendar_plus",
                            size=38,
                            color=ACCENT,
                            aria_hidden=True,
                        ),
                        rx.heading(
                            "Agende seu próximo horário",
                            as_="h2",
                            size="4",
                            color=FOREGROUND,
                            max_width="280px",
                        ),
                        rx.text(
                            "Escolha o serviço, o barbeiro e o melhor horário para você.",
                            color=MUTED,
                            font_size="0.82rem",
                            max_width="300px",
                        ),
                        rx.link(
                            "Agendar Agora",
                            href="/agendar",
                            color="#090909",
                            background_color=ACCENT,
                            border_radius="9px",
                            padding="11px 16px",
                            font_size="0.78rem",
                            font_weight="700",
                            text_decoration="none",
                            _focus={
                                "outline": f"2px solid {FOREGROUND}",
                                "outline_offset": "2px",
                            },
                        ),
                        align="start",
                        spacing="3",
                        justify="center",
                        width="100%",
                        min_height="260px",
                        background_image=(
                            f"linear-gradient(90deg, #090909f2 0%, #090909cc 58%, #09090966 100%), "
                            f"url('{rx.asset('barbershop_chair.jpg')}')"
                        ),
                        background_size="cover",
                        background_position="center",
                        border=f"1px solid {SURFACE_BORDER}",
                        border_radius="14px",
                        padding="24px",
                        box_shadow="0 12px 32px #00000055",
                    ),
                    flex="1 1 420px",
                    min_width="0",
                ),
                align="start",
                flex_wrap="wrap",
                gap="18px",
                width="100%",
            ),
            rx.flex(
                rx.box(
                    _card(
                        "Nossos Serviços",
                        rx.vstack(
                            rx.flex(
                                rx.text(
                                    "Escolha seu próximo atendimento.",
                                    color=MUTED,
                                    font_size="0.8rem",
                                ),
                                rx.link(
                                    "Ver todos",
                                    href="/servicos",
                                    color=ACCENT,
                                    font_weight="700",
                                    text_decoration="none",
                                ),
                                align="center",
                                justify="between",
                                gap="10px",
                                width="100%",
                            ),
                            rx.cond(
                                AppState.services.length() == 0,
                                rx.cond(
                                    AppState.is_loading,
                                    rx.text("Carregando serviços...", color=MUTED),
                                    rx.text(
                                        "Nenhum serviço disponível no momento.",
                                        color=MUTED,
                                    ),
                                ),
                                rx.grid(
                                    rx.foreach(
                                        AppState.services[:4],
                                        _service_card,
                                    ),
                                    gap="12px",
                                    width="100%",
                                    class_name="grid grid-cols-2 xl:grid-cols-4",
                                ),
                            ),
                            align="stretch",
                            spacing="3",
                        ),
                    ),
                    flex="2 1 620px",
                    min_width="0",
                ),
                rx.box(
                    _card(
                        "Meu Histórico",
                        rx.vstack(
                            rx.flex(
                                rx.text(
                                    "Atendimentos anteriores",
                                    color=MUTED,
                                    font_size="0.8rem",
                                ),
                                rx.link(
                                    "Ver todos",
                                    href="/historico",
                                    color=ACCENT,
                                    font_weight="700",
                                    text_decoration="none",
                                ),
                                align="center",
                                justify="between",
                                gap="8px",
                                width="100%",
                            ),
                            rx.cond(
                                AppState.historical_appointments.length() == 0,
                                rx.cond(
                                    AppState.is_loading,
                                    rx.text(
                                        "Carregando histórico...",
                                        color=MUTED,
                                        role="status",
                                    ),
                                    rx.text(
                                        "Nenhum atendimento no histórico.",
                                        color=MUTED,
                                    ),
                                ),
                                rx.vstack(
                                    rx.foreach(
                                        AppState.historical_appointments[:3],
                                        _mini_history_item,
                                    ),
                                    align="stretch",
                                    spacing="0",
                                ),
                            ),
                            align="stretch",
                            spacing="3",
                        ),
                    ),
                    flex="1 1 340px",
                    min_width="0",
                ),
                align="start",
                flex_wrap="wrap",
                gap="18px",
                width="100%",
            ),
            rx.flex(
                rx.icon(tag="crown", size=26, color=ACCENT, aria_hidden=True),
                rx.vstack(
                    rx.text(
                        "Cuide do seu estilo!",
                        color=FOREGROUND,
                        font_size="1.05rem",
                        font_weight="700",
                    ),
                    rx.text(
                        "Uma barbearia completa, sempre ao seu lado.",
                        color=MUTED,
                        font_size="0.82rem",
                    ),
                    align="start",
                    spacing="1",
                ),
                align="center",
                gap="14px",
                width="100%",
                min_height="112px",
                background_image=(
                    f"linear-gradient(90deg, #090909f0 0%, #090909cc 55%, #09090966 100%), "
                    f"url('{rx.asset('barbershop_tools.jpg')}')"
                ),
                background_size="cover",
                background_position="center",
                border=f"1px solid {SURFACE_BORDER}",
                border_radius="14px",
                padding="18px 22px",
                overflow="hidden",
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
            rx.box(
                rx.vstack(
                    rx.heading(
                        "Serviços de qualidade para um visual ainda melhor.",
                        as_="h1",
                        size="6",
                        color=FOREGROUND,
                        max_width="600px",
                    ),
                    rx.text(
                        "Corte, barba e muito mais, com os melhores serviços.",
                        color=MUTED,
                        font_size="0.9rem",
                    ),
                    align="start",
                    spacing="3",
                    max_width="620px",
                    justify="center",
                    min_height="190px",
                ),
                background_image=(
                    f"linear-gradient(90deg, #090909f5 0%, #090909d9 48%, #09090955 100%), "
                    f"url('{rx.asset('barbershop_tools.jpg')}')"
                ),
                background_size="cover",
                background_position="center",
                border=f"1px solid {ACCENT}",
                border_radius="14px",
                padding="24px",
                width="100%",
                box_shadow="0 12px 32px #00000055",
            ),
            rx.flex(
                rx.flex(
                    rx.link(
                        "Serviços",
                        href="/servicos",
                        color="#090909",
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
                        background_color=SURFACE_RAISED,
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
                    background_color=SURFACE_RAISED,
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
                    background_color=SURFACE_RAISED,
                    color=FOREGROUND,
                    border=f"1px solid {SURFACE_BORDER}",
                    border_radius="8px",
                    padding="9px 12px",
                    font_size="0.77rem",
                    width="200px",
                    max_width="100%",
                    _focus={
                        "outline": f"2px solid {ACCENT}",
                        "outline_offset": "2px",
                    },
                ),
                justify="between",
                align="center",
                flex_wrap="wrap",
                gap="12px",
                width="100%",
            ),
            rx.grid(
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
                    rx.foreach(AppState.filtered_services, _catalog_service_card),
                ),
                gap="16px",
                width="100%",
                class_name="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3",
            ),
            rx.flex(
                rx.vstack(
                    rx.heading(
                        "Por que escolher o BarberFlow?",
                        as_="h2",
                        size="4",
                        color=FOREGROUND,
                    ),
                    rx.text(
                        "Qualidade, conforto e um atendimento feito para você.",
                        color=MUTED,
                        font_size="0.76rem",
                    ),
                    align="start",
                    spacing="1",
                    flex="1",
                ),
                *[
                    rx.vstack(
                        rx.icon(tag=icon, size=23, color=ACCENT, aria_hidden=True),
                        rx.text(
                            label,
                            color=FOREGROUND,
                            font_size="0.7rem",
                            font_weight="600",
                            text_align="center",
                        ),
                        align="center",
                        justify="center",
                        spacing="2",
                        flex="1 1 130px",
                        padding="8px",
                        border_left=f"1px solid {SURFACE_BORDER}",
                    )
                    for icon, label in [
                        ("scissors", "Barbeiros Especializados"),
                        ("shield_check", "Ambiente Seguro"),
                        ("zap", "Agendamento Rápido"),
                    ]
                ],
                align="center",
                flex_wrap="wrap",
                gap="12px",
                width="100%",
                background_image=(
                    f"linear-gradient(90deg, #090909eb 0%, #090909cc 100%), "
                    f"url('{rx.asset('barbershop_tools.jpg')}')"
                ),
                background_size="cover",
                background_position="center",
                border=f"1px solid {SURFACE_BORDER}",
                border_radius="12px",
                padding="18px",
            ),
            align="stretch",
            spacing="5",
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
                    background_color=SURFACE_RAISED,
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
                    color="#090909",
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
                background_color=SURFACE_RAISED,
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


def _history_appointment_card(item: AppointmentRecord) -> rx.Component:
    return rx.flex(
        rx.box(
            _appointment_photo(item["service_title"]),
            width="96px",
            height="96px",
            flex_shrink="0",
            border_radius="10px",
            overflow="hidden",
        ),
        rx.vstack(
            rx.heading(
                item["service_title"],
                as_="h3",
                size="3",
                color=FOREGROUND,
            ),
            rx.text("Barbeiro: ", item["barber_name"], color=MUTED, font_size="0.76rem"),
            rx.text(
                item["date_display"],
                " · ",
                item["time"],
                color=MUTED,
                font_size="0.76rem",
            ),
            align="start",
            spacing="1",
            flex="1",
            min_width="0",
        ),
        rx.vstack(
            rx.text(
                item["status_label"],
                color=rx.cond(item["status"] == "completed", "#d9ffe7", FOREGROUND),
                background_color=rx.cond(
                    item["status"] == "completed",
                    SUCCESS,
                    SURFACE_RAISED,
                ),
                border_radius="999px",
                padding="5px 10px",
                font_size="0.68rem",
                font_weight="700",
                white_space="nowrap",
            ),
            rx.text(
                item["price_display"],
                color=ACCENT,
                font_size="0.92rem",
                font_weight="700",
            ),
            _coming_soon_button("Detalhes"),
            align="end",
            spacing="2",
        ),
        align="center",
        flex_wrap="wrap",
        gap="14px",
        width="100%",
        background_color=SURFACE_RAISED,
        border=f"1px solid {SURFACE_BORDER}",
        border_radius="12px",
        padding="14px",
    )


def _brl_total(cents: rx.Var[int]) -> rx.Var[str]:
    remainder = cents % 100
    formatted_cents = rx.cond(
        remainder < 10,
        "0" + remainder.to_string(),
        remainder.to_string(),
    )
    return "R$ " + (cents // 100).to_string() + "," + formatted_cents


def appointments_page() -> rx.Component:
    upcoming_content = rx.vstack(
        _card(
            "Próximo Agendamento",
            rx.cond(
                AppState.upcoming_appointments.length() == 0,
                rx.cond(
                    AppState.is_loading,
                    rx.text("Carregando agendamentos...", color=MUTED, role="status"),
                    rx.vstack(
                        rx.text(
                            "Você ainda não tem próximos agendamentos.",
                            color=MUTED,
                        ),
                        rx.link(
                            "Agendar um horário",
                            href="/agendar",
                            color=ACCENT,
                            text_decoration="none",
                        ),
                        align="start",
                        spacing="2",
                    ),
                ),
                rx.vstack(
                    rx.foreach(AppState.next_appointments, _featured_appointment),
                    align="stretch",
                    spacing="3",
                ),
            ),
        ),
        _card(
            "Todos os Próximos Agendamentos",
            rx.cond(
                AppState.upcoming_appointments.length() == 0,
                rx.cond(
                    AppState.is_loading,
                    rx.text("Carregando agendamentos...", color=MUTED, role="status"),
                    rx.text("Nenhum próximo agendamento.", color=MUTED),
                ),
                rx.vstack(
                    rx.foreach(AppState.filtered_upcoming_appointments, _appointment_item),
                    align="stretch",
                    spacing="0",
                ),
            ),
        ),
        _card(
            "Agendamentos Anteriores",
            rx.cond(
                AppState.historical_appointments.length() == 0,
                rx.cond(
                    AppState.is_loading,
                    rx.text("Carregando histórico...", color=MUTED, role="status"),
                    rx.text("Nenhum atendimento anterior.", color=MUTED),
                ),
                rx.vstack(
                    rx.foreach(AppState.filtered_historical_appointments, _mini_history_item),
                    align="stretch",
                    spacing="0",
                ),
            ),
        ),
        align="stretch",
        spacing="4",
        width="100%",
    )
    history_content = _card(
        "Histórico",
        rx.cond(
            AppState.historical_appointments.length() == 0,
            rx.cond(
                AppState.is_loading,
                rx.text("Carregando histórico...", color=MUTED, role="status"),
                rx.text("Nenhum atendimento no histórico.", color=MUTED),
            ),
            rx.vstack(
                rx.foreach(
                    AppState.filtered_historical_appointments,
                    _history_appointment_card,
                ),
                align="stretch",
                spacing="3",
            ),
        ),
    )
    return _customer_page(
        active_path="/agendamentos",
        links=APPOINTMENT_LINKS,
        content=rx.vstack(
            _page_header(
                "Área do cliente",
                "Meus Agendamentos",
                "Confira seus próximos horários e atendimentos anteriores.",
            ),
            rx.cond(
                AppState.selected_appointment != None,
                _card(
                    "Detalhes do Agendamento",
                    rx.vstack(
                        rx.text(
                            AppState.selected_appointment["service_title"],
                            color=FOREGROUND,
                            font_weight="700",
                        ),
                        rx.text(
                            "Barbeiro: " + AppState.selected_appointment["barber_name"],
                            color=MUTED,
                        ),
                        rx.text(
                            AppState.selected_appointment["date_display"]
                            + " às "
                            + AppState.selected_appointment["time"],
                            color=FOREGROUND,
                        ),
                        rx.text(
                            AppState.selected_appointment["price_display"],
                            color=ACCENT,
                            font_weight="700",
                        ),
                        rx.cond(
                            AppState.reschedule_appointment_id != "",
                            rx.vstack(
                                rx.el.input(
                                    type="date",
                                    value=AppState.reschedule_date,
                                    on_change=AppState.set_reschedule_date,
                                    on_blur=AppState.load_reschedule_times,
                                    aria_label="Nova data",
                                    background_color=SURFACE_RAISED,
                                    color=FOREGROUND,
                                    border=f"1px solid {SURFACE_BORDER}",
                                    border_radius="7px",
                                    padding="8px 10px",
                                ),
                                rx.select(
                                    AppState.reschedule_available_times,
                                    value=AppState.reschedule_time,
                                    on_change=AppState.select_reschedule_time,
                                    placeholder="Selecione o novo horário",
                                ),
                                rx.button(
                                    "Confirmar Remarcação",
                                    type="button",
                                    on_click=AppState.confirm_reschedule,
                                    color="#090909",
                                    background_color=ACCENT,
                                    border_radius="8px",
                                    padding="10px 12px",
                                ),
                                align="stretch",
                                spacing="2",
                            ),
                            rx.fragment(),
                        ),
                        rx.button(
                            "Fechar",
                            type="button",
                            on_click=AppState.close_appointment_details,
                            color=ACCENT,
                            background_color="transparent",
                            border=f"1px solid {ACCENT}",
                            border_radius="8px",
                            padding="8px 10px",
                        ),
                        align="stretch",
                        spacing="2",
                    ),
                ),
                rx.fragment(),
            ),
            rx.flex(
                rx.flex(
                    rx.button(
                        "Próximos Agendamentos",
                        on_click=AppState.set_appointment_filter("upcoming"),
                        type="button",
                        aria_pressed=AppState.appointment_filter != "history",
                        color=rx.cond(
                            AppState.appointment_filter != "history",
                            "#090909",
                            FOREGROUND,
                        ),
                        font_weight="700",
                        background_color=rx.cond(
                            AppState.appointment_filter != "history",
                            ACCENT,
                            SURFACE_RAISED,
                        ),
                        border=f"1px solid {SURFACE_BORDER}",
                        border_radius="9px",
                        padding="10px 14px",
                        _focus={
                            "outline": f"2px solid {ACCENT}",
                            "outline_offset": "2px",
                        },
                    ),
                    rx.button(
                        "Histórico",
                        on_click=AppState.set_appointment_filter("history"),
                        type="button",
                        aria_pressed=AppState.appointment_filter == "history",
                        color=rx.cond(
                            AppState.appointment_filter == "history",
                            "#090909",
                            FOREGROUND,
                        ),
                        font_weight="700",
                        background_color=rx.cond(
                            AppState.appointment_filter == "history",
                            ACCENT,
                            SURFACE_RAISED,
                        ),
                        border=f"1px solid {SURFACE_BORDER}",
                        border_radius="9px",
                        padding="10px 14px",
                        _focus={
                            "outline": f"2px solid {ACCENT}",
                            "outline_offset": "2px",
                        },
                    ),
                    align="center",
                    flex_wrap="wrap",
                    gap="8px",
                ),
                rx.select(
                    ["Todos", "7 dias", "30 dias", "90 dias"],
                    value=rx.cond(
                        AppState.appointment_filter == "history",
                        rx.cond(
                            AppState.history_period_filter == "all",
                            "Todos",
                            AppState.history_period_filter + " dias",
                        ),
                        rx.cond(
                            AppState.upcoming_period_filter == "all",
                            "Todos",
                            AppState.upcoming_period_filter + " dias",
                        ),
                    ),
                    on_change=AppState.set_period_filter,
                    size="2",
                    aria_label="Filtrar agendamentos por período",
                ),
                align="center",
                justify="between",
                flex_wrap="wrap",
                gap="12px",
                width="100%",
            ),
            rx.flex(
                rx.box(
                    rx.cond(
                        AppState.appointment_filter == "history",
                        history_content,
                        upcoming_content,
                    ),
                    flex="1 1 620px",
                    min_width="0",
                ),
                rx.vstack(
                    _card(
                        "Resumo dos Agendamentos",
                        rx.vstack(
                            rx.flex(
                                rx.icon(
                                    tag="calendar_days",
                                    size=25,
                                    color=ACCENT,
                                    aria_hidden=True,
                                ),
                                rx.vstack(
                                    rx.text(
                                        AppState.upcoming_appointments.length(),
                                        color=FOREGROUND,
                                        font_size="1.4rem",
                                        font_weight="700",
                                    ),
                                    rx.text(
                                        "Próximos agendamentos",
                                        color=MUTED,
                                        font_size="0.74rem",
                                    ),
                                    align="start",
                                    spacing="0",
                                ),
                                align="center",
                                gap="12px",
                                width="100%",
                                border_bottom=f"1px solid {SURFACE_BORDER}",
                                padding_bottom="12px",
                            ),
                            rx.flex(
                                rx.icon(
                                    tag="history",
                                    size=25,
                                    color=ACCENT,
                                    aria_hidden=True,
                                ),
                                rx.vstack(
                                    rx.text(
                                        AppState.customer_appointments.length(),
                                        color=FOREGROUND,
                                        font_size="1.4rem",
                                        font_weight="700",
                                    ),
                                    rx.text(
                                        "Registros no total",
                                        color=MUTED,
                                        font_size="0.74rem",
                                    ),
                                    align="start",
                                    spacing="0",
                                ),
                                align="center",
                                gap="12px",
                                width="100%",
                            ),
                            align="stretch",
                            spacing="3",
                        ),
                    ),
                    _card(
                        "Ações Rápidas",
                        rx.vstack(
                            rx.link(
                                "Agendar Novo",
                                href="/agendar",
                                color="#090909",
                                background_color=ACCENT,
                                border_radius="8px",
                                padding="10px 12px",
                                font_size="0.76rem",
                                font_weight="700",
                                text_decoration="none",
                                text_align="center",
                                width="100%",
                            ),
                            rx.link(
                                "Ver Serviços",
                                href="/servicos",
                                color=ACCENT,
                                background_color="transparent",
                                border=f"1px solid {ACCENT}",
                                border_radius="8px",
                                padding="10px 12px",
                                font_size="0.76rem",
                                font_weight="700",
                                text_decoration="none",
                                text_align="center",
                                width="100%",
                            ),
                            align="stretch",
                            spacing="2",
                        ),
                    ),
                    flex="0 1 280px",
                    width="100%",
                    min_width="0",
                ),
                align="start",
                flex_wrap="wrap",
                gap="18px",
                width="100%",
            ),
            align="stretch",
            spacing="4",
            width="100%",
        ),
    )


def history_page() -> rx.Component:
    completed_appointments = AppState.historical_appointments.filter(
        lambda item: item["status"] == "completed"
    )
    total_spent_cents = completed_appointments.reduce(
        lambda total, item: total + item["price_cents"],
        0,
    )
    return _customer_page(
        active_path="/historico",
        links=PORTAL_LINKS,
        content=rx.vstack(
            _page_header(
                "Área do cliente",
                "Meu Histórico",
                "Confira o histórico dos seus atendimentos.",
            ),
            rx.flex(
                rx.flex(
                    rx.button(
                        "Todos",
                        type="button",
                        disabled=True,
                        aria_pressed=True,
                        color="#090909",
                        background_color=ACCENT,
                        border=f"1px solid {ACCENT}",
                        border_radius="999px",
                        padding="9px 16px",
                        font_weight="700",
                    ),
                    *[
                        _coming_soon_button(label)
                        for label in ("Cortes", "Barba", "Combos")
                    ],
                    align="center",
                    flex_wrap="wrap",
                    gap="8px",
                ),
                _coming_soon_button("Período"),
                align="center",
                justify="between",
                flex_wrap="wrap",
                gap="12px",
                width="100%",
            ),
            rx.cond(
                AppState.historical_appointments.length() == 0,
                rx.cond(
                    AppState.is_loading,
                    _card(
                        "Histórico",
                        rx.text(
                            "Carregando histórico...",
                            color=MUTED,
                            role="status",
                        ),
                    ),
                    _card(
                        "Histórico",
                        rx.vstack(
                            rx.text(
                                "Você ainda não tem atendimentos no histórico.",
                                color=MUTED,
                            ),
                            rx.link(
                                "Ver serviços",
                                href="/servicos",
                                color=ACCENT,
                                text_decoration="none",
                            ),
                            align="start",
                            spacing="2",
                        ),
                    ),
                ),
                rx.vstack(
                    rx.foreach(
                        AppState.filtered_historical_appointments,
                        _history_appointment_card,
                    ),
                    align="stretch",
                    spacing="3",
                    width="100%",
                ),
            ),
            _card(
                "Resumo do Histórico",
                rx.flex(
                    rx.vstack(
                        rx.text(
                            "Total gasto com serviços",
                            color=FOREGROUND,
                            font_size="0.8rem",
                            font_weight="600",
                        ),
                        rx.text(
                            _brl_total(total_spent_cents),
                            color=ACCENT,
                            font_size="1.2rem",
                            font_weight="700",
                        ),
                        align="start",
                        spacing="1",
                    ),
                    rx.vstack(
                        rx.text(
                            "Total de atendimentos",
                            color=MUTED,
                            font_size="0.8rem",
                        ),
                        rx.text(
                            completed_appointments.length(),
                            color=FOREGROUND,
                            font_size="1.4rem",
                            font_weight="700",
                        ),
                        align="start",
                        spacing="1",
                    ),
                    align="center",
                    justify="between",
                    flex_wrap="wrap",
                    gap="20px",
                    width="100%",
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
                color="#090909" if active else MUTED,
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
                rx.text(
                    title,
                    color=FOREGROUND,
                    font_size="0.8rem",
                    font_weight="600",
                    line_height="1.35",
                    width="100%",
                    text_align="left",
                    overflow_wrap="anywhere",
                ),
                rx.text(
                    description,
                    color=MUTED,
                    font_size="0.7rem",
                    line_height="1.45",
                    width="100%",
                    text_align="left",
                    overflow_wrap="anywhere",
                ),
                align="start",
                spacing="2",
                flex="1",
                min_width="0",
            ),
            rx.icon(
                tag=rx.cond(selected, "circle_check", "circle"),
                size=16,
                color=rx.cond(selected, ACCENT, MUTED),
                aria_hidden=True,
            ),
            align="start",
            justify="between",
            gap="10px",
            width="100%",
        ),
        type="button",
        aria_pressed=selected,
        on_click=on_click,
        background_color=rx.cond(selected, "#30210a", SURFACE_RAISED),
        border=rx.cond(
            selected,
            f"1px solid {ACCENT}",
            f"1px solid {SURFACE_BORDER}",
        ),
        border_radius="10px",
        padding="12px 10px",
        width="100%",
        min_height="78px",
        display="flex",
        align_items="flex-start",
        gap="10px",
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
        selected=AppState.selected_service_ids.contains(service["id"]),
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
        rx.box(width="30px", height="30px"),
        rx.button(
            rx.text(
                day,
                color=rx.cond(
                    AppState.selected_day == day,
                    "#090909",
                    FOREGROUND,
                ),
                font_size="0.76rem",
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
            border_radius="8px",
            width="30px",
            height="30px",
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
            color=rx.cond(selected, "#090909", FOREGROUND),
            font_size="0.68rem",
            font_weight=rx.cond(selected, "700", "400"),
        ),
        type="button",
        aria_pressed=selected,
        on_click=AppState.select_booking_time(time_value),
        background_color=rx.cond(selected, ACCENT, SURFACE_RAISED),
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
        active_path="/agendamentos",
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
                    flex="1 1 250px",
                    min_width="230px",
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
                    flex="1 1 250px",
                    min_width="230px",
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
                                        font_size="0.68rem",
                                        text_align="center",
                                    )
                                    for day in ("Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom")
                                ],
                                columns="7",
                                width="100%",
                                gap="2px",
                            ),
                            rx.grid(
                                rx.foreach(
                                    AppState.calendar_days,
                                    _booking_calendar_cell,
                                ),
                                columns="7",
                                width="100%",
                                gap="2px",
                                justify_items="center",
                            ),
                            align="stretch",
                            spacing="2",
                        ),
                    ),
                    flex="1 1 280px",
                    min_width="260px",
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
                    flex="1 1 250px",
                    min_width="230px",
                ),
                rx.box(
                    _card(
                        "Resumo do Agendamento",
                        rx.flex(
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
                                flex="1 1 240px",
                            ),
                            rx.flex(
                                rx.icon(tag="calendar_days", size=15, color=MUTED),
                                rx.vstack(
                                    rx.text(
                                        AppState.selected_date_display,
                                        color=FOREGROUND,
                                        font_size="0.7rem",
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
                                    align="start",
                                    spacing="1",
                                ),
                                align="center",
                                gap="8px",
                                flex="0 1 180px",
                            ),
                            rx.button(
                                rx.icon(tag="check", size=15, aria_hidden=True),
                                "Confirmar Agendamento",
                                type="button",
                                on_click=AppState.confirm_booking,
                                disabled=AppState.is_loading
                                | (AppState.selected_time == ""),
                                background_color=ACCENT,
                                color="#090909",
                                font_size="0.68rem",
                                font_weight="700",
                                border_radius="7px",
                                white_space="nowrap",
                                class_name="w-full md:w-auto",
                            ),
                            align="center",
                            justify="between",
                            flex_wrap="wrap",
                            gap="16px",
                            width="100%",
                        ),
                    ),
                    flex="1 1 100%",
                    min_width="0",
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
    profile_card = _card(
        "Meu Perfil",
        rx.vstack(
            rx.flex(
                rx.box(
                    rx.icon(
                        tag="user_round",
                        size=60,
                        color="#d2d0cb",
                        aria_hidden=True,
                    ),
                    background_color=SURFACE_RAISED,
                    border=f"3px solid {ACCENT}",
                    border_radius="50%",
                    width="120px",
                    height="120px",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    flex_shrink="0",
                ),
                rx.vstack(
                    rx.heading(
                        AppState.user_name,
                        as_="h2",
                        size="4",
                        color=FOREGROUND,
                    ),
                    rx.text(AppState.user_email, color=MUTED, font_size="0.8rem"),
                    rx.el.input(
                        type="url",
                        placeholder="URL HTTPS da foto",
                        value=AppState.profile_avatar_url,
                        on_change=AppState.set_profile_avatar_url,
                        aria_label="URL HTTPS da foto",
                        background_color=SURFACE_RAISED,
                        color=FOREGROUND,
                        border=f"1px solid {SURFACE_BORDER}",
                        border_radius="7px",
                        padding="8px 10px",
                        width="220px",
                        max_width="100%",
                    ),
                    align="start",
                    spacing="2",
                    min_width="0",
                ),
                align="center",
                flex_wrap="wrap",
                gap="16px",
                width="100%",
            ),
            rx.flex(
                rx.icon(tag="phone", size=17, color=ACCENT, aria_hidden=True),
                rx.text(
                    AppState.user_phone,
                    color=FOREGROUND,
                    font_size="0.8rem",
                    flex="1",
                ),
                rx.link(
                    "Editar",
                    href="#profile-phone",
                    color=ACCENT,
                    font_size="0.74rem",
                    text_decoration="none",
                ),
                align="center",
                gap="10px",
                width="100%",
                padding_top="12px",
                border_top=f"1px solid {SURFACE_BORDER}",
            ),
            rx.flex(
                rx.icon(tag="mail", size=17, color=ACCENT, aria_hidden=True),
                rx.text(
                    AppState.user_email,
                    color=FOREGROUND,
                    font_size="0.8rem",
                    flex="1",
                ),
                rx.link(
                    "Editar",
                    href="#profile-email",
                    color=ACCENT,
                    font_size="0.74rem",
                    text_decoration="none",
                ),
                align="center",
                gap="10px",
                width="100%",
            ),
            align="stretch",
            spacing="3",
        ),
    )
    personal_info_card = _card(
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
                    background_color=SURFACE_RAISED,
                    color=FOREGROUND,
                    border=f"1px solid {SURFACE_BORDER}",
                    border_radius="7px",
                    padding="10px 12px",
                    width="100%",
                    _focus={
                        "outline": f"2px solid {ACCENT}",
                        "outline_offset": "2px",
                    },
                ),
                align="stretch",
                spacing="1",
                width="100%",
            ),
            rx.vstack(
                rx.el.label(
                    "Telefone",
                    color=MUTED,
                    font_size="0.75rem",
                    html_for="profile-phone",
                ),
                rx.el.input(
                    id="profile-phone",
                    type="tel",
                    value=AppState.profile_phone,
                    on_change=AppState.set_profile_phone,
                    aria_label="Telefone",
                    background_color=SURFACE_RAISED,
                    color=FOREGROUND,
                    border=f"1px solid {SURFACE_BORDER}",
                    border_radius="7px",
                    padding="10px 12px",
                    width="100%",
                    _focus={
                        "outline": f"2px solid {ACCENT}",
                        "outline_offset": "2px",
                    },
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
                    background_color=SURFACE_RAISED,
                    color=FOREGROUND,
                    border=f"1px solid {SURFACE_BORDER}",
                    border_radius="7px",
                    padding="10px 12px",
                    width="100%",
                    _focus={
                        "outline": f"2px solid {ACCENT}",
                        "outline_offset": "2px",
                    },
                ),
                align="stretch",
                spacing="1",
                width="100%",
            ),
            rx.button(
                "Salvar Alterações",
                type="button",
                on_click=AppState.save_profile,
                color="#090909",
                background_color=ACCENT,
                border_radius="9px",
                padding="11px 16px",
                font_weight="700",
                width="100%",
                _focus={
                    "outline": f"2px solid {FOREGROUND}",
                    "outline_offset": "2px",
                },
            ),
            align="stretch",
            spacing="3",
        ),
    )
    security_card = _card(
        "Segurança",
        rx.vstack(
            rx.flex(
                rx.icon(tag="lock_keyhole", size=20, color=ACCENT, aria_hidden=True),
                rx.text(
                    "Senha",
                    color=FOREGROUND,
                    font_size="0.8rem",
                    flex="1",
                ),
                rx.button(
                    "Alterar Senha",
                    type="button",
                    on_click=AppState.change_account_password,
                    color=ACCENT,
                    background_color="transparent",
                    border=f"1px solid {ACCENT}",
                    border_radius="8px",
                    padding="8px 10px",
                    font_size="0.72rem",
                    font_weight="700",
                ),
                align="center",
                gap="10px",
                width="100%",
                padding="10px 0",
                border_bottom=f"1px solid {SURFACE_BORDER}",
            ),
            rx.flex(
                rx.icon(tag="shield_check", size=20, color=ACCENT, aria_hidden=True),
                rx.text(
                    "Autenticação em Duas Etapas",
                    color=FOREGROUND,
                    font_size="0.8rem",
                    flex="1",
                ),
                rx.button(
                    "Configurar",
                    type="button",
                    on_click=AppState.start_totp_setup,
                    color="#090909",
                    background_color=ACCENT,
                    border_radius="8px",
                    padding="8px 10px",
                    font_size="0.72rem",
                    font_weight="700",
                ),
                align="center",
                flex_wrap="wrap",
                gap="10px",
                width="100%",
                padding="10px 0",
                border_bottom=f"1px solid {SURFACE_BORDER}",
            ),
            rx.button(
                "Sair de Todos os Dispositivos",
                type="button",
                on_click=AppState.revoke_all_sessions,
                color="#090909",
                background_color=ACCENT,
                border_radius="8px",
                padding="10px 12px",
                font_size="0.76rem",
                font_weight="700",
                width="100%",
            ),
            align="stretch",
            spacing="3",
        ),
    )
    history_card = _card(
        "Meu Histórico",
        rx.vstack(
            rx.cond(
                AppState.historical_appointments.length() == 0,
                rx.cond(
                    AppState.is_loading,
                    rx.text("Carregando histórico...", color=MUTED, role="status"),
                    rx.text(
                        "Acesse seu histórico completo para ver os atendimentos.",
                        color=MUTED,
                        font_size="0.78rem",
                    ),
                ),
                rx.vstack(
                    rx.foreach(
                        AppState.historical_appointments[:3],
                        _mini_history_item,
                    ),
                    align="stretch",
                    spacing="0",
                ),
            ),
            rx.link(
                "Ver Histórico",
                href="/historico",
                color=ACCENT,
                font_size="0.76rem",
                font_weight="700",
                text_decoration="none",
                align_self="end",
            ),
            align="stretch",
            spacing="3",
        ),
    )
    return _customer_page(
        active_path="/perfil",
        links=PORTAL_LINKS,
        content=rx.vstack(
            _page_header(
                "Área do cliente",
                "Meu Perfil",
                "Gerencie suas informações pessoais e preferências.",
            ),
            rx.grid(
                profile_card,
                personal_info_card,
                security_card,
                history_card,
                gap="16px",
                width="100%",
                class_name="grid grid-cols-1 xl:grid-cols-2",
            ),
            align="stretch",
            spacing="4",
            width="100%",
        ),
    )
