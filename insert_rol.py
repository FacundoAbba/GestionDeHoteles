def insertar_rol(rol_desc):
    cursor.execute('''
    INSERT INTO Rol (RolDesc)
    VALUES (?)
    ''', (rol_desc,))
    conn.commit()

# Ejemplo de uso
#insertar_rol('Administrador')
