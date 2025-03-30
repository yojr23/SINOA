import os
import pandas as pd

def load_and_clean_excel(file_path):
    """
    Carga un archivo Excel, limpia los datos y devuelve la secuencia válida.
    """
    file_extension = os.path.splitext(file_path)[-1].lower()
    engine = 'xlrd' if file_extension == '.xls' else 'openpyxl'
    
    try:
        df = pd.read_excel(file_path, sheet_name=0, header=None, engine=engine)
        
        if df.iloc[12, 2] != "OD [mg/L]":
            raise ValueError("Formato inválido: la celda C13 no contiene 'OD [mg/L]'.")
        
        column_data = df.iloc[13:, 2].dropna().reset_index(drop=True)
        column_data = column_data.apply(pd.to_numeric, errors='coerce').dropna()
        
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
    except Exception as e:
        raise ValueError(f"Error procesando {file_path}: {str(e)}")

def consolidate_data(input_folder, output_file, consolidated_folder, rejected_folder):
    """
    Consolida datos de archivos Excel en un único CSV, moviendo los inválidos a rechazados y los válidos a consolidados.
    """
    consolidated_data = []
    rejected_count = 0
    
    os.makedirs(consolidated_folder, exist_ok=True)
    os.makedirs(rejected_folder, exist_ok=True)
    
    for file_name in os.listdir(input_folder):
        file_path = os.path.join(input_folder, file_name)
        if file_name.endswith('.xls') or file_name.endswith('.xlsx'):
            try:
                cleaned_data = load_and_clean_excel(file_path)
                consolidated_data.extend(cleaned_data)
                os.rename(file_path, os.path.join(consolidated_folder, file_name))
            except ValueError:
                os.rename(file_path, os.path.join(rejected_folder, file_name))
                rejected_count += 1
    
    if consolidated_data:
        pd.DataFrame(consolidated_data, columns=['Nivel de Oxígeno']).to_csv(output_file, index=False)
    
    return rejected_count

def consolidar_o_cargar_historico():
    """
    Consolida nuevos datos si existen, o carga el histórico consolidado.
    """
    carpeta_pruebas = 'sistema_alertas/data/pruebas_anteriores'
    archivo_consolidado = 'sistema_alertas/data/registro_historico/consolidated_data.csv'
    carpeta_rechazados = 'sistema_alertas/data/pruebas_rechazadas'
    carpeta_revisados = 'sistema_alertas/data/pruebas_anteriores_revisados'
    carpeta_consolidados = 'sistema_alertas/data/pruebas_consolidadas'
    
    if not os.listdir(carpeta_pruebas):
        if os.path.exists(archivo_consolidado):
            return pd.read_csv(archivo_consolidado), 0
        else:
            raise FileNotFoundError("No se encontró el archivo consolidado histórico.")
    
    rejected_count = consolidate_data(carpeta_pruebas, archivo_consolidado, carpeta_revisados, carpeta_consolidados, carpeta_rechazados)
    return pd.read_csv(archivo_consolidado), rejected_count
