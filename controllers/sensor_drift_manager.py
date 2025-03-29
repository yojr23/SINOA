import pandas as pd

class SensorDriftManager:
    """
    Gestiona el análisis de desviación del sensor utilizando datos históricos.
    """
    
    def __init__(self, historical_data_path):
        """
        Inicializa el gestor con la ruta a los datos históricos.
        
        Parameters:
        - historical_data_path (str): Ruta al archivo CSV con datos históricos.
        """
        self.historical_data_path = historical_data_path
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
            return True  # El sensor necesita ser reemplazado
        return False

def analizar_datos(data):
    """
    Analiza los niveles de oxígeno y genera alertas si están fuera del rango.
    
    Parameters:
    - data (DataFrame): Datos históricos con niveles de oxígeno.
    """
    limite_inferior = 2.0
    limite_superior = 4.0
    
    for index, row in data.iterrows():
        nivel_oxigeno = row['nivel_oxigeno']
        if nivel_oxigeno < limite_inferior:
            enviar_alerta(f"{row['timestamp']} - El nivel de oxígeno está por debajo del rango permitido.", "CRITICAL")
        elif nivel_oxigeno > limite_superior:
            enviar_alerta(f"{row['timestamp']} - El nivel de oxígeno está por encima del rango permitido.", "CRITICAL")
        else:
            print(f"{row['timestamp']} - Nivel de oxígeno en rango aceptable.")
