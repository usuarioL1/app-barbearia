import reflex as rx

from app_barbearia.state import AppState
from app_barbearia.ui import (
    ACCENT,
    FOREGROUND,
    MUTED,
    SURFACE_BORDER,
    request_feedback,
)


BACKGROUND = "#090909"
FIELD_BACKGROUND = "#111110"


def _brand_lockup(*, compact: bool = False) -> rx.Component:
    mark_size = "58px" if compact else "168px"
    word_size = "1rem" if compact else "3.5rem"
    return rx.vstack(
        rx.icon(
            tag="crown",
            size=18 if compact else 36,
            color=ACCENT,
            aria_hidden=True,
        ),
        rx.box(
            rx.text(
                "B",
                color=ACCENT,
                font_family="Georgia, serif",
                font_size=mark_size,
                font_style="italic",
                font_weight="700",
                line_height="0.9",
                text_shadow=f"0 0 24px {ACCENT}55",
            ),
            border_bottom=f"2px solid {ACCENT}",
            padding_x="12px",
            padding_bottom="6px",
        ),
        rx.flex(
            rx.text(
                "BARBER",
                color=FOREGROUND,
                font_size=word_size,
                font_weight="800",
                letter_spacing="0.08em",
            ),
            rx.text(
                "FLOW",
                color=ACCENT,
                font_size=word_size,
                font_weight="800",
                letter_spacing="0.08em",
            ),
            justify="center",
            align="center",
        ),
        rx.text(
            "S I S T E M A   D E   G E R E N C I A M E N T O",
            color=FOREGROUND,
            font_size="0.62rem" if compact else "0.82rem",
            letter_spacing="0.14em",
        ),
        align="center",
        spacing="1",
    )


def _auth_field(
    label: str,
    field_type: str,
    autocomplete: str,
    *,
    icon: str,
    height: str,
    show_password_control: bool = False,
    value: rx.Var[str] | None = None,
    on_change: rx.EventHandler | None = None,
) -> rx.Component:
    field_id = f"auth-{'-'.join(label.casefold().replace('/', ' ').split())}"
    return rx.hstack(
        rx.icon(
            tag=icon,
            color="#aaa69d",
            size=20,
            aria_hidden="true",
        ),
        rx.el.input(
            type=field_type,
            id=field_id,
            name=field_id,
            placeholder=label,
            aria_label=label,
            auto_complete=autocomplete,
            value=value,
            on_change=on_change,
            width="100%",
            height="100%",
            background="transparent",
            border="none",
            outline="none",
            color=FOREGROUND,
            font_size="1rem",
            padding="0",
            _placeholder={"color": "#898782"},
        ),
        rx.cond(
            show_password_control,
            rx.icon(
                tag="eye",
                color="#aaa69d",
                size=20,
                aria_hidden="true",
            ),
            rx.fragment(),
        ),
        align="center",
        gap="12px",
        width="100%",
        height=height,
        padding_x="20px",
        background_color=FIELD_BACKGROUND,
        border=f"1px solid {SURFACE_BORDER}",
        border_radius="12px",
        _focus_within={
            "border_color": ACCENT,
            "box_shadow": f"0 0 0 1px {ACCENT}",
        },
    )


def _submit_button(
    label: str,
    *,
    height: str = "58px",
    on_click: rx.EventHandler | None = None,
) -> rx.Component:
    return rx.button(
        rx.hstack(
            rx.icon(tag="log_in", size=20, aria_hidden=True),
            rx.text(label),
            align="center",
            justify="center",
            gap="12px",
            width="100%",
        ),
        type="button",
        on_click=on_click,
        width="100%",
        height=height,
        background=f"linear-gradient(100deg, #dcae5b 0%, #bd8732 100%)",
        color="#11100e",
        font_size="1rem",
        font_weight="700",
        border_radius="12px",
        cursor="pointer",
        _hover={"filter": "brightness(1.08)"},
        _focus={"outline": f"2px solid {FOREGROUND}", "outline_offset": "3px"},
    )


