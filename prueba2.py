import yagmail

# Configurar el cliente con tu cuenta Gmail
yag = yagmail.SMTP('juniorrincon1992@gmail.com', 'wxnszzchlpqkogre')  # Usa aquí la contraseña generada

# Enviar correo
try:
    yag.send(
        to='juniorrincon1992@hotmail.com',
        subject='Prueba con Yagmail',
        contents='Este es un mensaje de prueba enviado con yagmail.'
    )
    print("Correo enviado exitosamente.")
except Exception as e:
    print(f"Error al enviar el correo: {e}")
