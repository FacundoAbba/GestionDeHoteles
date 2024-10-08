import flet as ft
from login import Login

def main(page: ft.Page):
    login_page = Login(page)
    login_page.mostrar_login()  # Mostrar la pantalla de login al iniciar

ft.app(target=main)
