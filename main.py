import os

import flet as ft
from supabase import create_client

from authenticate import Authenticate


def main(page: ft.Page) -> None:
    supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

    authenticate = Authenticate(supabase)
    page.add(authenticate.page)


ft.app(main)
