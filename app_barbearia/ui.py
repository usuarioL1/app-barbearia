import reflex as rx

from app_barbearia.state import AppState


BACKGROUND = "#090909"
SURFACE = "#121212"
SURFACE_RAISED = "#1b1b1b"
SURFACE_BORDER = "#302c26"
FOREGROUND = "#f5f3ef"
MUTED = "#b8b4ac"
ACCENT = "#F2A900"
ACCENT_HOVER = "#ffd36a"
SUCCESS = "#16a34a"
WARNING = "#d99a16"
DANGER = "#dc3b35"
ERROR = DANGER
INFO = "#2878c7"
UNPUBLISHED_ENDPOINT_ERROR = "Unable to locate request."


def _is_unpublished_endpoint_error(
    error_message: str | rx.Var[str],
) -> bool | rx.Var[bool]:
    if isinstance(error_message, str):
        return UNPUBLISHED_ENDPOINT_ERROR in error_message
    return error_message.contains(UNPUBLISHED_ENDPOINT_ERROR)


def brand() -> rx.Component:
    return rx.link(
        rx.text(
            "BARBERFLOW",
            color=FOREGROUND,
            font_size="1.05rem",
            font_weight="800",
            letter_spacing="0.16em",
            font_family="Inter, Arial, sans-serif",
        ),
        href="/",
        text_decoration="none",
        aria_label="BarberFlow, início",
        _focus={"outline": f"2px solid {ACCENT}", "outline_offset": "3px"},
    )


def _customer_account_menu() -> rx.Component:
    return rx.el.details(
        rx.el.summary(
            rx.flex(
                rx.box(
                    rx.icon(
                        tag="user_round",
                        size=19,
                        color="#d2d0cb",
                        aria_hidden=True,
                    ),
                    background_color=SURFACE_RAISED,
                    border=f"1px solid {ACCENT}",
                    border_radius="50%",
                    width="42px",
                    height="42px",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    flex_shrink="0",
                ),
                rx.vstack(
                    rx.text(
                        AppState.user_name,
                        color=FOREGROUND,
                        font_size="0.8rem",
                        font_weight="700",
                    ),
                    rx.text(
                        "Cliente",
                        color=MUTED,
                        font_size="0.68rem",
                    ),
                    align="start",
                    spacing="0",
                ),
                rx.icon(
                    tag="chevron_down",
                    size=16,
                    color=MUTED,
                    aria_hidden=True,
                ),
                align="center",
                gap="9px",
            ),
            aria_label="Menu da conta",
            style={"list_style": "none", "cursor": "pointer"},
        ),
        rx.vstack(
            rx.link(
                "Meu Perfil",
                href="/perfil",
                color=FOREGROUND,
                text_decoration="none",
                padding="8px 12px",
                border_radius="7px",
                _hover={"background_color": SURFACE_RAISED},
            ),
            rx.link(
                "Sair",
                href="/login",
                on_click=AppState.logout,
                color=FOREGROUND,
                text_decoration="none",
                padding="8px 12px",
                border_radius="7px",
                _hover={"background_color": SURFACE_RAISED},
            ),
            align="stretch",
            spacing="1",
            position="absolute",
            top="calc(100% + 8px)",
            right="0",
            z_index="20",
            min_width="160px",
            background_color=SURFACE,
            border=f"1px solid {SURFACE_BORDER}",
            border_radius="10px",
            padding="6px",
            box_shadow="0 12px 30px #000000aa",
        ),
        position="relative",
        flex_shrink="0",
    )


