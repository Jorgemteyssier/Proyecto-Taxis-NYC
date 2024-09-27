from thefuzz import fuzz
from thefuzz import process

def encontrar_columnas_similares(dfs, umbral_similitud=90):
    # Obtener todas las columnas únicas de todos los DataFrames
    todas_las_columnas = set()
    for df in dfs:
        todas_las_columnas.update(df.columns)

    # Crear un diccionario para mapear las columnas similares
    mapa_columnas = {}
    columnas_normalizadas = set()
    
    for columna in todas_las_columnas:
        # Encontrar la mejor coincidencia de cada columna en el conjunto de columnas normalizadas
        mejor_coincidencia = process.extractOne(columna, columnas_normalizadas, scorer=fuzz.ratio)
        if mejor_coincidencia and mejor_coincidencia[1] >= umbral_similitud:
            # Si la coincidencia es buena, mapea la columna al nombre común
            mapa_columnas[columna] = mejor_coincidencia[0]
        else:
            # Si no hay una buena coincidencia, agregar la columna al conjunto de columnas normalizadas
            columnas_normalizadas.add(columna)
            mapa_columnas[columna] = columna
    
    # Renombrar las columnas de cada DataFrame
    dfs_corregidos = []
    for df in dfs:
        df_corregido = df.rename(mapa_columnas)
        dfs_corregidos.append(df_corregido)
    
    return dfs_corregidos


# Función para alinear columnas (basada en las comunes)
def alinear_columnas(dfs):
    # Obtener las columnas comunes a todos los DataFrames
    columnas_comunes = set(dfs[0].columns)
    for df in dfs[1:]:
        columnas_comunes.intersection_update(df.columns)
    
    # Mantener sólo las columnas comunes en cada DataFrame
    dfs_alineados = [df.select(columnas_comunes) for df in dfs]
    
    return dfs_alineados

# Aplicar la función a la lista de DataFrames 'dfs_yellow'
#dfs_yellow_corregidos = encontrar_columnas_similares(dfs_yellow)

# Obtener columnas comunes después de la corrección
#dfs_yellow_alineados = alinear_columnas(dfs_yellow_corregidos)

# Concatenar los DataFrames alineados
#final_df_yellow = pl.concat(dfs_yellow_alineados)
