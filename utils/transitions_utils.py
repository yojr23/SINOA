import streamlit as st
import time

class TransitionManager:
    def __init__(self):
        self.animation_lock = False
    
    def _ensure_css(self):
        """Inyecta los estilos CSS necesarios"""
        st.markdown("""
        <style>
            @keyframes fadeIn {
                from { opacity: 0; transform: scale(0.95); }
                to { opacity: 1; transform: scale(1); }
            }
            @keyframes fadeBackground {
                0% { opacity: 0; }
                100% { opacity: 1; }
            }
            .welcome-container {
                position: relative;
                min-height: 80vh;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
            }
            .transition-overlay {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                z-index: 1000;
                pointer-events: none;
            }
        </style>
        """, unsafe_allow_html=True)

    def welcome_animation(self):
        """Animación de bienvenida mejorada"""
        if self.animation_lock:
            return
            
        self.animation_lock = True
        try:
            self._ensure_css()
            placeholder = st.empty()
            
            for i in range(1, 4):
                placeholder.markdown(f"""
                <div class="welcome-container">
                    <h1 style='
                        color: #4CAF50;
                        font-size: 2.5rem;
                        animation: fadeIn 0.5s;
                    '>
                        Bienvenido a SINOA{'.' * i}
                    </h1>
                </div>
                """, unsafe_allow_html=True)
                time.sleep(0.75)
            
            placeholder.empty()
        finally:
            self.animation_lock = False

    def fade_transition(self, direction='out'):
        """Transición de fundido optimizada"""
        if self.animation_lock:
            return
            
        self.animation_lock = True
        try:
            overlay = st.empty()
            steps = 6  # Reducido para mayor fluidez
            for i in range(steps, 0, -1) if direction == 'out' else range(1, steps+1):
                opacity = i/steps if direction == 'out' else 1-(i/steps)
                overlay.markdown(
                    f"""<div class="transition-overlay" style="background:white;opacity:{opacity};"></div>""",
                    unsafe_allow_html=True
                )
                time.sleep(0.04)
            overlay.empty()
        finally:
            self.animation_lock = False

transitions = TransitionManager()