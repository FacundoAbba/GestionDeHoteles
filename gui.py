import tkinter as tk
from tkinter import ttk
from login import Login
from register import crear_cuenta
from password import actualizar_contrasena
from reservas import mostrar_habitaciones

# Constantes para los títulos y geometrías de las ventanas
TITULO_VENTANA_INICIO = "Bienvenido"
TITULO_VENTANA_MENU = "Menú Principal"
GEOMETRIA_VENTANA = "400x200"

def pantalla_inicial(ventana):
    # Crear contenedor para la pantalla inicial
    contenedor = tk.Frame(ventana)
    contenedor.pack(fill="both", expand=True)

    ttk.Label(contenedor, text="¿Tienes un usuario creado?").pack(pady=20)
    
    login = Login(ventana)
    btn_si = ttk.Button(contenedor, text="Sí", command=login.mostrar_login)
    btn_si.pack(side=tk.LEFT, padx=20, pady=10)

    btn_no = ttk.Button(contenedor, text="No", command=crear_cuenta)
    btn_no.pack(side=tk.RIGHT, padx=20, pady=10)

def mostrar_menu_principal(ventana):
    # Crear contenedor para el menú principal
    contenedor = tk.Frame(ventana)
    contenedor.pack(fill="both", expand=True)

    ttk.Label(contenedor, text="Bienvenido al Menú Principal").pack(pady=20)
    
    btn_cambiar_contrasena_menu = ttk.Button(contenedor, text="Cambiar Contraseña", command=actualizar_contrasena)
    btn_cambiar_contrasena_menu.pack(pady=10)

    btn_reservar_habitacion = ttk.Button(contenedor, text="Reservar Habitación", command=lambda: mostrar_habitaciones(ventana))
    btn_reservar_habitacion.pack(pady=10)