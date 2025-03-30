import pandas as pd
import time
import os

class DataSimulator:
    """
    Simula la llegada de datos en streaming desde un archivo CSV consolidado.
    """
    
    def __init__(self,):
        """
        Inicializa el simulador de datos.
        
        Parameters:
        - source_csv (str): Ruta al archivo CSV consolidado.
        - output_csv (str): Ruta donde se guardarán los datos simulados.
        - delay (int): Tiempo en segundos entre envíos de datos simulados.
        """
        self.source_csv = "data/consolidado.csv"
        self.output_csv = "data/registro_historico/datos.csv"
        self.delay = 1
    
    def simulate_data_stream(self):
        """Lee el archivo consolidado y simula la llegada de datos continuamente."""
        if not os.path.exists(self.source_csv):
            raise FileNotFoundError(f"El archivo {self.source_csv} no existe.")
        
        while True:
            data = pd.read_csv(self.source_csv)
            for _, row in data.iterrows():
                self.save_data(row)
                time.sleep(self.delay)
            
            print("Ciclo de simulación completado. Reiniciando...")
            time.sleep(5)  # Espera antes de volver a procesar el archivo
    
    def save_data(self, row):
        """Guarda los datos en el archivo de salida, creando el archivo si no existe."""
        new_data = pd.DataFrame([row])
        
        if not os.path.exists(self.output_csv):
            new_data.to_csv(self.output_csv, index=False)
        else:
            new_data.to_csv(self.output_csv, mode='a', header=False, index=False)

# Ejemplo de uso
if __name__ == "__main__":
    simulator = DataSimulator()
    simulator.simulate_data_stream()
