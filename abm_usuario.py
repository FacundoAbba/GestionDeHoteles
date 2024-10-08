import sqlite3
import flet as ft

RUTA_DB = "C:\\Users\\Usuario\\Documents\\Itec facu\\Segundo\\Programacion\\TrabajoPractico\\GestionDeHoteles.db"

def crear_usuario(nombre, password, email, rol):
    try:
        conn = sqlite3.connect(RUTA_DB, timeout=10)  # Aumentamos el timeout para evitar bloqueo
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Usuario (UsuarioNombre, UsuarioPassword, UsuarioRolId, UsuarioEmail) VALUES (?, ?, ?, ?)",
            (nombre, password, rol, email)
        )
        conn.commit()
        conn.close()

        ft.Text("Éxito", "Usuario creado con éxito.")
    except sqlite3.Error as e:
        ft.Text("Error", f"Error al crear usuario")

def modificar_usuario(usuario_id, nombre, password, rol, email, page):
    try:
        conn = sqlite3.connect(RUTA_DB, timeout=10)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Usuario SET UsuarioPassword = ?, UsuarioEmail = ?, UsuarioRolId = ?, UsuarioNombre = ? WHERE UsuarioId = ?",
            (password, email, rol, nombre, usuario_id)
        )
        conn.commit()
        conn.close()

        # Mostrar mensaje de éxito
        page.snack_bar = ft.SnackBar(ft.Text("Usuario modificado con éxito."), bgcolor=ft.colors.GREEN)
        page.snack_bar.open = True
        page.update()

    except sqlite3.Error as e:
        # Mostrar el error usando Snackbar
        page.snack_bar = ft.SnackBar(ft.Text(f"Error al modificar usuario: {e}"), bgcolor=ft.colors.RED)
        page.snack_bar.open = True
        page.update()

def eliminar_usuario(usuario_id):
    try:
        conn = sqlite3.connect(RUTA_DB, timeout=10)
        cursor = conn.cursor()
        
        # Ejecuta la eliminación
        cursor.execute("DELETE FROM Usuario WHERE UsuarioId = ?", (usuario_id,))
        if cursor.rowcount == 0:
            # No se encontró el usuario
            ft.Text(f"No se encontró un usuario con el ID {usuario_id}", color="red")
            print('no encontrado')
        else:
            conn.commit()
            ft.Text("Usuario eliminado con éxito.", color="green")
        
        conn.close()
    except sqlite3.Error as e:
        # Mensaje de error en caso de excepción
        ft.Text(f"Error al eliminar usuario: {e}", color="red")
        print('error')

def obtener_todos_usuarios():
    try:
        conn = sqlite3.connect(RUTA_DB, timeout=10)
        cursor = conn.cursor()
        cursor.execute("SELECT UsuarioId, UsuarioNombre, UsuarioEmail, UsuarioRolId FROM Usuario")
        usuarios = cursor.fetchall()
        conn.close()
        return usuarios
    except sqlite3.Error as e:
        return f"Error al obtener usuarios: {e}"
