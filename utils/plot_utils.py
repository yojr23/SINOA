import streamlit as st
import pandas as pd
import time
import numpy as np
import altair as alt
from data_pipeline.data_ingestion import DataSimulator

class RealTimePlotter:
    """
    Utilidad para visualización de datos en tiempo real con líneas de referencia y fondo coloreado.
    """
    
    def __init__(self, data_simulator=None):
        self.data_simulator = data_simulator or DataSimulator()
        self.data_window = 100  # Número de puntos a mostrar
        self.chart = st.empty()  # Espacio reservado para el gráfico
        self.base_chart = None
        self.setup_static_plot()
        
    def setup_static_plot(self):
        """Configura la estructura inicial del gráfico con elementos estáticos"""
        
        # Agregar líneas de referencia
        self.lineas = alt.Chart(pd.DataFrame({'Nivel Oxígeno': [4, 7]})).mark_rule(
            color='gray', strokeDash=[5, 5]
        ).encode(y='Nivel Oxígeno:Q')
        
        # Agregar áreas de color de fondo
        self.areas = alt.Chart(pd.DataFrame({
            'y': [3, 4, 7],
            'y2': [4, 7, 8],
            'color': ['red', 'green', 'yellow']
        })).mark_rect(opacity=0.2).encode(
            y='y:Q',
            y2='y2:Q',
            color=alt.Color('color:N', scale=alt.Scale(domain=['red', 'green', 'yellow'], range=['red', 'green', 'yellow']), legend=None)
        )
        
        # Crear el gráfico base estático
        self.base_chart = alt.layer(self.areas, self.lineas)
        
        # Iniciar el simulador de datos
        self.data_simulator.start_streaming()
        
    def create_realtime_plot(self):
        """Devuelve el gráfico actualizado en tiempo real"""
        data = self.data_simulator.get_latest_data(self.data_window)
        if data:
            df = pd.DataFrame({
                'Tiempo': range(len(data)),
                'Nivel Oxígeno': data
            })

            # Crear gráfico de línea dinámico
            dynamic_line = alt.Chart(df).mark_line(color='blue').encode(
                x=alt.X('Tiempo:Q', title=None, axis=alt.Axis(labels=False, ticks=False)),  # Ocultar valores del eje X
                y=alt.Y('Nivel Oxígeno:Q', title='Nivel de Oxígeno (mg/L)', scale=alt.Scale(domain=[3, 8], nice=False))
            )

            # Combinar el gráfico base estático con la línea dinámica
            updated_chart = alt.layer(self.base_chart, dynamic_line)
            return updated_chart
        return None

def test_plot():
    """Función de prueba para visualización"""
    plotter = RealTimePlotter()
    while True:
        updated_chart = plotter.create_realtime_plot()
        if updated_chart:
            plotter.chart.altair_chart(updated_chart, use_container_width=True)
        time.sleep(1)