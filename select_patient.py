from typing import Callable, Sequence

import flet as ft
from supabase import Client


class SelectPatient(ft.Column):
    def __init__(
        self,
        supabase: Client,
        show_snack: Callable,
        on_confirm: Callable,
    ) -> None:
        super().__init__()

        self.supabase = supabase
        self.show_snack = show_snack
        self.on_confirm = on_confirm

        self.patient_id = ft.TextField(
            hint_text="Patient ID",
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        self.name_field = ft.TextField(hint_text="Patient name")
        self.name = ft.Text()

        self.controls = [
            self.patient_id,
            ft.TextButton("Search", on_click=self.search),
        ]
        self.create_controls = [
            *self.controls,
            self.name_field,
            ft.TextButton("Add patient", on_click=self.create),
        ]
        self.confirm_controls = [
            *self.controls,
            self.name,
            ft.TextButton(
                "Confirm",
                on_click=lambda _: self.on_confirm(self.patient_id.value),
            ),
        ]

    def open(self, controls: Sequence[ft.Control]) -> None:
        self.controls = controls
        self.update()

    def search(self, _: None) -> None:
        response = (
            self.supabase.table("patients")
            .select("name")
            .eq("id", self.patient_id.value)
            .execute()
            .data
        )
        if len(response) == 0:
            self.open(self.create_controls)
        else:
            self.name.value = response[0]["name"]
            self.open(self.confirm_controls)

    def create(self, _: None) -> None:
        self.supabase.table("patients").insert(
            {"id": self.patient_id.value, "name": self.name_field.value},
        ).execute()

        self.on_confirm(self.patient_id.value)
