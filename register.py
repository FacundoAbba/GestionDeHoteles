import flet as ft
import sqlite3

# Constantes para la base de datos
RUTA_DB = "C:\\Users\\Usuario\\Documents\\Itec facu\\Segundo\\Programacion\\GestionDeHoteles.db"

def registrar_usuario(entry_nuevo_usuario: ft.TextField, entry_nueva_contrasena: ft.TextField, page: ft.Page):
    nuevo_usuario = entry_nuevo_usuario.value
    nueva_contrasena = entry_nueva_contrasena.value

    if not nuevo_usuario or not nueva_contrasena:
        page.add(ft.Text("Por favor, complete todos los campos.", color="red"))
        page.update()
        return

    try:
        # Conectar a la base de datos
        conn = sqlite3.connect(RUTA_DB)
        cursor = conn.cursor()

        # Insertar el nuevo usuario
        cursor.execute("INSERT INTO Usuario (usuario, contrasena) VALUES (?, ?)", (nuevo_usuario, nueva_contrasena))
        conn.commit()

        # Cerrar la conexión
        conn.close()

        page.add(ft.Text("Usuario registrado correctamente.", color="green"))
        page.update()
        # Opcional: Redirigir o cerrar la página actual
        page.go("/login")
    except sqlite3.IntegrityError:
        page.add(ft.Text("El usuario ya existe.", color="red"))
        page.update()
    except sqlite3.Error as e:
        page.add(ft.Text(f"Error al registrar usuario: {e}", color="red"))
        page.update()

def crear_cuenta(page: ft.Page):
    def on_registrar_click(e):
        registrar_usuario(entry_nuevo_usuario, entry_nueva_contrasena, page)

    # Configurar la página de registro
    page.clean()
    page.title = "Registrar Usuario"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Crear campos de entrada
    entry_nuevo_usuario = ft.TextField(placeholder="Ingrese nuevo usuario")
    entry_nueva_contrasena = ft.TextField(placeholder="Ingrese nueva contraseña", password=True)

    # Crear botón de registro
    btn_registrar = ft.ElevatedButton("Registrar", on_click=on_registrar_click)

    # Añadir elementos a la página
    page.add(
        ft.Text("Nuevo Usuario"),
        entry_nuevo_usuario,
        ft.Text("Nueva Contraseña"),
        entry_nueva_contrasena,
        btn_registrar
    )

    page.update()

def main(page: ft.Page):
    crear_cuenta(page)

ft.app(target=main)
