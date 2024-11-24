#-----------------RECOPILACIÓN DE PRECIOS DE COMMODITIES Y CREACIÓN DE DATAFRAME--------------------------

def comm_price_df(): #commodities price funcition
    """  ESTEBAN
    Por medio del uso de yfinance, esta función obtiene los precios históricos
    de diversas materias primas (commodities) como oro, plata, petróleo y gas natural.
    Devuelve un DataFrame consolidado con los precios mensuales para su análisis posterior.
    """
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
        
        # Se recupera el precio de cierre para cada año
        datos[activo] = historial[['Close']] #con close se toman los valores del precio de cierre

    # Crear un DataFrame consolidado
    df = pd.DataFrame({activo: datos[activo]['Close'] for activo in activos})
    
    # Alinear el DataFrame por la fecha, para que todos los activos tengan la misma columna 'Date'
    df = df.reset_index()
    df = df.sort_index()  # Asegura que las fechas están ordenadas
    
    return df 



def completar_columnas_interpolacion(df):
    """
    Rellena las fechas faltantes en la columna 'date' y 
    realiza la interpolación de los valores faltantes en las demás columnas.
    
    Parámetros:
    df (DataFrame): El dataframe con una columna 'date'
    
    Retorna:
    DataFrame: El dataframe con las fechas completadas y los valores interpolados.
    """
    import pandas as pd
    # Asegúrate de que la columna 'date' sea de tipo datetime
    df['date'] = pd.to_datetime(df['date'])
    
    # Crear un rango de fechas completo (mensual) desde la fecha mínima hasta la máxima
    fechas_completas = pd.date_range(start=df['date'].min(), end=df['date'].max(), freq='MS')
    
    # Reindexar el dataframe con el rango completo de fechas
    df_completo = df.set_index('date').reindex(fechas_completas).reset_index()
    
    # Renombrar la columna 'index' a 'date'
    df_completo = df_completo.rename(columns={'index': 'date'})
    
    # Interpolar los valores faltantes en las otras columnas
    df_completo = df_completo.interpolate(method='linear')
    
    return df_completo


#--------------CONSTRUCCIÓN DE COLUMNAS DE ÍNDICES DE PRECIO DE COMMODITIES EN DATAFRAME--------------------------

def indices_precios_comm(df):
    """ESTEBAN
    Genera las columnas en el dataframe de los índices de precios por commodity
    """
    for material in df.columns[1:]: #Iterar en los nombres de las columnas, a partir de la segunda.
        df[f"indice_{material}"]=(df[f"{material}"]/df[f"{material}"].iloc[201])*100 #se toma como base junio 2020, considerando años base de ICP e INCP
    return df
