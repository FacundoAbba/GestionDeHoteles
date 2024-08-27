def actualizar_usuario(usuario_id, nuevo_nombre, nuevo_password, nuevo_rol_id):
    cursor.execute('''
    UPDATE Usuario
    SET UsuarioNombre = ?, UsuarioPassword = ?, RolId = ?
    WHERE UsuarioId = ?
    ''', (nuevo_nombre, nuevo_password, nuevo_rol_id, usuario_id))
    conn.commit()

# Ejemplo de uso
#actualizar_usuario(1, 'Juan P. Perez', 'newpassword123', 2)
