import streamlit as st
import os
import time
import pandas as pd
from datetime import datetime
from utils.transitions_utils import transitions


from views.home_view import home_view
from views.data_management_view import run_gui as data_management_view
from views.report_view import report_view
from views.alert_view import alert_view

# ======================================================================
# CONFIGURACIÓN INICIAL Y CONTEXTO GLOBAL
# ======================================================================

# Rutas de datos compartidas entre vistas
HISTORICAL_DATA_PATH = 'sistema_alertas/data/registro_historico/consolidated_data.csv'
ALERT_HISTORY_PATH = 'sistema_alertas/data/alertas_historicas.csv'
INPUT_FOLDER = 'sistema_alertas/data/pruebas_anteriores/'
REVIEWED_FOLDER = 'sistema_alertas/data/pruebas_anteriores_revisados/'
REJECTED_FOLDER = 'sistema_alertas/data/pruebas_rechazadas/'

# Aseguramos que las carpetas existen
for folder in [INPUT_FOLDER, REVIEWED_FOLDER, REJECTED_FOLDER, os.path.dirname(HISTORICAL_DATA_PATH)]:
    os.makedirs(folder, exist_ok=True)

# ======================================================================
# COMPONENTES REUTILIZABLES
# ======================================================================

def check_for_data_updates():
    """Verifica si hay actualizaciones en los datos para notificaciones"""
    # Comprobamos archivos pendientes para gestión de datos
    pending_files = [f for f in os.listdir(INPUT_FOLDER) if f.endswith(('.xls', '.xlsx', '.csv'))]
    st.session_state.data_alerts = len(pending_files)
    
    # Comprobamos alertas activas
    if os.path.exists(ALERT_HISTORY_PATH):
        try:
            alerts_df = pd.read_csv(ALERT_HISTORY_PATH, parse_dates=["timestamp"])
            # Alertas de las últimas 24 horas
            recent_alerts = alerts_df[
                alerts_df["timestamp"] > (datetime.now() - pd.Timedelta(days=1))
            ]
            st.session_state.active_alerts = len(recent_alerts)
        except Exception:
            st.session_state.active_alerts = 0
    else:
        st.session_state.active_alerts = 0

def setup_menu_styles():
    """Estilos CSS optimizados para el menú y el sistema general"""
    st.markdown(f"""
        <style>
        /* Sidebar y menú principal */
        [data-testid="stSidebar"] {{
            background: {st.get_option('theme.secondaryBackgroundColor')};
            border-right: 1px solid {st.get_option('theme.backgroundColor')};
        }}
        
        /* Estilo de los radio buttons del menú */
        div.row-widget.stRadio > div {{
            flex-direction: column;
            gap: 0.5rem;
        }}
        
        div.row-widget.stRadio > div > label {{
            padding: 0.75rem 1.25rem;
            border-radius: 0.5rem;
            display: flex;
            align-items: center;
            gap: 0.75rem;
            cursor: pointer;
            transition: all 0.2s ease;
            margin: 0.25rem 0;
            font-weight: normal;
        }}
        
        div.row-widget.stRadio > div [data-testid="stMarkdownContainer"] p {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        
        div.row-widget.stRadio > div > label:hover {{
            background: {st.get_option('theme.primaryColor')}15;
            transform: translateX(0.25rem);
        }}
        
        /* Ocultar los círculos de los radio buttons */
        div.row-widget.stRadio > div input[type="radio"] {{
            position: absolute;
            opacity: 0;
        }}
        
        div.row-widget.stRadio > div input[type="radio"]:checked + label {{
            background: {st.get_option('theme.primaryColor')}25;
            box-shadow: inset 3px 0 0 {st.get_option('theme.primaryColor')};
            font-weight: bold;
        }}
        
        /* Notificaciones */
        .notification-badge {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background: #dc3545;
            color: white;
            font-size: 0.75rem;
            border-radius: 9999px;
            min-width: 1.5rem;
            height: 1.5rem;
            padding: 0 0.4rem;
            margin-left: auto;
        }}
        
        /* Indicadores de estado */
        .status-indicator {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.9rem;
            color: {st.get_option('theme.textColor')};
            opacity: 0.85;
        }}
        
        .pulse-dot {{
            width: 8px;
            height: 8px;
            border-radius: 50%;
            display: inline-block;
            margin-right: 4px;
            animation: pulse 1.5s infinite;
        }}
        
        .pulse-dot.online {{
            background-color: #28a745;
        }}
        
        .pulse-dot.offline {{
            background-color: #dc3545;
        }}
        
        @keyframes pulse {{
            0% {{ opacity: 0.7; transform: scale(1); }}
            50% {{ opacity: 0.3; transform: scale(0.95); }}
            100% {{ opacity: 0.7; transform: scale(1); }}
        }}
        
        /* Compatibilidad con prefers-reduced-motion */
        @media (prefers-reduced-motion: reduce) {{
            .pulse-dot {{
                transition: none;
                animation: none;
            }}
        }}
        
        /* Indicador sincronización */
        .syncing-indicator {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.9rem;
            margin-left: auto;
        }}
        
        .sync-dot {{
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #17a2b8;
            animation: sync-pulse 1s infinite;
        }}
        
        @keyframes sync-pulse {{
            0% {{ opacity: 1; }}
            50% {{ opacity: 0.3; }}
            100% {{ opacity: 1; }}
        }}
        
        /* Ocultar el título del radio button */
        div.row-widget.stRadio > div:first-child {{
            display: none;
        }}
        </style>
    """, unsafe_allow_html=True)