def public_layout(
    content: rx.Component,
    links: list[tuple[str, str]] | None = None,
    active_path: str = "/",
) -> rx.Component:
    navigation = links or [
        ("Início", "/"),
        ("Meus Agendamentos", "/agendamentos"),
        ("Serviços", "/servicos"),
        ("Meu Perfil", "/perfil"),
        ("Histórico", "/historico"),
        ("Sair", "/login"),
    ]
    icons = {
        "Início": "house",
        "Minha Conta": "user_round",
        "Meus Agendamentos": "calendar_days",
        "Meu Perfil": "user_round",
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
                rx.flex(
                    *[
                        rx.link(
                            rx.icon(
                                tag=icons.get(label, "circle"),
                                size=21,
                                aria_hidden=True,
                            ),
                            rx.text(
                                label,
                                font_size="0.95rem",
                                line_height="1.25",
                                font_weight="600" if target == active_path else "500",
                            ),
                            href=target,
                            on_click=AppState.logout if label == "Sair" else None,
                            color="#090909" if target == active_path else FOREGROUND,
                            background_color=ACCENT
                            if target == active_path
                            else "transparent",
                            border_radius="7px",
                            padding="12px 16px",
                            text_decoration="none",
                            display="flex",
                            align_items="center",
                            gap="12px",
                            aria_current="page" if target == active_path else None,
                            class_name="w-max md:w-full",
                            _hover={
                                "color": "#090909",
                                "background_color": ACCENT,
                            },
                            _focus={
                                "outline": f"2px solid {FOREGROUND}",
                                "outline_offset": "2px",
                            },
                        )
                        for label, target in navigation
                    ],
                    align="stretch",
                    gap="12px",
                    role="navigation",
                    aria_label="Navegação do cliente",
                    padding="20px 16px",
                    class_name="flex-row flex-nowrap gap-2 overflow-x-auto md:flex-col md:overflow-visible",
                ),
                align="stretch",
                spacing="0",
                background_color=SURFACE,
                border_bottom=f"1px solid {SURFACE_BORDER}",
                min_height="auto",
                class_name="w-full md:min-h-screen md:w-[256px] md:flex-none md:border-b-0 md:border-r md:border-r-[#f2a900]",
            ),
            rx.flex(
                rx.box(
                    rx.flex(
                        rx.box(flex="1"),
                        rx.cond(
                            AppState.is_authenticated,
                            _customer_account_menu(),
                            rx.fragment(),
                        ),
                        align="center",
                        justify="end",
                        width="100%",
                        padding_bottom="12px",
                    ),
                    request_feedback(),
                    content,
                    width="100%",
                    min_width="0",
                    flex="1 1 520px",
                    background_image=(
                        f"linear-gradient(180deg, #090909aa 0%, #090909e8 260px, #090909 100%), "
                        f"url('{rx.asset('barbershop_chair.jpg')}')"
                    ),
                    background_size="cover",
                    background_position="top center",
                    background_repeat="no-repeat",
                ),
                align="stretch",
                flex_wrap="wrap",
                flex="1 1 520px",
                width="100%",
                min_width="0",
            ),
            align="stretch",
            width="100%",
            min_height="100vh",
            class_name="flex-col md:flex-row",
        ),
        background_color=BACKGROUND,
        background_image=(
            "linear-gradient(135deg, transparent 0 46%, #f2a90022 47% 48%, transparent 49%), "
            "linear-gradient(315deg, transparent 0 46%, #f2a90022 47% 48%, transparent 49%)"
        ),
        background_size="120px 120px, 120px 120px",
        background_position="left top, right bottom",
        background_repeat="no-repeat",
        color=FOREGROUND,
        min_height="100vh",
        font_family="Inter, Arial, sans-serif",
    )


