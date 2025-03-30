# main.py
import streamlit as st  
from config.config import setup_app
setup_app()
import os
from dotenv import load_dotenv
from utils.transitions_utils import transitions
from views import (
    home_view,
    menu_view,
    data_management_view,
    report_view,
    alert_view,
    welcome_view
)
from notifiers.email_notifier import EmailNotifier



# Inicializar transiciones
if 'transitions' not in st.session_state:
    st.session_state.transitions = transitions



def main():
    # Cargar variables de entorno
    load_dotenv()

    # Inicializar transiciones
    transitions = st.session_state.transitions
    # Configurar notificador de email
    email_notifier = EmailNotifier(
        smtp_server=os.getenv('SMTP_SERVER'),
        port=int(os.getenv('SMTP_PORT')),
        sender_email=os.getenv('EMAIL_USER'),
        sender_password=os.getenv('EMAIL_PASS'),
        recipient_email='juniorrincon1992@hotmail.com'
    )

    # Lógica de bienvenida
    if not st.session_state.get('welcome_completed'):
        welcome_view.show_welcome()
        return  # Detener ejecución aquí

    # Resto de la aplicación
    menu_view.menu_view()
    
    current_view = st.session_state.get('current_view', 'Home')
    if current_view == 'Home':
        home_view.home_view()
    elif current_view == 'Gestión de Datos':
        data_management_view.run_gui(email_notifier)


    # Renderizar menú lateral
    menu_view.menu_view()

    # Navegación dinámica
    current_view = st.session_state.get('current_view', 'Home')
    
    # Transición suave entre vistas
    with st.container():
        st.session_state.transitions.fade_transition(direction='in')
        
        if current_view == 'Home':
            home_view.home_view()
            
        elif current_view == 'Gestión de Datos':
            data_management_view.run_gui(email_notifier)
            
        elif current_view == 'Reportes':
            report_view.report_view()
            
        elif current_view == 'Alertas':
            alert_view.alert_view()
            
        elif current_view == 'Configuración':
            st.title("⚙️ Configuración del Sistema")
            st.write("Personaliza los parámetros de operación")
            
            # Ejemplo de configuración
            with st.expander("Preferencias de notificación"):
                st.checkbox("Recibir alertas por email", value=True)
                st.checkbox("Notificaciones push", value=False)
                
            with st.expander("Parámetros técnicos"):
                st.slider("Frecuencia de muestreo (Hz)", 1, 60, 10)
                st.number_input("Umbral de error permitido (%)", 1, 20, 5)

if __name__ == "__main__":
    main()