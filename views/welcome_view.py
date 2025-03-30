import streamlit as st
import time
from utils.transitions_utils import transitions

def show_welcome():
    """Animación de bienvenida fullscreen con gestión de estado robusta"""
    if not st.session_state.get('welcome_completed'):
        # Configurar estado inicial
        st.session_state.welcome_completed = False
        
        # Ocultar elementos de la UI
        st.markdown("""
            <style>
                header {visibility: hidden !important;}
                .stApp {max-width: 100% !important; padding: 0 !important;}
                div[data-testid="stVerticalBlock"] {
                    height: 100vh !important;
                    justify-content: center;
                }
                .stProgress > div {display: none !important;}
            </style>
        """, unsafe_allow_html=True)

        # Contenido de la animación
        placeholder = st.empty()
        for i in range(3):
            placeholder.markdown(f"""
                <div style="text-align: center; animation: fadeIn 0.5s;">
                    <h1 style="font-size: 2.5rem; color: {st.get_option('theme.primaryColor')};">
                        {'🚀' * (i+1)}<br>
                        INICIALIZANDO SINOA
                    </h1>
                    <div style="margin: 2rem auto; width: 50%; height: 4px; background: rgba(0,0,0,0.1);">
                        <div style="width: {(i+1)*33}%; height: 100%; background: {st.get_option('theme.primaryColor')};
                            transition: all 0.3s;"></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            time.sleep(0.5)

        # Finalizar animación
        transitions.welcome_animation()
        st.session_state.welcome_completed = True
        time.sleep(0.5)
        placeholder.empty()
        st.rerun()