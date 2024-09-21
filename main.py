import os

import flet as ft
from dotenv import load_dotenv
from supabase import create_client

from authenticate import Authenticate
from patient_history import PatientHistory
from select_patient import SelectPatient

load_dotenv()


def main(page: ft.Page) -> None:
    supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

    def show_snack(snack_bar: ft.SnackBar) -> None:
        page.snack_bar = snack_bar
        snack_bar.open = True
        page.update()

    def go_home() -> None:
        page.controls = [SelectPatient(show_snack, go_patient_history)]
        page.update()

    def go_patient_history(patient_id: int) -> None:
        page.controls = [PatientHistory(supabase, show_snack, go_home, patient_id)]
        page.update()

    authenticate = Authenticate(supabase, show_snack, go_home)

    page.add(authenticate)


ft.app(main)
