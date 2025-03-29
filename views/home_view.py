import streamlit as st

def home_view():
    st.title("Sistema de Alertas de Oxígeno")
    st.subheader("Monitoreo en tiempo real")
    st.write("🔴 Implementación en desarrollo... (Próximamente)")
    
    st.subheader("Últimas alertas generadas")
    st.text_area("", value="No hay alertas aún.", height=150, key="alerts")

if __name__ == "__main__":
    home_view()
