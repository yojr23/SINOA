import pandas as pd
from observers.alert_observer import AlertObserver

class SensorDriftManager:
    """
    Gestiona el análisis de desviación del sensor utilizando datos históricos.
    """
    
    def __init__(self, historical_data_path, alert_observer: AlertObserver):
        """
        Inicializa el gestor con la ruta a los datos históricos y un observador de alertas.
        
        Parameters:
        - historical_data_path (str): Ruta al archivo CSV con datos históricos.
        - alert_observer (AlertObserver): Instancia para manejar alertas.
        """
        self.historical_data_path = historical_data_path
        self.alert_observer = alert_observer
        self.data = None
    
    def load_historical_data(self):
        """Carga los datos históricos desde el archivo CSV."""
        try:
            self.data = pd.read_csv(self.historical_data_path)
        except FileNotFoundError:
            raise FileNotFoundError(f"El archivo {self.historical_data_path} no existe.")
        except Exception as e:
            raise Exception(f"Error al cargar los datos históricos: {str(e)}")
    
    def calculate_statistics(self):
        """
        Calcula estadísticas básicas de los datos históricos.
        
        Returns:
        - dict: Contiene la media y desviación estándar de los datos.
        """
        if self.data is None:
            raise ValueError("Los datos históricos no han sido cargados.")
        
        mean_value = self.data['Nivel de Oxígeno'].mean()
        std_dev = self.data['Nivel de Oxígeno'].std()
        
        return {
            "mean": mean_value,
            "std_dev": std_dev
        }
    
    def check_sensor_drift(self, threshold=0.5):
        """
        Verifica si la desviación estándar supera un umbral, indicando que el sensor puede necesitar reemplazo.
        
        Parameters:
        - threshold (float): Umbral de desviación estándar aceptable.
        
        Returns:
        - bool: True si se detecta un problema con el sensor, False en caso contrario.
        """
        stats = self.calculate_statistics()
        if stats["std_dev"] > threshold:
            mensaje = f"ALERTA: Se detectó una desviación inusual en el sensor. Desviación estándar: {stats['std_dev']:.2f}"
            self.alert_observer.notify(mensaje, "WARNING")
            return True  # El sensor necesita ser reemplazado
        return False
