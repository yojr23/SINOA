import streamlit as st
import time

class TransitionManager:
    def __init__(self):
        self.animation_lock = False
    
    def _inject_css(self):
        st.markdown("""
            <style>
                @keyframes fadeIn {
                    from { opacity: 0; transform: scale(0.95); }
                    to { opacity: 1; transform: scale(1); }
                }
                @keyframes slideLeft {
                    from { transform: translateX(-100%); opacity: 0; }
                    to { transform: translateX(0); opacity: 1; }
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
        if self.animation_lock: return
        self.animation_lock = True
        placeholder = st.empty()
        try:
            self._inject_css()
            for i in range(3):
                placeholder.markdown(f"""
                    <h1 style='animation: fadeIn 0.5s; text-align: center; color: #4CAF50;'>
                        Bienvenido a SINOA{'.' * i}
                    </h1>
                """, unsafe_allow_html=True)
                time.sleep(0.5)
        finally:
            placeholder.empty()
            self.animation_lock = False

    def fade_transition(self, direction="out"):
        if self.animation_lock: return
        self.animation_lock = True
        overlay = st.empty()
        try:
            steps = 10
            for i in range(steps, 0, -1) if direction == "out" else range(1, steps+1):
                opacity = i/steps if direction == "out" else 1-(i/steps)
                overlay.markdown(
                    f"<div class='transition-overlay' style='background:white;opacity:{opacity};'></div>", 
                    unsafe_allow_html=True
                )
                time.sleep(0.03)
        finally:
            overlay.empty()
            self.animation_lock = False

    def slide_transition(self, direction="left"):
        if self.animation_lock: return
        self.animation_lock = True
        try:
            self._inject_css()
            animation = f"slide{direction.capitalize()} 0.5s ease-out"
            st.markdown(f"""
                <div style='animation: {animation};'>
                    <!-- Contenido animado -->
                </div>
            """, unsafe_allow_html=True)
            time.sleep(0.5)
        finally:
            self.animation_lock = False

# Instancia global para manejar transiciones
transitions = TransitionManager()