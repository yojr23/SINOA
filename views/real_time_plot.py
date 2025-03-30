import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import threading
import time

class RealTimePlot:
    """
    Clase para visualizar los datos en tiempo real.
    """

    def __init__(self, data_ingestion):
        """
        Inicializa la gráfica en tiempo real.

        Parameters:
        - data_ingestion (DataIngestion): Módulo que proporciona los datos en tiempo real.
        """
        self.data_ingestion = data_ingestion
        self.fig, self.ax = plt.subplots()
        self.x_data, self.y_data = [], []
        self.ani = animation.FuncAnimation(self.fig, self.update_plot, interval=1000)

    def update_plot(self, frame):
        """
        Actualiza la gráfica con los nuevos datos.
        """
        new_data = self.data_ingestion.get_latest_data()
        
        if new_data is not None:
            timestamp, nivel_oxigeno = new_data['timestamp'], new_data['nivel_oxigeno']
            self.x_data.append(timestamp)
            self.y_data.append(nivel_oxigeno)

            self.ax.clear()
            self.ax.plot(self.x_data, self.y_data, marker='o', linestyle='-')
            self.ax.set_title("Nivel de Oxígeno en Tiempo Real")
            self.ax.set_xlabel("Tiempo")
            self.ax.set_ylabel("Nivel de Oxígeno")
            self.ax.grid(True)
            plt.xticks(rotation=45)

    def start(self):
        """
        Inicia la visualización en un hilo separado.
        """
        thread = threading.Thread(target=self.run_plot, daemon=True)
        thread.start()

    def run_plot(self):
        """
        Ejecuta el bucle de la gráfica.
        """
        plt.show()

# Ejemplo de uso
if __name__ == "__main__":
    from data_pipeline.data_ingestion import DataSimulator  # Asegúrate de que existe este módulo
    data_ingestion = DataSimulator()
    
    real_time_plot = RealTimePlot(data_ingestion)
    real_time_plot.start()

    # Simula la ejecución del programa sin bloquear el hilo principal
    while True:
        time.sleep(1)
