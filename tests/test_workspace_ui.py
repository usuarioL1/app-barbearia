import unittest
from unittest.mock import patch

import reflex as rx

from app_barbearia.app_barbearia import app
from app_barbearia.customer_portal import (
    _appointment_item,
    _service_image_name,
    appointments_page,
)
from app_barbearia.ui import (
    UNPUBLISHED_ENDPOINT_ERROR,
    _is_unpublished_endpoint_error,
    public_layout,
    role_layout,
)
from app_barbearia.workspace_pages import admin_console, admin_reports_page
from app_barbearia.xano_repository import XanoRepository, repository_for


class UnpublishedEndpointMessageTests(unittest.TestCase):
    def test_exact_xano_message_is_recognized(self) -> None:
        self.assertTrue(_is_unpublished_endpoint_error(UNPUBLISHED_ENDPOINT_ERROR))

    def test_other_errors_remain_visible(self) -> None:
        for message in (
            "Not found",
            "Forbidden",
        ):
            with self.subTest(message=message):
                self.assertFalse(_is_unpublished_endpoint_error(message))

    def test_message_containing_technical_text_is_recognized(self) -> None:
        for message in (
            "Unable to locate request. ",
            "Xano: Unable to locate request. (404)",
        ):
            with self.subTest(message=message):
                self.assertTrue(_is_unpublished_endpoint_error(message))

    def test_role_layout_filters_banner_and_public_layout_does_not(self) -> None:
        role = role_layout(
            role_title="Administração",
            title="Dashboard",
            description="Resumo",
            active_path="/admin",
            links=[],
            content=rx.text("Resumo"),
        )
        public = public_layout(rx.text("Resumo"))

        self.assertIn(
            f'includes("{UNPUBLISHED_ENDPOINT_ERROR}")',
            str(role.children[0]),
        )
        self.assertNotIn(
            f'includes("{UNPUBLISHED_ENDPOINT_ERROR}")',
            str(public.children[0]),
        )

    def test_xano_mode_selects_xano_without_demo_fallback(self) -> None:
        with patch.dict("os.environ", {"BARBERFLOW_MODE": "xano"}):
            self.assertIsInstance(repository_for(), XanoRepository)

    def test_admin_pages_only_load_user_records_when_needed(self) -> None:
        users_page = app._unevaluated_pages["admin/usuarios"]
        settings_page = app._unevaluated_pages["admin/configuracoes"]

        self.assertEqual(users_page.on_load.fn.__name__, "load_admin_users")
        self.assertIsNone(settings_page.on_load)

    def test_admin_reports_controls_are_unbounded_and_reload_on_change(self) -> None:
        page = str(admin_reports_page())

        self.assertIn("set_admin_report_period", page)
        self.assertIn("set_admin_report_date", page)
        self.assertNotIn("max=", page)

    def test_admin_dashboard_includes_completed_monthly_appointment_count(self) -> None:
        page = str(admin_console())

        self.assertIn("Atendimentos Conclu\\u00eddos no M\\u00eas", page)
        self.assertIn("admin_completed_count", page)


class ServiceImageMappingTests(unittest.TestCase):
    def test_service_images_map_to_distinct_assets(self) -> None:
        expected = {
            "Corte Masculino": "service_haircut.jpg",
            "Barba": "service_beard.jpg",
            "Combo": "service_combo.jpg",
            "corte + Barba": "service_combo.jpg",
            "Sobrancelha": "service_eyebrow.jpg",
            "Pezinho / Acabamento": "service_edgeup.jpg",
            "Hidratação Capilar": "service_hydration.jpg",
        }

        for title, image in expected.items():
            with self.subTest(title=title):
                self.assertEqual(_service_image_name(title), image)

        self.assertNotEqual(
            _service_image_name("Corte Masculino"),
            _service_image_name("corte + Barba"),
        )

    def test_service_image_mapping_ignores_title_case_and_whitespace(self) -> None:
        self.assertEqual(
            _service_image_name("  CORTE + BARBA "),
            "service_combo.jpg",
        )
        self.assertEqual(
            _service_image_name("HIDRATAÇÃO CAPILAR"),
            "service_hydration.jpg",
        )

    def test_upcoming_appointment_page_contains_complete_list(self) -> None:
        page = str(appointments_page())

        self.assertIn("Pr\\u00f3ximo Agendamento", page)
        self.assertIn("Todos os Pr\\u00f3ximos Agendamentos", page)
        self.assertIn("upcoming_appointments", page)
        self.assertIn("next_appointments", page)
        self.assertIn("Carregando agendamentos...", page)
        self.assertIn("Nenhum pr\\u00f3ximo agendamento.", page)

    def test_upcoming_appointment_item_keeps_supported_cancel_control(self) -> None:
        item = {
            "id": "appointment-1",
            "date_display": "25/08/2026",
            "time": "09:00",
            "service_title": "Corte Masculino",
            "barber_name": "Rafael",
            "status_label": "Confirmado",
            "status_color": "#54a86b",
        }

        component = str(_appointment_item(item))

        self.assertIn("Cancelar", component)
        self.assertIn("appointment-1", component)


if __name__ == "__main__":
    unittest.main()
