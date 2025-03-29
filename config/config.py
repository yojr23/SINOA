import streamlit as st
from utils.transitions_utils import transitions  # Importamos el módulo de transiciones

def setup_app():
    """Configuración inicial que debe ejecutarse PRIMERO"""
    # 1. Configuración de página (DEBE SER EL PRIMER COMANDO)
    st.set_page_config(
        page_title="SINOA - Sistema de Alertas",
        layout="wide",  # Cambiado a wide para mejor soporte de animaciones
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://example.com/help',
            'Report a bug': "https://example.com/bug",
            'About': "Sistema de Notificación de Alertas"
        }
    )
    
    # 2. Inyección de estilos globales
    st.markdown("""
    <style>
        /* Previene flashes de contenido no estilizado */
        [data-testid="stAppViewContainer"] {
            opacity: 0;
            animation: fadeIn 0.5s ease-out forwards;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
    </style>
    """, unsafe_allow_html=True)
    
    # 3. Inicialización del sistema de transiciones
    if 'transitions' not in st.session_state:
        st.session_state.transitions = transitions
        
    # 4. Estado inicial de la aplicación
    if 'app_initialized' not in st.session_state:
        st.session_state.app_initialized = True
        st.session_state.current_view = "Home"