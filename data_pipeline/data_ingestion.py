import pandas as pd
import time
import os
from queue import Queue
from threading import Thread
from observers.alert_observer import AlertObserver

class DataSimulator:
    """
    Simula la llegada de datos en streaming desde un archivo CSV consolidado.
    Proporciona datos en tiempo real para visualización.
    """
    
    def __init__(self, source_csv="data/registro_historico/consolidated_data.csv", delay=1):
        """
        Inicializa el simulador de datos.
        
        Parameters:
        - source_csv (str): Ruta al archivo CSV consolidado.
        - delay (int): Tiempo en segundos entre envíos de datos simulados.
        """
        self.source_csv = source_csv
        self.delay = delay
        self.data_queue = Queue()
        self.observers = []
        self.running = False
        self.current_data = None
        
    def add_observer(self, observer):
        """Añade un observador para notificar nuevos datos"""
        if isinstance(observer, AlertObserver):
            self.observers.append(observer)
            
    def notify_observers(self, data):
        """Notifica a los observadores con nuevos datos"""
        for observer in self.observers:
            observer.update(data)
    
    def get_latest_data(self, n_points=100):
        """Obtiene los últimos n puntos de datos"""
        if self.current_data is None:
            return []
        return self.current_data[-n_points:]
    
    def start_streaming(self):
        """Inicia el streaming de datos en segundo plano"""
        if self.running:
            return
            
        self.running = True
        Thread(target=self._stream_data, daemon=True).start()
        
    def stop_streaming(self):
        """Detiene el streaming de datos"""
        self.running = False
        
    def _stream_data(self):
        """Hilo principal para streaming de datos simulados"""
        try:
            # Cargar datos una sola vez al inicio
            if not os.path.exists(self.source_csv):
                raise FileNotFoundError(f"Archivo {self.source_csv} no encontrado")
            
            full_data = pd.read_csv(self.source_csv)
            oxygen_levels = full_data['Nivel de Oxígeno'].tolist()
            total_points = len(oxygen_levels)
            current_idx = 0
            
            while self.running:
                try:
                    # Obtener el siguiente punto de datos (cicla cuando llega al final)
                    value = oxygen_levels[current_idx % total_points]
                    
                    # Crear punto de datos
                    data_point = {
                        'timestamp': time.time(),
                        'value': value,
                        'index': current_idx
                    }
                    
                    # Mantener referencia a últimos 100 puntos
                    if self.current_data is None:
                        self.current_data = []
                    self.current_data.append(value)
                    if len(self.current_data) > 100:
                        self.current_data = self.current_data[-100:]
                    
                    # Enviar datos
                    self.data_queue.put(data_point)
                    self.notify_observers(data_point)
                    
                    # Avanzar índice y esperar
                    current_idx += 1
                    time.sleep(self.delay)
                    
                except Exception as e:
                    print(f"Error en streaming: {e}")
                    time.sleep(5)
                    
        except Exception as e:
            print(f"Error inicial en DataSimulator: {e}")
            self.running = False