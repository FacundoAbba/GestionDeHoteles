import flet as ft
from utils import verificar_credenciales, obtener_rol_usuario, obtener_usuario_id
from menu_principal_admin import MenuPrincipalAdmin
from menu_principal_usuario import MenuPrincipalUsuario
from abm_usuario import crear_usuario  # Importamos la función para crear usuarios

class Login:
    def __init__(self, page: ft.Page):
        self.page = page

    def mostrar_login(self):
        # Limpiar la pantalla antes de mostrar el login
        self.page.clean()

        # Campos de entrada para usuario y contraseña
        entry_usuario = ft.TextField(
            label="Usuario",
            hint_text="Ingrese su email",
            bgcolor=ft.colors.WHITE,
            width=300,
            text_align=ft.TextAlign.CENTER
        )
        entry_contrasena = ft.TextField(
            label="Contraseña",
            hint_text="Ingrese su contraseña",
            password=True,
            bgcolor=ft.colors.WHITE,
            width=300,
            text_align=ft.TextAlign.CENTER
        )

        # Función al hacer clic en "Iniciar sesión"
        def iniciar_sesion(e):
            usuario_email = entry_usuario.value
            contrasena = entry_contrasena.value

            if verificar_credenciales(usuario_email, contrasena):
                self.page.clean()  # Limpiar la pantalla de login

                usuario_id = obtener_usuario_id(usuario_email)
                rol_usuario = obtener_rol_usuario(usuario_id)

                # Mostrar el menú correspondiente según el rol
                if rol_usuario == 1:
                    menu = MenuPrincipalAdmin(self.page, usuario_id)
                elif rol_usuario == 2:
                    menu = MenuPrincipalUsuario(self.page, usuario_id)
                else:
                    self.page.add(ft.Text("Rol no reconocido", color="red"))
                    return
                
                menu.crear_menu()  # Mostrar el menú del rol correspondiente

            else:
                self.page.add(ft.Text("Credenciales incorrectas", color="red"))
                self.page.update()

        # Función para ir a la pantalla de registro
        def registrarse(e):
            self.mostrar_registro()  # Cambiar a la pantalla de registro

        # Contenedor del formulario centrado
        contenedor_formulario = ft.Container(
            content=ft.Column(
                [
                    ft.Text("HOTEL LA PERLA", size=32, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE),
                    ft.Text("Ingrese sus credenciales", size=18, color=ft.colors.GREY),
                    entry_usuario,
                    entry_contrasena,
                    ft.ElevatedButton(
                        "Iniciar sesión",
                        on_click=iniciar_sesion,
                        bgcolor=ft.colors.BLUE,
                        color=ft.colors.WHITE,
                        width=150,
                        height=50
                    ),
                    ft.ElevatedButton(
                        "Registrarse",  # Botón de registro
                        on_click=registrarse,
                        bgcolor=ft.colors.GREEN,  # Color verde para el botón de registro
                        color=ft.colors.WHITE,
                        width=150,
                        height=50
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=30,
            ),
            padding=50,
            width=400,
            height=500,
            alignment=ft.alignment.center,
            bgcolor=ft.colors.with_opacity(0.1, ft.colors.BLUE_GREY),
        )

        # Agregar solo el formulario centrado
        self.page.add(ft.Container(content=contenedor_formulario, alignment=ft.alignment.center))
        self.page.update()  # Actualizar la pantalla

    # Función para mostrar el formulario de registro
    def mostrar_registro(self):
        # Limpiamos la pantalla actual antes de mostrar el formulario de registro
        self.page.clean()

        # Campos para el registro de usuario
        entry_nombre = ft.TextField(
            label="Nombre de Usuario",
            hint_text="Ingrese su nombre de usuario",
            bgcolor=ft.colors.WHITE,
            width=300,
            text_align=ft.TextAlign.CENTER
        )
        entry_contrasena = ft.TextField(
            label="Contraseña",
            hint_text="Ingrese su contraseña",
            password=True,
            bgcolor=ft.colors.WHITE,
            width=300,
            text_align=ft.TextAlign.CENTER
        )
        entry_email = ft.TextField(
            label="Email",
            hint_text="Ingrese su email",
            bgcolor=ft.colors.WHITE,
            width=300,
            text_align=ft.TextAlign.CENTER
        )

        # Función para crear el usuario
        def confirmar_registro(e):
            nombre = entry_nombre.value
            contrasena = entry_contrasena.value
            email = entry_email.value

            if nombre and contrasena and email:
                # Crear el usuario utilizando la función de abm_usuario
                crear_usuario(nombre, contrasena, email, 2)
                self.page.add(ft.Text("Usuario creado exitosamente", color="green"))
            else:
                self.page.add(ft.Text("Todos los campos son obligatorios", color="red"))

            self.page.update()

        # Botón de confirmación de registro y botón de volver
        boton_registro = ft.ElevatedButton(
            "Confirmar Registro",
            on_click=confirmar_registro,
            bgcolor=ft.colors.BLUE,
            color=ft.colors.WHITE,
            width=200,
            height=50
        )

        # Ajuste del botón "Volver"
        boton_volver = ft.ElevatedButton(
            "Volver",
            on_click=lambda e: self.mostrar_login(),
            bgcolor=ft.colors.RED,
            color=ft.colors.WHITE,
            width=150,
            height=50
        )

        # Contenedor del formulario de registro centrado
        contenedor_registro = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Registro de Nuevo Usuario", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE),
                    entry_nombre,
                    entry_contrasena,
                    entry_email,
                    boton_registro,
                    boton_volver  # Asegurarse que el botón "Volver" esté bien colocado
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=30,
            ),
            padding=50,
            width=400,
            height=600,  # Incrementé la altura para evitar solapamiento de elementos
            alignment=ft.alignment.center,
            bgcolor=ft.colors.with_opacity(0.1, ft.colors.BLUE_GREY),
        )

        # Agregar el formulario de registro
        self.page.add(ft.Container(content=contenedor_registro, alignment=ft.alignment.center))
        self.page.update()  # Asegurarse de actualizar la pantalla
