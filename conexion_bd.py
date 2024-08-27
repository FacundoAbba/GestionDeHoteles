import sqlite3

# Ruta de la base de datos
RUTA_DB = 'C:\\Users\\Usuario\\Documents\\Itec facu\\Segundo\\Programacion\\TrabajoPractico\\GestionDeHoteles.db'

# Función para conectar a la base de datos
def conectar_db():
    try:
        conn = sqlite3.connect(RUTA_DB)
        return conn
    except sqlite3.Error as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None

# Función para obtener el cursor de la base de datos
def obtener_cursor():
    conn = conectar_db()
    if conn:
        return conn.cursor()
    else:
        return None

# Función para cerrar la conexión con la base de datos
def cerrar_conexion(conn):
    try:
        conn.close()
    except sqlite3.Error as e:
        print(f"Error al cerrar la conexión con la base de datos: {e}")

# Ejemplo de uso
if __name__ == "__main__":
    conn = conectar_db()
    cursor = obtener_cursor()
    if cursor:
        # Aquí puedes ejecutar consultas con el cursor
        cursor.execute("SELECT * FROM tu_tabla")
        resultados = cursor.fetchall()
        for resultado in resultados:
            print(resultado)
        cerrar_conexion(conn)