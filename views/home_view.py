import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import time

# ======================================================================
# FUNCIONALIDADES AVANZADAS
# ======================================================================

def apply_dynamic_styles():
    """Carga estilos CSS dinámicos y configura el tema."""
    st.markdown(f"""
        <style>
        /* Tema base */
        :root {{
            --primary: {st.get_option('theme.primaryColor')};
            --background: {st.get_option('theme.backgroundColor')};
            --secondary-background: {st.get_option('theme.secondaryBackgroundColor')};
            --text: {st.get_option('theme.textColor')};
        }}
        
        /* Tarjetas interactivas mejoradas */
        .metric-card {{
            padding: 1.5rem;
            border-radius: 1rem;
            background: var(--secondary-background);
            margin: 1rem 0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            border-left: 4px solid var(--primary);
            position: relative;
            overflow: hidden;
        }}
        
        .metric-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        }}
        
        .metric-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 4px;
            background: linear-gradient(90deg, var(--primary) 0%, transparent 100%);
        }}
        
        /* Indicadores de estado animados */
        .status-indicator {{
            width: 12px;
            height: 12px;
            border-radius: 50%;
            display: inline-block;
            margin-right: 8px;
            animation: pulse 1.5s infinite;
        }}
        
        .status-online {{ background: #28a745; }}
        .status-offline {{ background: #dc3545; }}
        
        /* Animaciones */
        @keyframes pulse {{
            0% {{ opacity: 0.8; transform: scale(1); }}
            50% {{ opacity: 0.4; transform: scale(0.95); }}
            100% {{ opacity: 0.8; transform: scale(1); }}
        }}
        
        /* Responsive design */
        @media (max-width: 768px) {{
            .metric-card {{
                padding: 1rem;
                margin: 0.5rem 0;
            }}
            
            .metric-col {{
                margin-bottom: 1rem;
            }}
        }}
        </style>
    """, unsafe_allow_html=True)

def generate_realistic_data():
    """Genera datos simulados con patrones realistas"""
    now = datetime.now()
    data = {
        "timestamp": [],
        "value": []
    }
    
    # Patrón diario simulado
    for i in range(1440):  # 24 horas en minutos
        minute = now - timedelta(minutes=i)
        base = 3.0 + 0.1 * (i % 60)
        fluctuation = 0.5 * (i % 120) / 60
        noise = (0.2 if (i % 10) == 0 else 0.05) * (i % 3 - 1)
        
        data["timestamp"].append(minute)
        data["value"].append(round(base + fluctuation + noise, 2))
    
    return pd.DataFrame(data).sort_values("timestamp")

def toggle_theme():
    """Cambia entre tema claro/oscuro con persistencia"""
    current_theme = st.session_state.get("theme", "light")
    new_theme = "dark" if current_theme == "light" else "light"
    st.session_state.theme = new_theme
    st.experimental_set_query_params(theme=new_theme)

# ======================================================================
# VISTA PRINCIPAL
# ======================================================================

def home_view():
    # Configuración de estilos
    apply_dynamic_styles()
    
    # Encabezado responsivo
    with st.container():
        header_col1, header_col2, header_col3 = st.columns([6, 1, 1])
        with header_col1:
            st.markdown("""
                <h1 style="margin: 0; font-size: 2.2rem; line-height: 1.2;">
                    🚨 SINOA<br>
                    <span style="font-size: 1.2rem; opacity: 0.8;">Sistema Inteligente de Monitoreo de Oxígeno Acuático</span>
                </h1>
            """, unsafe_allow_html=True)
            
        with header_col2:
            st.button(
                "🌓", 
                on_click=toggle_theme, 
                help="Cambiar tema claro/oscuro",
                key="theme_toggle"
            )
            
        with header_col3:
            st.markdown("""
                <div style="display: flex; align-items: center; margin-top: 0.8rem;">
                    <span class="status-indicator status-online"></span>
                    <span style="font-size: 0.9rem;">Conectado</span>
                </div>
            """, unsafe_allow_html=True)
    
    # Tarjetas métricas dinámicas
    with st.container():
        metric_cols = st.columns(4)
        metrics = [
            {"icon": "📈", "title": "Tendencia Actual", "value": "Estable", "subtext": "Últimos 15 min"},
            {"icon": "⚡", "title": "Máximo Reciente", "value": "4.2 ppm", "subtext": "Hace 8 minutos"},
            {"icon": "🔄", "title": "Variabilidad", "value": "2.8%", "subtext": "±0.15 ppm"},
            {"icon": "🔔", "title": "Alertas (24h)", "value": "3", "subtext": "1 crítica"}
        ]
        
        for col, metric in zip(metric_cols, metrics):
            with col:
                st.markdown(f"""
                    <div class="metric-card">
                        <div style="font-size: 1.8rem; margin-bottom: 0.5rem;">
                            {metric['icon']}
                        </div>
                        <div style="font-weight: 600; margin-bottom: 0.25rem;">
                            {metric['title']}
                        </div>
                        <h2 style="margin: 0 0 0.25rem 0;">{metric['value']}</h2>
                        <div style="font-size: 0.9rem; opacity: 0.7;">
                            {metric['subtext']}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
    
    # Gráfico principal con datos simulados
    with st.container():
        with st.spinner("Actualizando datos en tiempo real..."):
            df = generate_realistic_data()
            fig = px.line(
                df, 
                x="timestamp", 
                y="value", 
                title="Monitorización en Tiempo Real",
                labels={"value": "Nivel (ppm)", "timestamp": "Hora"},
                template="plotly_dark" if st.session_state.get("theme") == "dark" else "plotly_white"
            )
            
            fig.update_layout(
                hovermode="x unified",
                margin=dict(t=40, b=20, l=20, r=20),
                xaxis=dict(
                    rangeselector=dict(
                        buttons=list([
                            dict(count=1, label="1h", step="hour", stepmode="backward"),
                            dict(count=6, label="6h", step="hour", stepmode="backward"),
                            dict(step="all")
                        ])
                    ),
                    rangeslider=dict(visible=True)
                ),
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    # Historial de eventos interactivo
    with st.container():
        st.markdown("### 📜 Historial Detallado de Eventos")
        
        alertas = [
            {"tipo": "CRITICAL", "mensaje": "Nivel crítico: 1.8 ppm", "timestamp": "14:30", "duracion": "12 min"},
            {"tipo": "WARNING", "mensaje": "Fluctuación inusual", "timestamp": "12:15", "duracion": "8 min"},
            {"tipo": "INFO", "mensaje": "Mantenimiento programado", "timestamp": "09:00", "duracion": "-"}
        ]
        
        for alerta in alertas:
            icono = "🔥" if alerta["tipo"] == "CRITICAL" else "⚠️" if alerta["tipo"] == "WARNING" else "ℹ️"
            
            with st.expander(f"{icono} {alerta['tipo']}: {alerta['mensaje']}", expanded=True):
                cols = st.columns([3, 1])
                with cols[0]:
                    st.markdown(f"**Detalle:** {alerta['mensaje']}")
                with cols[1]:
                    st.markdown(f"""
                        <div style="text-align: right;">
                            <div style="opacity: 0.7; font-size: 0.9rem;">{alerta['timestamp']}</div>
                            <code>{alerta['duracion']}</code>
                        </div>
                    """, unsafe_allow_html=True)

if __name__ == "__main__":
    home_view()