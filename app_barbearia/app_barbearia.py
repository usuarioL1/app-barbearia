"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from app_barbearia.auth_pages import (
    login_page,
    password_reset_page,
    signup_page,
)
from app_barbearia.customer_portal import (
    appointments_page,
    booking_page,
    customer_portal,
    profile_page,
    services_page,
    team_page,
)
from app_barbearia.state import AppState
from app_barbearia.workspace_pages import (
    admin_agenda_page,
    admin_clients_page,
    admin_console,
    admin_reports_page,
    admin_services_page,
    admin_settings_page,
    admin_team_page,
    admin_users_page,
    barber_appointments_page,
    barber_profile_page,
    barber_workspace,
)
from rxconfig import config


app = rx.App()
app.add_page(
    customer_portal,
    route="/",
    title="BarberFlow | Portal do Cliente",
    on_load=AppState.load_client_portal,
)
app.add_page(
    services_page,
    route="/servicos",
    title="BarberFlow | Serviços",
    on_load=AppState.load_catalog,
)
app.add_page(
    team_page,
    route="/equipe",
    title="BarberFlow | Equipe",
    on_load=AppState.load_catalog,
)
app.add_page(
    booking_page,
    route="/agendar",
    title="BarberFlow | Agendar",
    on_load=AppState.load_booking,
)
app.add_page(
    appointments_page,
    route="/agendamentos",
    title="BarberFlow | Agendamentos",
    on_load=AppState.load_appointments,
)
app.add_page(
    profile_page,
    route="/perfil",
    title="BarberFlow | Meu Perfil",
    on_load=AppState.load_profile,
)
app.add_page(login_page, route="/login", title="BarberFlow | Entrar")
app.add_page(signup_page, route="/cadastro", title="BarberFlow | Cadastro")
app.add_page(
    password_reset_page,
    route="/recuperar-senha",
    title="BarberFlow | Recuperar senha",
    on_load=AppState.load_password_reset,
)
app.add_page(
    barber_workspace,
    route="/barbeiro",
    title="BarberFlow | Painel do Barbeiro",
    on_load=AppState.load_barber_workspace,
)
app.add_page(
    barber_appointments_page,
    route="/barbeiro/atendimentos",
    title="BarberFlow | Atendimentos",
    on_load=AppState.load_barber_workspace,
)
app.add_page(
    barber_profile_page,
    route="/barbeiro/perfil",
    title="BarberFlow | Perfil do Barbeiro",
)
app.add_page(
    admin_console,
    route="/admin",
    title="BarberFlow | Administração",
    on_load=AppState.load_admin_dashboard,
)
app.add_page(
    admin_agenda_page,
    route="/admin/agenda",
    title="BarberFlow | Agenda",
    on_load=AppState.load_admin_agenda,
)
app.add_page(
    admin_clients_page,
    route="/admin/clientes",
    title="BarberFlow | Clientes",
    on_load=AppState.load_admin_data,
)
app.add_page(
    admin_services_page,
    route="/admin/servicos",
    title="BarberFlow | Serviços",
    on_load=AppState.load_admin_data,
)
app.add_page(
    admin_team_page,
    route="/admin/equipe",
    title="BarberFlow | Equipe",
    on_load=AppState.load_admin_data,
)
app.add_page(
    admin_reports_page,
    route="/admin/relatorios",
    title="BarberFlow | Relatórios",
    on_load=AppState.load_admin_reports,
)
app.add_page(
    admin_users_page,
    route="/admin/usuarios",
    title="BarberFlow | Usuários",
    on_load=AppState.load_admin_data,
)
app.add_page(
    admin_settings_page,
    route="/admin/configuracoes",
    title="BarberFlow | Configurações",
)
