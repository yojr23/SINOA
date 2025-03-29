import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuración del servidor SMTP
smtp_server = 'smtp.gmail.com'
smtp_port = 587
email_user = 'juniorrincon1992@gmail.com'
email_password = 'wxnszzchlpqkogre' 

# Configuración del correo
destinatario = 'juniorrincon1992@hotmail.com'
asunto = 'Prueba de envío de correo'
mensaje = 'Este es un mensaje de prueba enviado desde Python.'

# Crear el mensaje
msg = MIMEMultipart()
msg['From'] = email_user
msg['To'] = destinatario
msg['Subject'] = asunto
msg.attach(MIMEText(mensaje, 'plain'))

try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.set_debuglevel(1)  # Habilitar depuración para ver detalles
    server.starttls()
    server.login(email_user, email_password)
    server.send_message(msg)
    print("Correo enviado exitosamente.")
except smtplib.SMTPException as e:
    print(f"Error al enviar el correo: {e}")
finally:
    try:
        server.quit()
    except smtplib.SMTPServerDisconnected:
        print("La conexión SMTP ya estaba cerrada.")
