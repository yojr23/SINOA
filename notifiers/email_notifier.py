from utils.email_utils import create_email_message, send_email
from datetime import datetime
from observers.alert_observer import AlertObserver

class EmailNotifier(AlertObserver):
    """
    Observador que envía correos electrónicos para alertas críticas y de advertencia.
    """
    def __init__(self, smtp_server, port, sender_email, sender_password, recipient_email):
        """
        Inicializa el notificador de correos con la configuración del servidor SMTP.
        """
        self.smtp_server = smtp_server
        self.port = port
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.recipient_email = recipient_email

    def notify(self, message, alert_type):
        """
        Envía un correo si el tipo de alerta es CRITICAL.
        """
        if alert_type in ["CRITICAL"]:
            subject = f"Alerta {alert_type} - Sistema de Oxígeno"
            body = f"{datetime.now()} - {message}"
            try:
                # Crear el mensaje de correo
                msg = create_email_message(
                    sender_email=self.sender_email,
                    recipient_email=self.recipient_email,
                    subject=subject,
                    body=body
                )
                # Enviar el correo
                send_email(
                    smtp_server=self.smtp_server,
                    port=self.port,
                    sender_email=self.sender_email,
                    sender_password=self.sender_password,
                    msg=msg
                )
                print(f"Correo enviado exitosamente a {self.recipient_email}.")
            except Exception as e:
                print(f"Error al enviar el correo: {e}")