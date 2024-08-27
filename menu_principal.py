import flet as ft
from login import Login
from utils import get_rol
from reservas import obtener_habitaciones_disponibles
import sqlite3
from datetime import datetime

RUTA_DB = "C:\\Users\\Usuario\\Documents\\Itec facu\\Segundo\\Programacion\\TrabajoPractico\\GestionDeHoteles.db"

class MenuPrincipal:
    def __init__(self, page: ft.Page, usuario_id: int):
        self.page = page
        self.usuario_id = usuario_id
        self.page.title = "Menú Principal"
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def crear_menu(self):
        def on_reservar_habitacion_click(e):
            self.mostrar_busqueda_habitaciones()

        def on_checkin_click(e):
            # Lógica para check-in
            pass

        def on_checkout_click(e):
            # Lógica para check-out
            pass

        def on_gestion_habitaciones_click(e):
            self.gestion_habitaciones()

        def on_gestion_clientes_click(e):
            self.gestion_clientes()

        # Crear los botones del menú
        btn_reservar_habitacion = ft.ElevatedButton("Reservar Habitación", on_click=on_reservar_habitacion_click)
        btn_checkin = ft.ElevatedButton("Check-in", on_click=on_checkin_click)
        btn_checkout = ft.ElevatedButton("Check-out", on_click=on_checkout_click)
        btn_gestion_habitaciones = ft.ElevatedButton("Gestión de Habitaciones", on_click=on_gestion_habitaciones_click)
        btn_gestion_clientes = ft.ElevatedButton("Gestión de Clientes", on_click=on_gestion_clientes_click)

        # Añadir botones a la página
        self.page.add(
            btn_reservar_habitacion,
            btn_checkin,
            btn_checkout,
            btn_gestion_habitaciones,
            btn_gestion_clientes
        )

        self.page.update()

    def mostrar_busqueda_habitaciones(self):
        def buscar_habitaciones_click(e):
            fecha_desde = fecha_desde_input.value
            fecha_hasta = fecha_hasta_input.value
            cantidad_personas = int(cantidad_personas_input.value)
            self.mostrar_habitaciones_disponibles(fecha_desde, fecha_hasta, cantidad_personas)

        fecha_desde_input = ft.TextField(label="Fecha desde (YYYY-MM-DD)")
        fecha_hasta_input = ft.TextField(label="Fecha hasta (YYYY-MM-DD)")
        cantidad_personas_input = ft.TextField(label="Cantidad de personas", keyboard_type=ft.KeyboardType.NUMBER)
        buscar_button = ft.ElevatedButton(text="Buscar", on_click=buscar_habitaciones_click)

        contenedor_busqueda = ft.Column(
            controls=[
                fecha_desde_input,
                fecha_hasta_input,
                cantidad_personas_input,
                buscar_button
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER
        )

        self.page.controls.append(contenedor_busqueda)
        self.page.update()

    def mostrar_habitaciones_disponibles(self, fecha_desde, fecha_hasta, cantidad_personas):
        def ver_detalles_habitacion(habitacion_num):
            try:
                conn = sqlite3.connect(RUTA_DB)
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM Habitacion WHERE HabitacionNumero = ?", (habitacion_num,))
                detalles = cursor.fetchone()
                conn.close()
                return detalles
            except sqlite3.Error as e:
                self.page.add(ft.Text(f"Error al ver detalles de la habitación: {e}", color="red"))
                self.page.update()
                return None

        def hacer_reserva(habitacion_num):
            try:
                conn = sqlite3.connect(RUTA_DB)
                cursor = conn.cursor()
                cursor.execute("UPDATE Habitacion SET HabitacionDisp = 0 WHERE HabitacionNumero = ?", (habitacion_num,))
                conn.commit()
                conn.close()
                self.page.add(ft.Snackbar(text=f"Habitación {habitacion_num} reservada exitosamente."))
                self.page.update()
            except sqlite3.Error as e:
                self.page.add(ft.Text(f"Error al hacer reserva: {e}", color="red"))
                self.page.update()

        habitaciones_disponibles, error = obtener_habitaciones_disponibles(fecha_desde, fecha_hasta, cantidad_personas)
        
        contenedor_habitaciones = ft.Column(spacing=10, alignment=ft.MainAxisAlignment.CENTER)
        
        if error:
            contenedor_habitaciones.controls.append(ft.Text(error, color="red"))
        elif habitaciones_disponibles:
            contenedor_habitaciones.controls.append(ft.Text("Habitaciones disponibles", size=20, weight=ft.FontWeight.BOLD))
            for habitacion in habitaciones_disponibles:
                habitacion_num = habitacion[2]
                contenedor_habitaciones.controls.append(
                    ft.Column(
                        controls=[
                            ft.Text(f"Habitación {habitacion_num}", size=16),
                            ft.Row(
                                controls=[
                                    ft.ElevatedButton("Ver detalles", on_click=lambda e, num=habitacion_num: ver_detalles_habitacion(num)),
                                    ft.ElevatedButton("Reservar", on_click=lambda e, num=habitacion_num: hacer_reserva(num))
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
        
        self.page.controls.append(contenedor_habitaciones)
        self.page.update()

    def gestion_habitaciones(self):
        rol_id = get_rol(self.usuario_id)
        if rol_id == 1:  # Suponiendo que el rol 1 es el ADMIN
            self.mostrar_busqueda_habitaciones()
        else:
            self.page.add(ft.Text("No tienes permisos para acceder a esta sección", color="red"))
            self.page.update()

    def gestion_clientes(self):
        rol_id = get_rol(self.usuario_id)
        if rol_id == 1:  # Suponiendo que el rol 1 es el ADMIN
            # Implementar lógica para abrir la ventana de gestión de clientes
            print("Abrir ventana de gestión de clientes")
        else:
            self.page.add(ft.Text("No tienes permisos para acceder a esta sección", color="red"))
            self.page.update()

def menu_principal_page(page: ft.Page, usuario_id: int):
    menu = MenuPrincipal(page, usuario_id)
    menu.crear_menu()

def main(page: ft.Page):
    page.on_route_change = lambda e: menu_principal_page(page, usuario_id=1) if e.route == "/menu_principal" else None
    # Inicializar la página de login
    login_page = Login(page)
    login_page.mostrar_login(entry_usuario=None, entry_contrasena=None)  # Ajustar según los argumentos necesarios

ft.app(target=main)
