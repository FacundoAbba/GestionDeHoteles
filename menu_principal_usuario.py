import flet as ft
from reservas import obtener_habitaciones_disponibles
from datetime import datetime
from datetime import date
from utils import generar_codigo_reserva, obtener_usuario_nombre, obtener_usuario_email, activar_tarjeta_si_inactiva, desactivar_tarjeta_si_activa, obtener_habitacion_desc
from envio_mail import enviar_mail
import sqlite3

RUTA_DB = "C:\\Users\\Usuario\\Documents\\Itec facu\\Segundo\\Programacion\\TrabajoPractico\\GestionDeHoteles.db"

class MenuPrincipalUsuario:
    def __init__(self, page: ft.Page, usuario_id: int):
        self.page = page
        self.usuario_id = usuario_id
        self.page.title = "Menú Principal"
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.padding = ft.padding.all(20)
        self.page.theme_mode = ft.ThemeMode.LIGHT  # Tema claro

    def crear_menu(self, e=None):
        self.page.controls.clear()
        
        usuario_nombre = obtener_usuario_nombre(self.usuario_id)
        bienvenida = ft.Text(f"Bienvenido, {usuario_nombre}", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE)

        botones = ft.Column(
            controls=[
                ft.ElevatedButton(
                    text="Reservar Habitación",
                    icon=ft.icons.BED,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=15),
                        color=ft.colors.WHITE,
                        bgcolor=ft.colors.BLUE_300
                    ),
                    on_click=self.mostrar_busqueda_habitaciones
                ),
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

        def realizar_checkout(e):
            numero_habitacion = numero_habitacion_input.value
            codigo = codigo_input.value

            self.page.controls.clear()
            if self.verificar_codigo_reserva(numero_habitacion, codigo):
                mensaje = desactivar_tarjeta_si_activa(numero_habitacion)
                self.page.add(ft.Text(mensaje, color="green"))
            else:
                self.page.add(ft.Text("Código incorrecto o habitación no ocupada", color="red"))

            volver_button = ft.ElevatedButton("Volver", on_click=self.crear_menu)
            self.page.add(volver_button)
            self.page.update()

        checkout_button = ft.ElevatedButton("Realizar Check-out", on_click=realizar_checkout)
        volver_button = ft.ElevatedButton("Volver", on_click=self.crear_menu)

        self.page.add(
            ft.Column(
                controls=[
                    numero_habitacion_input,
                    codigo_input,
                    checkout_button,
                    volver_button
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
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

    def verificar_habitacion_ocupada(self, numero_habitacion):
        pass  # Implementa la lógica de verificación de la habitación

    def desactivar_tarjeta_de_acceso(self, numero_habitacion):
        pass  # Implementa la lógica para desactivar la tarjeta de acceso

    def actualizar_estado_habitacion(self, numero_habitacion, estado):
        pass  # Implementa la lógica para actualizar el estado de la habitación en la base de datos
    
#------------------------------------------------------------------------------

    def mostrar_busqueda_habitaciones(self, e=None):
        self.page.controls.clear()
        fecha_desde_input = ft.TextField(label="Fecha desde (YYYY-MM-DD)")
        fecha_hasta_input = ft.TextField(label="Fecha hasta (YYYY-MM-DD)")
        cantidad_personas_input = ft.TextField(label="Cantidad de personas", keyboard_type=ft.KeyboardType.NUMBER)
        buscar_button = ft.ElevatedButton(text="Buscar", on_click=lambda e: self.buscar_habitaciones(fecha_desde_input, fecha_hasta_input, cantidad_personas_input))

        self.page.add(
            ft.Column(
                controls=[fecha_desde_input, fecha_hasta_input, cantidad_personas_input, buscar_button],
                spacing=10,
                alignment=ft.MainAxisAlignment.CENTER
            )
        )
        self.page.update()

    def buscar_habitaciones(self, fecha_desde_input, fecha_hasta_input, cantidad_personas_input):
        fecha_desde = fecha_desde_input.value
        fecha_hasta = fecha_hasta_input.value
        
        try:
            cantidad_personas = int(cantidad_personas_input.value)
        except ValueError:
            self.page.add(ft.Text("La cantidad de personas debe ser un número.", color="red"))
            self.page.update()
            return

        self.mostrar_habitaciones_disponibles(fecha_desde, fecha_hasta, cantidad_personas)

    def mostrar_habitaciones_disponibles(self, fecha_desde, fecha_hasta, cantidad_personas):
        self.page.controls.clear()
        habitaciones_disponibles, error = obtener_habitaciones_disponibles(fecha_desde, fecha_hasta, cantidad_personas)

        contenedor_habitaciones = ft.Column(spacing=10, alignment=ft.MainAxisAlignment.CENTER)

        if error:
            contenedor_habitaciones.controls.append(ft.Text(error, color="red"))
        elif habitaciones_disponibles:
            contenedor_habitaciones.controls.append(ft.Text("Habitaciones disponibles", size=20, weight=ft.FontWeight.BOLD))
            
            for habitacion in habitaciones_disponibles:
                habitacion_id = habitacion[0]
                habitacion_piso = habitacion[1]
                habitacion_num = habitacion[2]
                habitacion_desc = habitacion[3]
                monto_por_dia = habitacion[4]
                fecha_desde_dt = datetime.strptime(fecha_desde, '%Y-%m-%d')
                fecha_hasta_dt = datetime.strptime(fecha_hasta, '%Y-%m-%d')
                diferencia = fecha_hasta_dt - fecha_desde_dt
                dias_reserva = diferencia.days
                monto = monto_por_dia * dias_reserva
                codigo = generar_codigo_reserva()
                
                contenedor_habitaciones.controls.append(
                    ft.Column(
                        controls=[
                            ft.Text(f"Habitación {habitacion_num}", size=16),
                            ft.Row(
                                controls=[
                                    ft.ElevatedButton("Ver detalles", on_click=lambda e, id=habitacion_id: self.mostrar_descripcion_habitacion(id, fecha_desde, fecha_hasta, cantidad_personas)),
                                    ft.ElevatedButton("Reservar", on_click=lambda e, num=habitacion_num: self.hacer_reserva(num, fecha_desde, fecha_hasta, monto, codigo, cantidad_personas))
                                ],
                                alignment=ft.MainAxisAlignment.CENTER
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=5
                    )
                )
        else:
            contenedor_habitaciones.controls.append(ft.Text("No hay habitaciones disponibles", size=16))

        # Agregar botón "Volver" para regresar a la pantalla anterior
        contenedor_habitaciones.controls.append(
            ft.ElevatedButton("Volver", on_click=self.crear_menu)
        )

        self.page.add(contenedor_habitaciones)
        self.page.update()

    # Nueva función para mostrar la descripción de una habitación
    def mostrar_descripcion_habitacion(self, habitacion_id, fecha_desde, fecha_hasta, cantidad_personas):
        self.page.controls.clear()

        # Aquí obtienes la descripción de la habitación por su ID
        descripcion = obtener_habitacion_desc(habitacion_id)
        
        # Pantalla que muestra la descripción de la habitación
        self.page.add(
            ft.Column(
                controls=[
                    ft.Text(f"Detalles de la Habitación", size=24, weight=ft.FontWeight.BOLD),
                    ft.Text(f"Descripción: {descripcion}", size=16),
                    ft.ElevatedButton("Volver", on_click=lambda e: self.mostrar_habitaciones_disponibles(fecha_desde, fecha_hasta, cantidad_personas))  # Función pasada correctamente
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10
            )
        )

        self.page.update()

    def hacer_reserva(self, habitacion_id, fecha_desde, fecha_hasta, monto, codigo, cantidad_personas):
        try:
            conn = sqlite3.connect(RUTA_DB)
            cursor = conn.cursor()
            query = '''
            INSERT INTO Reserva (ReservaHabitacionNumero, ReservaFchDes, ReservaFchHas, ReservaMonto, ReservaCodigo)
            VALUES (?, ?, ?, ?, ?)
            '''
            cursor.execute(query, (habitacion_id, fecha_desde, fecha_hasta, monto, codigo))
            usuario_email = obtener_usuario_email(self.usuario_id)
            usuario_nombre = obtener_usuario_nombre(self.usuario_id)
            enviar_mail(usuario_email, usuario_nombre, codigo, habitacion_id, fecha_desde, fecha_hasta, monto, cantidad_personas) 
            conn.commit()
            conn.close()
            self.page.add(ft.Text(f"Reserva exitosa para la habitación {habitacion_id}", color="green"))
        except sqlite3.Error as e:
            self.page.add(ft.Text(f"Error al realizar la reserva: {e}", color="red"))
        self.page.update()
    
    def ver_detalles_habitacion(self, e, habitacion_id):
        try:
            # Conectar a la base de datos
            conn = sqlite3.connect(RUTA_DB)
            cursor = conn.cursor()
            
            # Consulta SQL para obtener la descripción de la habitación por ID
            cursor.execute("SELECT HabitacionDesc FROM Habitacion WHERE HabitacionId = ?", (habitacion_id,))
            resultado = cursor.fetchone()
            
            # Cerrar la conexión
            conn.close()
            
            # Verificar si se encontró la habitación
            if resultado:
                return resultado[0]  # Retorna la descripción de la habitación
            else:
                return "Habitación no encontrada."
        
        except sqlite3.Error as e:
            return f"Error al buscar la habitación: {e}"
        print(f"Mostrando detalles de la habitación: {habitacion_num}") #obtener numero
