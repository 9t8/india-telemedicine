from typing import Callable, Sequence

import flet as ft
from supabase import Client


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
                ft.Row(
                    [
                        ft.TextField(hint_text="Entry type"),
                        ft.TextField(hint_text="Description"),
                        ft.FloatingActionButton(icon=ft.icons.ADD),
                    ],
                ),
            ],
        )

    def open(self, controls: Sequence[ft.Control]) -> None:
        self.controls.controls = controls
        self.controls.update()
