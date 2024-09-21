from collections.abc import Callable

import flet as ft


class SelectPatient(ft.Column):
    def __init__(
        self,
        show_snack: Callable,
        on_confirm: Callable,
    ) -> None:
        super().__init__()

        self.show_snack = show_snack
        self.on_confirm = on_confirm

        self.patient_id = ft.TextField(
            hint_text="Patient ID",
            keyboard_type=ft.KeyboardType.NUMBER,
        )

        self.controls = [
            self.patient_id,
            ft.TextButton(
                "Confirm",
                on_click=lambda _: self.on_confirm(self.patient_id.value),
            ),
        ]
