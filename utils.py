import sqlite3
from tkinter import messagebox

# Constantes para la base de datos
RUTA_DB = "C:\\Users\\Usuario\\Documents\\Itec facu\\Segundo\\Programacion\\TrabajoPractico\\GestionDeHoteles.db"

def verificar_credenciales(usuario, contrasena):
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect(RUTA_DB)
        cursor = conn.cursor()

        # Consultar las credenciales
        cursor.execute("SELECT * FROM Usuario WHERE UsuarioNombre = ? AND UsuarioPassword = ?", (usuario, contrasena))
        resultado = cursor.fetchone()

        # Cerrar la conexión
        conn.close()

        # Verificar si se encontró un resultado
        if resultado is not None:
            return True
        else:
            return False
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error al verificar credenciales: {e}")
        return False

def get_rol(usuario_id):
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect(RUTA_DB)
        cursor = conn.cursor()

        # Consultar el rol del usuario
        cursor.execute("SELECT UsuarioRolId FROM Usuario WHERE UsuarioId = ?", (usuario_id,))
        rol_id = cursor.fetchone()[0]

        # Cerrar la conexión
        conn.close()

        return rol_id
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error al obtener rol: {e}")
        return None