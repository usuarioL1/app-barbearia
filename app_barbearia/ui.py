import reflex as rx

from app_barbearia.state import AppState


BACKGROUND = "#10100f"
SURFACE = "#191917"
SURFACE_BORDER = "#302e29"
FOREGROUND = "#f4f0e8"
MUTED = "#aaa69d"
ACCENT = "#d6a64f"
ERROR = "#d9776b"


def brand() -> rx.Component:
    return rx.link(
        rx.text(
            "BARBERFLOW",
            color=FOREGROUND,
            font_size="1.05rem",
            font_weight="800",
            letter_spacing="0.16em",
        ),
        href="/",
        text_decoration="none",
        aria_label="BarberFlow, início",
        _focus={"outline": f"2px solid {ACCENT}", "outline_offset": "3px"},
    )


def public_layout(
    content: rx.Component,
    links: list[tuple[str, str]] | None = None,
    active_path: str = "/",
) -> rx.Component:
    navigation = links or [
        ("Minha Conta", "/"),
        ("Meus Agendamentos", "/agendamentos"),
        ("Histórico", "/agendamentos#historico"),
        ("Sair", "/login"),
    ]
    icons = {
        "Início": "house",
        "Minha Conta": "user_round",
        "Meus Agendamentos": "calendar_days",
        "Histórico": "clock_3",
        "Serviços": "scissors",
        "Equipe": "users_round",
        "Agendamentos": "calendar_days",
        "Agendar": "calendar_plus",
        "Sair": "log_out",
    }
    return rx.box(
        rx.flex(
            rx.vstack(
                rx.vstack(
                    rx.box(
                        rx.icon(tag="crown", size=18, color=ACCENT, aria_hidden=True),
                        rx.text(
                            "B",
                            color=FOREGROUND,
                            font_size="2.2rem",
                            font_weight="700",
                            line_height="1",
                            font_style="italic",
                        ),
                        align_items="center",
                        justify_content="center",
                        position="relative",
                        height="58px",
                    ),
                    rx.text(
                        "BARBERFLOW",
                        color=FOREGROUND,
                        font_size="0.72rem",
                        font_weight="800",
                        letter_spacing="0.06em",
                    ),
                    rx.text(
                        "SISTEMA DE GERENCIAMENTO",
                        color=ACCENT,
                        font_size="0.34rem",
                        font_weight="700",
                        letter_spacing="0.04em",
                    ),
                    align="center",
                    spacing="1",
                    width="100%",
                    padding="14px 5px 18px",
                    border_bottom=f"1px solid {SURFACE_BORDER}",
                ),
                rx.vstack(
                    *[
                        rx.link(
                            rx.icon(
                                tag=icons.get(label, "circle"),
                                size=15,
                                aria_hidden=True,
                            ),
                            rx.text(
                                label,
                                font_size="0.67rem",
                                line_height="1.25",
                            ),
                            href=target,
                            on_click=AppState.logout if label == "Sair" else None,
                            color="#17140f" if target == active_path else FOREGROUND,
                            background_color=ACCENT
                            if target == active_path
                            else "transparent",
                            border_radius="7px",
                            padding="9px 8px",
                            text_decoration="none",
                            display="flex",
                            align_items="center",
                            gap="8px",
                            width="100%",
                            aria_current="page" if target == active_path else None,
                            _hover={
                                "color": "#17140f"
                                if target == active_path
                                else ACCENT,
                                "background_color": ACCENT
                                if target != active_path
                                else ACCENT,
                            },
                            _focus={
                                "outline": f"2px solid {FOREGROUND}",
                                "outline_offset": "2px",
                            },
                        )
                        for label, target in navigation
                    ],
                    align="stretch",
                    spacing="2",
                    role="navigation",
                    aria_label="Navegação do cliente",
                    width="100%",
                    padding="18px 10px",
                ),
                align="stretch",
                spacing="0",
                background_color="#10100f",
                border_right=f"1px solid {SURFACE_BORDER}",
                border_top=f"1px solid #6f5023",
                border_bottom=f"1px solid #6f5023",
                min_height="100vh",
                width="135px",
                flex="0 0 135px",
                position="relative",
            ),
            rx.flex(
                rx.box(
                    request_feedback(),
                    content,
                    width="100%",
                    min_width="0",
                    flex="1 1 520px",
                ),
                align="stretch",
                flex_wrap="wrap",
                width="100%",
            ),
            align="stretch",
            width="100%",
            min_height="100vh",
        ),
        background_color=BACKGROUND,
        color=FOREGROUND,
        min_height="100vh",
        font_family="Arial, sans-serif",
    )


