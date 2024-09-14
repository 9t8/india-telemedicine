import os

import flet as ft
from dotenv import load_dotenv
from supabase import create_client

from authenticate import Authenticate

load_dotenv()


def main(page: ft.Page) -> None:
    supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

    def show_snack(snack_bar: ft.SnackBar) -> None:
        page.snack_bar = snack_bar
        snack_bar.open = True
        page.update()

    def home() -> None:
        page.controls = [ft.Text("Signed in!")]
        page.update()

    authenticate = Authenticate(supabase, show_snack, home)
    page.controls = [authenticate.controls]
    page.update()


ft.app(main)
