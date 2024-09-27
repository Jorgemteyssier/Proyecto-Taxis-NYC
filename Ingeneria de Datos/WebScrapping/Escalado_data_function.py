import polars as pl
import numpy as np

def ajustar_rangos(df, columna_distancia, lim_superior, lim_inferior, step, columna_fecha):
    """
    df: DataFrame de Polars
    columna_distancia: Nombre de la columna de distancia a filtrar
    lim_superior: Valor superior del rango de distancia
    lim_inferior: Valor inferior del rango de distancia
    step: Tamaño del paso para la distancia
    columna_fecha: Nombre de la columna de fecha para agrupar por días
    """
    total_filas = df.shape[0]  # Número total de filas en el DataFrame
    resultado = []  # Lista para almacenar las filas filtradas y ajustadas
    
    # Extraer solo la fecha de tpep_pickup_datetime (sin hora)
    df = df.with_columns(pl.col(columna_fecha).dt.date().alias('grupo_fecha'))

    # Iterar sobre cada grupo de fechas
    for fecha_grupo, df_grupo in df.group_by('grupo_fecha'):  # Cambiar a group_by
        # Iterar sobre los límites del rango de distancia
        for limite in np.arange(lim_superior, lim_inferior, -step):
            rango_superior = limite
            rango_inferior = limite - step
            
            # Filtrar el DataFrame del grupo de fecha por el rango de distancia
            df_rango = df_grupo.filter(
                (pl.col(columna_distancia) > rango_inferior) & (pl.col(columna_distancia) <= rango_superior)
            )
            
            # Calcular la cantidad a mantener en este rango de distancia y grupo de fecha
            cantidad = int(df_rango.shape[0] / total_filas * 100 * 1000)
            
            # Si hay más filas de las necesarias, se reducen a la cantidad especificada
            if df_rango.shape[0] > cantidad:
                df_rango = df_rango.head(cantidad)  # O usa .sample(n=cantidad) para aleatoriedad
            
            # Agregar el DataFrame ajustado a la lista de resultados
            resultado.append(df_rango)

    # Concatenar todos los DataFrames ajustados en uno solo
    df_final = pl.concat(resultado)
    
    return df_final

# Ejemplo de uso:
# df_ajustado = ajustar_rangos_estratificado(df_yellow_parquet_1000, 'trip_distance', 6.25, -0.75, 1, 'tpep_pickup_datetime')