def request_feedback() -> rx.Component:
    return rx.vstack(
        rx.cond(
            AppState.is_loading,
            rx.text("Processando sua solicitação...", role="status"),
            rx.fragment(),
        ),
        rx.cond(
            AppState.error_message != "",
            rx.text(
                AppState.error_message,
                color="#ffd2cc",
                role="alert",
            ),
            rx.fragment(),
        ),
        rx.cond(
            AppState.success_message != "",
            rx.text(
                AppState.success_message,
                color=ACCENT,
                role="status",
            ),
            rx.fragment(),
        ),
        align="stretch",
        width="100%",
        max_width="1180px",
        margin="0 auto",
        padding_x="24px",
    )


def page_heading(title: str, description: str) -> rx.Component:
    return rx.vstack(
        rx.heading(
            title,
            as_="h1",
            size="7",
            color=FOREGROUND,
            line_height="1.15",
        ),
        rx.text(
            description,
            color=MUTED,
            font_size="1rem",
            line_height="1.7",
            max_width="760px",
        ),
        align="start",
        spacing="3",
    )


def panel(
    title: str,
    description: str,
    label: str | None = None,
) -> rx.Component:
    return rx.box(
        rx.cond(
            bool(label),
            rx.text(
                label or "",
                color=ACCENT,
                font_size="0.72rem",
                font_weight="700",
                letter_spacing="0.14em",
                margin_bottom="12px",
            ),
            rx.fragment(),
        ),
        rx.heading(title, as_="h2", size="5", color=FOREGROUND),
        rx.text(
            description,
            color=MUTED,
            font_size="0.95rem",
            line_height="1.7",
            margin_top="10px",
        ),
        background_color=SURFACE,
        border=f"1px solid {SURFACE_BORDER}",
        border_radius="18px",
        padding="24px",
        width="100%",
    )


