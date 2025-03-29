class AlertObserver:
    """
    Clase base para observadores de alertas.
    """
    def notify(self, message, alert_type):
        raise NotImplementedError("Este método debe ser implementado por subclases.")