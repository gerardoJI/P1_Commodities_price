
#-----------------RECOPILACIÓN DE DATOS DE SUICIDIO CREACIÓN DE DATAFRAME-------------------------------------------

def data_sui_es(): 
    """ 
    Realiza web scraping en la página de Wikipedia sobre el suicidio en España
    para extraer una tabla con datos y devolverla en un DataFrame.
    La función utiliza Selenium para automatizar la navegación en la página
    y extraer información estructurada de la tabla etiquetada con 'wikitable'.
    Retorna:
        DataFrame: Un DataFrame que contiene los datos extraídos de la tabla.
    """
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