from typing import Callable, Sequence

import flet as ft
from supabase import Client


class NewEntry(ft.Row):
    def __init__(self, cb: Callable) -> None:
        super().__init__()
        self.name = ft.TextField(hint_text="Entry type")
        self.value = ft.TextField(hint_text="Description")
        self.controls = [
            self.name,
            self.value,
            ft.FloatingActionButton(
                icon=ft.icons.ADD,
                on_click=lambda _: cb(self.name.value, self.value.value),
            ),
        ]


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
    def __init__(self, name: str, value: str) -> None:  # add date/time
        super().__init__()
        self.controls = [ft.Text(name), ft.Text(value)]


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

        self.controls = [
            ft.TextButton("Exit", on_click=lambda _: self.on_exit()),
            NewEntry(self.add_answered),
            SuggestedEntry("Suggestion", self.add_answered, self.add_unanswered),
            Entry("Name", "Value"),
        ]

    def open(self, controls: Sequence[ft.Control]) -> None:
        self.controls = controls
        self.update()

    def add_answered(self, name: str, value: str) -> None:
        self.supabase.table("text_entries").insert(
            {
                "name": name,
                "value": value,
                "patient": self.patient_id,
                "author": self.supabase.auth.get_user().user.id,
                "answered": True,
            },
        ).execute()

    def add_unanswered(self, name: str) -> None:
        self.supabase.table("text_entries").insert(
            {
                "name": name,
                "value": "",
                "patient": self.patient_id,
                "author": self.supabase.auth.get_user().user.id,
                "answered": False,
            },
        ).execute()
