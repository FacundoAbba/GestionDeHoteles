import flet as ft
from login import Login
from menu_principal import MenuPrincipal
from conexion_bd import conectar_db, obtener_cursor

# Constantes
TITULO_VENTANA = "Sistema de Usuarios"

def main(page: ft.Page):
    page.title = TITULO_VENTANA
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def show_login_page():
        page.clean()
        login_page = Login(page)
        entry_usuario = ft.TextField(hint_text="Usuario")
        entry_contrasena = ft.TextField(hint_text="Contraseña", password=True)
        login_page.mostrar_login(entry_usuario, entry_contrasena)  # Mostrar la página de login
        
    def show_menu_principal(usuario_id: int):
        page.clean()
        menu = MenuPrincipal(page, usuario_id)
        menu.crear_menu()

    # Inicializar la página de login
    show_login_page()

    page.on_route_change = lambda e: (
        show_menu_principal(int(e.route.split("/")[-1])) if e.route.startswith("/menu_principal") else None
    )

# Ejecutar la aplicación Flet
ft.app(target=main)
