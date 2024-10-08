import sqlite3
from tkinter import messagebox
import random

# Constantes para la base de datos
RUTA_DB = "C:\\Users\\Usuario\\Documents\\Itec facu\\Segundo\\Programacion\\TrabajoPractico\\GestionDeHoteles.db"

def verificar_credenciales(usuario_email, contrasena):
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect(RUTA_DB)
        cursor = conn.cursor()

        # Consultar las credenciales
        cursor.execute("SELECT * FROM Usuario WHERE UsuarioEmail = ? AND UsuarioPassword = ?", (usuario_email, contrasena))
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

def obtener_rol_usuario(usuario_id):
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect(RUTA_DB)
        cursor = conn.cursor()

        print('usuario_id: ' + str(usuario_id))
        
        # Consultar el rol del usuario
        cursor.execute("SELECT UsuarioRolId FROM Usuario WHERE UsuarioId = ?", (usuario_id,))
        usuario_rol = cursor.fetchone()[0]

        # Cerrar la conexión
        conn.close()

        return usuario_rol
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error al obtener rol: {e}")
        return None
        
def generar_codigo_reserva():
    try:
        conn = sqlite3.connect(RUTA_DB)
        cursor = conn.cursor()
                
        # Generar un código único
        while True:
            codigo = random.randint(100000, 999999)  # Código aleatorio de 6 dígitos
                    
            # Verificar si el código ya existe en la tabla Reserva
            cursor.execute('SELECT COUNT(*) FROM Reserva WHERE ReservaCodigo = ?', (codigo,))
            if cursor.fetchone()[0] == 0:
                # Código único encontrado
                break
                
        conn.close()
        return codigo

    except sqlite3.Error as e:
        print(f"Error al generar el código de reserva: {e}")
        return None
    
def obtener_usuario_id(usuario_email):
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect(RUTA_DB)
        cursor = conn.cursor()

        # Consultar el rol del usuario
        cursor.execute("SELECT UsuarioId FROM Usuario WHERE UsuarioEmail = ?", (usuario_email,))
        usuario_rol = cursor.fetchone()[0]

        # Cerrar la conexión
        conn.close()

        return usuario_rol
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error al obtener usuario email: {e}")
        return None
    
def obtener_usuario_nombre(usuario_id):
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect(RUTA_DB)
        cursor = conn.cursor()

        # Consultar el rol del usuario
        cursor.execute("SELECT UsuarioNombre FROM Usuario WHERE UsuarioId = ?", (usuario_id,))
        usuario_nombre = cursor.fetchone()[0]

        # Cerrar la conexión
        conn.close()

        return usuario_nombre
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error al obtener usuario id: {e}")
        return None
    
def obtener_usuario_email(usuario_id):
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect(RUTA_DB)
        cursor = conn.cursor()

        # Consultar el rol del usuario
        cursor.execute("SELECT UsuarioEmail FROM Usuario WHERE UsuarioId = ?", (usuario_id,))
        usuario_email = cursor.fetchone()[0]

        # Cerrar la conexión
        conn.close()

        return usuario_email
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error al obtener usuario id: {e}")
        return None    
        
def activar_tarjeta_si_inactiva(habitacion_nro):
    try:
        # Imprimir el valor recibido
        print(f"Valor de habitacion_nro recibido: {habitacion_nro}")

        # Establecer la conexión con la base de datos
        conexion = sqlite3.connect(RUTA_DB)
        cursor = conexion.cursor()

        # Realizar la consulta
        cursor.execute("SELECT HabitacionTarjetaActiva FROM Habitacion WHERE HabitacionNumero = ?", (habitacion_nro,))
        resultado = cursor.fetchone()

        if resultado is None:
            print(f"No se encontró ninguna habitación con el número {habitacion_nro}.")
            return

        # Extraer el valor de HabitacionTarjetaActiva
        tarjeta_activa = resultado[0]
        print(f"Resultado de HabitacionTarjetaActiva: {tarjeta_activa}")

        # Si la tarjeta está inactiva (0), activarla
        if tarjeta_activa == 0:
            cursor.execute("UPDATE Habitacion SET HabitacionTarjetaActiva = 1 WHERE HabitacionNumero = ?", (habitacion_nro,))
            conexion.commit()
            print(f"Tarjeta de la habitación {habitacion_nro} activada con éxito.")
            return "Tarjeta de la habitación " + str(habitacion_nro) + " activada con éxito. Check-in exitoso."
        else:
            print(f"La tarjeta de la habitación {habitacion_nro} ya está activa.")
            return "La tarjeta de la habitación " + str(habitacion_nro) + " ya está activa."
            
    except sqlite3.Error as e:
        print(f"Error al activar la tarjeta: {e}")
     # Cerrar la conexión
        conexion.close()

# Función para desactivar la tarjeta si está activa
def desactivar_tarjeta_si_activa(habitacion_nro):
    try:
        conexion = sqlite3.connect(RUTA_DB)
        cursor = conexion.cursor()

        # Consultar si la tarjeta está activa (HabitacionTarjetaActiva = 1)
        cursor.execute("SELECT HabitacionTarjetaActiva FROM Habitacion WHERE HabitacionNumero = ?", (habitacion_nro,))
        resultado = cursor.fetchone()

        if resultado and resultado[0] == 1:  # Si la tarjeta está activa (1)
            cursor.execute("UPDATE Habitacion SET HabitacionTarjetaActiva = 0 WHERE HabitacionNumero = ?", (habitacion_nro,))
            conexion.commit()
            print(f"Tarjeta de la habitación {habitacion_nro} desactivada con éxito.")
            return "Tarjeta de la habitación " + str(habitacion_nro) + " desactivada con éxito. Check-out exitoso."
        else:
            print(f"La tarjeta de la habitación {habitacion_nro} ya está inactiva o no se encontró la habitación.")
            return "La tarjeta de la habitación " + str(habitacion_nro) + " ya está inactiva."
        
    except sqlite3.Error as e:
        print(f"Error al desactivar la tarjeta: {e}")
        
        conexion.close()
def obtener_habitacion_desc(habitacion_id):
    # Conectar a la base de datos
    conn = sqlite3.connect(RUTA_DB)
    cursor = conn.cursor()

    # Ejecutar la consulta para obtener la descripción de la habitación
    cursor.execute("SELECT HabitacionDesc FROM Habitacion WHERE HabitacionId = ?", (habitacion_id,))

    # Obtener el resultado
    habitacion_desc = cursor.fetchone()

    # Cerrar la conexión
    conn.close()

    # Devolver la descripción si se encuentra la habitación, de lo contrario None
    if habitacion_desc:
        return habitacion_desc[0]  # El resultado es una tupla, devolver solo el primer valor
    else:
        return None