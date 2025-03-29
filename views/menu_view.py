import streamlit as st
from views.data_management_view import run_gui
from notifiers.email_notifier import EmailNotifier
from utils.transitions_utils import transitions
from views.welcome_view import show_welcome
from views.home_view import home_view

def menu_view():
    st.sidebar.title("Menú de Navegación")
    opciones = ["Home", "Gestión de Datos"]
    
    # Obtener selección previa
    prev = st.session_state.get("current_view", "Home")
    
    # Widget de selección
    current = st.sidebar.radio("Opciones:", opciones, index=opciones.index(prev))
    
    # Configuración del notificador
    email_notifier = EmailNotifier(
        smtp_server="smtp.example.com",
        port=587,
        sender_email="tu_email@example.com",
        sender_password="tu_contraseña",
        recipient_email="destinatario@example.com"
    )
    
    # Lógica de transición entre vistas
    if current != prev:
        # Ejecutar la animación de transición de salida (si es necesario)
        transitions.fade_transition(direction='out')

        # Cargar la vista correcta
        if current == "Home":
            home_view()  # Muestra la vista de Home
        elif current == "Gestión de Datos":
            run_gui()  
        # Establecer la vista actual en el estado de sesión
        st.session_state.current_view = current

        # Ejecutar la animación de transición de entrada (si es necesario)
        transitions.fade_transition(direction='in')
    else:
        # Si no hay cambio de vista, solo mostrar la vista actual
        if current == "Home":
            home_view()  # Muestra la vista de Home
        elif current == "Gestión de Datos":
            run_gui()  # Muestra la vista de Gestión de Datos
