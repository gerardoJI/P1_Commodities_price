#-----------------IMPORTACIÓN DE LIBERÍAS---------------------------------------------------------------
import pandas as pd

#-----------------RECOPILACIÓN DE PRECIOS DE COMMODITIES Y CREACIÓN DE DATAFRAME--------------------------

#Using yfinance to get commodities price data and create a Dataframe
def comm_price_df(): #commodities price funcition
    import yfinance as yf
    import pandas as pd

    # Símbolos de los futuros de los productos
    activos = {
        "Oro": "GC=F",
        "Plata": "SI=F",
        "Petroleo": "CL=F",
        "Gas Natural": "NG=F"
    }

    # Rango de fechas
    inicio = "1999-01-01"
    fin = "2024-11-01"

    # Diccionario para almacenar los datos
    datos = {}

    # Obtener los datos históricos
    for activo, simbolo in activos.items():
        # Crear el objeto Ticker para cada activo
        ticker = yf.Ticker(simbolo)
        
        # Obtener datos históricos anuales (frecuencia "1y" para anual)
        historial = ticker.history(start=inicio, end=fin, interval="1mo")
        
        # Solo necesitamos el precio de cierre para cada año
        datos[activo] = historial[['Close']] #con close se toman los valores del precio de cierre

    # Crear un DataFrame consolidado
    df = pd.DataFrame({activo: datos[activo]['Close'] for activo in activos})
    
    # Alinear el DataFrame por la fecha, para que todos los activos tengan la misma columna 'Date'
    df = df.reset_index()
    df = df.sort_index()  # Asegura que las fechas están ordenadas
    
    return df 

#-----------------EDICIÓN DE DATOS: ESTANDARIZACIÓN Y LIMPIEZA------------------------------------------------------

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

#Función para cambiar nombre en df_icp
def renombrar_columnas_icp(df_incp):
    nombres_inciales=df_incp.columns
    nombres_finales=["date","indice_general_es","alimentos_bebidas_es","vivienda_es","educacion_es","transporte_es"]
    nombres={inicial:final for inicial,final in zip(nombres_inciales,nombres_finales)}
    df_incp=df_incp.rename(columns=nombres)
    return df_incp

# Crear datos de ejemplo con fechas en diferentes formatos
fechas_ejemplo = pd.DataFrame({
    'fecha': [
        '2023-01-15',          # formato ISO
        '15/01/2023',          # formato europeo
        '01-15-23',            # formato americano abreviado
        '15-ene-2023',         # formato con mes en texto
        '2023.01.15',          # formato con puntos
        '15 enero 2023',       # formato texto español
        '2023/01/15 08:30:00', # formato con hora
        '15-Jan-2023',         # formato inglés
        'Jan 15, 2023',        # formato americano texto
        '20230115'             # formato compacto
    ]
})

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

#Función para aplicar 'limpiar_fecha' a la columna 'date' de un DataFrame"""
def estandarizar_fechas(df):
    df['date'] = df['date'].apply(limpiar_fecha) #Aplica la función limpiar fecha y lo guarda en df.
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    return df

#Función para identificar valores nulos, y eliminar filas sin datos. **Importante: Esta función elimina filas
#si encuentra un valor nulo, pero pregunta al usuario si desea reemplazar nulos por la media o un texto de desconocido.
def limpiar_dataframe(df):
    # Guardar el número de filas antes de la limpieza
    filas_antes = df.shape[0]
    
    # Imprimir información sobre los valores nulos antes de la limpieza
    print("Reporte de valores nulos antes de la limpieza:")
    print(df.isna().sum())  # Mostrar la cantidad de valores nulos por columna
    print("\n")
    
    # Preguntar al usuario si desea rellenar los valores nulos
    respuesta = input("¿Deseas rellenar los valores nulos? (sí/no): ").strip().lower()
    
    if respuesta == 'sí' or respuesta == 'si':
        # Rellenar valores numéricos con la media de la columna
        for col in df.select_dtypes(include=['float64', 'int64']).columns:
            df[col] = df[col].fillna(df[col].mean())  # Asignación explícita
            
        # Rellenar valores de texto con 'Desconocido'
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].fillna('Desconocido')  # Asignación explícita
        
        print("\nLos valores nulos han sido rellenados.")
    else:
        print("\nNo se han rellenado los valores nulos.")
    
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

#Limpieza de archivos -csv
import pandas as pd
import numpy as np

def limpiar_csv(df):
    """
    Limpia el DataFrame eliminando filas con valores N/E o NaN, 
    y convierte las columnas a tipo float, excepto la columna 'date'.   
    Retorna:
    - df: DataFrame limpio.
    """
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




#--------------CONSTRUCCIÓN DE COLUMNAS DE ÍNDICES DE PRECIO DE COMMODITIES EN DATAFRAME--------------------------

#Genera las columnas en el dataframe de los índices de precios por commodity
def indices_precios_comm(df):
    for material in df.columns[1:]: #Iterar en los nombres de las columnas, a partir de la segunda.
        df[f"indice_{material}"]=(df[f"{material}"]/df[f"{material}"].iloc[201])*100 #se toma como base junio 2020, considerando años base de ICP e INCP
    return df


#-------------DEFINICIÓN DE LÍMITES PARA LAS FECHAS DEL ANÁLISIS ---------------------------------------------------

def fechas_limite(df,df_incp,df_ipc):
    
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

#Función para intersectar (how="inner") 2 dataframes, a partir de los datos de la columna date
def unir_dataframes(df1,df2): 
    # Reporte de cantidad de datos antes de la unión
    print(f"Cantidad de filas en el DataFrame 'df1' antes de la unión: {len(df1)}")
    print(f"Cantidad de filas en el DataFrame 'df2' antes de la unión: {len(df2)}")
    
    # Realizamos la unión
    df_final = pd.merge(df1, df2, on="date",how="inner")
    
    # Reporte de cantidad de datos después de la unión
    print(f"Cantidad de filas en el DataFrame resultante después de la unión: {len(df_final)} \n")
    
    return df_final