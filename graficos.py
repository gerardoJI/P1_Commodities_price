#--------------------------CONSTRUCCIÓN DE GRÁFICAS-----------------------------------------------------------------


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