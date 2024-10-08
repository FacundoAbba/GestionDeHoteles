import flet as ft
from abm_usuario import crear_usuario, eliminar_usuario, modificar_usuario, obtener_todos_usuarios
from abm_habitacion import agregar_habitacion, eliminar_habitacion, modificar_habitacion, obtener_todas_las_habitaciones
from utils import obtener_usuario_nombre, obtener_habitacion_desc, desactivar_tarjeta_si_activa, activar_tarjeta_si_inactiva
from reservas import obtener_todas_las_reservas
from datetime import datetime
from datetime import date
import sqlite3

RUTA_DB = "C:\\Users\\Usuario\\Documents\\Itec facu\\Segundo\\Programacion\\TrabajoPractico\\GestionDeHoteles.db"

# Función para obtener una conexión a la base de datos con timeout
def get_db_connection():
    return sqlite3.connect(RUTA_DB, timeout=10)

class MenuPrincipalAdmin:
    def __init__(self, page: ft.Page, usuario_id: int):
        self.page = page
        self.usuario_id = usuario_id
        self.page.title = "Menú Principal"
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.padding = ft.padding.all(20)
        self.page.theme_mode = ft.ThemeMode.LIGHT  # Tema claro

    def agregar_habitacion(self, e=None):
        self.page.controls.clear()

        titulo = ft.Text("Agregar nueva habitación", size=24, weight=ft.FontWeight.BOLD)

        piso_input = ft.TextField(label="Piso", width=300)
        numero_input = ft.TextField(label="Número de habitación", width=300)
        disponible_input = ft.Dropdown(
            label="Disponibilidad",
            options=[
                ft.dropdown.Option("Disponible"),
                ft.dropdown.Option("No disponible")
            ],
            width=300
        )
        capacidad_input = ft.TextField(label="Capacidad", width=300)
        montoxdia_input = ft.TextField(label="Monto por día", width=300)
        descripcion_input = ft.TextField(label="Descripción", width=300)

        def guardar_habitacion(e):
            try:
                piso = int(piso_input.value)
                numero = int(numero_input.value)
                disponible = 1 if disponible_input.value == "Disponible" else 0
                capacidad = int(capacidad_input.value)
                montoxdia = float(montoxdia_input.value)
                descripcion = descripcion_input.value

                # Llamar a la función de abm_habitacion.py para crear la habitación
                agregar_habitacion(piso, numero, disponible, capacidad, montoxdia, descripcion)

                self.page.add(ft.Text(f"Habitación {numero} agregada con éxito", color="green"))
            except Exception as ex:
                self.page.add(ft.Text(f"Error al agregar la habitación: {str(ex)}", color="red"))
            self.page.update()

        boton_guardar = ft.ElevatedButton("Guardar", on_click=guardar_habitacion)
        boton_volver = ft.ElevatedButton("Volver", on_click=self.gestion_habitaciones)

        self.page.add(
            ft.Column(
                controls=[titulo, piso_input, numero_input, disponible_input, capacidad_input, montoxdia_input, descripcion_input, boton_guardar, boton_volver],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
            )
        )
        self.page.update()

    def listar_habitaciones(self, e=None):
        self.page.controls.clear()

        habitaciones = obtener_todas_las_habitaciones()

        titulo = ft.Text("Lista de Habitaciones", size=28, weight=ft.FontWeight.BOLD, color="blue", italic=True)

        def crear_fila_habitacion(habitacion):
            habitacion_id, piso, numero, disponible, capacidad, montoxdia, descripcion = habitacion

            # Define las opciones del ComboBox de Disponibilidad
            combo_disponibilidad = ft.Dropdown(
                options=[
                    ft.dropdown.Option("Disponible"),
                    ft.dropdown.Option("No disponible")
                ],
                value="Disponible" if disponible == 1 else "No disponible",  # Preselecciona el valor actual de disponibilidad
            )
            
            def eliminar_habitacion_click(e):
                try:
                    eliminar_habitacion(habitacion_id)  # Eliminar habitación
                    self.page.add(ft.Text(f"Habitación {numero} eliminada con éxito", color="green"))
                except Exception as ex:
                    self.page.add(ft.Text(f"Error al eliminar la habitación: {str(ex)}", color="red"))
                self.page.update()

            def modificar_habitacion_click(e):
                self.modificar_habitacion(habitacion_id)

            def ver_descripcion_click(e):
                self.mostrar_descripcion_habitacion(habitacion_id, numero)  # Abre la pantalla con la descripción

            # Función para obtener el valor de disponibilidad (1 o 0)
            def obtener_valor_disponibilidad():
                seleccion = combo_disponibilidad.value
                return 1 if seleccion == "Disponible" else 0

            return ft.Row(
                controls=[
                    ft.Container(ft.Text(f"ID: {habitacion_id}"), padding=8),
                    ft.Container(ft.Text(f"Piso: {piso}"), padding=8),
                    ft.Container(ft.Text(f"Número: {numero}"), padding=8),
                    ft.Container(combo_disponibilidad, padding=8),  # ComboBox de Disponibilidad
                    ft.Container(ft.Text(f"Capacidad: {capacidad}"), padding=8),
                    ft.Container(ft.Text(f"Monto por Día: {montoxdia}"), padding=8),
                    ft.Container(ft.ElevatedButton("Ver Descripción", on_click=ver_descripcion_click), padding=8),
                    ft.Container(ft.ElevatedButton("Eliminar", on_click=eliminar_habitacion_click), padding=8),
                    ft.Container(ft.ElevatedButton("Modificar", on_click=modificar_habitacion_click), padding=8)
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                spacing=10  # Espaciado entre los controles
            )
        
        """def habitacion_disponibilidad(seleccion):
            print('seleccion: '  + str(seleccion))
            if seleccion == 0:
                return "No"
            elif seleccion == 1:
                return "Si"""
            
        lista_habitaciones = [crear_fila_habitacion(habitacion) for habitacion in habitaciones]
        
        # Botón de "Volver" estilizado
        boton_volver = ft.ElevatedButton("Volver", on_click=self.gestion_habitaciones)

        # Usar ListView para permitir desplazamiento vertical
        scrollable_lista = ft.ListView(
            controls=[titulo] + lista_habitaciones + [boton_volver],
            expand=True,  # Esto permite que ocupe todo el espacio disponible
            spacing=15,
        )

        self.page.add(scrollable_lista)
        self.page.update()

    # Nueva función para mostrar la descripción de la habitación
    def mostrar_descripcion_habitacion(self, habitacion_id, numero_habitacion):
        self.page.controls.clear()

        # Obtener la descripción de la habitación
        descripcion = obtener_habitacion_desc(habitacion_id)

        if not descripcion:
            self.page.add(ft.Text(f"No se encontró la descripción para la habitación {numero_habitacion}", color="red"))
        else:
            titulo = ft.Text(f"Descripción de la Habitación {numero_habitacion}", size=24, weight=ft.FontWeight.BOLD)
            descripcion_text = ft.Text(descripcion)

            boton_volver = ft.ElevatedButton("Volver", on_click=self.listar_habitaciones)

            self.page.add(ft.Column([titulo, descripcion_text, boton_volver], spacing=20))

        self.page.update()

    def modificar_habitacion(self, habitacion_id):
        self.page.controls.clear()

        # Obtener la habitación de la base de datos
        conn = sqlite3.connect(RUTA_DB)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT HabitacionPiso, HabitacionNumero, HabitacionDisp, HabitacionCapacidad, HabitacionMontoXDia, HabitacionDesc FROM Habitacion WHERE HabitacionId = ?",
            (habitacion_id,)
        )
        habitacion = cursor.fetchone()
        conn.close()

        if not habitacion:
            self.page.add(ft.Text(f"Habitación con ID {habitacion_id} no encontrada", color="red"))
            self.page.update()
            return

        piso, numero, disponible, capacidad, montoxdia, descripcion = habitacion

        titulo = ft.Text(f"Modificar Habitación ID {habitacion_id}", size=24, weight=ft.FontWeight.BOLD)
        piso_input = ft.TextField(label="Piso", value=str(piso), width=300)
        numero_input = ft.TextField(label="Número de habitación", value=str(numero), width=300)
        disponible_input = ft.Dropdown(
            label="Disponibilidad",
            options=[
                ft.dropdown.Option("Disponible"),
                ft.dropdown.Option("No disponible")
            ],
            width=300
        )
        capacidad_input = ft.TextField(label="Capacidad", value=str(capacidad), width=300)
        montoxdia_input = ft.TextField(label="Monto por día", value=str(montoxdia), width=300)
        descripcion_input = ft.TextField(label="Descripción", value=descripcion, width=300)

        def guardar_cambios(e):
            try:
                nuevo_piso = int(piso_input.value)
                nuevo_numero = int(numero_input.value)
                nuevo_disponible = 1 if disponible_input.value == "Disponible" else 0
                nueva_capacidad = int(capacidad_input.value)
                nuevo_montoxdia = float(montoxdia_input.value)
                nueva_descripcion = descripcion_input.value

                # Llamar a la función de abm_habitacion.py para modificar la habitación
                modificar_habitacion(habitacion_id, nuevo_piso, nuevo_numero, nuevo_disponible, nueva_capacidad, nuevo_montoxdia, nueva_descripcion)

                self.page.add(ft.Text(f"Habitación {nuevo_numero} modificada con éxito", color="green"))
            except Exception as ex:
                self.page.add(ft.Text(f"Error al modificar la habitación: {str(ex)}", color="red"))
            self.page.update()

        boton_guardar = ft.ElevatedButton("Guardar cambios", on_click=guardar_cambios)
        boton_volver = ft.ElevatedButton("Volver", on_click=self.listar_habitaciones)

        self.page.add(
            ft.Column(
                controls=[titulo, piso_input, numero_input, disponible_input, capacidad_input, montoxdia_input, descripcion_input, boton_guardar, boton_volver],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
            )
        )
        self.page.update()

    # Método para gestionar habitaciones
    def gestion_habitaciones(self, e=None):
        self.page.controls.clear()

        gestion_label = ft.Text("Gestión de Habitaciones", size=24, weight=ft.FontWeight.BOLD)
        boton_agregar = ft.ElevatedButton("Agregar habitación", on_click=self.agregar_habitacion)
        boton_listar = ft.ElevatedButton("Listar habitaciones", on_click=self.listar_habitaciones)
        volver_button = ft.ElevatedButton("Volver", on_click=self.crear_menu)

        self.page.add(
            ft.Column(
                controls=[gestion_label, boton_agregar, boton_listar, volver_button],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
            )
        )
        self.page.update()

    # Método para gestionar clientes
    def agregar_usuario(self, e=None):
        self.page.controls.clear()

        titulo = ft.Text("Agregar nuevo usuario", size=24, weight=ft.FontWeight.BOLD)

        nombre_input = ft.TextField(label="Nombre de usuario", width=300)
        password_input = ft.TextField(label="Contraseña", width=300, password=True, can_reveal_password=True)
        rol_input = ft.TextField(label="Rol (ADMIN/USER)", width=300)
        email_input = ft.TextField(label="Email", width=300)

        def guardar_usuario(e):
            nombre = nombre_input.value
            password = password_input.value
            rol = 1 if rol_input.value.upper() == "ADMIN" else 2  # Suponiendo 1 = ADMIN, 2 = USER
            email = email_input.value

            # Llamar a la función de `abm_usuario.py` para crear el usuario
            crear_usuario(nombre, password, email, rol)

            self.page.add(ft.Text(f"Usuario {nombre} agregado con éxito", color="green"))
            self.page.update()

        boton_guardar = ft.ElevatedButton("Guardar", on_click=guardar_usuario)
        boton_volver = ft.ElevatedButton("Volver", on_click=self.gestion_clientes)

        self.page.add(
            ft.Column(
                controls=[titulo, nombre_input, password_input, rol_input, email_input, boton_guardar, boton_volver],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
            )
        )
        self.page.update()

    # Método para listar todos los usuarios
    def listar_usuarios(self, e=None):
        self.page.controls.clear()
        
        usuarios = obtener_todos_usuarios()  # Llamada a la función de `abm_usuario.py`
        
        titulo = ft.Text("Lista de Usuarios", size=24, weight=ft.FontWeight.BOLD)

        def crear_fila_usuario(usuario):
            usuario_id, nombre, email, rol = usuario

            def modificar_usuario_click(e):
                self.modificar_usuario(usuario_id)

            def eliminar_usuario_click(e):
                eliminar_usuario(usuario_id)  # Llamar a la función de `abm_usuario.py` para eliminar
                self.page.add(ft.Text(f"Usuario {usuario_id} eliminado con éxito", color="green"))
                self.page.update()

            rol_text = "ADMIN" if rol == 1 else "USER"
            return ft.Row(
                controls=[
                    ft.Text(f"ID: {usuario_id}"),
                    ft.Text(f"Nombre: {nombre}"),
                    ft.Text(f"Email: {email}"),
                    ft.Text(f"Rol: {rol_text}"),
                    ft.ElevatedButton("Modificar", on_click=modificar_usuario_click),
                    ft.ElevatedButton("Eliminar", on_click=eliminar_usuario_click)
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )

        lista_usuarios = [crear_fila_usuario(usuario) for usuario in usuarios]
        boton_volver = ft.ElevatedButton("Volver", on_click=self.gestion_clientes)

        self.page.add(ft.Column([titulo] + lista_usuarios + [boton_volver]))
        self.page.update()

    # Método para modificar un usuario
    def modificar_usuario(self, usuario_id):
        self.page.controls.clear()

        # Obtener el usuario de la base de datos
        conn = sqlite3.connect(RUTA_DB)
        cursor = conn.cursor()
        cursor.execute("SELECT UsuarioNombre, UsuarioPassword, UsuarioRolId, UsuarioEmail FROM Usuario WHERE UsuarioId = ?", (usuario_id,))
        usuario = cursor.fetchone()
        conn.close()

        if not usuario:
            self.page.add(ft.Text(f"Usuario con ID {usuario_id} no encontrado", color="red"))
            self.page.update()
            return

        nombre, password, rol, email = usuario
        rol_text = "ADMIN" if rol == 1 else "USER"

        titulo = ft.Text(f"Modificar Usuario ID {usuario_id}", size=24, weight=ft.FontWeight.BOLD)
        nombre_input = ft.TextField(label="Nombre de usuario", value=nombre, width=300)
        password_input = ft.TextField(label="Contraseña", value=password, password=True, can_reveal_password=True, width=300)
        rol_input = ft.TextField(label="Rol (ADMIN/USER)", value=rol_text, width=300)
        email_input = ft.TextField(label="Email", value=email, width=300)

        def guardar_cambios(e):
            nuevo_nombre = nombre_input.value
            nueva_password = password_input.value
            nuevo_rol = 1 if rol_input.value.upper() == "ADMIN" else 2
            nuevo_email = email_input.value

            # Llamar a la función de `abm_usuario.py` para modificar el usuario
            modificar_usuario(usuario_id, nuevo_nombre, nueva_password, nuevo_rol, nuevo_email, self.page)

            self.page.add(ft.Text(f"Usuario {nuevo_nombre} modificado con éxito", color="green"))
            self.page.update()

        boton_guardar = ft.ElevatedButton("Guardar cambios", on_click=guardar_cambios)
        boton_volver = ft.ElevatedButton("Volver", on_click=self.listar_usuarios)

        self.page.add(
            ft.Column(
                controls=[titulo, nombre_input, password_input, rol_input, email_input, boton_guardar, boton_volver],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
            )
        )
        self.page.update()

    # Método para gestionar clientes
    def gestion_clientes(self, e=None):
        self.page.controls.clear()

        gestion_label = ft.Text("Gestión de Clientes", size=24, weight=ft.FontWeight.BOLD)
        boton_agregar = ft.ElevatedButton("Agregar usuario", on_click=self.agregar_usuario)
        boton_listar = ft.ElevatedButton("Listar usuarios", on_click=self.listar_usuarios)
        volver_button = ft.ElevatedButton("Volver", on_click=self.crear_menu)

        self.page.add(
            ft.Column(
                controls=[gestion_label, boton_agregar, boton_listar, volver_button],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
            )
        )
        self.page.update()

    def crear_menu(self, e=None):
        self.page.controls.clear()
        
        usuario_nombre = obtener_usuario_nombre(self.usuario_id)

        bienvenida = ft.Text(
            f"Bienvenido, {usuario_nombre}",
            size=24,
            weight=ft.FontWeight.BOLD,
            color=ft.colors.BLUE
        )

        botones = ft.Column(
            controls=[
                ft.ElevatedButton(
                    text="Check-in",
                    icon=ft.icons.LOGIN,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=15),
                        color=ft.colors.WHITE,
                        bgcolor=ft.colors.GREEN_300
                    ),
                    on_click=self.mostrar_checkin
                ),
                ft.ElevatedButton(
                    text="Check-out",
                    icon=ft.icons.LOGOUT,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=15),
                        color=ft.colors.WHITE,
                        bgcolor=ft.colors.ORANGE_300
                    ),
                    on_click=self.mostrar_checkout
                ),
                ft.ElevatedButton(
                    text="Gestión de Habitaciones",
                    icon=ft.icons.ROOM_SERVICE,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=15),
                        color=ft.colors.WHITE,
                        bgcolor=ft.colors.PURPLE_300
                    ),
                    on_click=self.gestion_habitaciones
                ),
                ft.ElevatedButton(
                    text="Gestión de Clientes",
                    icon=ft.icons.GROUP,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=15),
                        color=ft.colors.WHITE,
                        bgcolor=ft.colors.TEAL_300
                    ),
                    on_click=self.gestion_clientes
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )

        menu_card = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    controls=[bienvenida, botones],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20
                ),
                padding=ft.padding.all(30),
                border_radius=15,
                bgcolor=ft.colors.WHITE,
                shadow=ft.BoxShadow(blur_radius=10, color=ft.colors.GREY_400),
            ),
            elevation=10
        )

        self.page.add(menu_card)
        self.page.update()

    def mostrar_checkin(self, e=None):
        self.page.controls.clear()

        numero_habitacion_input = ft.TextField(label="Número de Habitación")
        codigo_input = ft.TextField(label="Código de Reserva")

        def verificar_checkin(e):
            numero_habitacion = numero_habitacion_input.value
            codigo = codigo_input.value

            if self.verificar_codigo_reserva(numero_habitacion, codigo) == 'OK':
                mensaje = activar_tarjeta_si_inactiva(numero_habitacion)
                self.page.controls.clear()
                self.page.add(ft.Text(mensaje, color="green"))
            elif self.verificar_codigo_reserva(numero_habitacion, codigo) == 'CODHAB':
                self.page.add(ft.Text("Código incorrecto o habitación no válida", color="red"))
            elif self.verificar_codigo_reserva(numero_habitacion, codigo) == 'FECHAS':
                self.page.add(ft.Text("Debes realizar el Check-in cuando comience tu hospedaje en el Hotel", color="red"))

            volver_button = ft.ElevatedButton("Volver", on_click=self.crear_menu)    
            self.page.add(volver_button)
            self.page.update()

        checkin_button = ft.ElevatedButton("Realizar Check-in", on_click=verificar_checkin)
        volver_button = ft.ElevatedButton("Volver", on_click=self.crear_menu)

        self.page.add(
            ft.Column(
                controls=[
                    numero_habitacion_input,
                    codigo_input,
                    checkin_button,
                    volver_button
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
        self.page.update()

    def mostrar_checkout(self, e=None):
        self.page.controls.clear()
        numero_habitacion_input = ft.TextField(label="Número de habitación")
        codigo_input = ft.TextField(label="Código de acceso")

        checkout_button = ft.ElevatedButton(
            "Check-out",
            on_click=lambda e: self.realizar_checkout(numero_habitacion_input.value, codigo_input.value)
        )
        volver_button = ft.ElevatedButton("Volver", on_click=self.crear_menu)

        self.page.add(
            ft.Column(
                controls=[numero_habitacion_input, codigo_input, checkout_button, volver_button]
            )
        )
        self.page.update()

    def realizar_checkout(self, numero_habitacion, codigo):
        self.page.controls.clear()
        try:
            if self.verificar_codigo_reserva(numero_habitacion, codigo) == 'OK':
                mensaje = desactivar_tarjeta_si_activa(numero_habitacion)
                self.page.controls.clear()
                self.page.add(ft.Text(mensaje, color="green"))
            elif self.verificar_codigo_reserva(numero_habitacion, codigo) == 'CODHAB':
                self.page.add(ft.Text("Código incorrecto o habitación no válida", color="red"))
            elif self.verificar_codigo_reserva(numero_habitacion, codigo) == 'FECHAS':
                self.page.add(ft.Text("Error con las fehcas al realizar el check-out", color="red"))

        except Exception as e:
            self.page.add(ft.Text(f"Error al realizar el check-out: {e}", color="red"))

        volver_button = ft.ElevatedButton("Volver", on_click=self.crear_menu)
        self.page.add(volver_button)
        self.page.update()

    def verificar_codigo_reserva(self, numero_habitacion, codigo):
        hoy = date.today()
        
        try:
            conn = sqlite3.connect(RUTA_DB)
            cursor = conn.cursor()
            cursor.execute("SELECT ReservaCodigo, ReservaFchDes, ReservaFchHas FROM Reserva WHERE ReservaHabitacionNumero = ?", (numero_habitacion,))
            resultado = cursor.fetchone()
            conn.close()
            
            if resultado:
                reserva_codigo, reserva_fch_desd, reserva_fch_has = resultado
                
                # Convertir las fechas obtenidas a objetos de tipo date
                reserva_fch_desd = date.fromisoformat(reserva_fch_desd)  # La fecha en formato YYYY-MM-DD
                reserva_fch_has = date.fromisoformat(reserva_fch_has)
                
                # Verificar que el código coincida y que la fecha de hoy esté dentro del rango
                if reserva_codigo == int(codigo):
                    if hoy >= reserva_fch_desd and hoy <= reserva_fch_has:
                        return 'OK'
                    else:
                        return 'FECHAS'
                else:
                    return 'CODHAB' 
            
            return 'CODHAB'
            
        except sqlite3.Error as e:
            self.page.add(ft.Text(f"Error al verificar el código: {e}", color="red"))
            self.page.update()
            return 'CODHAB'
