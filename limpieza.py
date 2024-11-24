# Función para corregir mayúsculas y espacios en nombres de columnas
def renombrar_columnas(df):
    df = df.rename(columns={df.columns[n]: df.columns[n].strip().replace(" ", "_").lower() for n in range(len(df.columns))})
    return df


#Función para cambiar nombre en df_incp
def renombrar_columnas_incp(df_incp):
    nombres_inciales=df_incp.columns
    nombres_finales=["date","indice_general_mx","alimentos_bebidas_mx","vivienda_mx","educacion_mx","transporte_mx"]
    nombres={inicial:final for inicial,final in zip(nombres_inciales,nombres_finales)}
    df_incp=df_incp.rename(columns=nombres)
    return df_incp

#Función para cambiar nombre en df_ipc
def renombrar_columnas_ipc(df_ipc):
    nombres_inciales=df_ipc.columns
    nombres_finales=["date","indice_general_es","alimentos_bebidas_es","vivienda_es","educacion_es","transporte_es"]
    nombres={inicial:final for inicial,final in zip(nombres_inciales,nombres_finales)}
    df_ipc=df_ipc.rename(columns=nombres)
    return df_ipc

#Función para aplicar 'limpiar_fecha' a la columna 'date' de un DataFrame"""
def estandarizar_fechas(df):
    """Función para aplicar 'limpiar_fecha' a la columna 'date' de un DataFrame"""
    import pandas as pd
    df['date'] = df['date'].apply(limpiar_fecha) #Aplica la función limpiar fecha y lo guarda en df.
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    return df

#Función para convertir datos de columnas object a float
def convertir_columnas_a_float(df, columnas):
    import pandas as pd
    # Iterar sobre la lista de columnas que se desean convertir
    for col in columnas:
        # Verificar que la columna existe en el DataFrame
        if col in columnas:
            # Intentar convertir los valores de la columna a float
            df[col] = pd.to_numeric(df[col], errors='coerce')  # 'coerce' convierte a NaN los valores no numéricos
            # Redondear los valores a 2 decimales
            df[col] = df[col].round(2)
        else:
            print(f"La columna '{col}' no existe en el DataFrame.")
    
    # Regresar el DataFrame modificado
    return df

#Función para eliminar columnas no necesarias en un dataframe
def eliminar_columnas(df, columnas_a_borrar):
    import pandas as pd
    """
    Elimina las columnas indicadas de un dataframe.

    Argumentos:
    df : pandas.DataFrame
        El dataframe del cual se eliminarán las columnas.
    columnas_a_borrar : list
        Lista de nombres de las columnas a eliminar.

    Retorna:
    pandas.DataFrame
        El dataframe modificado sin las columnas eliminadas.
    """
    # Elimina las columnas especificadas en 'columnas_a_borrar'
    df_modificado = df.drop(columns=columnas_a_borrar, errors='ignore')
    return df_modificado

#Eliminación de puntos
def eliminar_puntos(df, columnas):
    import pandas as pd
    """
    Elimina los puntos (".") dentro de los valores de las columnas especificadas del DataFrame.
    
    Args:
    df (pd.DataFrame): El DataFrame que contiene las columnas a modificar.
    columnas (list): Lista de nombres de columnas a las que se les eliminarán los puntos.

    Returns:
    pd.DataFrame: El DataFrame modificado.
    """
    for columna in columnas:
        if columna in df.columns:
            # Aplica la eliminación de los puntos en cada valor de la columna
            df[columna] = df[columna].astype(str).str.replace('.', '', regex=False)
    return df

#Limpieza dataframes
def limpiar_dataframe(df):
    """ ESTEBAN
    Función para identificar valores nulos, y eliminar filas sin datos. **Importante: Esta función elimina filas
    si encuentra un valor nulo, pero pregunta al usuario si desea reemplazar nulos por la media o un texto de desconocido.
    """
    # Guardar el número de filas antes de la limpieza
    filas_antes = df.shape[0]
    
    # Imprimir información sobre los valores nulos antes de la limpieza
    print("Reporte de valores nulos antes de la limpieza:")
    print(df.isna().sum())  # Mostrar la cantidad de valores nulos por columna
    print("\n")
    
    # Eliminar filas con valores nulos
    df_limpio = df.dropna(axis=0, how='any')  # Elimina filas con al menos un NaN
    
    # Guardar el número de filas después de la limpieza
    filas_despues = df_limpio.shape[0]
    
    # Imprimir el reporte de lo que se hizo
    print(f"\nSe eliminaron las filas con al menos un valor nulo.")
    print(f"Cantidad de datos antes de la limpieza: {filas_antes} filas.")
    print(f"Cantidad de datos después de la limpieza: {filas_despues} filas.")
    print(f"Se eliminaron {filas_antes - filas_despues} filas con valores nulos.")
    
    # Devolver el DataFrame limpio
    return df_limpio

