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
    def __init__(self, cb: Callable, name: str) -> None:
        super().__init__()
        self.value = ft.TextField(hint_text="Description")
        self.controls = [
            ft.Text(name),
            self.value,
            ft.FloatingActionButton(
                icon=ft.icons.ADD,
                on_click=lambda _: cb(name, self.value.value),
            ),
        ]


class Entry(ft.Row):
    def __init__(self, name: str, value: str) -> None:  # add date/time
        super().__init__()
        self.controls = [ft.Text(name), ft.Text(value)]


class PatientHistory:
    def __init__(
        self,
        supabase: Client,
        show_snack: Callable,
        on_exit: Callable,
        patient_id: int,
    ) -> None:
        self.supabase = supabase
        self.show_snack = show_snack
        self.on_exit = on_exit
        self.patient_id = patient_id

        self.controls = ft.Column(
            [
                ft.TextButton("Exit", on_click=lambda _: self.on_exit()),
                NewEntry(print),
                SuggestedEntry(print, "Suggestion"),
                Entry("Name", "Value"),
            ],
        )

    def open(self, controls: Sequence[ft.Control]) -> None:
        self.controls.controls = controls
        self.controls.update()
