"""
Este documento con tiene el código para la construcción del frontend del proyecto "Análisis de precios de commodities e ínidicies de precios al consumidor en México y España, para el periodo 2002 a 2024"
Se utiliza streamlit.

"""

import streamlit as st
import general_functions as f
import graficos as g

# Configuración de la página
st.set_page_config(page_title="Commodities y precios al consumidor", layout="wide")

# Títulos de las secciones en la barra lateral
PAGES = {
    "Home": "home",
    "Obtención de datos": "data_obtaining",
    "Limpieza y exploración de datos": "data_cleaning",
    "Análisis gráfico de datos": "graphics",
    "Acerca de": "about"
}

# Barra lateral con botones de navegación
st.sidebar.title("Navegación")
selection = st.sidebar.radio("Selecciona una página", list(PAGES.keys()))

# Función para mostrar la página correspondiente
def show_home():
    st.title("Home")
    st.header("¿Si el precio del oro aumenta, comprar alimentos se hace más caro? 💰💰💰")
    st.image("https://cdn-3.expansion.mx/dims4/default/df61a57/2147483647/strip/true/crop/3264x1847+0+0/resize/1200x679!/quality/90/?url=https%3A%2F%2Fcdn-3.expansion.mx%2Fdb%2Ff1%2Ff96e100043f4b45a6a90a0e95cab%2Foro-plata-platino-precio-metales-preciosos.jpg", caption="", use_column_width=True)
    
    st.header("Commodities")
    st.write("Según un artículo de universidadeuropea.com, commodity es un material tangible que se puede comerciar, comprar o vender. Al encontrarse sin procesar, no posee ningún valor añadido o diferencial más allá de su proveniencia, por eso se suele usar como materia prima para fabricar productos más refinados.")
    st.write("En el mercado podemos encontrar diferentes tipos de commodities que se clasifican en función de las materias primas para facilitar su comercialización: granos, ganadería, energéticos, metales, entre otros.")
    st.markdown("Clic al [link](https://universidadeuropea.com/blog/que-son-los-commodities/) para conocer más.")
    
    st.header("Índice de precios al consumidor")
    st.image("https://www.bbva.es/content/dam/public-web/bbvaes/images/finanzas-vistazo/ef/finanzas-personales/2400x1600/2400x1600-inflacion-subyacente.jpg", caption="", use_column_width=True)
    st.write("Acorde con el INE (Instituto Nacional de Estadística) en España, el Índice de Precios de Consumo (IPC) tiene como objetivo proporcionar una medida estadística de la evolución del conjunto de precios de los bienes y servicios que consume la población residente en viviendas familiares en España.")
    st.write("Este índice se elabora con cerca de 210.000 precios de los cuales informan unos 29.000 establecimientos distribuidos en 177 municipios de todo el territorio nacional. La recogida de datos de 462 artículos se realiza de forma tradicional (mediante visita personal a los establecimientos en las fechas que corresponda), así como por teléfono y correo electrónico. Además, mediante medios automatizados (como scanner data o web scrapping) se recogen datos de otros 493 artículos. En determinados artículos tarifados se obtiene información de las publicaciones oficiales correspondientes.")
    st.markdown("Clic para [seguir leyendo](https://www.ine.es/prensa/ipc_prensa.htm#:~:text=El%20%C3%8Dndice%20de%20Precios%20de,en%20viviendas%20familiares%20en%20Espa%C3%B1a.)")
    st.write("En México, la medida equivalente es el INPC, Índice Nacional de Precios al Consumidor, publicado periódicamente por el INEGI (Instituto Nacional de Estadística y Geografía).")
    
    st.subheader("⚠️ El objetivo es obtener información que permita visualizar una relación entre la variación del precio de los commodities, el IPC en España y el INPC en México ⚠️")
    st.header("Y, además...🚩")
    st.image("https://img.lavdg.com/sc/LNuVdytZjyAwwlqUJuA5HhWImOc=/1280x/2021/12/13/00121639419839536536929/Foto/SUICIDIO.jpg", caption="", use_column_width=True)
    st.subheader("¿La cantidad de suicidios en España y México puede estar relacionada con la variación de estos precios? 📉")
    st.write("¡A explorar datos para buscar respuestas!")


