def insertar_usuario(nombre, password, rol_id):
    cursor.execute('''
    INSERT INTO Usuario (UsuarioNombre, UsuarioPassword, RolId)
    VALUES (?, ?, ?)
    ''', (nombre, password, rol_id))
    conn.commit()

# Ejemplo de uso
#insertar_usuario('Juan Perez', 'password123', 1)
