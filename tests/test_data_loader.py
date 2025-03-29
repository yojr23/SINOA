import pandas as pd
import os

def load_and_clean_excel(file_path):
    """
    Carga un archivo Excel, limpia los datos según las reglas dadas y devuelve la secuencia de datos válida.
    """
    # Detectar la extensión del archivo y usar el motor correcto
    file_extension = os.path.splitext(file_path)[-1].lower()
    engine = 'xlrd' if file_extension == '.xls' else 'openpyxl'

    # Leer el archivo Excel con el motor adecuado
    df = pd.read_excel(file_path, sheet_name=0, header=None, engine=engine)
    
    column_data = df.iloc[13:, 2].dropna().reset_index(drop=True)
    
    valid_data = []
    null_count = 0
    for value in column_data:
        if pd.isnull(value):
            null_count += 1
        else:
            null_count = 0
        
        if null_count < 2:
            valid_data.append(value)
        else:
            break
    
    return pd.Series(valid_data).dropna()

# Ruta al archivo
file_path = 'data/pruebas_anteriores/prueba cal - enfri.xls'  # Ajusta la ruta según tu sistema
if os.path.exists(file_path):
    cleaned_data = load_and_clean_excel(file_path)
    print(cleaned_data)
else:
    print(f"Archivo no encontrado en: {file_path}. Reemplaza la ruta con un archivo válido.")