def request_feedback(*, hide_unpublished_endpoint_message: bool = False) -> rx.Component:
    error_message = AppState.error_message
    success_message = AppState.success_message
    if hide_unpublished_endpoint_message:
        error_message = rx.cond(
            _is_unpublished_endpoint_error(AppState.error_message),
            "",
            AppState.error_message,
        )
        success_message = rx.cond(
            _is_unpublished_endpoint_error(AppState.error_message),
            "",
            AppState.success_message,
        )
    return rx.vstack(
        rx.cond(
            AppState.is_loading,
            rx.text("Processando sua solicitação...", role="status"),
            rx.fragment(),
        ),
        rx.cond(
            error_message != "",
            rx.text(
                error_message,
                color="#ffd2cc",
                role="alert",
            ),
            rx.fragment(),
        ),
        rx.cond(
            success_message != "",
            rx.text(
                success_message,
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
        border_radius="14px",
        padding="24px",
        width="100%",
        box_shadow="0 12px 32px #00000033",
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
    unavailable_data = rx.box(
        rx.icon(tag="circle_alert", size=22, color=ACCENT, aria_hidden=True),
        rx.heading(
            "Dados indisponíveis",
            as_="h2",
            size="4",
            color=FOREGROUND,
            margin_top="12px",
        ),
        rx.text(
            "Não foi possível carregar as informações desta tela. "
            "Nenhum registro anterior ou demonstrativo está sendo exibido.",
            color=MUTED,
            line_height="1.7",
            margin_top="6px",
        ),
        background_color=SURFACE,
        border=f"1px solid {SURFACE_BORDER}",
        border_radius="14px",
        padding="24px",
        width="100%",
        role="status",
    )
    visible_content = rx.cond(
        _is_unpublished_endpoint_error(AppState.error_message),
        unavailable_data,
        content,
    )
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
    navigation = rx.flex(
        *[
            rx.link(
                rx.icon(
                    tag=icons.get(label, "circle"),
                    size=21,
                    aria_hidden=True,
                ),
                rx.text(label, font_size="1rem", line_height="1.25"),
                href=target,
                color="#17140f" if target == active_path else FOREGROUND,
                background_color=ACCENT if target == active_path else "transparent",
                border_radius="7px",
                padding="12px 16px",
                text_decoration="none",
                display="flex",
                align_items="center",
                gap="12px",
                aria_current="page" if target == active_path else None,
                class_name="w-max md:w-full",
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
        gap="12px",
        role="navigation",
        aria_label=f"Navegação {role_title}",
        padding="20px 16px",
        width="100%",
        class_name="flex-row flex-nowrap gap-2 overflow-x-auto md:flex-col md:overflow-visible",
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
                background_color="#101010ee",
                border_bottom=f"1px solid {SURFACE_BORDER}",
                min_height="auto",
                border_right=f"1px solid {ACCENT}",
                class_name="w-full md:min-h-screen md:w-[256px] md:flex-none md:border-b-0 md:border-r",
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
                            font_size="0.88rem",
                        ),
                        align="start",
                        spacing="1",
                    ),
                    rx.text(
                        role_title,
                        color=ACCENT,
                        font_size="0.75rem",
                        font_weight="700",
                        background_color=SURFACE_RAISED,
                        border=f"1px solid {SURFACE_BORDER}",
                        border_radius="999px",
                        padding="7px 12px",
                    ),
                    align="center",
                    justify="between",
                    gap="14px",
                    width="100%",
                    padding_bottom="20px",
                    class_name="flex-wrap",
                ),
                request_feedback(hide_unpublished_endpoint_message=True),
                content,
                align="stretch",
                spacing="4",
                width="100%",
                min_width="0",
                flex="1 1 520px",
                max_width="1600px",
                margin="0 auto",
                padding="24px 28px 36px",
                background_image=(
                    f"linear-gradient(180deg, #090909aa 0%, #090909e8 260px, #090909 100%), "
                    f"url('{rx.asset('barbershop_chair.jpg')}')"
                ),
                background_size="cover",
                background_position="top center",
                background_repeat="no-repeat",
                min_height="100vh",
            ),
            align="stretch",
            width="100%",
            min_height="100vh",
            class_name="flex-col md:flex-row",
        ),
        background_color=BACKGROUND,
        background_image=(
            "radial-gradient(ellipse at 70% 8%, #f2a90012 0%, transparent 48%), "
            "linear-gradient(135deg, transparent 0 46%, #f2a90018 47% 48%, transparent 49%), "
            "linear-gradient(315deg, transparent 0 46%, #f2a90018 47% 48%, transparent 49%)"
        ),
        background_size="auto, 120px 120px, 120px 120px",
        background_position="center top, left top, right bottom",
        background_repeat="no-repeat",
        color=FOREGROUND,
        min_height="100vh",
        font_family="Inter, Arial, sans-serif",
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