def show_data_obtaining():
    st.title("Obtención de datos")
    st.image("https://universidadeuropea.com/resources/media/images/commodity.width-1200.format-webp.webp", caption="", use_column_width=True)
    st.header("Web scraping, Yahoo finance API e información pública gubernamental")
    
    st.subheader("Web scraping mediante Selenium")
    st.write("En el proceso de recolección de datos, se utilizó la librería Selenium de Python para ejecutar web scraping en páginas con datos requeridos. Esto permite generar un dataframe mediante la lectura de los elementos presentes en el código HTML del sitio. De esta manera se construyeron dataframe sobre los valores anuales de suicidios en España, para el periodo 1980 al 2023. Un proceso análogo se ejecutó para la información de México. A continuación se muestra una de las funciones generadas para la obtención de datos a un link de Wikipedia:")
    
    codigo="""
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

            """
    st.code(codigo, language='python')
    st.image("https://blog.apify.com/content/images/2023/09/what-is-web-scraping-websites-web-scraper-structured-data-1.png", caption="Proceso de web scraping", use_column_width=True)

    st.subheader("Yahoo finance API")
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Yahoo%21_Finance_logo_2021.png/800px-Yahoo%21_Finance_logo_2021.png",caption="",use_column_width=True)
    st.write("Los datos históricos del precio de los commodities analizados, oro, plata, petróleo y gas natural, fueron información obtenida de Yahoo, mediante la librería yfinance en Python. De esta manera, se utilizaron las API hacia los datos de Yahoo, y se almacenaron en una base de datos. Como resultado, se recuperaron datos mensuales del precio de commodities en USD, para el periodo 2000 a 2024. \nEn el siguiente cuadro se muestran las líneas de código de la función en la que se utiliza la librería yfinance:")

    codigo2= """
            import yfinance as yf
            # Obtener los datos históricos
            for activo, simbolo in activos.items():
                # Crear el objeto Ticker para cada activo
                ticker = yf.Ticker(simbolo)
                
                # Obtener datos históricos anuales (frecuencia "1mo" para mensual)
                historial = ticker.history(start=inicio, end=fin, interval="1mo")
                
                # Se recupera el precio de cierre para cada año
                datos[activo] = historial[['Close']] #con close se toman los valores del precio de cierre

            """
    st.code(codigo2, language='python')

    st.subheader("Recolección de datos públicos en sitios gubernamentales oficiales")
    st.write("Finalmente, las paginas web de las dependencias encargadas de los registros estadísticos publicos permiten descargar una gran cantidad de datos de diferentes índoles en archivos compatibles con diferentes aplicaciones. En esta ocasión, se obtuvieron archivos .csv. Esto permite una sencilla lectura y manejo de datos con Python.")
    
    st.subheader("🔎🔎Conoce a detalle el código utilizado en este trabajo🔎🔎")
    st.markdown("💡--> Visita el [repositorio](https://github.com/gerardoJI/P1_Commodities_price) en GitHub.")
    