# ======================================================================
# VISTA DEL MENÚ PRINCIPAL
# ======================================================================

def initialize_session_state():
    """Inicializa variables de estado global para la aplicación"""
    if "current_view" not in st.session_state:
        st.session_state.current_view = "Home"
    
    if "theme" not in st.session_state:
        st.session_state.theme = "light"
    
    if "last_data_check" not in st.session_state:
        st.session_state.last_data_check = datetime.now()
        check_for_data_updates()

def menu_view():
    """Vista principal del menú de navegación"""
    initialize_session_state()
    setup_menu_styles()
    
    # Actualizamos las notificaciones cada minuto
    current_time = datetime.now()
    if (current_time - st.session_state.get("last_data_check", current_time)).seconds > 60:
        check_for_data_updates()
        st.session_state.last_data_check = current_time
    
    with st.sidebar:
        # Encabezado con versión y modo
        st.markdown(f"""
            <div style="padding: 1.25rem 1rem; 
                        border-bottom: 1px solid {st.get_option('theme.backgroundColor')};">
                <div style="font-size: 1.75rem; 
                           font-weight: 700; 
                           color: {st.get_option('theme.primaryColor')};">
                    SINOA
                </div>
                <div style="font-size: 0.9rem; 
                           color: {st.get_option('theme.textColor')}; 
                           opacity: 0.8;
                           display: flex;
                           justify-content: space-between;
                           margin-top: 0.25rem;">
                    <span>v2.1</span>
                    <span>•</span>
                    <span>Modo {st.session_state.get('theme', 'claro').title()}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Menú principal usando radio buttons nativos de Streamlit
        menu_options = {
            "Home": {"icon": "🏠", "notifications": 0},
            "Gestión de Datos": {"icon": "📊", "notifications": st.session_state.get('data_alerts', 0)},
            "Reportes": {"icon": "📈", "notifications": 0},
            "Alertas": {"icon": "🚨", "notifications": st.session_state.get('active_alerts', 0)},
            "Configuración": {"icon": "⚙️", "notifications": 0}
        }
        
        # Función para formatear las opciones del menú
        def format_menu_option(option):
            notifications = menu_options[option]["notifications"]
            icon = menu_options[option]["icon"]
            if notifications > 0:
                return f"{icon} {option} <span class='notification-badge'>{notifications}</span>"
            else:
                return f"{icon} {option}"
        
        # Usar radio buttons como menú de navegación
        selected_view = st.radio(
            "Navegación",
            options=list(menu_options.keys()),
            format_func=lambda x: format_menu_option(x),
            key="navigation_menu",
            index=list(menu_options.keys()).index(st.session_state.get("current_view", "Home")),
            horizontal=False,
            label_visibility="collapsed"
        )
        
        # Cambiar de vista si se selecciona una diferente
        if selected_view != st.session_state.get("current_view", "Home"):
            transitions.slide_transition(direction="left")
            st.session_state.current_view = selected_view
            st.rerun()
        
        # Sección de estado del sistema
        system_status = "online" if check_system_status() else "offline"
        status_text = "Operativo" if system_status == "online" else "No disponible"
        
        st.markdown(f"""
            <div style="padding: 1.25rem; 
                        margin-top: 2rem; 
                        background: {st.get_option('theme.backgroundColor')}15; 
                        border-radius: 0.75rem;">
                <div class="status-indicator">
                    <span class="pulse-dot {system_status}"></span>
                    Estado: {status_text}
                </div>
                <div style="margin-top: 0.5rem; font-size: 0.8rem; opacity: 0.8;">
                    Última actualización: {datetime.now().strftime('%H:%M:%S')}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Botón para cambiar tema en el sidebar
        st.markdown("<div style='margin-top: 1.5rem;'>", unsafe_allow_html=True)
        if st.button("🌓 Cambiar Tema", key="theme_sidebar"):
            toggle_theme()
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ======================================================================
# FUNCIONES AUXILIARES
# ======================================================================

def check_system_status():
    """Verifica estado del sistema"""
    # En un sistema real, comprobaríamos conexión con sensores, bases de datos, etc.
    # Para este ejemplo, simulamos que está online
    return True

def toggle_theme():
    """Cambia entre tema claro/oscuro con persistencia"""
    current_theme = st.session_state.get("theme", "light")
    new_theme = "dark" if current_theme == "light" else "light"
    st.session_state.theme = new_theme
    # Intentamos establecer parámetros de consulta, con manejo de excepciones por seguridad
    try:
        st.query_params["theme"] = new_theme
    except:
        pass

# ======================================================================
# MANEJO DE NAVEGACIÓN
# ======================================================================

def handle_navigation():
    """Gestión centralizada de las vistas con contexto compartido"""
    current_view = st.session_state.get("current_view", "Home")
    
    # Contenedor principal para la vista actual
    with st.container():
        # Aplicamos una transición suave
        transitions.fade_transition(direction='in', duration=0.25)
        
        # Mapeamos vistas a sus funciones correspondientes
        view_mapping = {
            "Home": home_view,
            "Gestión de Datos": data_management_view,
            "Reportes": report_view,
            "Alertas": alert_view,
        }
        
        # Renderizamos la vista actual
        try:
            if current_view in view_mapping:
                # Pasamos contexto compartido a las vistas que lo necesiten
                if current_view == "Gestión de Datos":
                    view_mapping[current_view]()
                else:
                    view_mapping[current_view]()
            else:
                # Fallback por si hay un error en el estado
                st.error("Vista no encontrada")
                st.session_state.current_view = "Home"
                st.rerun()
        except Exception as e:
            # Capturamos errores en las vistas para evitar fallos catastróficos
            st.error(f"Error al cargar la vista: {str(e)}")
            st.code(f"{type(e).__name__}: {str(e)}")
            
            # Opción para volver a inicio si hay error
            if st.button("Volver a Inicio"):
                st.session_state.current_view = "Home"
                st.rerun()

# ======================================================================
# PUNTO DE ENTRADA PRINCIPAL
# ======================================================================

def main():
    """Función principal que ejecuta la aplicación"""
    # Configuración global de la página
    st.set_page_config(
        page_title="SINOA - Sistema Inteligente de Monitoreo",
        page_icon="🚨",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Renderizamos el menú y manejamos la navegación
    menu_view()
    handle_navigation()

if __name__ == "__main__":
    main()