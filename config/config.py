import streamlit as st

def setup_app():
    """Configuración única de la página"""
    if not st.session_state.get('page_configured'):
        st.set_page_config(
            page_title="SINOA - Sistema de Alertas",
            page_icon="⚠️",
            layout="wide",
            initial_sidebar_state="auto"
        )
        st.session_state.page_configured = True