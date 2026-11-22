import os
from pathlib import Path

import reflex as rx
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().with_name(".env"), override=False)

if (
    os.environ.get("BARBERFLOW_MODE", "").casefold() == "xano"
    or "XANO_API_BASE_URL" in os.environ
):
    os.environ["REFLEX_SSR"] = "false"

config = rx.Config(
    app_name="app_barbearia",
    show_built_with_reflex=False,
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
        rx.plugins.RadixThemesPlugin(),
    ]
)