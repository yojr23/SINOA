import os
import pandas as pd
import shutil

# Declaración de las carpetas a usar
INPUT_FOLDER = 'data/pruebas_anteriores'  # Carpeta de pruebas anteriores
REVIEWED_FOLDER = 'data/pruebas_anteriores_revisados'  # Carpeta de pruebas anteriores revisados
REJECTED_FOLDER = 'data/pruebas_rechazadas'  # Carpeta de pruebas rechazadas
CONSOLIDATED_FOLDER = 'data/pruebas_consolidadas'  # Carpeta de pruebas consolidadas (declarada, tú defines el path)
CONSOLIDATED_FILE = 'data/registro_historico/consolidated_data.csv'  # Archivo consolidado
LOG_FILE = 'data/logs/operations.log'  # Archivo de registro de actividades

# Asegurar que las carpetas existen
os.makedirs(INPUT_FOLDER, exist_ok=True)
os.makedirs(REVIEWED_FOLDER, exist_ok=True)
os.makedirs(REJECTED_FOLDER, exist_ok=True)
os.makedirs(CONSOLIDATED_FOLDER, exist_ok=True)
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)



def load_and_clean_excel(file_path):
    """
    Limpia y valida los datos de un archivo Excel.
    """
    try:
        df = pd.read_excel(file_path, sheet_name=0, header=None)
        # Validar que la columna de datos exista (por ejemplo, columna 2)
        if df.shape[1] < 3 or df.iloc[12, 2] != "OD [mg/L]":
            raise ValueError("Formato inválido: no se encontró la columna 'OD [mg/L]'.")
        
        # Extraer y limpiar los datos
        data = df.iloc[13:, 2].dropna().reset_index(drop=True)
        data = data.apply(pd.to_numeric, errors='coerce').dropna()
        return data.tolist()
    except Exception as e:
        print(f"Error al procesar el archivo {file_path}: {e}")
        raise ValueError(f"Archivo inválido: {file_path}")

def verificar_pruebas_anteriores():
    """
    Verifica si hay archivos en la carpeta de pruebas anteriores.
    """
    if not os.listdir(INPUT_FOLDER):
        print("No hay archivos en la carpeta de pruebas anteriores.")
        return False
    return True

def limpiar_y_mover_archivos():
    """
    Limpia los datos de los archivos en la carpeta de pruebas anteriores y los mueve a la carpeta revisados.
    """
    for file_name in os.listdir(INPUT_FOLDER):
        file_path = os.path.join(INPUT_FOLDER, file_name)
        if file_name.endswith('.xls') or file_name.endswith('.xlsx'):
            try:
                # Limpia los datos (aunque no se usen aquí, se valida el archivo)
                load_and_clean_excel(file_path)
                shutil.move(file_path, os.path.join(REVIEWED_FOLDER, file_name))
                print(f"Archivo procesado y movido a revisados: {file_name}")
            except ValueError:
                shutil.move(file_path, os.path.join(REJECTED_FOLDER, file_name))
                print(f"Archivo rechazado: {file_name}")

def consolidar_datos_revisados():
    """
    Consolida los datos de la carpeta revisados en el archivo consolidado.
    Si el archivo consolidado no existe, lo crea.
    """
    if not CONSOLIDATED_FOLDER:
        raise ValueError("La variable CONSOLIDATED_FOLDER no está definida. Por favor, asigna un path válido.")

    consolidated_data = []
    rejected_count = 0

    # Crear el archivo consolidado si no existe
    if not os.path.exists(CONSOLIDATED_FILE):
        print(f"El archivo consolidado no existe. Creando {CONSOLIDATED_FILE}...")
        os.makedirs(os.path.dirname(CONSOLIDATED_FILE), exist_ok=True)
        pd.DataFrame(columns=['Nivel de Oxígeno']).to_csv(CONSOLIDATED_FILE, index=False)

    for file_name in os.listdir(REVIEWED_FOLDER):
        file_path = os.path.join(REVIEWED_FOLDER, file_name)
        if file_name.endswith('.xls') or file_name.endswith('.xlsx'):
            try:
                # Limpia los datos y los agrega directamente a consolidated_data
                consolidated_data.extend(load_and_clean_excel(file_path))
                shutil.move(file_path, os.path.join(CONSOLIDATED_FOLDER, file_name))  # Mover a consolidados
                print(f"Archivo consolidado y movido a consolidados: {file_name}")
            except ValueError:
                shutil.move(file_path, os.path.join(REJECTED_FOLDER, file_name))
                rejected_count += 1
                print(f"Archivo rechazado durante la consolidación: {file_name}")

    # Anexar los datos consolidados al archivo existente
    if consolidated_data:
        df_existing = pd.read_csv(CONSOLIDATED_FILE)
        df_new = pd.DataFrame(consolidated_data, columns=['Nivel de Oxígeno'])
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        df_combined.to_csv(CONSOLIDATED_FILE, index=False)
        print(f"Datos consolidados correctamente en {CONSOLIDATED_FILE}.")
    else:
        print("No se encontraron datos válidos para consolidar.")

    return rejected_count

def manejar_archivos_rechazados():
    """
    Cuenta los archivos rechazados y los registra en el log.
    """
    archivos_rechazados = os.listdir(REJECTED_FOLDER)
    with open(LOG_FILE, "a") as log:
        log.write(f"Archivos rechazados: {len(archivos_rechazados)}\n")
    return len(archivos_rechazados)

def registrar_actividad(mensaje):
    """
    Registra una actividad en el archivo de log.
    """
    with open(LOG_FILE, "a") as log:
        log.write(f"{mensaje}\n")
        