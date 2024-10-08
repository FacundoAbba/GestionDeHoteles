#ALTA - BAJA - MODIFICACIÓN - HABITACION
import sqlite3
import flet as ft

RUTA_DB = "C:\\Users\\Usuario\\Documents\\Itec facu\\Segundo\\Programacion\\TrabajoPractico\\GestionDeHoteles.db"


# Función para añadir una nueva habitación a la base de datos
def agregar_habitacion(habitacion_piso, habitacion_numero, habitacion_disp, habitacion_capacidad, habitacion_monto, habitacion_desc):
    try: 
        conexion = sqlite3.connect(RUTA_DB)
        cursor = conexion.cursor()
        cursor.execute('''
            INSERT INTO Habitacion (HabitacionPiso, HabitacionNumero, HabitacionDisp, HabitacionCapacidad, HabitacionMontoXDia, HabitacionDesc)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (habitacion_piso, habitacion_numero, habitacion_disp, habitacion_capacidad, habitacion_monto, habitacion_desc))
        conexion.commit()
        conexion.close()
        ft.Text("Éxito", "Habitación creada con éxito.")
    except sqlite3.Error as e:
        ft.Text("Error", f"Error al crear habitación: {e}")

# Función para modificar una habitación existente en la base de datos
def modificar_habitacion(habitacion_id, habitacion_piso, habitacion_numero, habitacion_disp, habitacion_capacidad, habitacion_monto, habitacion_desc):
    try:
        conexion = sqlite3.connect(RUTA_DB)
        cursor = conexion.cursor()
        cursor.execute('''
        UPDATE Habitacion
        SET HabitacionPiso = ?, HabitacionNumero = ?, HabitacionDisp = ?, HabitacionCapacidad = ?, HabitacionMontoXDia = ?, HabitacionDesc = ?
        WHERE HabitacionId = ?
        ''', (habitacion_piso, habitacion_numero, habitacion_disp, habitacion_capacidad, habitacion_monto, habitacion_desc, habitacion_id))
        conexion.commit()
        conexion.close()
        ft.Text("Éxito", "Habitación modificada con éxito.")
    except sqlite3.Error as e:
        ft.Text("Error", f"Error al modificar habitación: {e}")

# Función para eliminar una habitación de la base de datos
def eliminar_habitacion(habitacion_id):
    try:
        conexion = sqlite3.connect(RUTA_DB)
        cursor = conexion.cursor()
        cursor.execute('DELETE FROM Habitacion WHERE HabitacionId = ?', (habitacion_id,))
        conexion.commit()
        conexion.close()
        ft.Text("Éxito", "Habitación eliminada con éxito.")
    except sqlite3.Error as e:
        ft.Text("Error", f"Error al eliminar habitación: {e}")

def obtener_todas_las_habitaciones():
    conn = sqlite3.connect(RUTA_DB)
    cursor = conn.cursor()

    query = """
    SELECT HabitacionId, HabitacionPiso, HabitacionNumero, HabitacionDisp, HabitacionCapacidad, HabitacionMontoXDia, HabitacionDesc
    FROM Habitacion
    """
    cursor.execute(query)
    habitaciones = cursor.fetchall()

    conn.close()
    return habitaciones