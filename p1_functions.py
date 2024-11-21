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
        
        # Se recupera el precio de cierre para cada año
        datos[activo] = historial[['Close']] #con close se toman los valores del precio de cierre

    # Crear un DataFrame consolidado
    df = pd.DataFrame({activo: datos[activo]['Close'] for activo in activos})
    
    # Alinear el DataFrame por la fecha, para que todos los activos tengan la misma columna 'Date'
    df = df.reset_index()
    df = df.sort_index()  # Asegura que las fechas están ordenadas
    
    return df 

#-----------------------INTERPOLACIÓN DE DATOS FALTANTES ------------------------------------------------------------

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


#-----------------RECOPILACIÓN DE DATOS DE SUICIDIO CREACIÓN DE DATAFRAME-------------------------------------------

def data_sui_es(): #Función para hacer web scraping en wikipedia y obtener datos de tabla en la wiki
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    import pandas as pd
    # Inicializa una instancia del controlador de Google Chrome
    driver = webdriver.Chrome()
    driver.get('https://es.wikipedia.org/wiki/Suicidio_en_Espa%C3%B1a')

    #Busca y obtiene el primer elemento en la página que tiene la clase wikitable
    table = driver.find_element(By.CLASS_NAME, 'wikitable')
    data = []# Inicializar una lista vacía para almacenar los datos
    
    rows = table.find_elements(By.TAG_NAME, 'tr') #Encontrar todas las filas de la tabla <tr> y guardarlas en rows
    
    # Iterar sobre las filas y extraer las celdas para separar títulos de columna de datos de columnas:
    for row in rows:
        # Encuentra todas las celdas de encabezado dentro de la fila y almacena los datos en header_cells
        header_cells = row.find_elements(By.TAG_NAME, 'th')
        # Encuentra todas las los valores dentro de la fila y almacena los datos en data_cells
        data_cells = row.find_elements(By.TAG_NAME, 'td')
        #---> Hasta aquí, todos los datos son de tipo selenium

        #<tr> es una fila completa
        #<th> es el título de una columna
        #<td> es una celda

        # Extraer y procesar los datos:
        if header_cells: #Si hay celdad de encabezado, extraer y limpiar espacios del texto en la celda, y guardarla en headers
            headers = [cell.text.strip() for cell in header_cells]
        else:
            # Para los datos de celda, generar lista con los valores de la fila, y gardar dentro de la lista data
            row_data = [cell.text.strip() for cell in data_cells]
            data.append(row_data)
    
    # Cierra navegador
    driver.quit()

    # Crea data frame con la lista data, y la lista headers para títulos de columna
    df_sui_es = pd.DataFrame(data, columns=headers)
    return df_sui_es

def data_sui_mx():
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    import pandas as pd
    import time

    # Configurar headers para simular navegador real
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'DNT': '1'
    }

    # Configurar el navegador
    options = webdriver.ChromeOptions()
    #options.add_argument('--headless')

    # Agregar los headers
    for key, value in headers.items():
        options.add_argument(f'--header="{key}:{value}"')

    # Configuraciones adicionales para parecer más humano
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-infobars')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=options)

    try:
        # Abrir la página
        driver.get('https://datosmacro.expansion.com/demografia/mortalidad/causas-muerte/suicidio/mexico')
        time.sleep(3)
        
        # Aceptar cookies si aparece el botón
        try:
            boton_cookies = driver.find_element(By.ID, 'ue-accept-notice-button')
            boton_cookies.click()
        except:
            print("No hay botón de cookies")
        
        # Encontrar la tabla
        tabla = driver.find_element(By.CLASS_NAME, 'table')
        
        # Obtener datos
        filas = tabla.find_elements(By.TAG_NAME, 'tr')
        datos = []
        
        # Primera fila para encabezados
        encabezados = [celda.text for celda in filas[0].find_elements(By.TAG_NAME, 'th')]
        
        # Resto de filas para datos
        for fila in filas[1:]:
            celdas = fila.find_elements(By.TAG_NAME, 'td')
            fila_datos = [celda.text for celda in celdas]
            if fila_datos:
                datos.append(fila_datos)
        
        # Crear DataFrame
        df = pd.DataFrame(datos, columns=encabezados)

    except Exception as e:
        print(f"Ocurrió un error: {e}")

    finally:
        driver.quit()
    return df

#-----------------EDICIÓN DE DATOS: ESTANDARIZACIÓN Y LIMPIEZA------------------------------------------------------

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

#Función para convertir datos de columnas object a float
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
    import pandas as pd
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


#--------------CONSTRUCCIÓN DE COLUMNAS DE ÍNDICES DE PRECIO DE COMMODITIES EN DATAFRAME--------------------------

#Genera las columnas en el dataframe de los índices de precios por commodity
def indices_precios_comm(df):
    for material in df.columns[1:]: #Iterar en los nombres de las columnas, a partir de la segunda.
        df[f"indice_{material}"]=(df[f"{material}"]/df[f"{material}"].iloc[201])*100 #se toma como base junio 2020, considerando años base de ICP e INCP
    return df


