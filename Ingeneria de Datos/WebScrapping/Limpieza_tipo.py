import polars as pl

def limpieza_tipo(df, num_filas=500):
    # Eliminar la columna 'store_and_fwd_flag' si existe
    if 'store_and_fwd_flag' in df.columns:
        df = df.drop('store_and_fwd_flag')

    # Procesar solo los primeros `num_filas` registros de cada columna
    df_sample = df.head(num_filas)
    
    # Lista de columnas a eliminar
    columnas_a_eliminar = []

    # Revisar cada columna para ver qué tipo de valores predomina
    for col in df.columns:
        # No tocar las columnas de fecha y hora
        if col in ['tpep_pickup_datetime', 'tpep_dropoff_datetime','lpep_pickup_datetime','lpep_dropoff_datetime']:
            continue
        
        # Contar los valores no nulos
        num_no_nulos = df_sample[col].drop_nulls().len()
        num_nulos = df_sample[col].len() - num_no_nulos
        
        # Contar valores numéricos y de texto
        num_numericos = df_sample[col].cast(pl.Float64).drop_nulls().len()
        num_strings = df_sample[col].cast(pl.Utf8).drop_nulls().len() - num_numericos
        
        # Si hay más nulos que cualquier otro tipo de dato, eliminar la columna
        if num_nulos > max(num_numericos, num_strings):
            columnas_a_eliminar.append(col)
        else:
            # Si hay más valores numéricos que de texto, mantener solo los numéricos
            if num_numericos > num_strings:
                try:
                    df = df.with_columns([df[col].cast(pl.Float64)])  # Convertir a numérico
                except:
                    columnas_a_eliminar.append(col)  # Si falla la conversión, eliminar la columna
            # Si hay más valores de texto, mantener solo los de texto
            elif num_strings > num_numericos:
                try:
                    df = df.with_columns([df[col].cast(pl.Utf8)])  # Convertir a string
                except:
                    columnas_a_eliminar.append(col)  # Si falla la conversión, eliminar la columna

    # Eliminar las columnas que no cumplen
    if columnas_a_eliminar:
        df = df.drop(columnas_a_eliminar)

    return df

def limpiar_nombres_columnas(df):
    df.columns = [col.strip().lower() for col in df.columns]
    return df

def escalado(serie):
    # Calcular el primer cuartil (Q1) y el tercer cuartil (Q3)
    q1 = serie.quantile(0.25)
    q3 = serie.quantile(0.75)
    
    # Calcular el rango intercuartílico (IQR)
    iqr = q3 - q1
    
    # Aplicar el factor de 1.5 para calcular los límites
    iqr_1 = q1 - (1.5 * iqr)
    iqr_3 = q3 + (1.5 * iqr)
    
    return iqr_1, iqr_3
