import streamlit as st
import pandas as pd

# Crear un DataFrame simple
data = {
    'x': [1, 2, 3, 4, 5],
    'y': [10, 20, 15, 25, 30]
}
df = pd.DataFrame(data)

# Crear un gráfico simple
st.line_chart(df.set_index('x'))