#-------------GENERACIÓN DE DATOS PARA CONVERTIR DATOS ANUALES A MENSUALES ---------------------------------------------------

#Esta función considera el total anual de datos, y lo reparte en partes iguales a los 12 meses del año.
def convertir_a_mensual(df):
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

#Función para unir (how="inner") 2 dataframes, a partir de los datos de la columna date
def unir_dataframes(df1,df2,col_name,union): 
    import pandas as pd
    # Reporte de cantidad de datos antes de la unión
    print(f"Cantidad de filas en el DataFrame 'df1' antes de la unión: {len(df1)}")
    print(f"Cantidad de filas en el DataFrame 'df2' antes de la unión: {len(df2)}")
    
    # Realizamos la unión
    df_final = pd.merge(df1, df2, on=col_name,how=union)
    
    # Reporte de cantidad de datos después de la unión
    print(f"Cantidad de filas en el DataFrame resultante después de la unión: {len(df_final)} \n")
    
    return df_final

#---------------------LLAMADO A CSV DE DATA FRAME FINAL---------------------------------------------------------------
def llama_datos():
    import pandas as pd
    df_final=pd.read_csv("df_final.csv")
    return df_final

#--------------------------CONSTRUCCIÓN DE GRÁFICAS-----------------------------------------------------------------

#Construcción de gráfica de líneas en plotly
def graficar_comportamiento_lineas(df, y, x,etiquetas,titulo):
    """
    Genera un gráfico de líneas para observar el comportamiento de varias columnas respecto al tiempo.

    Parámetros:
    - df: DataFrame que contiene los datos.
    - y: lista de nombres de las columnas que se desean graficar.
    - x: nombre de la columna que contiene la variable temporal.
    - titulo: Título del gráfico
    """
    import pandas as pd
    import plotly.express as px
    # Verificar que la lista de columnas no esté vacía
    if not y:
        raise ValueError("Debe proporcionar al menos una columna para graficar.")
    
    # Crear el gráfico de líneas
    #Los argumentos de l función son: (dataframe,[lista con los valores para eje y], valores de eje x, {"x":"etiqueta para x","values":"etiqueta en y"} )
    fig = px.line(df, x=x, y=y,
                  title=titulo,
                  labels=etiquetas,
                  markers=False,
                  template="plotly_dark",  # Puedes cambiar el tema
                  )
    
    # Mostrar el gráfico
    return fig



#Construcción de gráfica de barras y líneas (2 ejes) en plotly
def grafica_barras_lineas_2ejes(df,columnas_barras,columnas_lineas,x_colum,y1_label,y1_range,y2_label,y2_range,titulo):
    
    """
    Genera un gráfico de barras y líneas para observar su comportamiento en conjunto respecto al tiempo.

    Parámetros:
    - df: DataFrame que contiene los datos.
    - columnas_barras: lista de nombres de las columnas que se desean graficar como barras.
    - columnas_lineas: lista de nombres de las columnas que se desean graficar como líneas.
    - x_colum: nombre de la columna que contiene la variable temporal.
    - y1_label: Etiqueta para el eje y1
    - y1_range: lista con límite inferior y superior del eje y1
    - y2_label: Etiqueta para el eje y2
    - y2_range: lista con límite inferior y superior del eje y2
    - titulo: Título del gráfico
    """
    import pandas as pd
    import plotly.graph_objects as go
    import plotly.express as px

    # Crear la figura
    fig = go.Figure()

    # Graficar las barras para las columnas seleccionadas (unidad 1)
    for i, col in enumerate(columnas_barras):
        fig.add_trace(go.Bar(x=df[x_colum], y=df[col], name=col, marker_color=px.colors.qualitative.Set3[i]))

    # Graficar las líneas para las columnas seleccionadas (unidad 2)
    for col in columnas_lineas:
        fig.add_trace(go.Scatter(x=df[x_colum], y=df[col], mode='lines', name=col, line=dict(width=2), yaxis='y2'))

    # Actualizar la disposición de los ejes
    fig.update_layout(
        title=titulo,
        xaxis_title="Fecha",
        yaxis_title="Unidad 1",  # Título para el eje Y de las barras
        yaxis=dict(
            title=y1_label,  # Eje Y principal
            side='left',  # Eje Y en el lado izquierdo
            range=y1_range, # Establecer el rango del eje Y primario (por ejemplo, de 100 a 200)
            showgrid=True
        ),
        yaxis2=dict(
            title=y2_label,  # Título para el eje Y de las líneas
            overlaying='y',  # Superpone este eje sobre el principal
            side='right',  # Eje Y secundario en el lado derecho
            showgrid=False,  # No mostrar la cuadrícula para el eje Y secundario
            range=y2_range,  # Establecer el rango del eje Y secundario (por ejemplo, de 100 a 200)
            position=0.95  # Ajuste la posición del eje secundario si es necesario
        ),
        template="plotly_dark",  # Puedes cambiar el tema
        barmode='group',  # Agrupar las barras
        legend_title="Unidades"
    )

    # Mostrar el gráfico
    return fig