def _line_separator() -> rx.Component:
    return rx.hstack(
        rx.box(height="1px", background_color=SURFACE_BORDER, flex="1"),
        rx.text("ou", color=MUTED, font_size="0.9rem"),
        rx.box(height="1px", background_color=SURFACE_BORDER, flex="1"),
        align="center",
        gap="18px",
        width="100%",
    )


def _field_group(
    fields: list[tuple[str, str, str, str]],
    *,
    spacing: str = "5",
    height: str = "58px",
    bindings: dict[
        str, tuple[rx.Var[str] | None, rx.EventHandler | None]
    ] | None = None,
) -> rx.Component:
    return rx.vstack(
        *[
            _auth_field(
                label,
                field_type,
                autocomplete,
                icon=icon,
                height=height,
                show_password_control=field_type == "password",
                value=(bindings or {}).get(label, (None, None))[0],
                on_change=(bindings or {}).get(label, (None, None))[1],
            )
            for label, field_type, autocomplete, icon in fields
        ],
        align="stretch",
        spacing=spacing,
        width="100%",
    )


def _decorative_lines() -> rx.Component:
    return rx.box(
        position="absolute",
        inset="0",
        pointer_events="none",
        background_image=(
            "linear-gradient(135deg, transparent 0 7%, #d7a64b 7.1% 7.3%, "
            "transparent 7.4% 11%, #f0c36d 11.1% 11.3%, transparent 11.4%), "
            "linear-gradient(315deg, transparent 0 8%, #d7a64b 8.1% 8.3%, "
            "transparent 8.4% 12%, #f0c36d 12.1% 12.3%, transparent 12.4%)"
        ),
        opacity="0.72",
    )


def _login_promo() -> rx.Component:
    features = [
        ("calendar_days", "Agendamentos\nInteligentes"),
        ("users_round", "Gestão de\nClientes"),
        ("chart_no_axes_combined", "Relatórios\nem Tempo Real"),
        ("zap", "Tudo em\num só lugar"),
    ]
    return rx.vstack(
        _brand_lockup(),
        rx.text(
            "Sua barbearia mais organizada,\nsempre um passo à frente.",
            color="#d2cec6",
            font_size="1.2rem",
            line_height="1.35",
            text_align="center",
            white_space="pre-line",
            margin_top="30px",
        ),
        rx.hstack(
            *[
                rx.vstack(
                    rx.icon(
                        tag=icon,
                        color=ACCENT,
                        size=30,
                        aria_hidden=True,
                    ),
                    rx.text(
                        label,
                        color="#dedbd5",
                        font_size="0.88rem",
                        line_height="1.35",
                        text_align="center",
                        white_space="pre-line",
                    ),
                    align="center",
                    justify="center",
                    gap="8px",
                    flex="1",
                    min_width="100px",
                )
                for icon, label in features
            ],
            align="center",
            justify="between",
            width="100%",
            max_width="700px",
            margin_top="38px",
        ),
        align="center",
        justify="center",
        min_height="100vh",
        flex="1 1 58%",
        width="58%",
        padding="48px",
        position="relative",
        overflow="hidden",
        background_image=(
            "radial-gradient(ellipse at 42% 34%, #392717 0%, #19130d 34%, "
            "#0c0b09 72%), linear-gradient(90deg, #0a0908, #17120c)"
        ),
        class_name="hidden lg:flex",
    )


