import streamlit as st
import threading
import time
import matplotlib.pyplot as plt
from views.real_time_plot import RealTimePlot
from data_pipeline.data_ingestion import DataSimulator

# Inicializar módulos
data_ingestion = DataSimulator()
real_time_plot = RealTimePlot(data_ingestion)

def home_view():
    st.title("Sistema de Alertas de Oxígeno")
    st.subheader("Monitoreo en tiempo real")

    # Mostrar el gráfico en Streamlit
    st.subheader("Gráfica en Tiempo Real")
    plot_placeholder = st.empty()

    def update_plot():
        while True:
            fig, ax = plt.subplots()
            real_time_plot.update_plot(None)  # Actualiza los datos de la gráfica
            ax.plot(real_time_plot.x_data, real_time_plot.y_data, marker='o', linestyle='-')
            ax.set_title("Nivel de Oxígeno en Tiempo Real")
            ax.set_xlabel("Tiempo")
            ax.set_ylabel("Nivel de Oxígeno")
            ax.grid(True)
            plot_placeholder.pyplot(fig)
            time.sleep(1)  # Actualiza cada segundo

    # Iniciar la actualización en un hilo separado
    threading.Thread(target=update_plot, daemon=True).start()

    st.subheader("Últimas alertas generadas")
    st.text_area("", value="No hay alertas aún.", height=150, key="alerts")

if __name__ == "__main__":
    home_view()
