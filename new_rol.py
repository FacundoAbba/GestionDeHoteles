def actualizar_rol(rol_id, nuevo_desc):
    cursor.execute('''
    UPDATE Rol
    SET RolDesc = ?
    WHERE RolId = ?
    ''', (nuevo_desc, rol_id))
    conn.commit()

# Ejemplo de uso
#actualizar_rol(1, 'Super Administrador')