def _login_form() -> rx.Component:
    return rx.vstack(
        rx.vstack(
            rx.heading(
                rx.fragment(
                    rx.text("Bem-vindo ", as_="span"),
                    rx.text("de volta!", as_="span", color=ACCENT),
                ),
                as_="h1",
                font_size="clamp(2rem, 3.2vw, 3rem)",
                color=FOREGROUND,
                font_weight="800",
                line_height="1.1",
            ),
            rx.text(
                "Acesse sua conta para continuar",
                color=MUTED,
                font_size="1.1rem",
            ),
            align="start",
            spacing="2",
            width="100%",
            margin_bottom="24px",
        ),
        _field_group(
            [
                ("E-mail", "email", "email", "mail"),
                ("Senha", "password", "current-password", "lock_keyhole"),
            ],
            bindings={
                "E-mail": (AppState.login_email, AppState.set_login_email),
                "Senha": (None, AppState.set_login_password),
            },
        ),
        request_feedback(),
        rx.hstack(
            rx.checkbox("Lembrar de mim", color_scheme="amber"),
            rx.link(
                "Esqueceu sua senha?",
                href="/recuperar-senha",
                color="#d4d0c8",
                font_size="0.87rem",
                text_decoration="underline",
                _focus={"outline": f"2px solid {ACCENT}", "outline_offset": "3px"},
            ),
            align="center",
            justify="between",
            flex_wrap="wrap",
            gap="12px",
            width="100%",
            margin_top="20px",
            margin_bottom="24px",
        ),
        _submit_button("Entrar", on_click=AppState.login),
        _line_separator(),
        rx.link(
            rx.hstack(
                rx.icon(tag="user_round_plus", size=20, aria_hidden=True),
                rx.text("Cadastrar Cliente"),
                align="center",
                justify="center",
                gap="12px",
                width="100%",
            ),
            href="/cadastro",
            color=FOREGROUND,
            font_size="1rem",
            font_weight="600",
            text_decoration="none",
            width="100%",
            border=f"1px solid {ACCENT}",
            border_radius="12px",
            padding="15px",
            _hover={"background_color": "#241d11"},
            _focus={"outline": f"2px solid {FOREGROUND}", "outline_offset": "3px"},
        ),
        rx.hstack(
            rx.box(width="52px", height="1px", background_color=ACCENT),
            rx.flex(
                rx.text("B A R B E R", color=FOREGROUND),
                rx.text("F L O W", color=ACCENT),
                gap="4px",
                font_size="0.72rem",
                font_weight="600",
            ),
            rx.box(width="52px", height="1px", background_color=ACCENT),
            align="center",
            justify="center",
            gap="18px",
            width="100%",
            margin_top="12px",
        ),
        align="stretch",
        spacing="5",
        width="100%",
        max_width="570px",
    )


def login_page() -> rx.Component:
    return rx.box(
        _decorative_lines(),
        rx.flex(
            _login_promo(),
            rx.box(
                rx.box(
                    _login_form(),
                    width="100%",
                    max_width="650px",
                    background_color="#111110",
                    border=f"1px solid {SURFACE_BORDER}",
                    border_radius="22px",
                    padding="clamp(28px, 3vw, 48px)",
                    box_shadow="0 18px 70px #00000088",
                ),
                display="flex",
                align_items="center",
                justify_content="center",
                flex="1 1 42%",
                width="42%",
                min_height="100vh",
                padding="clamp(16px, 2vw, 28px)",
                background_color="#0b0b0b",
            ),
            align="stretch",
            width="100%",
            min_height="100vh",
            position="relative",
            z_index="1",
        ),
        background_color=BACKGROUND,
        color=FOREGROUND,
        min_height="100vh",
        overflow="hidden",
        font_family="Arial, sans-serif",
    )


def _side_navigation(active_path: str) -> rx.Component:
    links = [
        ("Início", "/", "house"),
        ("Serviços", "/servicos", "scissors"),
        ("Equipe", "/servicos", "users_round"),
        ("Entrar", "/login", "log_in"),
        ("Cadastrar", "/cadastro", "lock_keyhole"),
    ]
    return rx.vstack(
        _brand_lockup(compact=True),
        rx.vstack(
            *[
                rx.link(
                    rx.hstack(
                        rx.icon(tag=icon, size=17, aria_hidden=True),
                        rx.text(label),
                        align="center",
                        gap="10px",
                        width="100%",
                    ),
                    href=target,
                    color="#f0ede7" if target == active_path else "#c3beb4",
                    background_color="#bd8732" if target == active_path else "transparent",
                    border_radius="7px",
                    font_size="0.84rem",
                    font_weight="600" if target == active_path else "400",
                    padding="10px 12px",
                    text_decoration="none",
                    width="100%",
                    _hover={"background_color": "#332718"},
                    _focus={
                        "outline": f"2px solid {ACCENT}",
                        "outline_offset": "2px",
                    },
                )
                for label, target, icon in links
            ],
            align="stretch",
            spacing="2",
            width="100%",
            margin_top="24px",
            role="navigation",
            aria_label="Navegação pública",
        ),
        align="stretch",
        width="150px",
        min_height="100vh",
        flex_shrink="0",
        padding="18px 12px",
        background_color="#0b0b0a",
        border_right=f"1px solid {SURFACE_BORDER}",
        position="relative",
        z_index="2",
        class_name="hidden lg:flex",
    )


