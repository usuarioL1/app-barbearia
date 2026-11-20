import unittest
from unittest.mock import patch

import reflex as rx

from app_barbearia.ui import (
    UNPUBLISHED_ENDPOINT_ERROR,
    _is_unpublished_endpoint_error,
    public_layout,
    role_layout,
)
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


if __name__ == "__main__":
    unittest.main()
