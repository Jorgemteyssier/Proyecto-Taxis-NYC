import polars as pl
import os 
import importlib
import sys

# Añadir la ruta de la carpeta principal
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import Escalado_data_function

from Escalado_data_function import ajustar_rangos

importlib.reload(Escalado_data_function)

# Importar el archivo Limpieza_tipo que contiene múltiples funciones para la limpieza de archivos en la extracción y transformación
import Limpieza_tipo

# Importar la función para limpiar los nombres de columnas
from Limpieza_tipo import escalado

# Recargar el módulo Limpieza_tipo para asegurarse de que se tiene la versión más reciente
importlib.reload(Limpieza_tipo)

# Importar el archivo ManejoFechaData que contiene funciones para la modificación de la ruta del archivo
import ManejoFechaData
# Recargar el módulo ManejoFechaData para asegurarse de que se tiene la versión más reciente
importlib.reload(ManejoFechaData)

# Importar las variables year, trimestre y ruta del módulo ManejoFechaData
from ManejoFechaData import year, trimestre, ruta, control_mes_tres

# Obtener el año y trimestre actual para su uso en la carga y el guardado de datos
year_value = year  
trim = trimestre()  
ruta = ruta() 
control_three = control_mes_tres()
# Definir la carpeta donde se encuentran los archivos parquet particionados
folder_path = 'data_particionada_temporal'

# Construir el nombre del archivo parquet de taxis amarillos para el trimestre actual
yellow_file = f'{year_value}_particion_yellow3_{control_three}.parquet'

# Construir la ruta completa al archivo parquet
file_path = os.path.join(folder_path, yellow_file)

# Intentar cargar el archivo parquet en un DataFrame
try:
    df_particion_yellow3 = pl.read_parquet(file_path)  # Cargar el archivo parquet
    print(f"Archivo {yellow_file} cargado exitosamente.")  # Confirmar que se cargó el archivo
except Exception as e:
    # Manejo de errores en caso de que no se pueda procesar el archivo
    print(f"Error procesando {yellow_file}: {e}")
    

# Filtrar el DataFrame para eliminar filas con conteo de pasajeros <= 0 o distancia de viaje <= 0.1
df_particion_yellow3 = df_particion_yellow3.filter(
    (pl.col('passenger_count') > 0.0) & 
    (pl.col('trip_distance') > 0.1)
)

#Normalizacion de los datos
lim_inferior, lim_superior = escalado(df_particion_yellow3["trip_distance"])

df_particion_yellow3 = df_particion_yellow3.filter(
    (df_particion_yellow3['trip_distance'] >= lim_inferior) & 
    (df_particion_yellow3['trip_distance'] <= lim_superior)
)

df_particion_yellow3 = ajustar_rangos(df_particion_yellow3,"trip_distance",lim_superior,lim_inferior,1,'tpep_pickup_datetime')

df_particion_yellow3.write_parquet(f'data_trimestral/df_particion_yellow3_{control_three}.parquet')



"""
# Definir la ruta para guardar el DataFrame temporal
folder_path_dataframes_temporales = 'dataframes_temporales'
# Construir el nombre del archivo para guardar el DataFrame utilizando pickle
nombre_archivo = os.path.join(folder_path_dataframes_temporales, f'{year_value}_particion_yellow3_{trim}.pkl')

# Guardar el DataFrame en un archivo utilizando pickle
with open(nombre_archivo, 'wb') as f:
    pickle.dump(df_particion_yellow3, f)  # Serializar el DataFrame en formato binario

# Confirmar que el DataFrame ha sido guardado correctamente
print(f'DataFrame guardado en: {nombre_archivo}')
"""