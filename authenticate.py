from typing import Sequence

import flet as ft


class Authenticate:
    def __init__(self) -> None:
        self.email = ft.TextField(hint_text="Email")
        self.password = ft.TextField(hint_text="Password")
        self.user_options = [
            ft.dropdown.Option("Patient"),
            ft.dropdown.Option("Nurse"),
            ft.dropdown.Option("Doctor"),
        ]
        self.new_user_type = ft.Dropdown(
            hint_text="Who are you signing up as?",
            options=self.user_options,
        )

        self.select_controls = [
            ft.TextButton("Log in", on_click=lambda _: self.open(self.login_controls)),
            ft.TextButton(
                "Sign up",
                on_click=lambda _: self.open(self.sign_up_controls),
            ),
        ]

        self.login_controls = [
            ft.TextButton("Back", on_click=lambda _: self.open(self.select_controls)),
            self.email,
            self.password,
            ft.TextButton("Log in"),
        ]

        self.sign_up_controls = [
            ft.TextButton("Back", on_click=lambda _: self.open(self.select_controls)),
            self.email,
            self.password,
            self.new_user_type,
            ft.TextButton("Sign up"),
        ]

        self.page = ft.Column(self.select_controls)

    def open(self, controls: Sequence[ft.Control]) -> None:
        self.page.controls = controls
        self.page.update()
