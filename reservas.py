import sqlite3
from datetime import datetime

# Constantes para la base de datos
RUTA_DB = "C:\\Users\\Usuario\\Documents\\Itec facu\\Segundo\\Programacion\\TrabajoPractico\\GestionDeHoteles.db"

def obtener_habitaciones_disponibles(fecha_desde, fecha_hasta, cantidad_personas):
    try:
        conn = sqlite3.connect(RUTA_DB)
        cursor = conn.cursor()
        
        # Convertir fechas a formato adecuado
        fecha_desde = datetime.strptime(fecha_desde, '%Y-%m-%d')
        fecha_hasta = datetime.strptime(fecha_hasta, '%Y-%m-%d')

        # Consulta para obtener las habitaciones disponibles
        query = '''
        SELECT h.HabitacionId, h.HabitacionPiso, h.HabitacionNumero
        FROM Habitacion h
        WHERE h.HabitacionCapacidad >= ?
        AND h.HabitacionId NOT IN (
            SELECT HabitacionId
            FROM Reserva r
            WHERE (
                ReservaFchDes <= ? AND ReservaFchHas >= ?
            )
        )
        '''
        cursor.execute(query, (cantidad_personas, fecha_hasta, fecha_desde))
        habitaciones_disponibles = cursor.fetchall()
        conn.close()
        return habitaciones_disponibles
    except sqlite3.Error as e:
        return [], f"Error al buscar habitaciones disponibles: {e}"
