import polars as pl


num_mes_uno = 7
num_mes_two = 8
num_mes_three = 9

def concatenacion(df_uno, df_dos, df_tres, df_cuatro, columna):
    # Inicializar listas para cada mes
    enero = []
    febrero = []
    marzo = []
    
    # Verificar y agregar registros del mes num_mes_uno a la lista de enero
    if len(df_uno.filter(pl.col(columna).dt.month() == num_mes_uno)) > 0:
        enero.append(df_uno.filter(pl.col(columna).dt.month() == num_mes_uno))
    if len(df_dos.filter(pl.col(columna).dt.month() == num_mes_uno)) > 0:
        enero.append(df_dos.filter(pl.col(columna).dt.month() == num_mes_uno))
    if len(df_tres.filter(pl.col(columna).dt.month() == num_mes_uno)) > 0:
        enero.append(df_tres.filter(pl.col(columna).dt.month() == num_mes_uno))
    if len(df_cuatro.filter(pl.col(columna).dt.month() == num_mes_uno)) > 0:
        enero.append(df_cuatro.filter(pl.col(columna).dt.month() == num_mes_uno))
    
    # Verificar y agregar registros del mes num_mes_two a la lista de febrero
    if len(df_uno.filter(pl.col(columna).dt.month() == num_mes_two)) > 0:
        febrero.append(df_uno.filter(pl.col(columna).dt.month() == num_mes_two))
    if len(df_dos.filter(pl.col(columna).dt.month() == num_mes_two)) > 0:
        febrero.append(df_dos.filter(pl.col(columna).dt.month() == num_mes_two))
    if len(df_tres.filter(pl.col(columna).dt.month() == num_mes_two)) > 0:
        febrero.append(df_tres.filter(pl.col(columna).dt.month() == num_mes_two))
    if len(df_cuatro.filter(pl.col(columna).dt.month() == num_mes_two)) > 0:
        febrero.append(df_cuatro.filter(pl.col(columna).dt.month() == num_mes_two))
    
    # Verificar y agregar registros del mes num_mes_three a la lista de marzo
    if len(df_uno.filter(pl.col(columna).dt.month() == num_mes_three)) > 0:
        marzo.append(df_uno.filter(pl.col(columna).dt.month() == num_mes_three))
    if len(df_dos.filter(pl.col(columna).dt.month() == num_mes_three)) > 0:
        marzo.append(df_dos.filter(pl.col(columna).dt.month() == num_mes_three))
    if len(df_tres.filter(pl.col(columna).dt.month() == num_mes_three)) > 0:
        marzo.append(df_tres.filter(pl.col(columna).dt.month() == num_mes_three))
    if len(df_cuatro.filter(pl.col(columna).dt.month() == num_mes_three)) > 0:
        marzo.append(df_cuatro.filter(pl.col(columna).dt.month() == num_mes_three))
    
    # Concatenar DataFrames de cada mes si las listas no están vacías
    df_enero = pl.concat(enero) if enero else None
    df_febrero = pl.concat(febrero) if febrero else None
    df_marzo = pl.concat(marzo) if marzo else None
    
    return df_enero, df_febrero, df_marzo