def role_layout(
    *,
    role_title: str,
    title: str,
    description: str,
    active_path: str,
    links: list[tuple[str, str]],
    content: rx.Component,
) -> rx.Component:
    icons = {
        "Dashboard": "house",
        "Agenda": "calendar_days",
        "Minha agenda": "calendar_days",
        "Atendimentos": "scissors",
        "Perfil": "user_round",
        "Meu perfil": "user_round",
        "Clientes": "users_round",
        "Serviços": "scissors",
        "Equipe": "users_round",
        "Relatórios": "bar_chart_3",
        "Usuários": "users_round",
        "Configurações": "settings",
        "Sair": "log_out",
    }
    navigation = rx.vstack(
        *[
            rx.link(
                rx.icon(
                    tag=icons.get(label, "circle"),
                    size=15,
                    aria_hidden=True,
                ),
                rx.text(label, font_size="0.68rem", line_height="1.25"),
                href=target,
                color="#17140f" if target == active_path else FOREGROUND,
                background_color=ACCENT if target == active_path else "transparent",
                border_radius="7px",
                padding="9px 8px",
                text_decoration="none",
                display="flex",
                align_items="center",
                gap="8px",
                width="100%",
                aria_current="page" if target == active_path else None,
                _hover={
                    "color": "#17140f" if target != active_path else "#17140f",
                    "background_color": ACCENT,
                },
                _focus={
                    "outline": f"2px solid {ACCENT}",
                    "outline_offset": "2px",
                },
            )
            for label, target in links
        ],
        align="stretch",
        spacing="2",
        role="navigation",
        aria_label=f"Navegação {role_title}",
        padding="18px 10px",
        width="100%",
    )
    return rx.box(
        rx.flex(
            rx.vstack(
                rx.vstack(
                    rx.box(
                        rx.icon(tag="crown", size=18, color=ACCENT, aria_hidden=True),
                        rx.text(
                            "B",
                            color=FOREGROUND,
                            font_size="2.2rem",
                            font_weight="700",
                            line_height="1",
                            font_style="italic",
                        ),
                        align_items="center",
                        justify_content="center",
                        height="58px",
                    ),
                    rx.text(
                        "BARBERFLOW",
                        color=FOREGROUND,
                        font_size="0.72rem",
                        font_weight="800",
                        letter_spacing="0.06em",
                    ),
                    rx.text(
                        "SISTEMA DE GERENCIAMENTO",
                        color=ACCENT,
                        font_size="0.34rem",
                        font_weight="700",
                        letter_spacing="0.04em",
                    ),
                    align="center",
                    spacing="1",
                    width="100%",
                    padding="14px 5px 18px",
                    border_bottom=f"1px solid {SURFACE_BORDER}",
                ),
                navigation,
                align="stretch",
                spacing="0",
                background_color="#10100f",
                border_right=f"1px solid {SURFACE_BORDER}",
                border_top=f"1px solid #6f5023",
                border_bottom=f"1px solid #6f5023",
                min_height="100vh",
                width="135px",
                flex="0 0 135px",
            ),
            rx.vstack(
                rx.flex(
                    rx.vstack(
                        rx.heading(
                            title,
                            as_="h1",
                            size="5",
                            color=FOREGROUND,
                            line_height="1.15",
                        ),
                        rx.text(
                            description,
                            color=MUTED,
                            font_size="0.76rem",
                        ),
                        align="start",
                        spacing="1",
                    ),
                    rx.flex(
                        rx.icon(
                            tag="bell",
                            size=17,
                            color=FOREGROUND,
                            aria_hidden=True,
                        ),
                        rx.box(
                            rx.icon(
                                tag="user_round",
                                size=18,
                                color="#d2d0cb",
                                aria_hidden=True,
                            ),
                            background_color="#454b53",
                            border_radius="50%",
                            width="32px",
                            height="32px",
                            display="flex",
                            align_items="center",
                            justify_content="center",
                        ),
                        rx.vstack(
                            rx.text(
                                "Administrador"
                                if role_title == "Administração"
                                else "Rafael Silva",
                                color=FOREGROUND,
                                font_size="0.68rem",
                                font_weight="600",
                            ),
                            rx.text(
                                "Admin"
                                if role_title == "Administração"
                                else "Barbeiro",
                                color=MUTED,
                                font_size="0.61rem",
                            ),
                            align="start",
                            spacing="0",
                        ),
                        rx.icon(
                            tag="chevron_down",
                            size=14,
                            color=MUTED,
                            aria_hidden=True,
                        ),
                        align="center",
                        gap="8px",
                    ),
                    align="center",
                    justify="between",
                    gap="14px",
                    width="100%",
                    padding_bottom="20px",
                ),
                request_feedback(),
                content,
                align="stretch",
                spacing="4",
                width="100%",
                min_width="0",
                flex="1 1 520px",
                max_width="1600px",
                margin="0 auto",
                padding="20px 24px 32px",
            ),
            align="stretch",
            flex_wrap="wrap",
            width="100%",
            min_height="100vh",
        ),
        background_color=BACKGROUND,
        color=FOREGROUND,
        min_height="100vh",
        font_family="Arial, sans-serif",
    )


def unavailable_panel(subject: str) -> rx.Component:
    return rx.box(
        rx.text(
            "INTEGRAÇÃO PENDENTE",
            color=ACCENT,
            font_size="0.72rem",
            font_weight="700",
            letter_spacing="0.14em",
            margin_bottom="12px",
        ),
        rx.heading(
            f"{subject} indisponível no momento",
            as_="h2",
            size="5",
            color=FOREGROUND,
        ),
        rx.text(
            "Esta área será preenchida quando a operação correspondente "
            "estiver conectada ao sistema. Nenhum dado de exemplo é exibido.",
            color=MUTED,
            line_height="1.7",
            margin_top="10px",
        ),
        background_color=SURFACE,
        border=f"1px solid {SURFACE_BORDER}",
        border_radius="18px",
        padding="24px",
        width="100%",
        role="status",
    )
