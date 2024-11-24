import commodities as c
import limpieza as l
import datos_mex as mx
import datos_esp as esp
import Union as u


#--------------------FUNCIONES INTEGRADORAS----------------------------------------------------------------------------
"""ESTEBAN"""

def commodities(df):
    """
    Función principal para procesar un DataFrame de datos de commodities.
    Realiza los siguientes pasos:
    1. Renombrar columnas para estandarizar nombres (sin espacios, acentos y en minúsculas).
    2. Estandarizar el formato de la columna de fecha.
    3. Convertir columnas numéricas a tipo float (exceptuando la columna de fecha).
    4. Completar columnas con valores faltantes usando interpolación.
    5. Limpiar el DataFrame, eliminando valores nulos o no deseados.

    Parámetros:
        df (DataFrame): DataFrame de datos de commodities con columna 'date'.

    Retorna:
        DataFrame: DataFrame procesado, limpio y listo para análisis.
    """

    # Renombrar columnas para estandarización
    df = l.renombrar_columnas(df) 
    
    # Estandarizar el formato de la fecha
    df = l.estandarizar_fechas(df) 
    
    # Convertir columnas numéricas a tipo float (exceptuando la columna de fecha)
    df = l.convertir_columnas_a_float(df, df.columns[1:].tolist()) 
    
    # Completar columnas con interpolación para valores faltantes
    df = c.completar_columnas_interpolacion(df)
    
    # Limpiar el DataFrame y eliminar valores nulos o no deseados
    df = l.limpiar_dataframe(df)

    # Construcción de Columnas de Indices de Precios de Commodities en Dataframe

    df =c.indices_precios_comm(df)
    
    return df


#LIMPIEZA Y ESTANDARIZACION DATAFRAME DATOS MEXICO
def mex_incp(df_incp):
    import pandas as pd
    """
    # RESUMEN DE LAS ACCIONES QUE SE VAN A REALIZAR EN ESTE PROCESO:
    1. **Renombrar Columnas**:
        - La función `renombrar_columnas` eliminará los espacios y convertirá a minúsculas los nombres de las columnas del DataFrame.
    2. **Renombrar Columnas Específicas (INCP)**:
        - Luego, la función `renombrar_columnas_incp` cambiará los nombres de las columnas a los nombres especificados en la función.
    3. **Convertir Columnas a Tipo Float**:
        - La función `convertir_columnas_a_float` convertirá los valores de las columnas (exceptuando la primera columna 'date') a tipo `float`.
    4. **Estandarizar Fechas**:
        - La función `estandarizar_fechas` aplicará una limpieza en la columna 'date', asegurando que todas las fechas estén en el mismo formato.
    5. **Limpiar CSV**:
        - Finalmente, la función `limpiar_csv` limpiará el DataFrame eliminando valores no deseados, como 'N/E', y convirtiendo las columnas a un formato numérico adecuado.
    6. **Resultado Final**:
        - El DataFrame se devolverá con todos los pasos de procesamiento aplicados para asegurar que los datos estén listos para el análisis.
    """
    
    # Paso 1: Renombrar columnas eliminando espacios y mayúsculas
    print("1. Renombrando columnas...")
    df_incp = l.renombrar_columnas(df_incp)

    # Paso 2: Renombrar columnas específicas para INCP
    print("2. Renombrando columnas INCP...")
    df_incp = l.renombrar_columnas_incp(df_incp)

    # Paso 3: Convertir las columnas a tipo float
    print("3. Convertiendo las columnas a float...")
    df_incp = l.convertir_columnas_a_float(df_incp, df_incp.columns[1:].tolist())

    # Paso 4: Estandarizar las fechas
    print("4. Estandarizando las fechas...")
    df_incp = l.estandarizar_fechas(df_incp)

    # Paso 5: Limpiar el CSV
    print("5. Limpiando el CSV...")
    df_incp = l.limpiar_csv(df_incp)

    # Paso final: El DataFrame procesado es devuelto
    print("PROCESAMIENTO COMPLETO DEL INCP.")
    return df_incp


#LIMPIEZA Y ESTANDARIZACION DATAFRAME DATOS ESPAÑA
def esp_ipc(df_ipc):
    import pandas as pd
    """
    # RESUMEN DE LAS ACCIONES QUE SE VAN A REALIZAR EN ESTE PROCESO:
    1. **Renombrar Columnas**:
        - La función `renombrar_columnas` eliminará los espacios y convertirá a minúsculas los nombres de las columnas del DataFrame.
    2. **Renombrar Columnas Específicas (INCP)**:
        - Luego, la función `renombrar_columnas_incp` cambiará los nombres de las columnas a los nombres especificados en la función.
    3. **Convertir Columnas a Tipo Float**:
        - La función `convertir_columnas_a_float` convertirá los valores de las columnas (exceptuando la primera columna 'date') a tipo `float`.
    4. **Estandarizar Fechas**:
        - La función `estandarizar_fechas` aplicará una limpieza en la columna 'date', asegurando que todas las fechas estén en el mismo formato.
    5. **Limpiar CSV**:
        - Finalmente, la función `limpiar_csv` limpiará el DataFrame eliminando valores no deseados, como 'N/E', y convirtiendo las columnas a un formato numérico adecuado.
    6. **Resultado Final**:
        - El DataFrame se devolverá con todos los pasos de procesamiento aplicados para asegurar que los datos estén listos para el análisis.
    """
    
    # Paso 1: Renombrar columnas eliminando espacios y mayúsculas
    print("1. Renombrando columnas...")
    df_ipc = l.renombrar_columnas(df_ipc)

    # Paso 3: Renombrar columnas específicas para IPC
    print("2. Renombrando columnas IPC...")
    df_ipc = l.renombrar_columnas_ipc(df_ipc)

    # Paso 3: Convertir las columnas a tipo float
    print("3. Convertiendo las columnas a float...")
    df_ipc = l.convertir_columnas_a_float(df_ipc, df_ipc.columns[1:].tolist())

    # Paso 4: Estandarizar las fechas
    print("4. Estandarizando las fechas...")
    df_ipc = l.estandarizar_fechas(df_ipc)

    # Paso 5: Limpiar el CSV
    print("5. Limpiando el CSV...")
    df_ipc = l.limpiar_csv(df_ipc)

    # Paso final: El DataFrame procesado es devuelto
    print("PROCESAMIENTO COMPLETO DEL IPC.")
    return df_ipc

