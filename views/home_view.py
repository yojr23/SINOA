from utils.plot_utils import RealTimePlotter
import streamlit as st
import pandas as pd
import time

def home_view():
    """Vista principal con monitoreo en tiempo real"""
    
    # Configuración inicial
    st.title("📊 Monitor de Niveles de Oxígeno")
    
    # Inicializar plotter mejorado
    plotter = RealTimePlotter()  # Initialize the plotter once

    
    # Layout principal
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Gráfico en tiempo real
        st.subheader("Tendencia de Niveles (Últimos 100 puntos)")
        chart = st.empty()
        
        # Histórico
        st.subheader("Datos Históricos")
        data_expander = st.expander("Ver datos completos")
        with data_expander:
            data_placeholder = st.empty()
    
    with col2:
        # Métricas
        st.subheader("📈 Métricas en Tiempo Real")
        metric = st.metric("Último Valor", "Cargando...")
        
        # Alertas
        st.subheader("⚠️ Alertas")
        alert_placeholder = st.empty()
    
  

if __name__ == "__main__":
    home_view()