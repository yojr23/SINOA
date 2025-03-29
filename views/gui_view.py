import streamlit as st
import time
from controllers.sensor_drift_manager import SensorDriftManager
from utils.data_loader import consolidate_data
from notifiers.email_notifier import EmailNotifier
import os

# Ruta del archivo consolidado
HISTORICAL_DATA_PATH = 'sistema_alertas/data/registro_historico/consolidated_data.csv'

# Rutas de las carpetas de entrada y revisados
INPUT_FOLDER = os.path.abspath('sistema_alertas/data/pruebas_anteriores/')
REVIEWED_FOLDER = os.path.abspath('sistema_alertas/data/pruebas_anteriores_revisados/')

# Asegurar que las carpetas existen
os.makedirs(INPUT_FOLDER, exist_ok=True)
os.makedirs(REVIEWED_FOLDER, exist_ok=True)

drift_manager = SensorDriftManager(HISTORICAL_DATA_PATH)

# Lista de observadores
observers = []

def add_observer(observer):
    """Añade un observador a la lista."""
    observers.append(observer)

def notify_observers(message, alert_type):
    """Notifica a los observadores sobre una alerta."""
    for observer in observers:
        observer.notify(message, alert_type)

def show_alert(message, alert_type="INFO"):
    """Muestra una alerta en la interfaz y notifica a los observadores."""
    st.error(message) if alert_type == "CRITICAL" else st.warning(message)
    notify_observers(message, alert_type)

def load_and_analyze_data():
    """Función de análisis de datos (aún no implementada)."""
    show_alert("Función aún no implementada.", "INFO")

def run_gui(email_notifier):
    add_observer(email_notifier)  # Registrar el notificador de correo
    
    st.markdown("""
        <style>
        .main-title {
            text-align: center;
            font-size: 40px;
            font-weight: bold;
            color: #4CAF50;
        }
        .alert-text {
            font-size: 18px;
            color: red;
        }
        </style>
        """, unsafe_allow_html=True)
    
    # Animación de bienvenida
    placeholder = st.empty()
    for i in range(3):
        placeholder.markdown(f"<h1 class='main-title'>Bienvenido a SINOA{'.' * (i+1)}</h1>", unsafe_allow_html=True)
        time.sleep(0.5)
    placeholder.empty()
    
    st.title("Sistema de Alertas de Oxígeno")
    st.subheader("Monitoreo en tiempo real y análisis de datos")
    
    if st.button("Cargar Datos Históricos"):
        archivos_validos = [f for f in os.listdir(INPUT_FOLDER) if f.endswith(('.xls', '.xlsx'))]
        if not archivos_validos:
            show_alert("No hay archivos para consolidar.", "NO_DATA")
        else:
            st.success(f"Se encontraron {len(archivos_validos)} archivos. Listos para consolidar.")
    
    if st.button("Consolidar y Analizar Datos Históricos"):
        archivos_validos = [f for f in os.listdir(INPUT_FOLDER) if f.endswith(('.xls', '.xlsx'))]
        if not archivos_validos:
            show_alert("No hay archivos disponibles para consolidar.", "NO_DATA")
        else:
            try:
                consolidate_data(INPUT_FOLDER, HISTORICAL_DATA_PATH, REVIEWED_FOLDER)
                archivos_despues = [f for f in os.listdir(INPUT_FOLDER) if f.endswith(('.xls', '.xlsx'))]
                if not archivos_despues:
                    st.success("Datos consolidados correctamente y archivos procesados.")
                    notify_observers("Datos históricos consolidados correctamente.", "INFO")
                    load_and_analyze_data()
                else:
                    show_alert("Algunos archivos no fueron procesados correctamente.", "WARNING")
            except Exception as e:
                show_alert(f"Error al consolidar los datos: {str(e)}", "CRITICAL")
    
    st.write("\n\nAlertas detectadas:")
    st.text_area("", value="No hay alertas aún.", height=150, key="alerts")