#UNION DE DATAFRAMES DE COMMODIETIS. INCP(MEX) Y IPC(ESP)
def unir_esp_mx_comm(df, df_incp, df_ipc):
    """
    Función para unir DataFrames de commodities (df), datos INCP (df_incp) y datos IPC (df_ipc)
    con base en las fechas comunes. 
    Determina los límites de fechas y realiza intersecciones de los DataFrames.

    Parámetros:
        df (DataFrame): DataFrame de precios de commodities.
        df_incp (DataFrame): DataFrame de datos INCP.
        df_ipc (DataFrame): DataFrame de datos IPC.

    Retorna:
        DataFrame: DataFrame resultante con la unión de los tres DataFrames basada en la columna 'date'.
    """
    # Calcular los límites de fechas comunes
    u.fechas_limite(df, df_incp, df_ipc)
    
    # Realizar la primera unión entre df y df_incp
    df_final = u.unir_dataframes(df, df_incp, "date", "inner")
    
    # Realizar la segunda unión entre el DataFrame resultante y df_ipc
    df_final = u.unir_dataframes(df_final, df_ipc, "date", "inner")
    
    return df_final


#----------------------------------------------------SUICIDIOS---------------------------------------------------------------
#SUICIDIOS ESPAÑA


def procesar_sui_es(df_sui_es):
    """
    Función para procesar el DataFrame 'df_sui_es' mediante los pasos de:
    - Estandarización de nombres de columnas.
    - Renombrado de columnas a nombres específicos.
    - Estandarización del formato de fecha.
    - Conversión de columnas a tipo float (excepto 'date').
    - Limpieza de valores en el DataFrame.
    - Conversión de datos anuales a datos mensuales.

    Parámetros:
        df_sui_es (DataFrame): DataFrame con los datos a procesar.

    Retorna:
        DataFrame: DataFrame procesado con datos mensuales.
    """
    # Estandarización de nombres de columnas
    df_sui_es = l.renombrar_columnas(df_sui_es)
    
    # Renombrado de columnas a nombres específicos
    df_sui_es = l.renombrar_columnas_sui_es(df_sui_es)
    
    # Estandarización del formato de fechas
    df_sui_es = l.estandarizar_fechas(df_sui_es)
    
    # Conversión de columnas a tipo float (excepto 'date')
    df_sui_es = l.convertir_columnas_a_float(df_sui_es, df_sui_es.columns[1:].tolist())
    
    # Limpieza del DataFrame
    df_sui_es = l.limpiar_dataframe(df_sui_es)
    
    # Conversión de datos anuales a datos mensuales
    df_sui_es = l.convertir_a_mensual(df_sui_es)
    
    return df_sui_es

#SUICIDIOS MEXICO
def procesar_sui_mx(df_sui_mx):
    """
    Función para procesar el DataFrame 'df_sui_mx' mediante los pasos de:
    - Estandarización de nombres de columnas.
    - Renombrado de columnas a nombres específicos.
    - Eliminación de columnas seleccionadas.
    - Estandarización del formato de fechas.
    - Eliminación de puntos en valores numéricos.
    - Conversión de columnas a tipo float (excepto 'date').
    - Limpieza de valores en el DataFrame.
    - Conversión de datos anuales a datos mensuales.

    Parámetros:
        df_sui_mx (DataFrame): DataFrame con los datos a procesar.

    Retorna:
        DataFrame: DataFrame procesado con datos mensuales.
    """
    # Estandarización de nombres de columnas
    df_sui_mx = l.renombrar_columnas(df_sui_mx)
    
    # Renombrado de columnas a nombres específicos
    df_sui_mx = l.renombrar_columnas_sui_mx(df_sui_mx)
    
    # Eliminación de columnas seleccionadas
    df_sui_mx = l.eliminar_columnas(df_sui_mx, df_sui_mx.columns[4:].tolist())
    
    # Estandarización del formato de fechas
    df_sui_mx = l.estandarizar_fechas(df_sui_mx)
    
    # Eliminación de puntos en valores numéricos
    df_sui_mx = l.eliminar_puntos(df_sui_mx, df_sui_mx.columns[1:].tolist())
    
    # Conversión de columnas a tipo float (excepto 'date')
    df_sui_mx = l.convertir_columnas_a_float(df_sui_mx, df_sui_mx.columns[1:].tolist())
    
    # Limpieza del DataFrame
    df_sui_mx = l.limpiar_dataframe(df_sui_mx)
    
    # Conversión de datos anuales a datos mensuales
    df_sui_mx = l.convertir_a_mensual(df_sui_mx)
    
    return df_sui_mx


#---------------------LLAMADO A CSV DE DATA FRAME FINAL PARA STREAMLIT---------------------------------------------------------------
def llama_datos():
    import pandas as pd
    df_final=pd.read_csv("df_final.csv")
    return df_final