import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import time
from utils.transitions_utils import transitions
from notifiers.email_notifier import EmailNotifier
import os

# ======================================================================
# CONFIGURACIÓN INICIAL
# ======================================================================

ALERT_HISTORY_PATH = "sistema_alertas/data/alertas_historicas.csv"
ALERT_CONFIG = {
    "umbral_critico": 2.0,
    "umbral_advertencia": 3.0,
    "canales_notificacion": ["email", "app"],
}

# ======================================================================
# COMPONENTES AVANZADOS
# ======================================================================

def alert_card(tipo, mensaje, timestamp, duracion=None):
    """Tarjeta interactiva para mostrar alertas"""
    iconos = {
        "CRITICAL": "🔥",
        "WARNING": "⚠️",
        "INFO": "ℹ️"
    }
    colores = {
        "CRITICAL": "#dc3545",
        "WARNING": "#ffc107",
        "INFO": "#17a2b8"
    }
    
    return f"""
        <div class="alert-card" data-tipo="{tipo}">
            <div class="alert-header">
                <span class="alert-icon" style="color: {colores[tipo]}">{iconos[tipo]}</span>
                <div class="alert-info">
                    <div class="alert-title">{tipo}</div>
                    <div class="alert-timestamp">{timestamp}</div>
                </div>
                <div class="alert-actions">
                    <button class="action-btn">🗑️</button>
                    <button class="action-btn">📌</button>
                </div>
            </div>
            <div class="alert-body">
                <p>{mensaje}</p>
                {f'<div class="alert-duration">Duración: {duracion}</div>' if duracion else ""}
            </div>
        </div>
    """

def setup_alert_styles():
    """Estilos CSS para el sistema de alertas"""
    st.markdown(f"""
        <style>
        .alert-card {{
            background: {st.get_option('theme.secondaryBackgroundColor')};
            border-radius: 12px;
            padding: 15px;
            margin: 15px 0;
            border-left: 4px solid;
            box-shadow: 0 3px 6px rgba(0,0,0,0.1);
            transition: all 0.3s;
        }}
        
        .alert-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }}
        
        .alert-header {{
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 10px;
        }}
        
        .alert-icon {{
            font-size: 2rem;
        }}
        
        .alert-title {{
            font-weight: 700;
            font-size: 1.2rem;
        }}
        
        .alert-timestamp {{
            font-size: 0.8rem;
            opacity: 0.7;
        }}
        
        .alert-actions {{
            margin-left: auto;
            display: flex;
            gap: 10px;
        }}
        
        .action-btn {{
            border: none;
            background: transparent;
            font-size: 1.2rem;
            cursor: pointer;
            padding: 5px;
            border-radius: 50%;
            transition: all 0.3s;
        }}
        
        .action-btn:hover {{
            background: {st.get_option('theme.backgroundColor')};
        }}
        
        .alert-duration {{
            margin-top: 10px;
            padding: 8px;
            background: {st.get_option('theme.primaryColor')}15;
            border-radius: 6px;
            font-size: 0.9rem;
        }}
        </style>
    """, unsafe_allow_html=True)

# ======================================================================
# FUNCIONALIDADES PRINCIPALES
# ======================================================================

def alertas_en_tiempo_real():
    """Simulación de alertas en tiempo real"""
    placeholder = st.empty()
    for i in range(5):
        with placeholder.container():
            nivel_simulado = 1.5 + i * 0.5
            tipo = "CRITICAL" if nivel_simulado < ALERT_CONFIG["umbral_critico"] else "WARNING"
            mensaje = f"Nivel de O2: {nivel_simulado:.1f} ppm"
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            st.markdown(
                alert_card(tipo, mensaje, timestamp, "3 min"),
                unsafe_allow_html=True
            )
            time.sleep(1)
    placeholder.empty()

def historial_alertas():
    """Muestra el historial de alertas con análisis"""
    if os.path.exists(ALERT_HISTORY_PATH):
        df = pd.read_csv(ALERT_HISTORY_PATH, parse_dates=["timestamp"])
        
        st.subheader("📅 Historial de Alertas")
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig = px.timeline(
                df,
                x_start="timestamp",
                x_end="timestamp_end",
                y="tipo",
                color="tipo",
                color_discrete_map={
                    "CRITICAL": "#dc3545",
                    "WARNING": "#ffc107",
                    "INFO": "#17a2b8"
                }
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.metric("Total Alertas", len(df))
            st.metric("Promedio Diario", f"{len(df)/30:.1f}/día")
            st.metric("Tiempo Respuesta", "8.2 min")
    else:
        st.warning("No hay historial de alertas registrado")

# ======================================================================
# VISTA PRINCIPAL
# ======================================================================

def alert_view():
    # Configuración inicial
    st.set_page_config(layout="wide")
    setup_alert_styles()
    
    # Header dinámico
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 20px; margin-bottom: 30px;">
            <h1 style="margin: 0;">🚨 Centro de Gestión de Alertas</h1>
            <div class="status-indicator">
                <span class="pulse-dot"></span>
                Monitoreo activo
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Sección en tiempo real
    with st.expander("🔴 Alertas Activas", expanded=True):
        alertas_en_tiempo_real()
    
    # Histórico y análisis
    historial_alertas()
    
    # Configuración de alertas
    with st.expander("⚙️ Configurar Umbrales"):
        col1, col2 = st.columns(2)
        with col1:
            nuevo_critico = st.number_input(
                "Umbral Crítico (ppm)",
                value=ALERT_CONFIG["umbral_critico"],
                min_value=0.0,
                step=0.1
            )
        with col2:
            nuevo_warning = st.number_input(
                "Umbral Advertencia (ppm)",
                value=ALERT_CONFIG["umbral_advertencia"],
                min_value=0.0,
                step=0.1
            )
        
        if st.button("💾 Guardar Configuración"):
            ALERT_CONFIG.update({
                "umbral_critico": nuevo_critico,
                "umbral_advertencia": nuevo_warning
            })
            st.success("Configuración actualizada")

if __name__ == "__main__":
    alert_view()