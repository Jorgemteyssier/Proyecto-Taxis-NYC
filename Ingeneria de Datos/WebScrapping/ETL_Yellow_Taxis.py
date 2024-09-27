import polars as pl
import os
import importlib
import Limpieza_tipo, Mapeo_Nivelacion_df,ManejoFechaData

from Limpieza_tipo import limpieza_tipo, limpiar_nombres_columnas

importlib.reload(Limpieza_tipo)


from ManejoFechaData import year, ruta, trimestre, control_mes_uno, control_mes_dos,control_mes_tres

importlib.reload(ManejoFechaData)

from Mapeo_Nivelacion_df import encontrar_columnas_similares, alinear_columnas

importlib.reload(Mapeo_Nivelacion_df)

year_value = year  
ruta = ruta() 
trim = trimestre()  
month_one = control_mes_uno()
month_two = control_mes_dos()
month_three = control_mes_tres()

folder_path = f'D:/visual/data/{year_value}/'

dfs_yellow = []

yellow_files = [
    f'{year_value}_{month_one}_Yellow.parquet', 
    f'{year_value}_{month_two}_Yellow.parquet', 
    f'{year_value}_{month_three}_Yellow.parquet']

# Procesar archivos Yellow
file_name = yellow_files[0]
file_path = os.path.join(folder_path, file_name)
try:
    df = pl.read_parquet(file_path)
    df = limpieza_tipo(df)
    df = limpiar_nombres_columnas(df)
    print(f"Archivo {file_name} cargado exitosamente.")
    dfs_yellow.append(df)
except Exception as e:
    print(f"Error procesando {file_name}: {e}")
    
file_name = yellow_files[1]
file_path = os.path.join(folder_path, file_name)
try:
    df = pl.read_parquet(file_path)
    df = limpieza_tipo(df)
    df = limpiar_nombres_columnas(df)
    print(f"Archivo {file_name} cargado exitosamente.")
    dfs_yellow.append(df)
except Exception as e:
    print(f"Error procesando {file_name}: {e}")

file_name = yellow_files[2]
file_path = os.path.join(folder_path, file_name)
try:
    df = pl.read_parquet(file_path)
    df = limpieza_tipo(df)
    df = limpiar_nombres_columnas(df)
    print(f"Archivo {file_name} cargado exitosamente.")
    dfs_yellow.append(df)
except Exception as e:
    print(f"Error procesando {file_name}: {e}")
    
# Aplicar la función a la lista de DataFrames 'dfs_yellow'
dfs_yellow_corregidos = encontrar_columnas_similares(dfs_yellow)

# Obtener columnas comunes después de la corrección
dfs_yellow_alineados = alinear_columnas(dfs_yellow_corregidos)

# Concatenar los DataFrames alineados
final_df_yellow = pl.concat(dfs_yellow_alineados)



# Crear las particiones

total_filas = len(final_df_yellow)

data_yellow_particionada = len(final_df_yellow) // 4


particion_yellow_1 = final_df_yellow.slice(0, data_yellow_particionada)
particion_yellow_2 = final_df_yellow.slice(data_yellow_particionada, data_yellow_particionada)
particion_yellow_3 = final_df_yellow.slice(2 * data_yellow_particionada, data_yellow_particionada)
particion_yellow_4 = final_df_yellow.slice(3 * data_yellow_particionada, total_filas)

particion_yellow_1.write_parquet(ruta + f'_yellow1_{trim}.parquet')

particion_yellow_2.write_parquet(ruta + f'_yellow2_{trim}.parquet')

particion_yellow_3.write_parquet(ruta + f'_yellow3_{trim}.parquet')

particion_yellow_4.write_parquet(ruta + f'_yellow4_{trim}.parquet')