def show_data_cleaning():
    st.title("Limpieza de datos 🔬🔬🔬")
    st.image("https://cdn.prod.website-files.com/5fbe376a36d4106214faaf3c/61e5f5a91735d6cc7515bcc6_0A4zVj7AA0kGao3qrDORDaRwOL70Bt5IiwEj18h1fZM23OLyWYUcanDfpFJtvANhBUR3gBUFeuGy1WchKVZFszv1D_BpOlIozOcZkG3ccKOpx_dmefqsVWCtjuouruF6K3EiBDOI.png", use_column_width=True)
    st.header("Estandarización de datos, cambios de tipo de dato, adición y eliminación de columnas, manejo de valores nulos, interpolación de datos, unión de dataframes.")
    st.write("Todos los datos recuperados fueron revisados para determinar las necesidades previas al inicio de su análisis. Los datos fueron sometidos a un proceso de estandarización y limpieza, para el que se construyeron funciones que realizaran tareas unitarias, basadas en la librería pandas. De esta manera, cada una de las funciones podía ser aplicada a cada dataframe, según lo observado durante la exploración de datos. En esta sección se presentan algunas de las funciones construidas. ")
    st.subheader("Interpolación de datos faltantes")
    st.write("Durante la exploración de datos, se detectó la necesidad de interpolar algunos datos faltantes en las bases de datos. Para esto, se construyó una función que emplea interpolación lineal para agregar los datos faltantes a los dataframe. En seguida se muestra la función aplicada.")
    codigo3="""

        def completar_columnas_interpolacion(df):
            import pandas as pd

            #Rellena las fechas faltantes en la columna 'date' y 
            #realiza la interpolación de los valores faltantes en las demás columnas.
            
            #Parámetros:
            #df (DataFrame): El dataframe con una columna 'date'
            
            #Retorna:
            #DataFrame: El dataframe con las fechas completadas y los valores interpolados.
            
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

            """
    st.code(codigo3, language='python')
    
    st.subheader("Generación de columnas para índices de precios de los commodities")
    st.write("Para poder comparar los precios del oro, plata, petróleo y gas natural con los IPC y INPC, fue necesario generar índices para los precios de los commodities, que con base en un año de referencia, representan la variación de los precios respecto al tiempo. De esta forma, se hace posible la comparación con los índices de precios al consumidor en México y España. El código generado para la construcción de estos índices se muestra a continuación:")

    codigo4="""
            #Genera las columnas en el dataframe de los índices de precios por commodity
            def indices_precios_comm(df):
                for material in df.columns[1:]: #Iterar en los nombres de las columnas, a partir de la segunda.
                    df[f"indice_{material}"]=(df[f"{material}"]/df[f"{material}"].iloc[201])*100 #se toma como base junio 2020, considerando años base de ICP e INCP
                return df
            """
    st.code(codigo4, language='python')

    st.subheader("Limpieza de archivos CSV")
    st.write("Por último, se muestra la función empleada para la limpieza de los archivos .csv, recuperados de los sitios oficiales de estadística. De manera general, la función identifica datos nulos y elimina las filas del dataframe donde se aloja. Luego, realiza la conversión de tipo de dato 'object' a 'float'. Finalmente imprime un reporte de la cantidad de datos en el dataframe antes y después de la limpieza.")
    codigo5="""
            def limpiar_csv(df):
                
                #Limpia el DataFrame eliminando filas con valores N/E o NaN, 
                #y convierte las columnas a tipo float, excepto la columna 'date'.   
                #Retorna:
                #- df: DataFrame limpio.
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
            
            """
    st.code(codigo5, language='python')
    st.header("")
    st.subheader("🔎🔎Conoce a detalle el código utilizado en este trabajo🔎🔎")
    st.markdown("💡--> Visita el [repositorio](https://github.com/gerardoJI/P1_Commodities_price) en GitHub.")
    
    st.header("")
    st.header("Dataframe final")
    st.subheader("El resultado de la limpieza, estandarización y unión de datos:")
    df = f.llama_datos() 
    st.dataframe(df)

