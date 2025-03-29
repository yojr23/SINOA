import smtplib

try:
    server = smtplib.SMTP('smtp.zoho.com', 587)
    server.starttls()
    server.login('juniorrincon1992@zoho.com', 'Joselala12')
    print("Conexión exitosa.")
    server.quit()
except smtplib.SMTPException as e:
    print(f"Error de conexión: {e}")
