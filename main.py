import os

import flet as ft
from dotenv import load_dotenv
from supabase import create_client

from authenticate import Authenticate
from select_patient import SelectPatient

load_dotenv()


def main(page: ft.Page) -> None:
    supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

    def show_snack(snack_bar: ft.SnackBar) -> None:
        page.snack_bar = snack_bar
        snack_bar.open = True
        page.update()

    select_patient = SelectPatient(supabase, show_snack, None)

    def go_home() -> None:
        page.controls = [select_patient.controls]
        page.update()

    authenticate = Authenticate(supabase, show_snack, go_home)
    page.controls = [authenticate.controls]
    page.update()


ft.app(main)
