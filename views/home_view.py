from utils.plot_utils import RealTimePlotter
import streamlit as st
import time

def home_view(email_notifier):
    """Vista principal con monitoreo en tiempo real"""
    
    # Configuración inicial
    st.title("📊 Monitor de Niveles de Oxígeno")
    
    # Inicializar y configurar plotter
    plotter = RealTimePlotter()
    
    # Estado para evitar correos repetidos
    last_alert_type = None  # Almacena el tipo de la última alerta enviada
    
    # Layout principal
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Espacio para el gráfico
        chart_placeholder = st.empty()
    
    with col2:
        # Métricas con protección contra división por cero
        st.subheader("📈 Métricas en Tiempo Real")
        metric_placeholder = st.empty()
        
        def safe_delta(current, previous):
            """Calcula delta de forma segura evitando división por cero"""
            try:
                if previous == 0:
                    return 0
                return current - previous
            except Exception:
                return 0
        
        # Alertas
        st.subheader("⚠️ Alertas")
        alert_placeholder = st.empty()

    # Bucle principal de actualización reactiva
    while True:
        # Actualizar gráfico
        updated_chart = plotter.create_realtime_plot()
        if updated_chart:
            chart_placeholder.altair_chart(updated_chart, use_container_width=True)
        
        # Obtener datos para métricas y alertas
        data = plotter.data_simulator.get_latest_data(100)
        if data and len(data) >= 1:
            # Actualizar métrica con validación robusta
            latest = data[-1]
            prev = data[-2] if len(data) > 1 else latest
            
            if isinstance(latest, (int, float)) and isinstance(prev, (int, float)):
                delta = safe_delta(latest, prev)
                metric_placeholder.metric(
                    "Nivel Actual", 
                    f"{latest:.2f} mg/L", 
                    delta=f"{delta:.2f}" if delta is not None else None
                )
            
            # Manejar alertas
            if latest < 4.0:
                alert_placeholder.error("⚠️ Nivel CRÍTICO de oxígeno!")
                if last_alert_type != "CRITICAL":
                    # Enviar correo solo si la alerta crítica es nueva
                    email_notifier.notify(
                        message=f"Nivel crítico detectado: {latest:.2f} mg/L",
                        alert_type="CRITICAL"
                    )
                    last_alert_type = "CRITICAL"  # Actualizar el estado de la última alerta
                    
                    
            if latest > 7.0:
                alert_placeholder.error("⚠️ Nivel CRÍTICO de oxígeno!")
                if last_alert_type != "CRITICAL":
                    # Enviar correo solo si la alerta crítica es nueva
                    email_notifier.notify(
                        message=f"Nivel crítico detectado: {latest:.2f} mg/L",
                        alert_type="CRITICAL"
                    )
                    last_alert_type = "CRITICAL"  # Actualizar el estado de la última alerta
            elif latest < 5.0:
                alert_placeholder.warning("⚠️ Nivel BAJO de oxígeno")
                last_alert_type = "WARNING"  # Actualizar el estado de la última alerta
            else:
                alert_placeholder.success("✅ Niveles normales")
                last_alert_type = None  # Reiniciar el estado de la última alerta
        
        # Pausa para permitir que Streamlit actualice la interfaz
        time.sleep(1)