def show_graphics():
    st.title("Gráficos")
    st.image("https://cdn.britannica.com/91/234691-050-C3D7476D/What-Are-Commodities-composite-image.jpg", use_column_width=True)
    st.write("En este apartado se muestran los gráficos realizados para la obtención de insighs del dataframe construido. Las figuras fueron construidas mediante la librería plotly.")
        
    df = f.llama_datos() #llama los datos del archivo .csv del dataframe final

    #Figura 1:
    fig_1=g.graficar_comportamiento_lineas(df, ['oro', 'plata', 'petroleo', 'gas_natural'], 'date',{"date": "Tiempo", 'value': 'Valor USD'},'Variación del precio de commodities en USD')
    st.plotly_chart(fig_1,use_container_width=True)
    st.write("Considerando que las unidades del eje ordenado se encuentran en USD, se observa como la línea del oro tiene protagonismo, al ser el commoditie de mayor precio. En este gráfico se pueden observar fácilmente los valores máximos y mínimos del precio por commodity. Al día de hoy, el elemento que más ha aumentado su valor desde el año 2002 es el oro, con una variación positiva de más de 900%")

    #Figura 2:
    fig_2=g.graficar_comportamiento_lineas(df, ['indice_oro', 'indice_plata', 'indice_petroleo', 'indice_gas_natural'], 'date',{"date": 'Tiempo', 'value': 'Unidades'},"Variación del ínidice del precio de commodities")
    st.plotly_chart(fig_2,use_container_width=True)
    st.write("Sin embargo, la comparación de los índices de variación del precio de commodities con base al 2020, permite ver con detalle cuál de ellos ha sufrido cambios más abruptos en su valor respecto al tiempo. El gas natural presenta una gráfica con varios picos, en contraste con el oro, que presenta un aumento más suavizado.")

    #Figura 3:
    fig_3=g.graficar_comportamiento_lineas(df,['alimentos_bebidas_es','vivienda_es','educacion_es','transporte_es','indice_general_es','alimentos_bebidas_mx','vivienda_mx','educacion_mx','transporte_mx','indice_general_mx'], 'date',{"date": 'Tiempo', 'value': 'Unidades'},"IPC vs INPC")
    st.plotly_chart(fig_3,use_container_width=True)
    st.write("Ahora, respecto al aumento de precios entre los años 2002 y 2004 en México y España, la pendiente del INPC de México es mayor que la del IPC de España, lo que indica un mayor crecimiento general de los precios al consumidor en el país latinoamericano. En ambos casos las pendientes son positivas, probablemente reflejo de la inflación. Llama la atención el similar comportamiento del aumento del precio en alimentos y bebidas para ambos países, a partir del 2020.")

    st.subheader("🔎🔎Conoce a detalle el código utilizado en este trabajo🔎🔎")
    st.markdown("💡--> Visita el [repositorio](https://github.com/gerardoJI/P1_Commodities_price) en GitHub.")

    #Figura 4:
    fig_4=g.grafica_barras_lineas_2ejes(df,['indice_oro', 'indice_plata','indice_petroleo','indice_gas_natural'],['alimentos_bebidas_es','vivienda_es','educacion_es','transporte_es','indice_general_es'],'date','Unidades',[0,350],'Unidades',[50, 150],"Índice de precio de commodities vs IPC España")
    st.plotly_chart(fig_4,use_container_width=True)
    st.write("Cuando se compara el índice de variación del oro y el IPC (indice_general_es), se observa cómo ambos presentan un cambio positivo respecto al tiempo. Sin embargo, esto no es evidencia suficiente para indicar que las variables están relacionadas. Por otra parte, cuando se compara el índice de variación del precio del petróleo y el índice de transporte (transporte_es), se aprecia uan coincidencia importante en el comportamiento de los valores, probablemente asociado al estrecho vínculo por la utilización de derivados del petróleo como combustibles.")

    #Figura 5:
    fig_5=g.grafica_barras_lineas_2ejes(df,['indice_oro', 'indice_plata','indice_petroleo','indice_gas_natural'],['alimentos_bebidas_mx','vivienda_mx','educacion_mx','transporte_mx','indice_general_mx'],'date','Unidades',[0,350],'Unidades',[50, 150],"Índice de precio de commodities vs INPC México")
    st.plotly_chart(fig_5,use_container_width=True)
    st.write("A diferencia de lo observado en España, la variación del precio del petróleo no pareciera tener relación con el índice del precio del transporte (transporte_mx). Por su parte, el índice del precio de los alimentos (alimentos_mx) mantiene una tendencia positiva a través del tiempo, como el oro. Pero la tendencia similar no representa una justificación para relacionar ambas variables.")
    st.subheader("A modo de conclusión después de este análisis gráfico, se determina la necesidad de aplicar al dataframe un análisis estadístico que permita profundizar en los datos, para poder visualizar algún tipo de correlación que pudieran tener las variables, y que con las gráficas construídas no es posible señalar. De las comparaciones realizadas, se destaca el acompañamiento del precio del oro con los índices de productos en México y España, respecto a la tendencia positiva durante el periodo 2002 a 2024. Por otra parte, en la comparación de variación de precio del petróleo con los precios de transporte en España, se observa una probable relación entre variables que vale la pena indagar.")

    st.header("🚩🚩🚩¿La variación de los precios está vinculada con los suicidios en México y España? 😧")

    #Figura 6:
    fig_6=g.grafica_barras_lineas_2ejes(df,['indice_oro', 'indice_plata','indice_petroleo','indice_gas_natural'],['sui_es', 'sui_mx'],'date','Unidades',[0,350],'Personas',[250, 700],"Índice de precio de commodities vs cantidad de suicidios en México y España")
    st.plotly_chart(fig_6,use_container_width=True)
    st.write("Cuando se grafican las combinaciones posibles dentro de la figura, no es posible visualizar alguna relación entre los valores de los índices de precios de los commodities y la cantidad de suicidios en México o España.")

    #Figura 7:
    fig_7=g.grafica_barras_lineas_2ejes(df,['alimentos_bebidas_es','vivienda_es','educacion_es','transporte_es','indice_general_es','alimentos_bebidas_mx','vivienda_mx','educacion_mx','transporte_mx','indice_general_mx'],['sui_es', 'sui_mx'],'date','Unidades',[0,175],'Personas',[250, 700],"IPC / INPC vs cantidad de suicidios en México / España")
    st.plotly_chart(fig_7,use_container_width=True)
    st.write("Para el caso de comparar los IPC e INPC contra la cantidad de suicidios en sus respectivos países, para España no se visualiza relación alguna. En el caso de México, la tendencia es positiva tanto para los suicidios como para los índices de precios al consumidor. Igualmente, se requiere ahondar el análisis de los datos para obtener resultados concluyentes.") 

