from datetime import datetime
from notifiers.email_notifier import EmailNotifier

class AlertSystemGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Alertas de Oxígeno")
        
        # Configuración del notificador de correos
        self.email_notifier = EmailNotifier(
            smtp_server='smtp.gmail.com',
            port=587,
            sender_email='',
            sender_password='',
            recipient_email=''
        )
        
        # Configuración de la interfaz (igual que antes)...
        
    def show_alert(self, message, alert_type="INFO"):
        """Muestra un mensaje de alerta en la GUI."""
        self.alerts_text.config(state="normal")
        self.alerts_text.insert("end", f"[{alert_type}] {message}\n")
        self.alerts_text.config(state="disabled")
        
        # Enviar correo para alertas WARNING o CRITICAL
        if alert_type in ["WARNING", "CRITICAL"]:
            subject = f"Alerta {alert_type} - Sistema de Oxígeno"
            body = f"{datetime.now()} - {message}"
            self.email_notifier.send_email(subject, body)

#pruebas
"""
# Ejemplo de uso:
alert_view = AlertView()
alert_view.show_range_alert(1.8, 2.0, 4.0)  # Por debajo
alert_view.show_range_alert(4.5, 2.0, 4.0)  # Por encima
alert_view.show_range_alert(3.0, 2.0, 4.0)  # Dentro del rango
"""