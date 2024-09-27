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
from ManejoFechaData import year, trimestre, ruta, control_mes_uno

# Obtener el año y trimestre 
year_value = year  
trim = trimestre()  
ruta = ruta() 
control_one = control_mes_uno()

# Definir la ruta de la carpeta y el nombre del archivo Parquet
folder_path = 'data_particionada_temporal'
yellow_file = f'{year_value}_particion_yellow1_{control_one}.parquet'
file_path = os.path.join(folder_path, yellow_file)

# Intentar cargar el archivo Parquet
try:
    df_particion_yellow1 = pl.read_parquet(file_path)
    print(f"Archivo {yellow_file} cargado exitosamente.")
except Exception as e:
    print(f"Error procesando {yellow_file}: {e}")


# Filtrar el DataFrame para eliminar registros no válidos
df_particion_yellow1 = df_particion_yellow1.filter(
    (pl.col('passenger_count') > 0.0) & 
    (pl.col('trip_distance') > 0.1)
)


#Normalizacion de los datos
lim_inferior, lim_superior = escalado(df_particion_yellow1["trip_distance"])

df_particion_yellow1 = df_particion_yellow1.filter(
    (df_particion_yellow1['trip_distance'] >= lim_inferior) & 
    (df_particion_yellow1['trip_distance'] <= lim_superior)
)


df_particion_yellow1 = ajustar_rangos(df_particion_yellow1,"trip_distance",lim_superior,lim_inferior,1,'tpep_pickup_datetime')

df_particion_yellow1.write_parquet(f'data_trimestral/df_particion_yellow1_{control_one}.parquet')


"""
# Definir la ruta para guardar el DataFrame temporal
folder_path_dataframes_temporales = 'dataframes_temporales'
nombre_archivo = os.path.join(folder_path_dataframes_temporales, f'{year_value}_particion_yellow1_{trim}.pkl')

# Guardar el DataFrame en un archivo utilizando pickle
with open(nombre_archivo, 'wb') as f:
    pickle.dump(df_particion_yellow1, f)

print(f'DataFrame guardado en: {nombre_archivo}')
"""

