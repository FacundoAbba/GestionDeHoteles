def seleccionar_usuarios():
    cursor.execute('SELECT * FROM Usuario')
    return cursor.fetchall()

# Ejemplo de uso
#usuarios = seleccionar_usuarios()
#for usuario in usuarios:
#    print(usuario)