def show_about():
    st.title("Acerca de")
    st.header("Referencias")
    referencias="""
    Banco de México. (n.d.). Cuadro de precios al consumidor (CP154). Banco de México. Recuperado de https://www.banxico.org.mx/SieInternet/consultarDirectorioInternetAction.do?sector=8&accion=consultarCuadro&idCuadro=CP154&locale=es

    Instituto Nacional de Estadística y Geografía (INEGI). (n.d.). Índice Nacional de Precios al Consumidor (INPC). INEGI. Recuperado de https://www.inegi.org.mx/temas/inpc/

    Instituto Nacional de Estadística (INE). (n.d.). Índice de Precios de Consumo (IPC). INE. Recuperado de https://www.ine.es/jaxiT3/Datos.htm?t=50902#_tabs-tabla

    AlgoTrading101. (2021). Guía completa de yFinance: aprende a usar la API de Yahoo Finance. Recuperado de https://algotrading101.com/learn/yfinance-guide/

    Wikipedia. (2024). Suicidio en España. Wikipedia. Recuperado de https://es.wikipedia.org/wiki/Suicidio_en_Espa%C3%B1a

    Universidad Europea. (n.d.). ¿Qué son los commodities? Universidad Europea. Recuperado de https://universidadeuropea.com/blog/que-son-los-commodities/

    Instituto Nacional de Estadística (INE). (2024). El Índice de Precios de Consumo (IPC). INE. Recuperado de https://www.ine.es/prensa/ipc_prensa.htm#:~:text=El%20%C3%8Dndice%20de%20Precios%20de,en%20viviendas%20familiares%20en%20Espa%C3%B1a.

    """
    st.write(referencias)
    st.write("Novimebre 2024. Realizado para practicar uso de streamlit, web scraping, uso de APIs, limpieza de datos, creación de gráficas.")
    


# Agregar los datos del autor y enlaces de redes sociales en la parte inferior de la barra lateral
st.sidebar.markdown("---")  # Línea separadora
st.sidebar.markdown("## Datos del autor")
st.sidebar.markdown("**Autor:** Gerardo Jiménez Islas")
st.sidebar.markdown("📌 [LinkedIn](https://www.linkedin.com/in/gerardo-jimenez-islas/)")
st.sidebar.markdown("📎 [GitHub](https://github.com/gerardoJI)")
st.sidebar.markdown("📭 Correo: [gerardoji.0918@gmail.com](mailto:gerardoji.0918@gmail.com)")

# Selección de la página según el botón de la barra lateral
if selection == "Home":
    show_home()
elif selection == "Obtención de datos":
    show_data_obtaining()
elif selection == "Limpieza y exploración de datos":
    show_data_cleaning()
elif selection == "Análisis gráfico de datos":
    show_graphics()
elif selection == "Acerca de":
    show_about()