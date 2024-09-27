import polars as pl
import os 
import importlib
import sys

# Añadir la ruta de la carpeta principal
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import Escalado_data_function

from Escalado_data_function import ajustar_rangos

importlib.reload(Escalado_data_function)

# Importar el archivo Limpieza_tipo con múltiples funciones para la limpieza de los archivos en la extracción y para transformar
import Limpieza_tipo

# Importar la función para limpiar los nombres de columnas
from Limpieza_tipo import escalado

# Recargar el módulo Limpieza_tipo
importlib.reload(Limpieza_tipo)

# Importar el archivo ManejoFechaData con múltiples funciones para la modificación de ruta del archivo
import ManejoFechaData
# Recargar el módulo ManejoFechaData
importlib.reload(ManejoFechaData)

# Importar las variables year, trimestre y ruta del módulo ManejoFechaData
from ManejoFechaData import year, trimestre, ruta, control_mes_dos

# Obtener el año y trimestre actual
year_value = year  
trim = trimestre()  
ruta = ruta() 
control_two = control_mes_dos()
# Definir la carpeta donde se encuentran los archivos particionados
folder_path = 'data_particionada_temporal'

# Construir el nombre del archivo parquet de taxis amarillos
yellow_file = f'{year_value}_particion_yellow2_{control_two}.parquet'

# Construir la ruta completa al archivo parquet
file_path = os.path.join(folder_path, yellow_file)

# Intentar cargar el archivo parquet en un DataFrame
try:
    df_particion_yellow2 = pl.read_parquet(file_path)
    print(f"Archivo {yellow_file} cargado exitosamente.")
except Exception as e:
    # Manejo de errores en caso de que no se pueda procesar el archivo
    print(f"Error procesando {yellow_file}: {e}")
    

# Filtrar el DataFrame para eliminar filas con conteo de pasajeros <= 0 o distancia de viaje <= 0.1
df_particion_yellow2 = df_particion_yellow2.filter(
    (pl.col('passenger_count') > 0.0) & 
    (pl.col('trip_distance') > 0.1)
)

#Normalizacion de los datos
lim_inferior, lim_superior = escalado(df_particion_yellow2["trip_distance"])

df_particion_yellow2 = df_particion_yellow2.filter(
    (df_particion_yellow2['trip_distance'] >= lim_inferior) & 
    (df_particion_yellow2['trip_distance'] <= lim_superior)
)


df_particion_yellow2 = ajustar_rangos(df_particion_yellow2,"trip_distance",lim_superior,lim_inferior,1,'tpep_pickup_datetime')

df_particion_yellow2.write_parquet(f'data_trimestral/df_particion_yellow2_{control_two}.parquet')


"""
# Definir la ruta para guardar el DataFrame temporal
folder_path_dataframes_temporales = 'dataframes_temporales'
# Construir el nombre del archivo para guardar el DataFrame
nombre_archivo = os.path.join(folder_path_dataframes_temporales, f'{year_value}_particion_yellow2_{trim}.pkl')

# Guardar el DataFrame en un archivo utilizando pickle
with open(nombre_archivo, 'wb') as f:
    pickle.dump(df_particion_yellow2, f)

# Confirmar que el DataFrame ha sido guardado
print(f'DataFrame guardado en: {nombre_archivo}')

"""