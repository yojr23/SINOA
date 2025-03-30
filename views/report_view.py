import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from utils.transitions_utils import transitions
import os
import base64

# ======================================================================
# CONFIGURACIÓN INICIAL
# ======================================================================

HISTORICAL_DATA_PATH = 'sistema_alertas/data/registro_historico/consolidated_data.csv'
REPORT_CONFIG = {
    'date_range': {
        'start': datetime(2024, 1, 1),
        'end': datetime.now()
    },
    'metrics': ['O2_level', 'temperature', 'ph'],
    'chart_types': ['Línea', 'Barras', 'Área']
}

# ======================================================================
# COMPONENTES AVANZADOS
# ======================================================================

def create_download_link(data, filename, file_type):
    """Genera enlace de descarga para diferentes formatos"""
    if file_type == 'csv':
        data.to_csv(filename, index=False)
        with open(filename, "rb") as f:
            csv = f.read()
        b64 = base64.b64encode(csv).decode()
        return f'<a href="data:file/csv;base64,{b64}" download="{filename}">📥 Descargar CSV</a>'
    
    elif file_type == 'png':
        img_bytes = data.to_image(format="png")
        b64 = base64.b64encode(img_bytes).decode()
        return f'<a href="data:image/png;base64,{b64}" download="{filename}">📥 Descargar Imagen</a>'

def create_metric_summary(df):
    """Crea resumen estadístico con tarjetas interactivas"""
    cols = st.columns(5)
    metrics = {
        'Promedio O2': df['O2_level'].mean(),
        'Máximo Temp': df['temperature'].max(),
        'Mínimo pH': df['ph'].min(),
        'Desviación O2': df['O2_level'].std(),
        'Registros': len(df)
    }
    
    for (name, value), col in zip(metrics.items(), cols):
        with col:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">{name}</div>
                    <div class="metric-value">{value:.2f}</div>
                </div>
            """, unsafe_allow_html=True)

# ======================================================================
# VISTA PRINCIPAL
# ======================================================================

def report_view():
    # Configuración inicial
    st.set_page_config(layout="wide")
    transitions.fade_transition(direction='in')
    
    # Header interactivo
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 20px; margin-bottom: 30px;">
            <h1 style="margin: 0;">📊 Centro de Análisis Avanzado</h1>
            <div class="syncing-indicator">
                <div class="sync-dot"></div>
                <span>Actualizando datos...</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Carga de datos
    try:
        df = pd.read_csv(HISTORICAL_DATA_PATH, parse_dates=['timestamp'])
    except FileNotFoundError:
        st.error("No se encontraron datos históricos")
        return
    
    # Panel de control
    with st.expander("⚙️ Configurar Reporte", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            date_range = st.date_input(
                "Rango Fechas",
                value=(REPORT_CONFIG['date_range']['start'], REPORT_CONFIG['date_range']['end'])
            )
            
        with col2:
            selected_metrics = st.multiselect(
                "Métricas a Visualizar",
                options=REPORT_CONFIG['metrics'],
                default=REPORT_CONFIG['metrics']
            )
            
        with col3:
            chart_type = st.selectbox(
                "Tipo de Gráfico",
                options=REPORT_CONFIG['chart_types']
            )
    
    # Filtrado de datos
    filtered_df = df[
        (df['timestamp'] >= pd.to_datetime(date_range[0])) &
        (df['timestamp'] <= pd.to_datetime(date_range[1]))
    ]
    
    # Sección de resumen
    st.markdown("### 📈 Resumen Estadístico")
    create_metric_summary(filtered_df)
    
    # Visualizaciones principales
    st.markdown("### 📊 Visualización Interactiva")
    if not selected_metrics:
        st.warning("Selecciona al menos una métrica para visualizar")
    else:
        fig = go.Figure()
        for metric in selected_metrics:
            if chart_type == 'Línea':
                fig.add_trace(go.Scatter(
                    x=filtered_df['timestamp'],
                    y=filtered_df[metric],
                    name=metric,
                    mode='lines+markers'
                ))
            elif chart_type == 'Barras':
                fig.add_trace(go.Bar(
                    x=filtered_df['timestamp'],
                    y=filtered_df[metric],
                    name=metric
                ))
            else:
                fig.add_trace(go.Scatter(
                    x=filtered_df['timestamp'],
                    y=filtered_df[metric],
                    name=metric,
                    fill='tozeroy'
                ))
        
        fig.update_layout(
            template="plotly_dark" if st.session_state.get("theme") == "dark" else "plotly",
            hovermode="x unified",
            height=600
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Opciones de exportación
        export_col1, export_col2 = st.columns(2)
        with export_col1:
            st.markdown(create_download_link(filtered_df, "reporte.csv", "csv"), unsafe_allow_html=True)
        with export_col2:
            st.markdown(create_download_link(fig, "grafico.png", "png"), unsafe_allow_html=True)
    
    # Análisis complementario
    st.markdown("### 🔍 Análisis Detallado")
    tab1, tab2, tab3 = st.tabs(["Correlaciones", "Distribución", "Datos Crudos"])
    
    with tab1:
        corr_matrix = filtered_df[selected_metrics].corr()
        fig = px.imshow(
            corr_matrix,
            labels=dict(x="Métrica", y="Métrica", color="Correlación"),
            x=selected_metrics,
            y=selected_metrics,
            color_continuous_scale='RdBu'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        selected_dist = st.selectbox("Seleccionar Métrica", selected_metrics)
        fig = px.histogram(filtered_df, x=selected_dist, nbins=30, marginal="box")
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.dataframe(filtered_df.style.highlight_max(axis=0), height=400)

if __name__ == "__main__":
    report_view()