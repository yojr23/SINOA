import streamlit as st
import os
import pandas as pd
from utils.data_loader import (
    verificar_pruebas_anteriores,
    limpiar_y_mover_archivos,
    consolidar_datos_revisados,
    manejar_archivos_rechazados,
    registrar_actividad
)
from observers.alert_observer import AlertObserver

# Rutas de datos
INPUT_FOLDER = 'data/pruebas_anteriores'
REVIEWED_FOLDER = 'data/pruebas_anteriores_revisados'
REJECTED_FOLDER = 'data/pruebas_rechazadas'
CONSOLIDATED_FILE = 'data/registro_historico/consolidated_data.csv'
LOG_FILE = 'data/logs/operations.log'

# Inicializar el objeto de alertas
alert_observer = AlertObserver()

def show_alert(message, alert_type="INFO"):
    """Muestra una alerta en la interfaz y notifica al observador."""
    if alert_type == "CRITICAL":
        st.error(message)
    elif alert_type == "WARNING":
        st.warning(message)
    elif alert_type == "INFO":
        st.info(message)
    # Notificar al observador para registrar la alerta
    alert_observer.notify(message, alert_type)

def check_folder_status():
    """Muestra el estado de las carpetas de datos."""
    archivos_pruebas = [f for f in os.listdir(INPUT_FOLDER) if not f.startswith('.DS_Store')]
    archivos_revisados = [f for f in os.listdir(REVIEWED_FOLDER) if not f.startswith('.DS_Store')]
    archivos_rechazados = [f for f in os.listdir(REJECTED_FOLDER) if not f.startswith('.DS_Store')]
    
    st.subheader("Estado de las Carpetas de Datos")
    
    if archivos_pruebas:
        st.success(f"📂 {len(archivos_pruebas)} archivo(s) por cargar en 'pruebas_anteriores'.")
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
    
    # Mostrar estado inicial de las carpetas
    check_folder_status()
    
    # Botón para cargar datos históricos
    if st.button("Cargar Datos Históricos"):
        if not verificar_pruebas_anteriores():
            show_alert("No hay archivos en la carpeta 'pruebas_anteriores'.", "WARNING")
        else:
            limpiar_y_mover_archivos()
            registrar_actividad("Archivos cargados y movidos a 'pruebas_anteriores_revisados'.")
            show_alert("Archivos procesados y movidos a 'pruebas_anteriores_revisados'.", "INFO")
        st.rerun()
    
    # Botón para consolidar datos históricos
    if st.button("Consolidar Datos Históricos"):
        consolidar_datos_revisados()
        registrar_actividad("Datos consolidados correctamente.")
        show_alert("Datos consolidados correctamente.", "INFO")
        st.rerun()
    
    # Estadísticas rápidas de los datos
    if os.path.exists(CONSOLIDATED_FILE):
        df = pd.read_csv(CONSOLIDATED_FILE)
        st.subheader("Estadísticas de los Datos Consolidados")
        st.write(f"Total de registros: {len(df)}")
        st.write(f"Promedio: {df['Nivel de Oxígeno'].mean():.2f}")
        st.write(f"Máximo: {df['Nivel de Oxígeno'].max():.2f}")
        st.write(f"Mínimo: {df['Nivel de Oxígeno'].min():.2f}")
    else:
        st.warning("El archivo consolidado no existe. Por favor, consolida los datos primero.")
    
    # Limpieza manual de archivos rechazados
    if os.listdir(REJECTED_FOLDER):
        st.subheader("Archivos Rechazados")
        archivos_rechazados = os.listdir(REJECTED_FOLDER)
        for archivo in archivos_rechazados:
            st.write(archivo)
            if st.button(f"Eliminar {archivo}", key=f"eliminar_{archivo}"):
                os.remove(os.path.join(REJECTED_FOLDER, archivo))
                registrar_actividad(f"Archivo rechazado eliminado: {archivo}")
                show_alert(f"Archivo {archivo} eliminado.", "INFO")
                st.rerun()
    else:
        # Mostrar el número de archivos rechazados usando manejar_archivos_rechazados
        num_rechazados = manejar_archivos_rechazados()
        st.info(f"No hay archivos rechazados. Total rechazados registrados: {num_rechazados}")
    
    # Registro de actividades
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as log_file:
            st.subheader("Registro de Actividades")
            st.text(log_file.read())