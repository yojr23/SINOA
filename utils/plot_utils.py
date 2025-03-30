import streamlit as st
import pandas as pd
import time
import numpy as np
from data_pipeline.data_ingestion import DataSimulator

class RealTimePlotter:
    """
    Utilidad para visualización de datos en tiempo real.
    """
    
    def __init__(self, data_simulator=None):
        self.data_simulator = data_simulator or DataSimulator()
        self.chart = st.empty()
        self.data_window = 100  # Número de puntos a mostrar
        
    def setup_plot(self, title="Datos en Tiempo Real"):
        """Configura el gráfico inicial"""
        st.subheader(title)
        self.data_simulator.start_streaming()
        
    def update_plot(self):
        """Actualiza el gráfico con nuevos datos"""
        while True:
            data = self.data_simulator.get_latest_data(self.data_window)
            if data:
                df = pd.DataFrame({
                    'index': range(len(data)),
                    'Nivel Oxígeno': data,
                    'Límite Inferior (4 mg/L)': [4]*len(data),
                    'Límite Superior (7 mg/L)': [7]*len(data)
                })
                
                # Create simple line chart showing oxygen level trend
                if not hasattr(self, 'chart'):
                    self.chart = st.line_chart(
                        df[['Nivel Oxígeno']].set_index(df['index']),
                        height=400,
                        use_container_width=True
                    )
                else:
                    # Update existing chart with new data
                    self.chart.add_rows(df[['Nivel Oxígeno']].set_index(df['index']))
            time.sleep(0.5)
            
    def create_realtime_plot(self, title="Nivel de Oxígeno"):
        """Crea y mantiene actualizado un gráfico en tiempo real"""
        self.setup_plot(title)
        self.update_plot()

def test_plot():
    """Función de prueba para visualización"""
    plotter = RealTimePlotter()
    plotter.create_realtime_plot()