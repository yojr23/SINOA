# Funciones auxiliares para manejo de correos
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr

import smtplib

def create_email_message(sender_email, recipient_email, subject, body):
    """
    Crea un mensaje de correo electrónico con codificación UTF-8.

    Parameters:
    - sender_email (str): Correo del remitente.
    - recipient_email (str): Correo del destinatario.
    - subject (str): Asunto del correo.
    - body (str): Cuerpo del mensaje.

    Returns:
    - MIMEMultipart: Mensaje de correo listo para enviar.
    """
    msg = MIMEMultipart()
    
    # Forzar codificación UTF-8 en las cabeceras
    msg['From'] = formataddr((str(Header('Sistema de Alertas', 'utf-8')), sender_email))
    msg['To'] = recipient_email
    msg['Subject'] = Header(subject, 'utf-8')
    
    # Codificar el cuerpo en UTF-8
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    return msg



def send_email(smtp_server, port, sender_email, sender_password, msg):
    """
    Envía un correo electrónico usando el servidor SMTP configurado.

    Parameters:
    - smtp_server (str): Dirección del servidor SMTP.
    - port (int): Puerto del servidor SMTP.
    - sender_email (str): Correo del remitente.
    - sender_password (str): Contraseña del remitente.
    - msg (MIMEMultipart): Mensaje de correo listo para enviar.
    """
    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.set_debuglevel(1)  # Activar depuración para ver interacciones SMTP
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(sender_email, sender_password)
            
            # Usar send_message para garantizar la codificación adecuada
            server.send_message(msg)
            
        print(f"Correo enviado a {msg['To']} con asunto: {msg['Subject']}")
    except Exception as e:
        print(f"Error al enviar el correo: {str(e)}")