import polars as pl
import os
import importlib
import Limpieza_tipo,ManejoFechaData,Mapeo_Nivelacion_df

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
dfs_green = []

green_files = [
    f'{year_value}_{month_one}_Green.parquet',
    f'{year_value}_{month_two}_Green.parquet',
    f'{year_value}_{month_three}_Green.parquet'
]
# Procesar archivos Green
for file_name in green_files:
    file_path = os.path.join(folder_path, file_name)
    try:
        # Cargar el archivo Parquet
        df = pl.read_parquet(file_path)
        df = limpieza_tipo(df)
        df = limpiar_nombres_columnas(df)
        print(f"Archivo {file_name} cargado exitosamente.")
        dfs_green.append(df)
    except Exception as e:
        print(f"Error procesando {file_name}: {e}")
        
# Aplicar la función a la lista de DataFrames 'dfs_yellow'
dfs_green_corregidos = encontrar_columnas_similares(dfs_green)

# Obtener columnas comunes después de la corrección
dfs_green_alineados = alinear_columnas(dfs_green_corregidos)

# Concatenar los DataFrames alineados
final_df_green = pl.concat(dfs_green_alineados)
    
final_df_green.write_parquet(f'data_temporal_green/{year}_particion' + f'_green_{trim}.parquet')