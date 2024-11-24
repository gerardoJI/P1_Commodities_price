#-------------DEFINICIÓN DE LÍMITES PARA LAS FECHAS DEL ANÁLISIS ---------------------------------------------------
#3 data frame#
def fechas_limite(df,df_incp,df_ipc):
    """ ESTEBAN
    Determina las fechas límites comunes (mínima y máxima) entre varios DataFrames,
    basándose en la columna 'date' de cada uno. Estas fechas se utilizan para garantizar
    un rango temporal consistente al analizar o combinar los datos.
    Parámetros:
        df (DataFrame): Primer DataFrame que contiene una columna 'date'.
        df_incp (DataFrame): Segundo DataFrame con una columna 'date'.
        df_ipc (DataFrame): Tercer DataFrame con una columna 'date'.
    Retorna:
        tuple: Una tupla con la fecha mínima común y la fecha máxima común entre los DataFrames.
    """
    
    fechas_mayor=[ #lista con las fechas más recientes de los dataframe
    df["date"].max(),
    df_incp["date"].max(),
    df_incp["date"].max()
    ]

    fechas_menor=[df["date"].min(), #lista con las fechas más antiguas de los dataframe
    df_incp["date"].min(),
    df_ipc["date"].min(),
    ]

    #Selección de los límites de fecha
    mayor=min(fechas_mayor)
    menor=max(fechas_menor)

    print(f"Fecha límite menor:{menor} \n Fecha límite mayor: {mayor}")    
    return 

#--------------------UNIÓN DE DATAFRAMES------------------------------------------------------------------------------


def unir_dataframes(df1,df2,col_name,union): 
    """ESTEBAN
    Realiza la unión (merge) de dos DataFrames en base a una columna común, y reporta
    la cantidad de filas en cada DataFrame antes y después de la unión.
    Parámetros:
        df1 (DataFrame): Primer DataFrame a unir.
        df2 (DataFrame): Segundo DataFrame a unir.
        col_name (str): Nombre de la columna en común para realizar la unión.
        Union (str): Tipo de unión a realizar ('inner', 'outer', 'left', 'right').
    Retorna:
        DataFrame: El DataFrame resultante después de realizar la unión.
    """

    import pandas as pd
    # Reporte de cantidad de datos antes de la unión
    print(f"Cantidad de filas en el DataFrame 'df1' antes de la unión: {len(df1)}")
    print(f"Cantidad de filas en el DataFrame 'df2' antes de la unión: {len(df2)}")
    
    # Realizamos la unión
    df_final = pd.merge(df1, df2, on=col_name,how=union)
    
    # Reporte de cantidad de datos después de la unión
    print(f"Cantidad de filas en el DataFrame resultante después de la unión: {len(df_final)} \n")
    
    return df_final