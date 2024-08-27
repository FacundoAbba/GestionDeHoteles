import flet as ft
from utils import verificar_credenciales

class Login:
    def __init__(self, page: ft.Page):
        self.page = page

    def mostrar_login(self, entry_usuario: ft.TextField, entry_contrasena: ft.TextField):
        def iniciar_sesion(e):
            usuario = entry_usuario.value
            contrasena = entry_contrasena.value
            if verificar_credenciales(usuario, contrasena):
                # Iniciar sesión exitosamente
                self.page.add(ft.Text("Inicio de sesión exitoso", color="green"))
                self.page.update()
                # Redirigir a la página del menú principal con un usuario_id ficticio (cambiar según sea necesario)
                self.page.go(f"/menu_principal/{self.obtener_usuario_id(usuario)}")
            else:
                self.page.add(ft.Text("Credenciales incorrectas", color="red"))
                self.page.update()

        self.page.add(
            ft.Column(
                [
                    ft.Text("Ingrese sus credenciales"),
                    entry_usuario,
                    entry_contrasena,
                    ft.ElevatedButton("Iniciar sesión", on_click=iniciar_sesion)
                ]
            )
        )

    def obtener_usuario_id(self, usuario: str) -> int:
        # Lógica para obtener el ID del usuario. Aquí es un valor ficticio.
        return 1

    """def mostrar_login(self):
        self.page.clean()
        self.page.title = "Login"
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        # Crear campos de entrada
        entry_usuario = ft.TextField(hint_text="Usuario")
        entry_contrasena = ft.TextField(hint_text="Contraseña", password=True)

        # Crear botón de login
        btn_login = ft.ElevatedButton("Iniciar Sesión", on_click=lambda e: self.login(entry_usuario, entry_contrasena))

        # Añadir elementos a la página
        self.page.add(
            ft.Text("Iniciar Sesión", size=30),
            entry_usuario,
            entry_contrasena,
            btn_login
        )

        self.page.update()"""
