from typing import Callable

import flet as ft
from supabase import Client


class NewEntry(ft.Row):
    def __init__(self, cb: Callable) -> None:
        super().__init__()
        self.cb = cb
        self.name = ft.TextField(hint_text="Entry type")
        self.value = ft.TextField(hint_text="Description")
        self.controls = [
            self.name,
            self.value,
            ft.FloatingActionButton(icon=ft.icons.ADD, on_click=self.add_clicked),
        ]

    def add_clicked(self, _: None) -> None:
        self.cb(self.name.value, self.value.value)
        self.name.value = ""
        self.value.value = ""


class SuggestedEntry(ft.Row):
    def __init__(self, name: str, ans_cb: Callable, no_ans_cb: Callable) -> None:
        super().__init__()
        self.value = ft.TextField(hint_text="Description")
        self.controls = [
            ft.Text(name),
            self.value,
            ft.FloatingActionButton(
                icon=ft.icons.ADD,
                on_click=lambda _: ans_cb(name, self.value.value),
            ),
            ft.TextButton("Unable to answer", on_click=lambda _: no_ans_cb(name)),
        ]


class Entry(ft.Row):
    def __init__(
        self,
        created_at: str,
        name: str,
        value: str,
        *,
        answered: bool,
    ) -> None:
        super().__init__()
        self.controls = [
            ft.Text(created_at),
            ft.Text(name),
            ft.Text(value)
            if answered
            else ft.Text(
                "Not answered",
                bgcolor=ft.colors.ERROR_CONTAINER,
                color=ft.colors.ON_ERROR_CONTAINER,
            ),
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
            NewEntry(self.add_answered),
            SuggestedEntry("Suggestion", self.add_answered, self.add_unanswered),
        ]
        self.fetch_history()
        self.controls = self.starting_controls + self.entries

    def fetch_history(self) -> None:
        response = (
            self.supabase.table("text_entries")
            .select("created_at, name, value, answered")
            .eq("patient", self.patient_id)
            .order("created_at", desc=True)
            .execute()
            .data
        )
        self.entries = [
            Entry(e["created_at"], e["name"], e["value"], answered=e["answered"])
            for e in response
        ]

    def reload(self) -> None:
        self.controls = self.starting_controls + self.entries
        self.update()

    def add_entry(self, name: str, value: str, *, answered: bool) -> None:
        self.supabase.table("text_entries").insert(
            {
                "name": name,
                "value": value,
                "patient": self.patient_id,
                "author": self.supabase.auth.get_user().user.id,
                "answered": answered,
            },
        ).execute()

        self.fetch_history()
        self.reload()

    def add_answered(self, name: str, value: str) -> None:
        self.add_entry(name, value, answered=True)

    def add_unanswered(self, name: str) -> None:
        self.add_entry(name, "", answered=False)
