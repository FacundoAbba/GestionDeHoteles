import flet as ft
import sqlite3

# Constantes para la base de datos
RUTA_DB = "C:\\Users\\Usuario\\Documents\\Itec facu\\Segundo\\Programacion\\usuarios.db"

# Variable global para el usuario logueado
usuario_logueado = None

def guardar_nueva_contrasena(entry_nueva_contrasena: ft.TextField, page: ft.Page):
    global usuario_logueado
    nueva_contrasena = entry_nueva_contrasena.value

    if not usuario_logueado:
        page.add(ft.Text("No hay ningún usuario logueado.", color="red"))
        page.update()
        return

    try:
        # Conectar a la base de datos
        conn = sqlite3.connect(RUTA_DB)
        cursor = conn.cursor()

        # Actualizar la contraseña
        cursor.execute("UPDATE usuarios SET contrasena = ? WHERE usuario = ?", (nueva_contrasena, usuario_logueado))
        conn.commit()

        # Cerrar la conexión
        conn.close()

        page.add(ft.Text("Contraseña actualizada correctamente.", color="green"))
        page.update()
        # Opcional: Redirigir a otra página
        page.go("/login")
    except sqlite3.Error as e:
        page.add(ft.Text(f"Error al actualizar contraseña: {e}", color="red"))
        page.update()

def actualizar_contrasena(page: ft.Page):
    global usuario_logueado
    if not usuario_logueado:
        page.add(ft.Text("No hay ningún usuario logueado.", color="red"))
        page.update()
        return

    page.clean()
    page.title = "Cambiar Contraseña"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Crear campos de entrada
    entry_usuario_actual = ft.TextField(value=usuario_logueado, enabled=False)
    entry_nueva_contrasena = ft.TextField(placeholder="Ingrese nueva contraseña", password=True)

    # Crear botón de guardar
    btn_guardar = ft.ElevatedButton("Guardar", on_click=lambda e: guardar_nueva_contrasena(entry_nueva_contrasena, page))

    # Añadir elementos a la página
    page.add(
        ft.Text("Usuario"),
        entry_usuario_actual,
        ft.Text("Nueva Contraseña"),
        entry_nueva_contrasena,
        btn_guardar
    )

    page.update()

def main(page: ft.Page):
    # Inicializar la página de actualización de contraseña
    actualizar_contrasena(page)

ft.app(target=main)
