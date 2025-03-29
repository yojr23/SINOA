import streamlit as st
import time
import os
from controllers.sensor_drift_manager import SensorDriftManager
from utils.data_loader import consolidate_data, consolidar_o_cargar_historico
from observers.alert_observer import AlertObserver

# Rutas de datos
HISTORICAL_DATA_PATH = 'data/registro_historico/consolidated_data.csv'
INPUT_FOLDER = 'data/pruebas_anteriores'
REVIEWED_FOLDER = 'data/pruebas_anteriores_revisados/'
REJECTED_FOLDER = 'data/pruebas_rechazadas/'

# Asegurar que las carpetas existen
os.makedirs(INPUT_FOLDER, exist_ok=True)
os.makedirs(REVIEWED_FOLDER, exist_ok=True)
os.makedirs(REJECTED_FOLDER, exist_ok=True)

drift_manager = SensorDriftManager(HISTORICAL_DATA_PATH)

# Lista de observadores
observers = []

def add_observer(observer):
    observers.append(observer)

def notify_observers(message, alert_type):
    for observer in observers:
        observer.notify(message, alert_type)

def show_alert(message, alert_type="INFO"):
    """Muestra una alerta en la interfaz y notifica a los observadores."""
    st.error(message) if alert_type == "CRITICAL" else st.warning(message)
    notify_observers(message, alert_type)

def check_folder_status():
    """Muestra el estado de las carpetas de datos."""
    archivos_pruebas = [f for f in os.listdir(INPUT_FOLDER) if not f.startswith('.DS_Store')]
    archivos_revisados = [f for f in os.listdir(REVIEWED_FOLDER) if not f.startswith('.DS_Store')]
    archivos_rechazados = [f for f in os.listdir(REJECTED_FOLDER) if not f.startswith('.DS_Store')]
    
    st.subheader("Estado de las Carpetas de Datos")
    
    if archivos_pruebas:
        st.success(f"📂 {len(archivos_pruebas)} archivo(s) por cargar en 'pruebas_anteriores'.")
        st.write(archivos_pruebas)
    else:
        st.warning("📂 No hay archivos en 'pruebas_anteriores'.")
    
    if archivos_revisados:
        st.success(f"📂 {len(archivos_revisados)} archivo(s) en 'pruebas_anteriores_revisados' listos para consolidar.")
    else:
        st.warning("📂 No hay archivos en 'pruebas_anteriores_revisados'.")
    
    if archivos_rechazados:
        show_alert(f"⚠️ {len(archivos_rechazados)} archivo(s) fueron rechazados para revisión manual.", "WARNING")

def run_gui():
    st.title("Gestión de Datos Históricos")
    
    # Mostrar estado de las carpetas
    check_folder_status()
    
    # Opción de cargar datos históricos
    if st.button("Cargar Datos Históricos", key="cargar_hist"):
        try:
            archivos_antes = len(os.listdir(INPUT_FOLDER))
            df = consolidar_o_cargar_historico()
            archivos_despues = len(os.listdir(INPUT_FOLDER))
            archivos_cargados = archivos_antes - archivos_despues
            
            if archivos_cargados > 0:
                st.success(f"Datos cargados correctamente. Se procesaron {archivos_cargados} archivos.")
            else:
                show_alert("No se encontraron archivos nuevos para cargar.", "NO_DATA")
            
            st.dataframe(df.head())  # Muestra una vista previa de los datos
            st.session_state["ultima_carga"] = time.strftime("%Y-%m-%d %H:%M:%S")
        except FileNotFoundError:
            show_alert("No hay datos históricos disponibles.", "NO_DATA")
    
    if "ultima_carga" in st.session_state:
        st.info(f"Última carga de datos: {st.session_state['ultima_carga']}")
    
    # Opción de consolidar y analizar datos
    if st.button("Consolidar y Analizar Datos Históricos", key="consolidar_hist"):
        archivos_validos = [f for f in os.listdir(REVIEWED_FOLDER) if f.endswith(('.xls', '.xlsx'))]
        
        if not archivos_validos:
            show_alert("No hay archivos disponibles para consolidar.", "NO_DATA")
        else:
            try:
                archivos_antes = len(archivos_validos)
                consolidate_data(REVIEWED_FOLDER, HISTORICAL_DATA_PATH, REVIEWED_FOLDER)
                archivos_despues = len([f for f in os.listdir(REVIEWED_FOLDER) if f.endswith(('.xls', '.xlsx'))])
                archivos_consolidados = archivos_antes - archivos_despues
                
                if archivos_consolidados > 0:
                    st.success(f"Datos consolidados correctamente. Se consolidaron {archivos_consolidados} archivos.")
                    notify_observers("Datos históricos consolidados correctamente.", "INFO")
                    st.session_state["ultima_consolidacion"] = time.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    show_alert("No se consolidaron nuevos archivos.", "NO_DATA")
            except Exception as e:
                show_alert(f"Error al consolidar los datos: {str(e)}", "CRITICAL")
    
    if "ultima_consolidacion" in st.session_state:
        st.info(f"Última consolidación de datos: {st.session_state['ultima_consolidacion']}")
