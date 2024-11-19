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
    inicio = "2000-01-01"
    fin = "2024-01-01"

    # Diccionario para almacenar los datos
    datos = {}

    # Obtener los datos históricos
    for activo, simbolo in activos.items():
        # Crear el objeto Ticker para cada activo
        ticker = yf.Ticker(simbolo)
        
        # Obtener datos históricos anuales (frecuencia "1y" para anual)
        historial = ticker.history(start=inicio, end=fin, interval="1d")
        
        # Solo necesitamos el precio de cierre para cada año
        datos[activo] = historial[['Close']]

    # Crear un DataFrame consolidado
    df = pd.DataFrame({activo: datos[activo]['Close'] for activo in activos})
    
    # Alinear el DataFrame por la fecha, para que todos los activos tengan la misma columna 'Date'
    df = df.sort_index()  # Asegura que las fechas están ordenadas

    # Asegurarse de que los índices (fechas) estén alineados correctamente
    df.index.name = 'Date'
    
    return df 