#Función de limpieza de fecha para homogenizar formato
def limpiar_fecha(fecha):
    """Función para estandarizar fechas usando regex"""
    import pandas as pd
    import re
    # Diccionario de meses en diferentes idiomas
    meses = {
        'ene': '01', 'jan': '01', 'enero': '01', 'january': '01',
        'feb': '02', 'february': '02', 'febrero': '02',
        'mar': '03', 'march': '03', 'marzo': '03',
        'abr': '04', 'apr': '04', 'abril': '04', 'april': '04',
        'may': '05', 'mayo': '05',
        'jun': '06', 'june': '06', 'junio': '06',
        'jul': '07', 'july': '07', 'julio': '07',
        'ago': '08', 'aug': '08', 'agosto': '08', 'august': '08',
        'sep': '09', 'september': '09', 'septiembre': '09',
        'oct': '10', 'october': '10', 'octubre': '10',
        'nov': '11', 'november': '11', 'noviembre': '11',
        'dic': '12', 'dec': '12', 'december': '12', 'diciembre': '12'
    }
    
    # Convertir a string si no lo es
    fecha = str(fecha).lower().strip()
    
    # Remover hora si existe
    fecha = re.sub(r'\s+\d{1,2}:\d{2}:\d{2}.*$', '', fecha)
    
    # Patrón para formato compacto YYYYMMDD
    if re.match(r'^\d{8}$', fecha):
        return f"{fecha[:4]}-{fecha[4:6]}-{fecha[6:]}"
    
    # Reemplazar varios separadores por '-'
    fecha = re.sub(r'[./\s]', '-', fecha)
    
    # Extraer componentes usando diferentes patrones
    patrones = [
        # YYYY-MM-DD
        r'^(\d{4})-(\d{1,2})-(\d{1,2})$',
        # DD-MM-YYYY
        r'^(\d{1,2})-(\d{1,2})-(\d{4})$',
        # DD-MMM-YYYY
        r'^(\d{1,2})-([a-z]{3,})-?(\d{4})$',
        # MM-DD-YY
        r'^(\d{1,2})-(\d{1,2})-(\d{2})$'
    ]
    
    for patron in patrones:
        match = re.match(patron, fecha)
        if match:
            grupos = match.groups()
            
            # Caso YYYY-MM-DD
            if len(grupos[0]) == 4:
                año = grupos[0]
                mes = grupos[1].zfill(2)
                dia = grupos[2].zfill(2)
            # Caso DD-MM-YYYY
            elif len(grupos[2]) == 4:
                año = grupos[2]
                # Verificar si el segundo grupo es un mes en texto
                if grupos[1].isalpha():
                    mes = meses.get(grupos[1][:3], '01')  # Buscar mes por nombre abreviado
                else:
                    mes = grupos[1].zfill(2)
                dia = grupos[0].zfill(2)
            # Caso MM-DD-YY
            else:
                año = f"20{grupos[2]}" if int(grupos[2]) < 50 else f"19{grupos[2]}"
                mes = grupos[0].zfill(2)
                dia = grupos[1].zfill(2)
            
            return f"{año}-{mes}-{dia}"

    # Si no coincide con ningún patrón, retornar valor original
    return fecha

#Limpieza de archivos -csv
def limpiar_csv(df):
    """
    Limpia el DataFrame eliminando filas con valores N/E o NaN, 
    y convierte las columnas a tipo float, excepto la columna 'date'.   
    Retorna:
    - df: DataFrame limpio.
    """
    import pandas as pd
    import numpy as np
    #Guarda en una varibale la cantidad incial total de datos
    antes=len(df)
    # Reemplazar 'N/E' por NaN para facilitar la limpieza
    df.loc[:, :] = df.replace('N/E', np.nan)

    # Verificar cuántos valores NaN existen en el DataFrame
    nulos_totales = df.isna().sum().sum()
    print(f"Total de valores NaN antes de la limpieza: {nulos_totales}")
    
    #Eliminar las filas con al menos un valor NaN
    df = df.dropna()
    print(f"Total de valores NaN después de eliminar filas: {df.isna().sum().sum()}")

    # Convertir las columnas a tipo float (excepto 'date')
    for col in df.columns:
        if col != 'date':  # No convertir la columna 'date'
            df.loc[:, col] = pd.to_numeric(df[col], errors='coerce')
    
    #Imprimir el reporte de la limpieza
    print(f"\nCantidad de datos antes de la limpieza: {antes} filas")
    print(f"Cantidad de datos después de la limpieza: {len(df)} filas")
    
    return df


#DISTRIBUCION DE DATOS A FORMA MENSUAL
def convertir_a_mensual(df):
    """ESTEBAN
    Esta función considera el total anual de datos, y lo reparte en partes iguales a los 12 meses del año.
    """
    import pandas as pd
    # Lista para almacenar las filas que se van a generar
    rows = []
    
    # Recorrer las filas del DataFrame original
    for index, row in df.iterrows():
        # Obtener el valor de la columna 'date' (asumimos que es de tipo datetime)
        year = row['date'].year
        
        # Para cada fila, repartir los valores entre los 12 meses
        for month in range(1, 13):  # de enero (1) a diciembre (12)
            # Crear una nueva fila con la fecha correspondiente (año y mes)
            new_row = row.copy()  # Copiar los valores de la fila original
            new_row['date'] = pd.Timestamp(f'{year}-{month:02d}-01')  # Actualizar la fecha al primer día del mes
            # Repartir los valores de cada columna (excepto 'date') entre los 12 meses
            for col in row.index:
                if col != 'date':  # No modificar la columna 'date'
                    new_row[col] = row[col] / 12
            # Añadir la nueva fila a la lista de filas
            rows.append(new_row)
    
    # Crear un nuevo DataFrame a partir de las filas generadas
    df_mensual = pd.DataFrame(rows)
    
    return df_mensual

#Función para cambiar nombre en df_sui_es
def renombrar_columnas_sui_es(df):
    nombres_inciales=df.columns
    nombres_finales=["date","sui_h_es","sui_m_es","sui_es"]
    nombres={inicial:final for inicial,final in zip(nombres_inciales,nombres_finales)}
    df=df.rename(columns=nombres)
    return df

#Función para cambiar nombre en df_sui_mx
def renombrar_columnas_sui_mx(df):
    nombres_inciales=df.columns
    nombres_finales=["date","sui_m_mx","sui_h_mx","sui_mx"]
    nombres={inicial:final for inicial,final in zip(nombres_inciales,nombres_finales)}
    df=df.rename(columns=nombres)
    return df