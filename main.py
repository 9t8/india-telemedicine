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
        select_patient = SelectPatient(supabase, show_snack, open_patient_history)
        page.controls = [select_patient.controls]
        page.update()

    def open_patient_history(patient_id: int) -> None:
        patient_history = PatientHistory(supabase, show_snack, go_home, patient_id)
        page.controls = [patient_history.controls]
        page.update()

    authenticate = Authenticate(supabase, show_snack, go_home)
    page.controls = [authenticate.controls]
    page.update()


ft.app(main)
