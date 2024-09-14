from typing import Callable, Sequence

import flet as ft
from supabase import Client


class Authenticate:
    def __init__(
        self,
        supabase: Client,
        show_snack: Callable,
        on_success: Callable,
    ) -> None:
        self.supabase = supabase
        self.show_snack = show_snack
        self.on_success = on_success

        self.email = ft.TextField(hint_text="Email")
        self.password = ft.TextField(hint_text="Password", password=True)

        self.user_type = ft.Dropdown(
            hint_text="Select user type",
            options=[
                ft.dropdown.Option("Nurse"),
                ft.dropdown.Option("Doctor"),
            ],
        )

        self.select_controls = [
            ft.TextButton(
                "Sign in",
                on_click=lambda _: self.open(self.sign_in_controls),
            ),
            ft.TextButton(
                "Sign up",
                on_click=lambda _: self.open(self.sign_up_controls),
            ),
        ]

        self.sign_in_controls = [
            ft.TextButton("Back", on_click=lambda _: self.open(self.select_controls)),
            self.email,
            self.password,
            ft.TextButton("Sign in", on_click=self.sign_in),
        ]

        self.confirm_type_controls = [
            self.user_type,
            ft.TextButton("Confirm", on_click=self.confirm_type),
        ]

        self.sign_up_controls = [
            ft.TextButton("Back", on_click=lambda _: self.open(self.select_controls)),
            self.email,
            self.password,
            ft.TextButton("Sign up", on_click=self.sign_up),
        ]

        self.controls = ft.Column(self.select_controls)

    def open(self, controls: Sequence[ft.Control]) -> None:
        self.controls.controls = controls
        self.controls.update()

    def sign_in(self, _: None) -> None:
        self.supabase.auth.sign_in_with_password(
            {"email": self.email.value, "password": self.password.value},
        )

        response = (
            self.supabase.table("profiles")
            .select("")
            .eq("id", self.supabase.auth.get_user().user.id)
            .execute()
            .data
        )

        if len(response) == 0:
            self.open(self.confirm_type_controls)
        else:
            self.on_success()

    def confirm_type(self, _: None) -> None:
        if not self.user_type.value:
            self.show_snack(ft.SnackBar(ft.Text("Select a user type.")))
            return

        self.supabase.table("profiles").insert(
            {
                "id": self.supabase.auth.get_user().user.id,
                "type": self.user_type.value.lower(),
            },
        ).execute()

        self.on_success()

    def sign_up(self, _: None) -> None:
        self.supabase.auth.sign_up(
            {"email": self.email.value, "password": self.password.value},
        )
        self.show_snack(ft.SnackBar(ft.Text("Success! Please sign in.")))

        self.open(self.sign_in_controls)