def _secondary_promo(*, recovery: bool) -> rx.Component:
    if recovery:
        content = rx.vstack(
            rx.icon(
                tag="lock_keyhole",
                color=ACCENT,
                size=68,
                text_shadow=f"0 0 24px {ACCENT}66",
                aria_hidden=True,
            ),
            rx.heading(
                "Recuperar senha",
                as_="h1",
                font_size="2rem",
                color=FOREGROUND,
            ),
            rx.text(
                "Digite seu e-mail para receber\num link de redefinição de senha.",
                color="#d1cdc5",
                text_align="center",
                white_space="pre-line",
                line_height="1.5",
            ),
            rx.box(width="140px", height="1px", background_color=ACCENT, margin_top="8px"),
            align="center",
            justify="center",
            width="100%",
            min_height="100%",
            spacing="3",
        )
    else:
        content = rx.vstack(
            rx.heading(
                "Criar sua conta",
                as_="h1",
                font_size="2rem",
                color=FOREGROUND,
            ),
            rx.text(
                "Faça parte da nossa barbearia!",
                color="#d1cdc5",
                font_size="1rem",
            ),
            rx.box(width="100px", height="1px", background_color=ACCENT, margin_top="14px"),
            align="start",
            justify="center",
            width="100%",
            min_height="100%",
            padding="36px",
            spacing="2",
        )
    return rx.box(
        content,
        min_height="100vh",
        flex="0 0 36%",
        width="36%",
        min_width="280px",
        position="relative",
        overflow="hidden",
        background_image=(
            "radial-gradient(ellipse at 55% 40%, #382818 0%, #21180f 30%, "
            "#100e0b 76%), linear-gradient(90deg, #100e0b, #21180f)"
        ),
        _before={
            "content": '""',
            "position": "absolute",
            "inset": "0",
            "pointer_events": "none",
            "background_image": (
                "linear-gradient(130deg, transparent 0 8%, #d6a64f 8.2% 8.5%, "
                "transparent 8.7%), linear-gradient(310deg, transparent 0 8%, "
                "#d6a64f 8.2% 8.5%, transparent 8.7%)"
            ),
        },
        class_name="hidden md:flex",
    )


def _secondary_auth_form(*, recovery: bool) -> rx.Component:
    fields = (
        [("E-mail cadastrado", "email", "email", "mail")]
        if recovery
        else [
            ("Nome completo", "text", "name", "user_round"),
            ("E-mail", "email", "email", "mail"),
            ("Telefone / WhatsApp", "tel", "tel", "phone"),
            ("Senha", "password", "new-password", "lock_keyhole"),
            ("Confirmar senha", "password", "new-password", "lock_keyhole"),
        ]
    )
    return rx.vstack(
        rx.icon(
            tag="mail" if recovery else "users_round",
            color=ACCENT,
            size=34,
            aria_hidden=True,
            margin_x="auto",
        ),
        _field_group(
            fields,
            spacing="2",
            height="44px",
            bindings=(
                {"E-mail cadastrado": (AppState.recovery_email, AppState.set_recovery_email)}
                if recovery
                else {
                    "Nome completo": (AppState.signup_name, AppState.set_signup_name),
                    "E-mail": (AppState.signup_email, AppState.set_signup_email),
                    "Telefone / WhatsApp": (
                        AppState.signup_phone,
                        AppState.set_signup_phone,
                    ),
                    "Senha": (None, AppState.set_signup_password),
                    "Confirmar senha": (
                        None,
                        AppState.set_signup_password_confirmation,
                    ),
                }
            ),
        ),
        request_feedback(),
        _submit_button(
            "Enviar link" if recovery else "Cadastrar",
            height="44px",
            on_click=(
                AppState.request_password_reset
                if recovery
                else AppState.signup
            ),
        ),
        rx.cond(
            recovery,
            rx.fragment(
                _line_separator(),
                rx.link(
                    "< Voltar para o login",
                    href="/login",
                    color=ACCENT,
                    font_size="0.88rem",
                    text_align="center",
                    width="100%",
                    _focus={"outline": f"2px solid {ACCENT}", "outline_offset": "3px"},
                ),
            ),
            rx.link(
                rx.hstack(
                    rx.text("Já tem uma conta?"),
                    rx.text("Entrar", color=ACCENT, text_decoration="underline"),
                    align="center",
                    justify="center",
                    gap="8px",
                    width="100%",
                    font_size="0.83rem",
                    color="#d2cec6",
                ),
                href="/login",
                text_decoration="none",
                width="100%",
            ),
        ),
        align="stretch",
        spacing="3",
        width="100%",
        max_width="460px",
    )


