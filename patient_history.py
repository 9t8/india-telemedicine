from typing import Callable

import flet as ft
from supabase import Client


class NewEntry(ft.Row):
    def __init__(self, cb: Callable) -> None:
        super().__init__()
        self.cb = cb
        self.name = ft.TextField(hint_text="Entry type")
        self.controls = [
            self.name,
            ft.TextButton(
                "Yes",
                on_click=lambda _: self.button_clicked(value=True),
            ),
            ft.TextButton(
                "No",
                on_click=lambda _: self.button_clicked(value=False),
            ),
        ]

    def button_clicked(self, *, value: bool) -> None:
        self.cb(self.name.value, value=value)
        self.name.value = ""
        self.update()


class SuggestedEntry(ft.Row):
    def __init__(self, name: str, cb: Callable) -> None:
        super().__init__()
        self.controls = [
            ft.Text(name),
            ft.TextButton(
                "Yes",
                on_click=lambda _: cb(name, value=True),
            ),
            ft.TextButton(
                "No",
                on_click=lambda _: cb(name, value=False),
            ),
            ft.TextButton(
                "Unable to answer",
                on_click=lambda _: cb(name, value=None),
            ),
        ]


class Entry(ft.Row):
    def __init__(
        self,
        created_at: str,
        name: str,
        *,
        value: bool,
    ) -> None:
        super().__init__()
        self.controls = [
            ft.Text(created_at),
            ft.Text(name),
            ft.Text(
                "Unable to answer",
                bgcolor=ft.colors.ERROR_CONTAINER,
                color=ft.colors.ON_ERROR_CONTAINER,
            )
            if value is None
            else ft.Checkbox(value=value, disabled=True),
        ]


class PatientHistory(ft.Column):
    def __init__(
        self,
        supabase: Client,
        show_snack: Callable,
        on_exit: Callable,
        patient_id: int,
    ) -> None:
        super().__init__()

        self.supabase = supabase
        self.show_snack = show_snack
        self.on_exit = on_exit
        self.patient_id = patient_id

        self.starting_controls = [
            ft.TextButton("Exit", on_click=lambda _: self.on_exit()),
            NewEntry(self.add_entry),
            SuggestedEntry("Suggestion", self.add_entry),
        ]
        self.fetch_history()
        self.controls = self.starting_controls + self.entries

    def fetch_history(self) -> None:
        response = (
            self.supabase.table("entries")
            .select("created_at, name, value")
            .eq("patient", self.patient_id)
            .order("created_at", desc=True)
            .execute()
            .data
        )
        self.entries = [
            Entry(e["created_at"], e["name"], value=e["value"]) for e in response
        ]

    def reload(self) -> None:
        self.controls = self.starting_controls + self.entries
        self.update()

    def add_entry(self, name: str, *, value: bool) -> None:
        self.supabase.table("entries").insert(
            {
                "name": name,
                "value": value,
                "patient": self.patient_id,
                "author": self.supabase.auth.get_user().user.id,
            },
        ).execute()

        self.fetch_history()
        self.reload()
