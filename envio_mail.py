import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time

def enviar_mail(receptor, usuario_nombre, reserva_codigo, habitacion_nro, fecha_desde, fecha_hasta, monto, cantidad_personas):
    # Configuración del servidor SMTP y credenciales
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_user = "facuabbatest@gmail.com"
    smtp_password = "h b y t q k a f c h k f u n h c"

    # Información del correo
    from_email = smtp_user
    to_emails = [receptor
    ]  # Lista de destinatarios
    subject = "¡Reserva exitosa!"
    body = """Estimado/a """ + usuario_nombre + """,
    Nos complace informarle que su reserva en Hotel La Perla se ha realizado exitosamente.
    A continuación, encontrará el código de acceso para su estancia:
    Número de habitación: """ + str(habitacion_nro) + """
    Cantidad de personas: """ + str(cantidad_personas) + """
    Código: """ + str(reserva_codigo) + """
    Fecha de ingreso: """ + str(fecha_desde) + """
    Fecha de finalización: """ + str(fecha_hasta) + """
    Monto: $""" + str(monto) + """
    Por favor, ingrese este código junto con su número de habitación en nuestra pantalla de check-in para acceder a su habitación y servicios exclusivos.
    Agradecemos su preferencia y esperamos que disfrute su estancia con nosotros.
    Atentamente,
    Hotel La Perla"""

    # Crear el mensaje
    message = MIMEMultipart()
    message["From"] = from_email
    message["To"] = ", ".join(to_emails)
    message["Subject"] = subject

    # Adjuntar el cuerpo del correo
    message.attach(MIMEText(body, "plain"))

    start_time = time.time()

    # Enviar el correo
    try:
        # Conectar al servidor SMTP
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Iniciar TLS
        server.login(smtp_user, smtp_password)

        # Enviar el correo
        text = message.as_string()
        server.sendmail(from_email, to_emails, text)

        end_time = time.time()

        print("Correo enviado con éxito.")

        print(f"Tiempo de envío: {end_time - start_time:.2f} segundos")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
    finally:
        server.quit()
