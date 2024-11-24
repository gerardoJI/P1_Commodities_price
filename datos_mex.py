

#-----------------RECOPILACIÓN DE DATOS DE SUICIDIO CREACIÓN DE DATAFRAME-------------------------------------------
def data_sui_mx():
    """ ESTEBAN
    Realiza web scraping en la página de datosmacro.com para obtener información sobre
    estadísticas de suicidios en México. 
    La función utiliza Selenium para automatizar la navegación en la página, interactuar
    con elementos como botones de cookies y extraer los datos estructurados de la tabla
    principal. Retorna un DataFrame con los datos recopilados.
    Retorna:
        DataFrame: Un DataFrame que contiene los datos extraídos de la tabla en la página web.
    """
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