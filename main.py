import flet as ft

from authenticate import Authenticate


def main(page: ft.Page) -> None:
    authenticate = Authenticate()
    page.add(authenticate.page)


ft.app(main)
