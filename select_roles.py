def seleccionar_roles():
    cursor.execute('SELECT * FROM Rol')
    return cursor.fetchall()

# Ejemplo de uso
#roles = seleccionar_roles()
#for rol in roles:
#    print(rol)
