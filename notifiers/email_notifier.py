from utils.email_utils import create_email_message, send_email
from datetime import datetime
from observers.alert_observer import AlertObserver

class EmailNotifier(AlertObserver):
    """
    Observador que envía correos electrónicos para alertas críticas y de advertencia.
    """
    def __init__(self, smtp_server, port, sender_email, sender_password, recipient_email):
        self.smtp_server = smtp_server
        self.port = port
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.recipient_email = recipient_email

    def notify(self, message, alert_type):
        """
        Envía un correo si el tipo de alerta es WARNING o CRITICAL.
        """
        if alert_type in ["CRITICAL"]:
            subject = f"Alerta {alert_type} - Sistema de Oxígeno"
            body = f"{datetime.now()} - {message}"
            msg = create_email_message(self.sender_email, self.recipient_email, subject, body)
            send_email(self.smtp_server, self.port, self.sender_email, self.sender_password, msg)
