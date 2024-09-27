import polars as pl
import os

# Directorio donde están los archivos .parquet
data_dir = 'data_trimestral/'

# Lista de archivos en el directorio
files = [f for f in os.listdir(data_dir) if f.endswith('.parquet')]

# Leer y concatenar todos los archivos
df_list = [pl.read_parquet(os.path.join(data_dir, file)) for file in files]
df_concatenated = pl.concat(df_list)

# Guardar el DataFrame concatenado en un archivo parquet
df_concatenated.write_parquet('green_taxis_2014_2023.parquet')

print("Archivos concatenados exitosamente.")