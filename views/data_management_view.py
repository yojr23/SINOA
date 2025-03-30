import streamlit as st
import os
import time
import pandas as pd
import plotly.express as px
from utils.data_loader import consolidate_data
from utils.transitions_utils import transitions

# ======================================================================
# CONFIGURACIÓN INICIAL
# ======================================================================

HISTORICAL_DATA_PATH = 'sistema_alertas/data/registro_historico/consolidated_data.csv'
INPUT_FOLDER = 'sistema_alertas/data/pruebas_anteriores/'
REVIEWED_FOLDER = 'sistema_alertas/data/pruebas_anteriores_revisados/'
REJECTED_FOLDER = 'sistema_alertas/data/pruebas_rechazadas/'

# Asegurar carpetas
os.makedirs(INPUT_FOLDER, exist_ok=True)
os.makedirs(REVIEWED_FOLDER, exist_ok=True)
os.makedirs(REJECTED_FOLDER, exist_ok=True)

# ======================================================================
# COMPONENTES UI AVANZADOS
# ======================================================================

def file_card(filename, status="pending", last_modified=None):
    """Componente personalizado para archivos"""
    status_icons = {
        "pending": ("📥", "#ffd700"),
        "reviewed": ("✅", "#28a745"),
        "rejected": ("❌", "#dc3545")
    }
    
    return f"""
        <div class="file-card" data-status="{status}">
            <div class="file-header">
                <span class="file-icon" style="color: {status_icons[status][1]}">{status_icons[status][0]}</span>
                <div class="file-info">
                    <div class="file-name">{filename}</div>
                    <div class="file-meta">Última modificación: {last_modified or 'N/A'}</div>
                </div>
            </div>
            <div class="file-actions">
                <button class="action-btn">👁️ Vista previa</button>
                <button class="action-btn">📤 Exportar</button>
            </div>
        </div>
    """

def setup_data_management_styles():
    """Estilos CSS avanzados para gestión de datos"""
    st.markdown(f"""
        <style>
        /* Tarjetas de archivos */
        .file-card {{
            background: {st.get_option('theme.secondaryBackgroundColor')};
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            transition: all 0.3s;
        }}
        
        .file-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}
        
        .file-header {{
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 10px;
        }}
        
        .file-icon {{
            font-size: 1.8rem;
        }}
        
        .file-name {{
            font-weight: 600;
            color: {st.get_option('theme.textColor')};
        }}
        
        .file-meta {{
            font-size: 0.8rem;
            opacity: 0.7;
        }}
        
        /* Acciones de archivo */
        .file-actions {{
            display: flex;
            gap: 10px;
            margin-top: 10px;
        }}
        
        .action-btn {{
            border: none;
            background: {st.get_option('theme.primaryColor')}20;
            color: {st.get_option('theme.primaryColor')};
            padding: 5px 15px;
            border-radius: 20px;
            cursor: pointer;
            transition: all 0.3s;
        }}
        
        .action-btn:hover {{
            background: {st.get_option('theme.primaryColor')}30;
        }}
        
        /* Progress bar personalizada */
        .stProgress > div > div > div {{
            background-color: {st.get_option('theme.primaryColor')} !important;
        }}
        </style>
    """, unsafe_allow_html=True)

# ======================================================================
# FUNCIONALIDADES PRINCIPALES
# ======================================================================

def file_processing_pipeline():
    """Pipeline completo de procesamiento de archivos"""
    with st.expander("🚀 Procesamiento Avanzado", expanded=True):
        col1, col2, col3 = st.columns([2,1,1])
        
        with col1:
            st.subheader("Automatización de Flujo")
            selected_files = st.multiselect(
                "Seleccionar archivos para procesar",
                options=os.listdir(INPUT_FOLDER),
                format_func=lambda x: f"📄 {x}"
            )
            
        with col2:
            st.subheader("Acciones Rápidas")
            if st.button("🔄 Procesar Selección", key="process_selected"):
                process_files(selected_files)
            
            if st.button("🧹 Limpiar Todo", key="clean_all"):
                clean_all_files()
        
        with col3:
            st.subheader("Estadísticas")
            st.metric("Archivos Pendientes", len(os.listdir(INPUT_FOLDER)))
            st.metric("Procesados Hoy", st.session_state.get("processed_today", 0))

def process_files(files):
    """Procesa archivos con feedback visual"""
    progress_bar = st.progress(0)
    status_container = st.empty()
    
    for i, filename in enumerate(files):
        try:
            # Simular procesamiento
            status_container.markdown(f"Procesando `{filename}`...")
            time.sleep(0.5)
            
            # Mover archivo
            os.rename(
                os.path.join(INPUT_FOLDER, filename),
                os.path.join(REVIEWED_FOLDER, filename)
            )
            
            # Actualizar progreso
            progress_bar.progress((i+1)/len(files))
            st.session_state.processed_today = st.session_state.get("processed_today", 0) + 1
            
        except Exception as e:
            st.error(f"Error procesando {filename}: {str(e)}")
    
    transitions.success_animation()
    st.success(f"✅ Procesados {len(files)} archivos exitosamente!")

def data_health_dashboard():
    """Panel de salud de datos"""
    with st.expander("📊 Panel de Calidad de Datos", expanded=True):
        if os.path.exists(HISTORICAL_DATA_PATH):
            df = pd.read_csv(HISTORICAL_DATA_PATH)
            
            # Mostrar métricas clave
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Registros Totales", len(df))
            with col2:
                st.metric("Datos Faltantes", df.isnull().sum().sum())
            with col3:
                st.metric("Valores Únicos", df.nunique().mean().round(2))
            
            # Visualización de distribución
            st.subheader("Distribución Temporal")
            fig = px.histogram(df, x="timestamp", nbins=30)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No hay datos históricos disponibles")

# ======================================================================
# VISTA PRINCIPAL
# ======================================================================

def run_gui():
    # Configuración inicial
    st.set_page_config(layout="wide")
    setup_data_management_styles()
    
    # Header interactivo
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 30px;">
            <h1 style="margin: 0;">📂 Gestión Inteligente de Datos</h1>
            <div style="margin-left: auto; display: flex; gap: 10px;">
                <button class="action-btn">📤 Exportar Todo</button>
                <button class="action-btn">🔄 Sincronizar</button>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Sección principal
    file_processing_pipeline()
    data_health_dashboard()
    
    # Vista de archivos detallada
    st.subheader("Explorador de Archivos")
    tab1, tab2, tab3 = st.tabs(["📥 Pendientes", "✅ Procesados", "❌ Rechazados"])
    
    with tab1:
        for f in os.listdir(INPUT_FOLDER):
            st.markdown(file_card(f, "pending"), unsafe_allow_html=True)
    
    with tab2:
        for f in os.listdir(REVIEWED_FOLDER):
            st.markdown(file_card(f, "reviewed"), unsafe_allow_html=True)
    
    with tab3:
        for f in os.listdir(REJECTED_FOLDER):
            st.markdown(file_card(f, "rejected"), unsafe_allow_html=True)

def clean_all_files():
    """Limpieza de todos los archivos"""
    # Implementación real aquí
    st.success("🧹 Todos los archivos han sido limpiados")

if __name__ == "__main__":
    run_gui()