def _secondary_auth_page(*, recovery: bool) -> rx.Component:
    return rx.flex(
        _side_navigation("/cadastro"),
        _secondary_promo(recovery=recovery),
        rx.box(
            rx.box(
                _secondary_auth_form(recovery=recovery),
                width="100%",
                max_width="520px",
                background_color="#111110",
                border=f"1px solid {SURFACE_BORDER}",
                border_radius="16px",
                padding="clamp(26px, 3vw, 48px)",
            ),
            display="flex",
            align_items="center",
            justify_content="center",
            min_height="100vh",
            padding="clamp(24px, 4vw, 54px)",
            background_color="#0b0b0b",
            flex="1 1 54%",
            width="54%",
            position="relative",
            z_index="1",
        ),
        align="stretch",
        width="100%",
        min_height="100vh",
        flex_wrap="wrap",
        position="relative",
        background_color=BACKGROUND,
        color=FOREGROUND,
        font_family="Arial, sans-serif",
        overflow="hidden",
    )


def _password_update_form() -> rx.Component:
    return rx.vstack(
        rx.icon(
            tag="lock_keyhole",
            color=ACCENT,
            size=34,
            aria_hidden=True,
            margin_x="auto",
        ),
        rx.heading(
            "Criar nova senha",
            color=FOREGROUND,
            font_size="1.5rem",
            text_align="center",
        ),
        _field_group(
            [
                ("Nova senha", "password", "new-password", "lock_keyhole"),
                ("Confirmar nova senha", "password", "new-password", "lock_keyhole"),
            ],
            spacing="3",
            height="50px",
            bindings={
                "Nova senha": (None, AppState.set_reset_password),
                "Confirmar nova senha": (
                    None,
                    AppState.set_reset_password_confirmation,
                ),
            },
        ),
        request_feedback(),
        _submit_button(
            "Salvar nova senha",
            height="48px",
            on_click=AppState.update_password,
        ),
        rx.link(
            "Voltar para o login",
            href="/login",
            color=ACCENT,
            text_align="center",
            width="100%",
        ),
        align="stretch",
        spacing="3",
        width="100%",
        max_width="460px",
    )


def signup_page() -> rx.Component:
    return _secondary_auth_page(recovery=False)


def password_reset_page() -> rx.Component:
    return rx.cond(
        AppState.is_reset_flow,
        rx.flex(
            _side_navigation("/cadastro"),
            rx.box(
                rx.box(
                    _password_update_form(),
                    width="100%",
                    max_width="520px",
                    background_color="#111110",
                    border=f"1px solid {SURFACE_BORDER}",
                    border_radius="16px",
                    padding="clamp(26px, 3vw, 48px)",
                ),
                display="flex",
                align_items="center",
                justify_content="center",
                min_height="100vh",
                padding="clamp(24px, 4vw, 54px)",
                background_color="#0b0b0b",
                flex="1 1 54%",
                width="54%",
                position="relative",
                z_index="1",
            ),
            align="stretch",
            width="100%",
            min_height="100vh",
            flex_wrap="wrap",
            position="relative",
            background_color=BACKGROUND,
            color=FOREGROUND,
            font_family="Arial, sans-serif",
            overflow="hidden",
        ),
        _secondary_auth_page(recovery=True),
    )
