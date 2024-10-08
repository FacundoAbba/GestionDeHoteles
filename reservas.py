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
        SELECT h.HabitacionId, h.HabitacionPiso, h.HabitacionNumero, h.HabitacionDesc, h.HabitacionMontoXDia
        FROM Habitacion h
        WHERE h.HabitacionCapacidad = ? and h.HabitacionDisp = 1
        AND h.HabitacionNumero NOT IN (
            SELECT r.ReservaHabitacionNumero
            FROM Reserva r
            WHERE (
                ? <= r.ReservaFchHas and ? >= r.ReservaFchDes
            )
        )
        '''
        cursor.execute(query, (cantidad_personas, fecha_hasta, fecha_desde))
        habitaciones_disponibles = cursor.fetchall()
        conn.close()
        return habitaciones_disponibles, None  # Éxito sin errores
    except sqlite3.Error as e:
        return [], f"Error al buscar habitaciones disponibles: {e}"
    
def obtener_todas_las_reservas():
    try:
        conn = sqlite3.connect(RUTA_DB)
        cursor = conn.cursor()
        cursor.execute("SELECT ReservaId, ReservaFchDes, ReservaFchHas, ReservaMonto, ReservaHabitacionNumero, ReservaCodigo, ReservaUsuarioId FROM Reserva")
        reservas = cursor.fetchall()
        conn.close()
        return reservas
    except sqlite3.Error as e:
        print(f"Error al obtener reservas: {e}")
        return None