# -*- coding: utf-8 -*-
"""
Created on Wed Nov 6 08:54:03 2024

@author: Hazael
"""
import streamlit as st
import pandas as pd
import altair as alt
import plotly.graph_objects as go




# Configuración del dash
st.set_page_config(
    page_title="Análisis Académico",
    layout="wide"
)


# Título
st.title("Trayectoria Académica de los Estudiantes")

# Sidebar de etiquetas
from streamlit_tags import st_tags_sidebar

tags = st_tags_sidebar(
    label="Filtrar visualizaciones. Tags a usar: Aplicada 2009, Física 2009, Física 2016, Aplicada 2016, SankeyFísica",
    text="Escribe y presiona enter para agregar etiquetas",
    value=[""],
    suggestions=["Aplicada 2009", "Física 2009", "Física 2016", "Aplicada 2016", "SankeyFísica"],
    maxtags=-5,
    key="tags"
)
if "Aplicada 2009" in tags:
    
    # Verificar si la etiqueta "Sankey" está seleccionada
    #if "Sankey" in tags:
    
        # Diagrama de Sankey original
    st.subheader("Progreso de los alumnos en tiempo y forma por Semestre")
    st.subheader("Diagrama de Sankey por Semestre")
    
    # Definición de la función para crear el diagrama de Sankey
    def create_dynamic_sankey(opacity=0.8):
        # Definir nodos manualmente en el orden deseado
        generaciones = ["Generación 2009", "Generación 2010", "Generación 2011", "Generación 2012",
                        "Generación 2013", "Generación 2014", "Generación 2015"]
        semestres = 9
    
        # Reordenar nodos finales para que "Egresados" y "Titulado" estén arriba
        nodos_finales = ["Egresados", "Titulado", "Deserción"]
        labels = generaciones + [f"Semestre {i+1}" for i in range(semestres)] + nodos_finales
    
        sources = []
        targets = []
        values = []
        colors = []
    
        colores_generaciones = [
            "255, 99, 71",
            "60, 179, 113",
            "30, 144, 255",
            "255, 215, 0",
            "218, 112, 214",
            "244, 164, 96",
            "123, 104, 238"
        ]
    
        valores_generaciones = [46, 56, 54, 57, 55, 61, 60]
    
        # Asegurar que los nodos iniciales estén ordenados cronológicamente
        for gen, valor in enumerate(valores_generaciones):
            sources.append(gen)
            targets.append(len(generaciones))
            values.append(valor)
            colors.append(f"rgba({colores_generaciones[gen]}, {opacity})")
    
        valores_semestres = [
            [46, 56, 48, 57, 55, 61, 54],
            [17, 36, 32, 28, 28, 31, 30],
            [17, 24, 16, 17, 19, 17, 24],
            [12, 15, 14, 17, 23, 20, 20],
            [11, 13, 7, 15, 16, 17, 16],
            [8, 9, 12, 14, 12, 16, 13],
            [5, 10, 10, 11, 14, 14, 13],
            [5, 8, 5, 11, 10, 10, 13]
        ]
    
        for semestre_index, valores in enumerate(valores_semestres):
            for gen, valor in enumerate(valores):
                sources.append(len(generaciones) + semestre_index)
                targets.append(len(generaciones) + semestre_index + 1)
                values.append(valor)
                colors.append(f"rgba({colores_generaciones[gen]}, {opacity})")
    
        valores_finales = {
            "Egresados": [15, 18, 4, 11, 14, 4, 9],
            "Titulado": [4, 2, 2, 6, 14, 14, 10],
            "Deserción": [31, 39, 48, 32, 6, 38, 4]
        }
    
        ultimo_semestre = len(generaciones) + semestres - 1
        targets_indices = [labels.index("Egresados"), labels.index("Titulado"), labels.index("Deserción")]
    
        for gen, color in enumerate(colores_generaciones):
            sources.extend([ultimo_semestre, ultimo_semestre, ultimo_semestre])
            targets.extend(targets_indices)
            values.extend([
                valores_finales["Egresados"][gen],
                valores_finales["Titulado"][gen],
                valores_finales["Deserción"][gen]
            ])
            colors.extend([f"rgba({color}, {opacity})"] * 3)
    
        fig = go.Figure(go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=labels,
                color=[f'rgba(30, 58, 138, {opacity})' for _ in labels]
            ),
            link=dict(
                source=sources,
                target=targets,
                value=values,
                color=colors
            )
        ))
    
        fig.update_layout(
            title="Diagrama de Sankey: Trayectoria Académica por Generación",
            font=dict(size=14),
            paper_bgcolor="rgba(0, 0, 0, 0)"
        )
    
        return fig
    
    # Mostrar el slider y el gráfico del Sankey
    opacity = st.slider("Ajustar opacidad:", 0.2, 1.0, 0.8, 0.1)
    st.plotly_chart(create_dynamic_sankey(opacity), use_container_width=True)


        
        # Datos para la primera tabla: Tasa de Retención
    retention_data = [
        ["2011", "63%", "72%", "85%", "86%"],
        ["2012", "75%", "82%", "92%", "97%"],
        ["2013", "79%", "78%", "86%", "87%"],
        ["2014", "79%", "80%", "77%", "90%"],
        ["2015", "71%", "89%", "77%", "87%"]
    ]
    
    # Tabla HTML - Fondo negro
    table_html_black = f"""
    <style>
        .table-black {{
            width: 100%;
            border-collapse: collapse;
            text-align: center;
        }}
        .table-black th {{
            background-color: #000000;
            color: #FFFFFF;
            padding: 8px;
        }}
        .table-black td {{
            border: 1px solid #ddd;
            padding: 8px;
        }}
    </style>
    <table class="table-black">
        <tr>
            <th rowspan="2">Cohorte</th>
            <th colspan="4">Tasa de Retención al</th>
        </tr>
        <tr>
            <th>Segundo Año</th>
            <th>Tercer Año</th>
            <th>Cuarto Año</th>
            <th>Quinto Año</th>
        </tr>
        {"".join(f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td></tr>" for row in retention_data)}
    </table>
    """

    # Datos para la segunda tabla: Tasa de Retención Femenina
    female_retention_data = [
        ["2011", "56%", "70%", "71%", "100%"],
        ["2012", "93%", "64%", "89%", "88%"],
        ["2013", "78%", "86%", "92%", "91%"],
        ["2014", "85%", "94%", "88%", "86%"],
        ["2015", "81%", "95%", "90%", "89%"]
    ]
    
    # Tabla HTML - Fondo #D9B1E0 para cabeceras y #862B96 para celdas de datos
    table_html_purple = f"""
    <style>
        .table-purple {{
            width: 100%;
            border-collapse: collapse;
            text-align: center;
        }}
        .table-purple th {{
            background-color: #5E1F83;
            color: white;
            padding: 8px;
        }}
        .table-purple td {{
            background-color: #B7A1D1; /* Fondo de celdas de datos */
            color: white; /* Texto blanco para contraste */
            border: 1px solid #ddd;
            padding: 8px;
        }}
    </style>
    <table class="table-purple">
        <tr>
            <th rowspan="2">Cohorte</th>
            <th colspan="4">Tasa de Retención Femenina al</th>
        </tr>
        <tr>
            <th>Segundo Año</th>
            <th>Tercer Año</th>
            <th>Cuarto Año</th>
            <th>Quinto Año</th>
        </tr>
        {"".join(f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td></tr>" for row in female_retention_data)}
    </table>
    """

    # Datos para la tabla: Tasa de Retención Masculina
    male_retention_data = [
        ["2011", "67%", "73%", "89%", "82%"],
        ["2012", "69%", "90%", "93%", "100%"],
        ["2013", "79%", "74%", "83%", "84%"],
        ["2014", "76%", "72%", "70%", "94%"],
        ["2015", "64%", "83%", "63%", "83%"]
    ]
    
    # Tabla HTML - Fondo #3D0C56 y texto contenido #B6A3C7
    table_html_male = f"""
    <style>
        .table-male {{
            width: 100%;
            border-collapse: collapse;
            text-align: center;
        }}
        .table-male th {{
            background-color: #2558C4; /* Fondo morado oscuro */
            color: white; /* Texto blanco */
            padding: 8px;
        }}
        .table-male td {{
            border: 1px solid #ddd;
            padding: 8px;
            background-color: #58A2D5; /* Celdas con fondo suave */
            color: white; /* Texto gris suave */
        }}
    </style>
    <table class="table-male">
        <tr>
            <th rowspan="2">Cohorte</th>
            <th colspan="4">Tasa de Retención Masculina al</th>
        </tr>
        <tr>
            <th>Segundo Año</th>
            <th>Tercer Año</th>
            <th>Cuarto Año</th>
            <th>Quinto Año</th>
        </tr>
        {"".join(f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td></tr>" for row in male_retention_data)}
    </table>
    """


    # Streamlit Layout
    col1, col2, col3 = st.columns([1, 5, 1])
    
    # Mostrar tablas en la columna central
    with col2:
        st.write("### Tasa de Retención por Cohorte")
        st.markdown(table_html_black, unsafe_allow_html=True)
        st.write("### Tasa de Retención Femenina")
        st.markdown(table_html_purple, unsafe_allow_html=True)
        st.write("### Tasa de Retención Masculina")
        st.markdown(table_html_male, unsafe_allow_html=True)

    

   

                # Datos ficticios por generación y género
    generation_data = {
        "Generación 2009": {
            "Bajas": {"General": 31, "Hombres": 21, "Mujeres": 10},
            "Egresados": {"General": 15, "Hombres": 10, "Mujeres": 5},
            "Titulados": {"General": 4, "Hombres": 3, "Mujeres": 1},
        },
        "Generación 2010": {
            "Bajas": {"General": 39, "Hombres": 27, "Mujeres": 12},
            "Egresados": {"General": 18, "Hombres": 11, "Mujeres": 7},
            "Titulados": {"General": 2, "Hombres": 1, "Mujeres": 1},
        },
        "Generación 2011": {
            "Bajas": {"General": 48, "Hombres": 33, "Mujeres": 15},
            "Egresados": {"General": 4, "Hombres": 3, "Mujeres": 1},
            "Titulados": {"General": 2, "Hombres": 2, "Mujeres": 0},
        },
        "Generación 2012": {
            "Bajas": {"General": 32, "Hombres": 23, "Mujeres": 9},
            "Egresados": {"General": 11, "Hombres": 9, "Mujeres": 2},
            "Titulados": {"General": 14, "Hombres": 10, "Mujeres": 4},
        },
        "Generación 2013": {
            "Bajas": {"General": 38, "Hombres": 28, "Mujeres": 10},
            "Egresados": {"General": 4, "Hombres": 3, "Mujeres": 1},
            "Titulados": {"General": 14, "Hombres": 7, "Mujeres": 7},
        },
        "Generación 2014": {
            "Bajas": {"General": 40, "Hombres": 30, "Mujeres": 10},
            "Egresados": {"General": 6, "Hombres": 3, "Mujeres": 3},
            "Titulados": {"General": 13, "Hombres": 7, "Mujeres": 6},
        },
        "Generación 2015": {
            "Bajas": {"General": 38, "Hombres": 29, "Mujeres": 9},
            "Egresados": {"General": 9, "Hombres": 1, "Mujeres": 8},
            "Titulados": {"General": 10, "Hombres": 3, "Mujeres": 7 },
        },
    }

        # Índice de rezago por generación
    rezago_data = {
        "Generación 2009": 26,
        "Generación 2010": 13.33333333,
        "Generación 2011": 22.80702,
        "Generación 2012": 26.6666667,
        "Generación 2013": 22.80702,
        "Generación 2014": 27.41935,
        "Generación 2015": 33.87097,
    }

    # Índice de rezago femenino
    rezago_femenino_data = {
        "Generación 2009": 25,
        "Generación 2010": 5,
        "Generación 2011": 16.66667,
        "Generación 2012": 20,
        "Generación 2013": 27.77778,
        "Generación 2014": 40,
        "Generación 2015": 46.1538,
    }
    
    # Índice de rezago masculino
    rezago_masculino_data = {
        "Generación 2009": 26.470588,
        "Generación 2010": 17.5,
        "Generación 2011": 25.64103,
        "Generación 2012": 28.88889,
        "Generación 2013": 20.51282,
        "Generación 2014": 21.42857,
        "Generación 2015": 25,
    }
    
    valores_semestres = [
        [46, 17, 17, 12, 11, 8, 5, 5, 19, 12],
        [56, 36, 24, 15, 13, 9, 10, 8, 13, 18],
        [54, 32, 16, 14, 7, 12, 10, 5, 10, 11],
        [57, 28, 17, 17, 15, 14, 11, 11, 14, 19],
        [55, 28, 19, 23, 16, 12, 14, 10, 15, 13],
        [61, 31, 17, 20, 17, 16, 14, 10, 16, 16],
        [60, 30, 24, 20, 16, 13, 13, 13, 18, 10]
    ]
    
    # DataFrame con los valores de los semestres
    df_semestres = pd.DataFrame(valores_semestres, index=list(generation_data.keys()), columns=[f"Semestre {i+1}" for i in range(10)])


    GRAPH_WIDTH = 130
    GRAPH_HEIGHT = 130
    
    def make_donut(input_response, input_text, input_color, title_text=None):
        chart_color = {
            "blue": ['#58A2D5', '#2558C4'],
            "pink": ['#D9B1E0', '#862B96'],
            "green": ['#27AE60', '#12783D'],
            "orange": ['#EFB444', '#F6E29D'],
            "red": ['#E74C3C', '#781F16']
        }.get(input_color, ['#dddddd', '#aaaaaa'])
    
        # Datos para el gráfico
        source = pd.DataFrame({
            "Topic": ['', input_text],
            "% value": [100 - input_response, input_response]
        })
        source_bg = pd.DataFrame({
            "Topic": ['', input_text],
            "% value": [100, 0]
        })
    
        # Gráfico principal de dona
        plot = alt.Chart(source).mark_arc(innerRadius=45, cornerRadius=25).encode(
            theta="% value",
            color=alt.Color("Topic:N",
                            scale=alt.Scale(
                                domain=[input_text, ''],
                                range=chart_color),
                            legend=None),
        ).properties(width=130, height=130)
    
        # Texto del porcentaje
        text = plot.mark_text(
            align='center',
            font="Lato",
            fontSize=25,
            fontWeight=700
        ).encode(text=alt.value(f'{input_response} %'))
    
        # Fondo de la dona
        plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=45, cornerRadius=20).encode(
            theta="% value",
            color=alt.Color("Topic:N",
                            scale=alt.Scale(
                                domain=[input_text, ''],
                                range=chart_color),
                            legend=None),
        ).properties(width=130, height=130)
    
        # Título (texto encima del gráfico)
        if title_text:
            title = alt.Chart(pd.DataFrame({'text': [title_text]})).mark_text(
                align='center',
                fontSize=16,
                fontWeight='bold',
                color=chart_color[0]
            ).encode(text='text:N')
    
            # Concatenar título y gráfico
            return alt.vconcat(title, plot_bg + plot + text)
        else:
            # Texto en blanco para alinear las gráficas generales
            blank_title = alt.Chart(pd.DataFrame({'text': ['‎ ‎ ‎ ‎ ']})).mark_text(
                align='center',
                fontSize=16,  # Tamaño similar al texto de hombres y mujeres
                fontWeight='bold',
                color="#ffffff"  # Texto blanco para que sea invisible
            ).encode(text='text:N')
    
            return alt.vconcat(blank_title, plot_bg + plot + text)

    
    # Dropdown generación
    generaciones = list(generation_data.keys())
    selected_generacion = st.selectbox("Selecciona una generación:", generaciones)
    
    
    col1, col2, col3 = st.columns(3)
    
    # Mostrar el índice de rezago general en la columna 1
    with col1:
        indice_rezago = rezago_data[selected_generacion]
        st.metric(label="Índice de Rezago", value=f"{indice_rezago:.2f}")
    # Mostrar el índice de rezago femenino
        indice_rezago_femenino = rezago_femenino_data[selected_generacion]
        st.metric(label="Índice de Rezago Femenino", value=f"{indice_rezago_femenino:.2f}")
    
        # Mostrar el índice de rezago masculino
        indice_rezago_masculino = rezago_masculino_data[selected_generacion]
        st.metric(label="Índice de Rezago Masculino", value=f"{indice_rezago_masculino:.2f}")

    # Mostrar los valores de la generación seleccionada
    with col2:
        st.write("Estudiantes inscritos por semestre para la generación seleccionada:")
        df = pd.DataFrame({
            "Semestre": range(1, 11),
            "Estudiantes inscritos": df_semestres.loc[selected_generacion].values
        })
        st.dataframe(df)

    
    # Columnas con gráficas de dona dinámicas basadas en la generación seleccionada
    col1, col2, col3 = st.columns([1, 1, 1])
    
    # Totales por generación
    valores_generaciones = [46, 56, 54, 57, 55, 61, 60]  # Totales de estudiantes por generación en orden 2009-2015
    totales_generacion = dict(zip(generation_data.keys(), valores_generaciones))  # Mapeo generación -> total
    
    def calcular_porcentajes(data, total):
        """
        Convierte los valores de 'General', 'Hombres', y 'Mujeres' a porcentajes basados en el total dado.
        """
        for categoria, valores in data.items():
            for grupo in ["General", "Hombres", "Mujeres"]:
                valores[grupo] = round((valores[grupo] / total) * 100, 2)  # Convertir a porcentaje
    
    # Convertir los valores de generation_data a porcentajes
    for generacion, data in generation_data.items():
        calcular_porcentajes(data, totales_generacion[generacion])
        categories = ["Bajas", "Egresados", "Titulados"]
        colors = ["red", "orange", "green"]
    
    for col, category, color in zip([col1, col2, col3], categories, colors):
        with col:
            st.title(category)
    
            # Gráfica general
            general = generation_data[selected_generacion][category]["General"]
            st.altair_chart(make_donut(general, "General", color), use_container_width=True)
    
            # Gráfica de hombres con texto encima
            hombres = generation_data[selected_generacion][category]["Hombres"]
            hombres_percent = round((hombres / general) * 100, 1)
            st.altair_chart(make_donut(hombres_percent, "Hombres", "blue", title_text="Hombres"), use_container_width=True)
    
            # Gráfica de mujeres con texto encima
            mujeres = generation_data[selected_generacion][category]["Mujeres"]
            mujeres_percent = round((mujeres / general) * 100, 1)
            st.altair_chart(make_donut(mujeres_percent, "Mujeres", "pink", title_text="Mujeres"), use_container_width=True)

if "Física 2009" in tags:
    
    
        # Diagrama de Sankey original
    st.subheader("Progreso de los alumnos en tiempo y forma por Semestre")
    st.subheader("Diagrama de Sankey por Semestre")
    
    # Definición de la función para crear el diagrama de Sankey
    def create_dynamic_sankey(opacity=0.8):
        # Definir nodos manualmente en el orden deseado
        generaciones = ["Generación 2009", "Generación 2010", "Generación 2011", "Generación 2012",
                        "Generación 2013", "Generación 2014", "Generación 2015"]
        semestres = 9
    
        # Reordenar nodos finales para que "Egresados" y "Titulado" estén arriba
        nodos_finales = ["Egresados", "Titulado", "Deserción"]
        labels = generaciones + [f"Semestre {i+1}" for i in range(semestres)] + nodos_finales
    
        sources = []
        targets = []
        values = []
        colors = []
    
        colores_generaciones = [
            "255, 99, 71",
            "60, 179, 113",
            "30, 144, 255",
            "255, 215, 0",
            "218, 112, 214",
            "244, 164, 96",
            "123, 104, 238"
        ]
    
        valores_generaciones = [81, 108, 91, 90, 90, 91, 93]
    
        # Asegurar que los nodos iniciales estén ordenados cronológicamente
        for gen, valor in enumerate(valores_generaciones):
            sources.append(gen)
            targets.append(len(generaciones))
            values.append(valor)
            colors.append(f"rgba({colores_generaciones[gen]}, {opacity})")
    
        valores_semestres = [
            [74, 104, 91, 84, 90, 88, 85],
            [28, 38, 46, 49, 50, 50, 51],
            [17, 22, 37, 33, 38, 39, 36],
            [16, 29, 34, 33, 38, 40, 35],
            [9, 22, 25, 26, 32, 34, 33],
            [5, 19, 24, 25, 27, 31, 31],
            [7, 17, 32, 31, 28, 30, 29],
            [2, 17, 27, 22, 23, 26, 31],
            [7, 17, 19, 24, 32, 27, 32],
        ]
    
        for semestre_index, valores in enumerate(valores_semestres):
            for gen, valor in enumerate(valores):
                sources.append(len(generaciones) + semestre_index)
                targets.append(len(generaciones) + semestre_index + 1)
                values.append(valor)
                colors.append(f"rgba({colores_generaciones[gen]}, {opacity})")
    
        valores_finales = {
            "Egresados": [24, 34, 26, 14, 7, 12, 13],
            "Titulado": [4, 6, 10, 9, 27, 27, 30],
            "Deserción": [52, 68, 51, 63, 54, 52, 47]
        }
    
        ultimo_semestre = len(generaciones) + semestres - 1
        targets_indices = [labels.index("Egresados"), labels.index("Titulado"), labels.index("Deserción")]
    
        for gen, color in enumerate(colores_generaciones):
            sources.extend([ultimo_semestre, ultimo_semestre, ultimo_semestre])
            targets.extend(targets_indices)
            values.extend([
                valores_finales["Egresados"][gen],
                valores_finales["Titulado"][gen],
                valores_finales["Deserción"][gen]
            ])
            colors.extend([f"rgba({color}, {opacity})"] * 3)
    
        fig = go.Figure(go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=labels,
                color=[f'rgba(30, 58, 138, {opacity})' for _ in labels]
            ),
            link=dict(
                source=sources,
                target=targets,
                value=values,
                color=colors
            )
        ))
    
        fig.update_layout(
            title="Diagrama de Sankey: Trayectoria Académica por Generación",
            font=dict(size=14),
            paper_bgcolor="rgba(0, 0, 0, 0)"
        )
    
        return fig
    
    # Mostrar el slider y el gráfico del Sankey
    opacity = st.slider("Ajustar opacidad:", 0.2, 1.0, 0.8, 0.1)
    st.plotly_chart(create_dynamic_sankey(opacity), use_container_width=True)
    
    # Datos para la primera tabla: Tasa de Retención
    retention_data = [
        ["2011", "81%", "86%", "91%", "93%"],
        ["2012", "67%", "78%", "89%", "88%"],
        ["2013", "82%", "85%", "87%", "82%"],
        ["2014", "81%", "88%", "80%", "91%"],
        ["2015", "71%", "85%", "91%", "92%"]
    ]
    
    # Tabla HTML - Fondo negro
    table_html_black = f"""
    <style>
        .table-black {{
            width: 100%;
            border-collapse: collapse;
            text-align: center;
        }}
        .table-black th {{
            background-color: #000000;
            color: #FFFFFF;
            padding: 8px;
        }}
        .table-black td {{
            border: 1px solid #ddd;
            padding: 8px;
        }}
    </style>
    <table class="table-black">
        <tr>
            <th rowspan="2">Cohorte</th>
            <th colspan="4">Tasa de Retención al</th>
        </tr>
        <tr>
            <th>Segundo Año</th>
            <th>Tercer Año</th>
            <th>Cuarto Año</th>
            <th>Quinto Año</th>
        </tr>
        {"".join(f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td></tr>" for row in retention_data)}
    </table>
    """
    
    # Datos para la segunda tabla: Tasa de Retención Femenina
    female_retention_data = [
        ["2011", "71%", "92%", "82%", "100%"],
        ["2012", "80%", "96%", "87%", "90%"],
        ["2013", "80%", "79%", "82%", "83%"],
        ["2014", "77%", "82%", "64%", "100%"],
        ["2015", "81%", "86%", "100%", "100%"]
    ]
    
    # Tabla HTML - Fondo #D9B1E0 para cabeceras y #862B96 para celdas de datos
    table_html_purple = f"""
    <style>
        .table-purple {{
            width: 100%;
            border-collapse: collapse;
            text-align: center;
        }}
        .table-purple th {{
            background-color: #5E1F83;
            color: white;
            padding: 8px;
        }}
        .table-purple td {{
            background-color: #B7A1D1; /* Fondo de celdas de datos */
            color: white; /* Texto blanco para contraste */
            border: 1px solid #ddd;
            padding: 8px;
        }}
    </style>
    <table class="table-purple">
        <tr>
            <th rowspan="2">Cohorte</th>
            <th colspan="4">Tasa de Retención Femenina al</th>
        </tr>
        <tr>
            <th>Segundo Año</th>
            <th>Tercer Año</th>
            <th>Cuarto Año</th>
            <th>Quinto Año</th>
        </tr>
        {"".join(f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td></tr>" for row in female_retention_data)}
    </table>
    """
    
    # Datos para la tabla: Tasa de Retención Masculina
    male_retention_data = [
        ["2011", "84%", "85%", "92%", "92%"],
        ["2012", "60%", "67%", "92%", "86%"],
        ["2013", "84%", "89%", "90%", "81%"],
        ["2014", "82%", "90%", "85%", "89%"],
        ["2015", "68%", "85%", "87%", "88%"]
    ]
    
    # Tabla HTML - Fondo #3D0C56 y texto contenido #B6A3C7
    table_html_male = f"""
    <style>
        .table-male {{
            width: 100%;
            border-collapse: collapse;
            text-align: center;
        }}
        .table-male th {{
            background-color: #2558C4; /* Fondo morado oscuro */
            color: white; /* Texto blanco */
            padding: 8px;
        }}
        .table-male td {{
            border: 1px solid #ddd;
            padding: 8px;
            background-color: #58A2D5; /* Celdas con fondo suave */
            color: white; /* Texto gris suave */
        }}
    </style>
    <table class="table-male">
        <tr>
            <th rowspan="2">Cohorte</th>
            <th colspan="4">Tasa de Retención Masculina al</th>
        </tr>
        <tr>
            <th>Segundo Año</th>
            <th>Tercer Año</th>
            <th>Cuarto Año</th>
            <th>Quinto Año</th>
        </tr>
        {"".join(f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td></tr>" for row in male_retention_data)}
    </table>
    """
    
    # Streamlit Layout
    col1, col2, col3 = st.columns([1, 5, 1])
    
    # Mostrar tablas en la columna central
    with col2:
        st.write("### Tasa de Retención por Cohorte")
        st.markdown(table_html_black, unsafe_allow_html=True)
        st.write("### Tasa de Retención Femenina")
        st.markdown(table_html_purple, unsafe_allow_html=True)
        st.write("### Tasa de Retención Masculina")
        st.markdown(table_html_male, unsafe_allow_html=True)
    
    
    generation_data = {
        "Generación 2009": {
            "Bajas": {"General": 52, "Hombres": 38, "Mujeres": 14},
            "Egresados": {"General": 24, "Hombres": 11, "Mujeres": 13},
            "Titulados": {"General": 4, "Hombres": 1, "Mujeres": 3},
        },
        "Generación 2010": {
            "Bajas": {"General": 68, "Hombres": 53, "Mujeres": 15},
            "Egresados": {"General": 34, "Hombres": 20, "Mujeres": 14},
            "Titulados": {"General": 6, "Hombres": 6, "Mujeres": 0},
        },
        "Generación 2011": {
            "Bajas": {"General": 51, "Hombres": 41, "Mujeres": 10},
            "Egresados": {"General": 26, "Hombres": 22, "Mujeres": 4},
            "Titulados": {"General": 10, "Hombres": 9, "Mujeres": 1},
        },
        "Generación 2012": {
            "Bajas": {"General": 63, "Hombres": 46, "Mujeres": 17},
            "Egresados": {"General": 14, "Hombres": 9, "Mujeres": 5},
            "Titulados": {"General": 9, "Hombres": 3, "Mujeres": 6},
        },
        "Generación 2013": {
            "Bajas": {"General": 54, "Hombres": 32, "Mujeres": 22},
            "Egresados": {"General": 7, "Hombres": 5, "Mujeres": 2},
            "Titulados": {"General": 27, "Hombres": 16, "Mujeres": 11},
        },
        "Generación 2014": {
            "Bajas": {"General": 52, "Hombres": 40, "Mujeres": 12},
            "Egresados": {"General": 12, "Hombres": 8, "Mujeres": 4},
            "Titulados": {"General": 27, "Hombres": 22, "Mujeres": 5},
        },
        "Generación 2015": {
            "Bajas": {"General": 47, "Hombres": 39, "Mujeres": 8},
            "Egresados": {"General": 13, "Hombres": 6, "Mujeres": 7},
            "Titulados": {"General": 30, "Hombres": 19, "Mujeres": 11},
        },
    }

    # Índice de rezago por generación
    rezago_data = {
        "Generación 2009": 24.69135802,
        "Generación 2010": 16.66666667,
        "Generación 2011": 4.395604396,
        "Generación 2012": 4.444444444,
        "Generación 2013": 2.222222222,
        "Generación 2014": 0,
        "Generación 2015": 3.191489362,
    }
    
    # Índice de rezago femenino
    rezago_femenino_data = {
        "Generación 2009": 23.33333333,
        "Generación 2010": 24.13793103,
        "Generación 2011": 11.76470588,
        "Generación 2012": 6.666666667,
        "Generación 2013": 0,
        "Generación 2014": 0,
        "Generación 2015": 0,
    }
    
    # Índice de rezago masculino
    rezago_masculino_data = {
        "Generación 2009": 25.49019608,
        "Generación 2010": 13.92405063,
        "Generación 2011": 2.702702703,
        "Generación 2012": 3.333333333,
        "Generación 2013": 3.636363636,
        "Generación 2014": 0,
        "Generación 2015": 4.411764706,
    } 

    # Datos ajustados a 9 elementos por fila
    valores_semestres = [
        [74, 28, 17, 16, 9, 5, 7, 2, 7, 7],
        [104, 38, 22, 29, 22, 19, 17, 17, 17, 17],
        [91, 46, 37, 34, 25, 24, 32, 27, 19, 17],
        [84, 49, 33, 33, 26, 25, 31, 22, 24, 24],
        [90, 50, 38, 38, 32, 27, 28, 23, 32, 32],
        [88, 50, 39, 40, 34, 31, 30, 26, 27, 27],
        [85, 51, 36, 35, 33, 31, 29, 31, 32, 32],
    ]
    
    # DataFrame con los valores de los semestres
    df_semestres = pd.DataFrame(valores_semestres, index=list(generation_data.keys()), columns=[f"Semestre {i+1}" for i in range(10)])
    


    GRAPH_WIDTH = 130
    GRAPH_HEIGHT = 130
    
    def make_donut(input_response, input_text, input_color, title_text=None):
        chart_color = {
            "blue": ['#58A2D5', '#2558C4'],
            "pink": ['#D9B1E0', '#862B96'],
            "green": ['#27AE60', '#12783D'],
            "orange": ['#EFB444', '#F6E29D'],
            "red": ['#E74C3C', '#781F16']
        }.get(input_color, ['#dddddd', '#aaaaaa'])
    
        # Datos para el gráfico
        source = pd.DataFrame({
            "Topic": ['', input_text],
            "% value": [100 - input_response, input_response]
        })
        source_bg = pd.DataFrame({
            "Topic": ['', input_text],
            "% value": [100, 0]
        })
    
        # Gráfico principal de dona
        plot = alt.Chart(source).mark_arc(innerRadius=45, cornerRadius=25).encode(
            theta="% value",
            color=alt.Color("Topic:N",
                            scale=alt.Scale(
                                domain=[input_text, ''],
                                range=chart_color),
                            legend=None),
        ).properties(width=130, height=130)
    
        # Texto del porcentaje
        text = plot.mark_text(
            align='center',
            font="Lato",
            fontSize=25,
            fontWeight=700
        ).encode(text=alt.value(f'{input_response} %'))
    
        # Fondo de la dona
        plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=45, cornerRadius=20).encode(
            theta="% value",
            color=alt.Color("Topic:N",
                            scale=alt.Scale(
                                domain=[input_text, ''],
                                range=chart_color),
                            legend=None),
        ).properties(width=130, height=130)
    
        # Título (texto encima del gráfico)
        if title_text:
            title = alt.Chart(pd.DataFrame({'text': [title_text]})).mark_text(
                align='center',
                fontSize=16,
                fontWeight='bold',
                color=chart_color[0]
            ).encode(text='text:N')
    
            # Concatenar título y gráfico
            return alt.vconcat(title, plot_bg + plot + text)
        else:
            # Texto en blanco para alinear las gráficas generales
            blank_title = alt.Chart(pd.DataFrame({'text': ['‎ ‎ ‎ ‎ ']})).mark_text(
                align='center',
                fontSize=16,  # Tamaño similar al texto de hombres y mujeres
                fontWeight='bold',
                color="#ffffff"  # Texto blanco para que sea invisible
            ).encode(text='text:N')
    
            return alt.vconcat(blank_title, plot_bg + plot + text)

    
    # Dropdown generación
    generaciones = list(generation_data.keys())
    selected_generacion = st.selectbox("Selecciona una generación:", generaciones)
    
    
    col1, col2, col3 = st.columns(3)
    
    # Mostrar el índice de rezago general en la columna 1
    with col1:
        indice_rezago = rezago_data[selected_generacion]
        st.metric(label="Índice de Rezago", value=f"{indice_rezago:.2f}")
    # Mostrar el índice de rezago femenino
        indice_rezago_femenino = rezago_femenino_data[selected_generacion]
        st.metric(label="Índice de Rezago Femenino", value=f"{indice_rezago_femenino:.2f}")
    
        # Mostrar el índice de rezago masculino
        indice_rezago_masculino = rezago_masculino_data[selected_generacion]
        st.metric(label="Índice de Rezago Masculino", value=f"{indice_rezago_masculino:.2f}")

    # Mostrar los valores de la generación seleccionada
    with col2:
        st.write("Estudiantes inscritos por semestre para la generación seleccionada:")
        df = pd.DataFrame({
            "Semestre": range(1, 11),
            "Estudiantes inscritos": df_semestres.loc[selected_generacion].values
        })
        st.dataframe(df)

    
    # Columnas con gráficas de dona dinámicas basadas en la generación seleccionada
    col1, col2, col3 = st.columns([1, 1, 1])
    
    # Totales por generación
    valores_generaciones = [81, 108, 91, 90, 90, 91, 93]  # Totales de estudiantes por generación en orden 2009-2015
    totales_generacion = dict(zip(generation_data.keys(), valores_generaciones))  # Mapeo generación -> total
    
    def calcular_porcentajes(data, total):
        """
        Convierte los valores de 'General', 'Hombres', y 'Mujeres' a porcentajes basados en el total dado.
        """
        for categoria, valores in data.items():
            for grupo in ["General", "Hombres", "Mujeres"]:
                valores[grupo] = round((valores[grupo] / total) * 100, 2)  # Convertir a porcentaje
    
    # Convertir los valores de generation_data a porcentajes
    for generacion, data in generation_data.items():
        calcular_porcentajes(data, totales_generacion[generacion])
        categories = ["Bajas", "Egresados", "Titulados"]
        colors = ["red", "orange", "green"]
    
    for col, category, color in zip([col1, col2, col3], categories, colors):
        with col:
            st.title(category)
    
            # Gráfica general
            general = generation_data[selected_generacion][category]["General"]
            st.altair_chart(make_donut(general, "General", color), use_container_width=True)
    
            # Gráfica de hombres con texto encima
            hombres = generation_data[selected_generacion][category]["Hombres"]
            hombres_percent = round((hombres / general) * 100, 1)
            st.altair_chart(make_donut(hombres_percent, "Hombres", "blue", title_text="Hombres"), use_container_width=True)
    
            # Gráfica de mujeres con texto encima
            mujeres = generation_data[selected_generacion][category]["Mujeres"]
            mujeres_percent = round((mujeres / general) * 100, 1)
            st.altair_chart(make_donut(mujeres_percent, "Mujeres", "pink", title_text="Mujeres"), use_container_width=True)
            
            
if "Física 2016" in tags:
    
    # Diagrama de Sankey modificado para generaciones 2016-2020
    st.subheader("Progreso de los alumnos en tiempo y forma por Semestre")
    st.subheader("Diagrama de Sankey por Semestre")
    
    # Definición de la función para crear el diagrama de Sankey
    def create_dynamic_sankey(opacity=0.8):
        # Definir nodos manualmente en el orden deseado
        generaciones = ["Generación 2016", "Generación 2017", "Generación 2018", "Generación 2019", "Generación 2020"]
        semestres = 8
    
        # Reordenar nodos finales para que "Egresados" y "Titulado" estén arriba
        nodos_finales = ["Egresados", "Titulado", "Deserción"]
        labels = generaciones + [f"Semestre {i+1}" for i in range(semestres)] + nodos_finales
    
        sources = []
        targets = []
        values = []
        colors = []
    
        colores_generaciones = [
            "255, 99, 71",
            "60, 179, 113",
            "30, 144, 255",
            "255, 215, 0",
            "218, 112, 214"
        ]
    
        valores_generaciones = [97, 125, 122, 219, 374]
    
        # Asegurar que los nodos iniciales estén ordenados cronológicamente
        for gen, valor in enumerate(valores_generaciones):
            sources.append(gen)
            targets.append(len(generaciones))
            values.append(valor)
            colors.append(f"rgba({colores_generaciones[gen]}, {opacity})")
    
        valores_semestres = [
            [85, 112, 111, 184, 301],
            [63, 97, 93, 116, 120],
            [51, 90, 97, 102, 111],
            [45, 66, 63, 84, 109],
            [41, 53, 74, 80, 98],
            [37, 38, 56, 76, 101],
            [28, 44, 45, 68, 106],
            [26, 35, 48, 44, 0]
        ]
    
        for semestre_index, valores in enumerate(valores_semestres):
            for gen, valor in enumerate(valores):
                sources.append(len(generaciones) + semestre_index)
                targets.append(len(generaciones) + semestre_index + 1)
                values.append(valor)
                colors.append(f"rgba({colores_generaciones[gen]}, {opacity})")
    
        valores_finales = {
            "Egresados": [13, 19, 23, 22, 0],
            "Titulado": [31, 39, 36, 12, 0],
            "Deserción": [45, 40, 36, 76, 101]
        }
    
        ultimo_semestre = len(generaciones) + semestres - 1
        targets_indices = [labels.index("Egresados"), labels.index("Titulado"), labels.index("Deserción")]
    
        for gen, color in enumerate(colores_generaciones):
            sources.extend([ultimo_semestre, ultimo_semestre, ultimo_semestre])
            targets.extend(targets_indices)
            values.extend([
                valores_finales["Egresados"][gen],
                valores_finales["Titulado"][gen],
                valores_finales["Deserción"][gen]
            ])
            colors.extend([f"rgba({color}, {opacity})"] * 3)
    
        fig = go.Figure(go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=labels,
                color=[f'rgba(30, 58, 138, {opacity})' for _ in labels]
            ),
            link=dict(
                source=sources,
                target=targets,
                value=values,
                color=colors
            )
        ))
    
        fig.update_layout(
            title="Diagrama de Sankey: Trayectoria Académica por Generación",
            font=dict(size=14),
            paper_bgcolor="rgba(0, 0, 0, 0)"
        )
    
        return fig
    
    # Mostrar el slider y el gráfico del Sankey
    opacity = st.slider("Ajustar opacidad:", 0.2, 1.0, 0.8, 0.1)
    st.plotly_chart(create_dynamic_sankey(opacity), use_container_width=True)


    # Datos para la primera tabla: Tasa de Retención
    retention_data = [
        ["2016", "76%", "88%", "92%", "97%", "43%", "36%"],
        ["2017", "82%", "88%", "91%", "96%", "46%", "46%"],
        ["2018", "86%", "90%", "99%", "94%", "48%", "31%"],
        ["2019", "75%", "89%", "92%", "92%", "57%", ""],
        ["2020", "86%", "86%", "90%", "92%", "", ""],
        ["2021", "74%", "85%", "91%", "", "", ""],
        ["2022", "70%", "78%", "", "", "", ""],
        ["2023", "60%", "", "", "", "", ""]
    ]
    
    # Tabla HTML - Fondo negro
    table_html_black = f"""
    <style>
        .table-black {{
            width: 100%;
            border-collapse: collapse;
            text-align: center;
        }}
        .table-black th {{
            background-color: #000000;
            color: #FFFFFF;
            padding: 8px;
        }}
        .table-black td {{
            border: 1px solid #ddd;
            padding: 8px;
        }}
    </style>
    <table class="table-black">
        <tr>
            <th rowspan="2">Cohorte</th>
            <th colspan="6">Tasa de Retención al</th>
        </tr>
        <tr>
            <th>Segundo Año</th>
            <th>Tercer Año</th>
            <th>Cuarto Año</th>
            <th>Quinto Año</th>
            <th>Sexto Año</th>
            <th>Séptimo Año</th>
        </tr>
        {"".join(f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td><td>{row[5]}</td><td>{row[6]}</td></tr>" for row in retention_data)}
    </table>
    """
    
    # Datos para la segunda tabla: Tasa de Retención Femenina
    female_retention_data = [
        ["2016", "71%", "85%", "88%", "100%", "53%", "13%"],
        ["2017", "72%", "83%", "100%", "100%", "53%", "13%"],
        ["2018", "86%", "96%", "100%", "96%", "27%", "17%"],
        ["2019", "79%", "83%", "91%", "100%", "52%", ""],
        ["2020", "84%", "88%", "88%", "90%", "", ""],
        ["2021", "73%", "86%", "89%", "", "", ""],
        ["2022", "71%", "78%", "", "", "", ""],
        ["2023", "55%", "", "", "", "", ""]
    ]
    
    # Tabla HTML - Fondo #D9B1E0 para cabeceras y #862B96 para celdas de datos
    table_html_purple = f"""
    <style>
        .table-purple {{
            width: 100%;
            border-collapse: collapse;
            text-align: center;
        }}
        .table-purple th {{
            background-color: #5E1F83;
            color: white;
            padding: 8px;
        }}
        .table-purple td {{
            background-color: #B7A1D1; /* Fondo de celdas de datos */
            color: white; /* Texto blanco para contraste */
            border: 1px solid #ddd;
            padding: 8px;
        }}
    </style>
    <table class="table-purple">
        <tr>
            <th rowspan="2">Cohorte</th>
            <th colspan="6">Tasa de Retención Femenina al</th>
        </tr>
        <tr>
            <th>Segundo Año</th>
            <th>Tercer Año</th>
            <th>Cuarto Año</th>
            <th>Quinto Año</th>
            <th>Sexto Año</th>
            <th>Séptimo Año</th>
        </tr>
        {"".join(f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td><td>{row[5]}</td><td>{row[6]}</td></tr>" for row in female_retention_data)}
    </table>
    """
    
    # Datos para la tabla: Tasa de Retención Masculina
    male_retention_data = [
        ["2016", "78%", "89%", "94%", "96%", "40%", "47%"],
        ["2017", "85%", "89%", "89%", "96%", "45%", "55%"],
        ["2018", "86%", "88%", "99%", "93%", "55%", "33%"],
        ["2019", "74%", "91%", "92%", "90%", "59%", ""],
        ["2020", "86%", "86%", "90%", "93%", "", ""],
        ["2021", "74%", "85%", "91%", "", "", ""],
        ["2022", "70%", "78%", "", "", "", ""],
        ["2023", "61%", "", "", "", "", ""]
    ]
    
    # Tabla HTML - Fondo #3D0C56 y texto contenido #B6A3C7
    table_html_male = f"""
    <style>
        .table-male {{
            width: 100%;
            border-collapse: collapse;
            text-align: center;
        }}
        .table-male th {{
            background-color: #2558C4; /* Fondo morado oscuro */
            color: white; /* Texto blanco */
            padding: 8px;
        }}
        .table-male td {{
            border: 1px solid #ddd;
            padding: 8px;
            background-color: #58A2D5; /* Celdas con fondo suave */
            color: white; /* Texto gris suave */
        }}
    </style>
    <table class="table-male">
        <tr>
            <th rowspan="2">Cohorte</th>
            <th colspan="6">Tasa de Retención Masculina al</th>
        </tr>
        <tr>
            <th>Segundo Año</th>
            <th>Tercer Año</th>
            <th>Cuarto Año</th>
            <th>Quinto Año</th>
            <th>Sexto Año</th>
            <th>Séptimo Año</th>
        </tr>
        {"".join(f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td><td>{row[5]}</td><td>{row[6]}</td></tr>" for row in male_retention_data)}
    </table>
    """

    # Streamlit Layout
    col1, col2, col3 = st.columns([1, 5, 1])
    
    # Mostrar tablas en la columna central
    with col2:
        st.write("### Tasa de Retención por Cohorte")
        st.markdown(table_html_black, unsafe_allow_html=True)
        st.write("### Tasa de Retención Femenina")
        st.markdown(table_html_purple, unsafe_allow_html=True)
        st.write("### Tasa de Retención Masculina")
        st.markdown(table_html_male, unsafe_allow_html=True)
    
    
    generation_data = {
        "Generación 2016": {
            "Bajas": {"General": 36, "Hombres": 27, "Mujeres": 9},
            "Egresados": {"General": 10, "Hombres": 8, "Mujeres": 2},
            "Titulados": {"General": 17, "Hombres": 12, "Mujeres": 5},
        },
        "Generación 2017": {
            "Bajas": {"General": 28, "Hombres": 22, "Mujeres": 6},
            "Egresados": {"General": 11, "Hombres": 4, "Mujeres": 7},
            "Titulados": {"General": 14, "Hombres": 9, "Mujeres": 5},
        },
        "Generación 2018": {
            "Bajas": {"General": 36, "Hombres": 32, "Mujeres": 4},
            "Egresados": {"General": 12, "Hombres": 9, "Mujeres": 3},
            "Titulados": {"General": 9, "Hombres": 9, "Mujeres": 0},
        },
        "Generación 2019": {
            "Bajas": {"General": 47, "Hombres": 35, "Mujeres": 12},
            "Egresados": {"General": 16, "Hombres": 9, "Mujeres": 7},
            "Titulados": {"General": 8, "Hombres": 5, "Mujeres": 3},
        },
        "Generación 2020": {
            "Bajas": {"General": 49, "Hombres": 34, "Mujeres": 15},
            "Egresados": {"General": 1, "Hombres": 0.000001, "Mujeres": 0.000001},
            "Titulados": {"General": 1, "Hombres": 0.000001, "Mujeres": 0.000001},
        },
    }



    
    # Índice de rezago por generación
    rezago_data = {
        "Generación 2016": 14.43298969,
        "Generación 2017": 25.6,
        "Generación 2018": 22.13114754,
        "Generación 2019": 49.0990991,
        "Generación 2020": 72.99465241,
    }
    
    # Índice de rezago femenino
    rezago_femenino_data = {
        "Generación 2016": 7.142857143,
        "Generación 2017": 16,
        "Generación 2018": 10.71428571,
        "Generación 2019": 57.69230769,
        "Generación 2020": 72.04301075,
    }
    
    # Índice de rezago masculino
    rezago_masculino_data = {
        "Generación 2016": 17.39130435,
        "Generación 2017": 28,
        "Generación 2018": 25.53191489,
        "Generación 2019": 46.47058824,
        "Generación 2020": 73.30960854,
    }
    
    # Datos ajustados a 9 elementos por fila
    valores_semestres = [
    [85, 63, 51, 45, 41, 37, 28, 26, "", ""],
    [112, 97, 90, 66, 53, 38, 44, 35, "", ""],
    [111, 93, 97, 63, 74, 56, 45, 48, "", ""],
    [184, 116, 102, 84, 80, 76, 68, 44, "", ""],
    [301, 120, 111, 109, 98, 101, 106, "", ""]
    ]
    
    # DataFrame con los valores de los semestres
    df_semestres = pd.DataFrame(valores_semestres, index=list(generation_data.keys()), columns=[f"Semestre {i+1}" for i in range(10)])
    
    
    
    GRAPH_WIDTH = 130
    GRAPH_HEIGHT = 130
    
    def make_donut(input_response, input_text, input_color, title_text=None):
        chart_color = {
            "blue": ['#58A2D5', '#2558C4'],
            "pink": ['#D9B1E0', '#862B96'],
            "green": ['#27AE60', '#12783D'],
            "orange": ['#EFB444', '#F6E29D'],
            "red": ['#E74C3C', '#781F16']
        }.get(input_color, ['#dddddd', '#aaaaaa'])
    
        # Datos para el gráfico
        source = pd.DataFrame({
            "Topic": ['', input_text],
            "% value": [100 - input_response, input_response]
        })
        source_bg = pd.DataFrame({
            "Topic": ['', input_text],
            "% value": [100, 0]
        })
    
        # Gráfico principal de dona
        plot = alt.Chart(source).mark_arc(innerRadius=45, cornerRadius=25).encode(
            theta="% value",
            color=alt.Color("Topic:N",
                            scale=alt.Scale(
                                domain=[input_text, ''],
                                range=chart_color),
                            legend=None),
        ).properties(width=130, height=130)
    
        # Texto del porcentaje
        text = plot.mark_text(
            align='center',
            font="Lato",
            fontSize=25,
            fontWeight=700
        ).encode(text=alt.value(f'{input_response} %'))
    
        # Fondo de la dona
        plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=45, cornerRadius=20).encode(
            theta="% value",
            color=alt.Color("Topic:N",
                            scale=alt.Scale(
                                domain=[input_text, ''],
                                range=chart_color),
                            legend=None),
        ).properties(width=130, height=130)
    
        # Título (texto encima del gráfico)
        if title_text:
            title = alt.Chart(pd.DataFrame({'text': [title_text]})).mark_text(
                align='center',
                fontSize=16,
                fontWeight='bold',
                color=chart_color[0]
            ).encode(text='text:N')
    
            # Concatenar título y gráfico
            return alt.vconcat(title, plot_bg + plot + text)
        else:
            # Texto en blanco para alinear las gráficas generales
            blank_title = alt.Chart(pd.DataFrame({'text': ['‎ ‎ ‎ ‎ ']})).mark_text(
                align='center',
                fontSize=16,  # Tamaño similar al texto de hombres y mujeres
                fontWeight='bold',
                color="#ffffff"  # Texto blanco para que sea invisible
            ).encode(text='text:N')
    
            return alt.vconcat(blank_title, plot_bg + plot + text)
    
    
    # Dropdown generación
    generaciones = list(generation_data.keys())
    selected_generacion = st.selectbox("Selecciona una generación:", generaciones)
    
    
    col1, col2, col3 = st.columns(3)
    
    # Mostrar el índice de rezago general en la columna 1
    with col1:
        indice_rezago = rezago_data[selected_generacion]
        st.metric(label="Índice de Rezago", value=f"{indice_rezago:.2f}")
    # Mostrar el índice de rezago femenino
        indice_rezago_femenino = rezago_femenino_data[selected_generacion]
        st.metric(label="Índice de Rezago Femenino", value=f"{indice_rezago_femenino:.2f}")
    
        # Mostrar el índice de rezago masculino
        indice_rezago_masculino = rezago_masculino_data[selected_generacion]
        st.metric(label="Índice de Rezago Masculino", value=f"{indice_rezago_masculino:.2f}")
    
    # Mostrar los valores de la generación seleccionada
    with col2:
        st.write("Estudiantes inscritos por semestre para la generación seleccionada:")
        df = pd.DataFrame({
            "Semestre": range(1, 11),
            "Estudiantes inscritos": df_semestres.loc[selected_generacion].values
        })
        st.dataframe(df)
    
    
    # Columnas con gráficas de dona dinámicas basadas en la generación seleccionada
    col1, col2, col3 = st.columns([1, 1, 1])
    
    # Totales por generación
    valores_generaciones = [97, 125, 122, 219, 374]  # Totales de estudiantes por generación en orden 2009-2015
    totales_generacion = dict(zip(generation_data.keys(), valores_generaciones))  # Mapeo generación -> total
    
    def calcular_porcentajes(data, total):
        """
        Convierte los valores de 'General', 'Hombres', y 'Mujeres' a porcentajes basados en el total dado.
        """
        for categoria, valores in data.items():
            for grupo in ["General", "Hombres", "Mujeres"]:
                valores[grupo] = round((valores[grupo] / total) * 100, 2)  # Convertir a porcentaje
    
    # Convertir los valores de generation_data a porcentajes
    for generacion, data in generation_data.items():
        calcular_porcentajes(data, totales_generacion[generacion])
        categories = ["Bajas", "Egresados", "Titulados"]
        colors = ["red", "orange", "green"]
        
        
        
    
    for col, category, color in zip([col1, col2, col3], categories, colors):
        with col:
            st.title(category)
    
            # Gráfica general
            general = generation_data[selected_generacion][category]["General"]
            st.altair_chart(make_donut(general, "General", color), use_container_width=True)
            
    
            # Gráfica de hombres con texto encima
            hombres = generation_data[selected_generacion][category]["Hombres"]
            hombres_percent = round((hombres / general) * 100, 1)
            st.altair_chart(make_donut(hombres_percent, "Hombres", "blue", title_text="Hombres"), use_container_width=True)
    
            # Gráfica de mujeres con texto encima
            mujeres = generation_data[selected_generacion][category]["Mujeres"]
            mujeres_percent = round((mujeres / general) * 100, 1)
            st.altair_chart(make_donut(mujeres_percent, "Mujeres", "pink", title_text="Mujeres"), use_container_width=True)
            
    
if "Aplicada 2016" in tags :
  
    # Diagrama de Sankey modificado para generaciones 2016-2020
    st.subheader("Progreso de los alumnos en tiempo y forma por Semestre")
    st.subheader("Diagrama de Sankey por Semestre")
    
    # Definición de la función para crear el diagrama de Sankey
    def create_dynamic_sankey(opacity=0.8):
        # Definir nodos manualmente en el orden deseado
        generaciones = ["Generación 2016", "Generación 2017", "Generación 2018", "Generación 2019", "Generación 2020"]
        semestres = 8
    
        # Reordenar nodos finales para que "Egresados" y "Titulado" estén arriba
        nodos_finales = ["Egresados", "Titulado", "Deserción"]
        labels = generaciones + [f"Semestre {i+1}" for i in range(semestres)] + nodos_finales
    
        sources = []
        targets = []
        values = []
        colors = []
    
        colores_generaciones = [
            "255, 99, 71",
            "60, 179, 113",
            "30, 144, 255",
            "255, 215, 0",
            "218, 112, 214"
        ]
    
        valores_generaciones = [65, 76, 76, 107, 127]
    
        # Asegurar que los nodos iniciales estén ordenados cronológicamente
        for gen, valor in enumerate(valores_generaciones):
            sources.append(gen)
            targets.append(len(generaciones))
            values.append(valor)
            colors.append(f"rgba({colores_generaciones[gen]}, {opacity})")
    
        valores_semestres = [
            [56, 71, 72, 78, 109],
            [41, 52, 54, 48, 41],
            [30, 41, 38, 49, 38],
            [23, 33, 24, 42, 40],
            [21, 26, 27, 41, 43],
            [22, 19, 21, 38, 41],
            [16, 22, 23, 34, 40],
            [15, 26, 29, 30, ""]
        ]
    
        for semestre_index, valores in enumerate(valores_semestres):
            for gen, valor in enumerate(valores):
                sources.append(len(generaciones) + semestre_index)
                targets.append(len(generaciones) + semestre_index + 1)
                values.append(valor)
                colors.append(f"rgba({colores_generaciones[gen]}, {opacity})")
    
        valores_finales = {
            "Egresados": [10, 11, 12, 16, ""],
            "Titulado": [17, 14, 9, 8, ""],
            "Deserción": [36, 28, 36, 47, ""]
        }
    
        ultimo_semestre = len(generaciones) + semestres - 1
        targets_indices = [labels.index("Egresados"), labels.index("Titulado"), labels.index("Deserción")]
    
        for gen, color in enumerate(colores_generaciones):
            sources.extend([ultimo_semestre, ultimo_semestre, ultimo_semestre])
            targets.extend(targets_indices)
            values.extend([
                valores_finales["Egresados"][gen],
                valores_finales["Titulado"][gen],
                valores_finales["Deserción"][gen]
            ])
            colors.extend([f"rgba({color}, {opacity})"] * 3)
    
        fig = go.Figure(go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=labels,
                color=[f'rgba(30, 58, 138, {opacity})' for _ in labels]
            ),
            link=dict(
                source=sources,
                target=targets,
                value=values,
                color=colors
            )
        ))
    
        fig.update_layout(
            title="Diagrama de Sankey: Trayectoria Académica por Generación",
            font=dict(size=14),
            paper_bgcolor="rgba(0, 0, 0, 0)"
        )
    
        return fig
    
    # Mostrar el slider y el gráfico del Sankey
    opacity = st.slider("Ajustar opacidad:", 0.2, 1.0, 0.8, 0.1)
    st.plotly_chart(create_dynamic_sankey(opacity), use_container_width=True)
    
    
    # Datos para la primera tabla: Tasa de Retención
    retention_data = [
        ["2016", "76%", "88%", "92%", "97%", "43%", "36%"],
        ["2017", "82%", "88%", "91%", "96%", "46%", "46%"],
        ["2018", "86%", "90%", "99%", "94%", "48%", "31%"],
        ["2019", "75%", "89%", "92%", "92%", "57%", ""],
        ["2020", "86%", "86%", "90%", "92%", "", ""],
        ["2021", "74%", "85%", "91%", "", "", ""],
        ["2022", "70%", "78%", "", "", "", ""],
        ["2023", "60%", "", "", "", "", ""]
    ]
    
    # Tabla HTML - Fondo negro
    table_html_black = f"""
    <style>
        .table-black {{
            width: 100%;
            border-collapse: collapse;
            text-align: center;
        }}
        .table-black th {{
            background-color: #000000;
            color: #FFFFFF;
            padding: 8px;
        }}
        .table-black td {{
            border: 1px solid #ddd;
            padding: 8px;
        }}
    </style>
    <table class="table-black">
        <tr>
            <th rowspan="2">Cohorte</th>
            <th colspan="6">Tasa de Retención al</th>
        </tr>
        <tr>
            <th>Segundo Año</th>
            <th>Tercer Año</th>
            <th>Cuarto Año</th>
            <th>Quinto Año</th>
            <th>Sexto Año</th>
            <th>Séptimo Año</th>
        </tr>
        {"".join(f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td><td>{row[5]}</td><td>{row[6]}</td></tr>" for row in retention_data)}
    </table>
    """
    
    # Datos para la segunda tabla: Tasa de Retención Femenina
    female_retention_data = [
        ["2016", "71%", "85%", "88%", "100%", "53%", "13%"],
        ["2017", "72%", "83%", "100%", "100%", "53%", "13%"],
        ["2018", "86%", "96%", "100%", "96%", "27%", "17%"],
        ["2019", "79%", "83%", "91%", "100%", "52%", ""],
        ["2020", "84%", "88%", "88%", "90%", "", ""],
        ["2021", "73%", "86%", "89%", "", "", ""],
        ["2022", "71%", "78%", "", "", "", ""],
        ["2023", "55%", "", "", "", "", ""]
    ]
    
    # Datos para la primera tabla: Tasa de Retención
    retention_data = [
        ["2016", "74%", "83%", "88%", "97%", "47%", "56%"],
        ["2017", "68%", "78%", "92%", "95%", "55%", "42%"],
        ["2018", "82%", "84%", "96%", "98%", "61%", "50%"],
        ["2019", "64%", "88%", "100%", "97%", "49%", ""],
        ["2020", "77%", "88%", "97%", "96%", "", ""],
        ["2021", "76%", "77%", "92%", "", "", ""],
        ["2022", "64%", "71%", "", "", "", ""],
        ["2023", "58%", "", "", "", "", ""]
    ]
    
    # Tabla HTML - Fondo negro
    table_html_black = f"""
    <style>
        .table-black {{
            width: 100%;
            border-collapse: collapse;
            text-align: center;
        }}
        .table-black th {{
            background-color: #000000;
            color: #FFFFFF;
            padding: 8px;
        }}
        .table-black td {{
            border: 1px solid #ddd;
            padding: 8px;
        }}
    </style>
    <table class="table-black">
        <tr>
            <th rowspan="2">Cohorte</th>
            <th colspan="6">Tasa de Retención al</th>
        </tr>
        <tr>
            <th>Segundo Año</th>
            <th>Tercer Año</th>
            <th>Cuarto Año</th>
            <th>Quinto Año</th>
            <th>Sexto Año</th>
            <th>Séptimo Año</th>
        </tr>
        {"".join(f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td><td>{row[5]}</td><td>{row[6]}</td></tr>" for row in retention_data)}
    </table>
    """
    
    # Datos para la segunda tabla: Tasa de Retención Femenina
    female_retention_data = [
        ["2016", "63%", "100%", "80%", "100%", "38%", "33%"],
        ["2017", "88%", "89%", "92%", "96%", "50%", "36%"],
        ["2018", "100%", "75%", "100%", "100%", "89%", "38%"],
        ["2019", "70%", "86%", "100%", "100%", "44%", ""],
        ["2020", "70%", "97%", "97%", "96%", "", ""],
        ["2021", "73%", "86%", "96%", "", "", ""],
        ["2022", "58%", "72%", "", "", "", ""],
        ["2023", "55%", "", "", "", "", ""]
    ]
    
    # Tabla HTML - Fondo #D9B1E0 para cabeceras y #862B96 para celdas de datos
    table_html_purple = f"""
    <style>
        .table-purple {{
            width: 100%;
            border-collapse: collapse;
            text-align: center;
        }}
        .table-purple th {{
            background-color: #5E1F83;
            color: white;
            padding: 8px;
        }}
        .table-purple td {{
            background-color: #B7A1D1; /* Fondo de celdas de datos */
            color: white; /* Texto blanco para contraste */
            border: 1px solid #ddd;
            padding: 8px;
        }}
    </style>
    <table class="table-purple">
        <tr>
            <th rowspan="2">Cohorte</th>
            <th colspan="6">Tasa de Retención Femenina al</th>
        </tr>
        <tr>
            <th>Segundo Año</th>
            <th>Tercer Año</th>
            <th>Cuarto Año</th>
            <th>Quinto Año</th>
            <th>Sexto Año</th>
            <th>Séptimo Año</th>
        </tr>
        {"".join(f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td><td>{row[5]}</td><td>{row[6]}</td></tr>" for row in female_retention_data)}
    </table>
    """
    
    # Datos para la tabla: Tasa de Retención Masculina
    male_retention_data = [
        ["2016", "78%", "79%", "90%", "96%", "50%", "62%"],
        ["2017", "61%", "72%", "92%", "94%", "59%", "45%"],
        ["2018", "78%", "86%", "95%", "98%", "55%", "55%"],
        ["2019", "62%", "90%", "100%", "95%", "51%", ""],
        ["2020", "81%", "84%", "96%", "96%", "", ""],
        ["2021", "77%", "72%", "89%", "", "", ""],
        ["2022", "66%", "71%", "", "", "", ""],
        ["2023", "59%", "", "", "", "", ""]
    ]
    
    # Tabla HTML - Fondo #3D0C56 y texto contenido #B6A3C7
    table_html_male = f"""
    <style>
        .table-male {{
            width: 100%;
            border-collapse: collapse;
            text-align: center;
        }}
        .table-male th {{
            background-color: #2558C4; /* Fondo morado oscuro */
            color: white; /* Texto blanco */
            padding: 8px;
        }}
        .table-male td {{
            border: 1px solid #ddd;
            padding: 8px;
            background-color: #58A2D5; /* Celdas con fondo suave */
            color: white; /* Texto gris suave */
        }}
    </style>
    <table class="table-male">
        <tr>
            <th rowspan="2">Cohorte</th>
            <th colspan="6">Tasa de Retención Masculina al</th>
        </tr>
        <tr>
            <th>Segundo Año</th>
            <th>Tercer Año</th>
            <th>Cuarto Año</th>
            <th>Quinto Año</th>
            <th>Sexto Año</th>
            <th>Séptimo Año</th>
        </tr>
        {"".join(f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td><td>{row[5]}</td><td>{row[6]}</td></tr>" for row in male_retention_data)}
    </table>
    """
    
    # Streamlit Layout
    col1, col2, col3 = st.columns([1, 5, 1])
    
    # Mostrar tablas en la columna central
    with col2:
        st.write("### Tasa de Retención por Cohorte")
        st.markdown(table_html_black, unsafe_allow_html=True)
        st.write("### Tasa de Retención Femenina")
        st.markdown(table_html_purple, unsafe_allow_html=True)
        st.write("### Tasa de Retención Masculina")
        st.markdown(table_html_male, unsafe_allow_html=True)
    
    
    generation_data = {
        "Generación 2016": {
            "Bajas": {"General": 36, "Hombres": 27, "Mujeres": 9},
            "Egresados": {"General": 10, "Hombres": 8, "Mujeres": 2},
            "Titulados": {"General": 17, "Hombres": 12, "Mujeres": 5}
        },
        "Generación 2017": {
            "Bajas": {"General": 28, "Hombres": 22, "Mujeres": 6},
            "Egresados": {"General": 11, "Hombres": 4, "Mujeres": 7},
            "Titulados": {"General": 14, "Hombres": 9, "Mujeres": 5}
        },
        "Generación 2018": {
            "Bajas": {"General": 36, "Hombres": 32, "Mujeres": 4},
            "Egresados": {"General": 12, "Hombres": 9, "Mujeres": 3},
            "Titulados": {"General": 9, "Hombres": 9, "Mujeres": 0}
        },
        "Generación 2019": {
            "Bajas": {"General": 47, "Hombres": 35, "Mujeres": 12},
            "Egresados": {"General": 16, "Hombres": 9, "Mujeres": 7},
            "Titulados": {"General": 8, "Hombres": 5, "Mujeres": 3}
        },
        "Generación 2020": {
            "Bajas": {"General": 49, "Hombres": 34, "Mujeres": 15},
            "Egresados": {"General": 1, "Hombres": 0.000001, "Mujeres": 0.000001},
            "Titulados": {"General": 1, "Hombres": 0.000001, "Mujeres": 0.000001},
        }
    }

    
    
    # Índice de rezago por generación
    rezago_data = {
        "Generación 2016": 13.84615385,
        "Generación 2017": 23.96694215,
        "Generación 2018": 25,
        "Generación 2019": 33.64485981,
        "Generación 2020": 77.16535433,
    }
    
    # Índice de rezago femenino
    rezago_femenino_data = {
        "Generación 2016": 6.25,
        "Generación 2017": 15.625,
        "Generación 2018": 41.66666667,
        "Generación 2019": 26.66666667,
        "Generación 2020": 72.09302326,
    }
    
    # Índice de rezago masculino
    rezago_masculino_data = {
        "Generación 2016": 16.32653061,
        "Generación 2017": 26.96629213,
        "Generación 2018": 21.875,
        "Generación 2019": 36.36363636,
        "Generación 2020": 79.76190476,
    }
    
    # Datos ajustados a 9 elementos por fila
    valores_semestres = [
    [56, 41, 30, 23, 21, 22, 16, 15, "", ""],
    [71, 52, 41, 33, 26, 19, 22, 26, "", ""],
    [72, 54, 38, 24, 27, 21, 23, 29, "", ""],
    [78, 48, 49, 42, 41, 38, 34, 30, "", ""],
    [109, 41, 38, 40, 43, 41, 40, "", "", ""]
    ]
    
    # DataFrame con los valores de los semestres
    df_semestres = pd.DataFrame(valores_semestres, index=list(generation_data.keys()), columns=[f"Semestre {i+1}" for i in range(10)])
    
    
    
    GRAPH_WIDTH = 130
    GRAPH_HEIGHT = 130
    
    def make_donut(input_response, input_text, input_color, title_text=None):
        chart_color = {
            "blue": ['#58A2D5', '#2558C4'],
            "pink": ['#D9B1E0', '#862B96'],
            "green": ['#27AE60', '#12783D'],
            "orange": ['#EFB444', '#F6E29D'],
            "red": ['#E74C3C', '#781F16']
        }.get(input_color, ['#dddddd', '#aaaaaa'])
    
        # Datos para el gráfico
        source = pd.DataFrame({
            "Topic": ['', input_text],
            "% value": [100 - input_response, input_response]
        })
        source_bg = pd.DataFrame({
            "Topic": ['', input_text],
            "% value": [100, 0]
        })
    
        # Gráfico principal de dona
        plot = alt.Chart(source).mark_arc(innerRadius=45, cornerRadius=25).encode(
            theta="% value",
            color=alt.Color("Topic:N",
                            scale=alt.Scale(
                                domain=[input_text, ''],
                                range=chart_color),
                            legend=None),
        ).properties(width=130, height=130)
    
        # Texto del porcentaje
        text = plot.mark_text(
            align='center',
            font="Lato",
            fontSize=25,
            fontWeight=700
        ).encode(text=alt.value(f'{input_response} %'))
    
        # Fondo de la dona
        plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=45, cornerRadius=20).encode(
            theta="% value",
            color=alt.Color("Topic:N",
                            scale=alt.Scale(
                                domain=[input_text, ''],
                                range=chart_color),
                            legend=None),
        ).properties(width=130, height=130)
    
        # Título (texto encima del gráfico)
        if title_text:
            title = alt.Chart(pd.DataFrame({'text': [title_text]})).mark_text(
                align='center',
                fontSize=16,
                fontWeight='bold',
                color=chart_color[0]
            ).encode(text='text:N')
    
            # Concatenar título y gráfico
            return alt.vconcat(title, plot_bg + plot + text)
        else:
            # Texto en blanco para alinear las gráficas generales
            blank_title = alt.Chart(pd.DataFrame({'text': ['‎ ‎ ‎ ‎ ']})).mark_text(
                align='center',
                fontSize=16,  # Tamaño similar al texto de hombres y mujeres
                fontWeight='bold',
                color="#ffffff"  # Texto blanco para que sea invisible
            ).encode(text='text:N')
    
            return alt.vconcat(blank_title, plot_bg + plot + text)
    
    
    # Dropdown generación
    generaciones = list(generation_data.keys())
    selected_generacion = st.selectbox("Selecciona una generación:", generaciones)
    
    
    col1, col2, col3 = st.columns(3)
    
    # Mostrar el índice de rezago general en la columna 1
    with col1:
        indice_rezago = rezago_data[selected_generacion]
        st.metric(label="Índice de Rezago", value=f"{indice_rezago:.2f}")
    # Mostrar el índice de rezago femenino
        indice_rezago_femenino = rezago_femenino_data[selected_generacion]
        st.metric(label="Índice de Rezago Femenino", value=f"{indice_rezago_femenino:.2f}")
    
        # Mostrar el índice de rezago masculino
        indice_rezago_masculino = rezago_masculino_data[selected_generacion]
        st.metric(label="Índice de Rezago Masculino", value=f"{indice_rezago_masculino:.2f}")
    
    # Mostrar los valores de la generación seleccionada
    with col2:
        st.write("Estudiantes inscritos por semestre para la generación seleccionada:")
        df = pd.DataFrame({
            "Semestre": range(1, 11),
            "Estudiantes inscritos": df_semestres.loc[selected_generacion].values
        })
        st.dataframe(df)
    
    
    # Columnas con gráficas de dona dinámicas basadas en la generación seleccionada
    col1, col2, col3 = st.columns([1, 1, 1])
    
    # Totales por generación
    valores_generaciones = [65, 76, 76, 107, 127]  # Totales de estudiantes por generación en orden 2009-2015
    totales_generacion = dict(zip(generation_data.keys(), valores_generaciones))  # Mapeo generación -> total
    
    def calcular_porcentajes(data, total):
        """
        Convierte los valores de 'General', 'Hombres', y 'Mujeres' a porcentajes basados en el total dado.
        """
        for categoria, valores in data.items():
            for grupo in ["General", "Hombres", "Mujeres"]:
                valores[grupo] = round((valores[grupo] / total) * 100, 2)  # Convertir a porcentaje
    
    # Convertir los valores de generation_data a porcentajes
    for generacion, data in generation_data.items():
        calcular_porcentajes(data, totales_generacion[generacion])
        categories = ["Bajas", "Egresados", "Titulados"]
        colors = ["red", "orange", "green"]
    
    for col, category, color in zip([col1, col2, col3], categories, colors):
        with col:
            st.title(category)
    
            # Gráfica general
            general = generation_data[selected_generacion][category]["General"]
            st.altair_chart(make_donut(general, "General", color), use_container_width=True)
    
            # Gráfica de hombres con texto encima
            hombres = generation_data[selected_generacion][category]["Hombres"]
            hombres_percent = round((hombres / general) * 100, 1)
            st.altair_chart(make_donut(hombres_percent, "Hombres", "blue", title_text="Hombres"), use_container_width=True)
    
            # Gráfica de mujeres con texto encima
            mujeres = generation_data[selected_generacion][category]["Mujeres"]
            mujeres_percent = round((mujeres / general) * 100, 1)
            st.altair_chart(make_donut(mujeres_percent, "Mujeres", "pink", title_text="Mujeres"), use_container_width=True)
    
        
if "SankeyFísica" in tags:

    # Sankey original
    st.subheader("Progreso de los alumnos en tiempo y forma por Semestre (2009-2015")
    st.subheader("Diagrama de Sankey por Semestre (2009-2015)")
    
    # Función para el primer Sankey
    def create_dynamic_sankey(opacity=0.8):
        generaciones = ["Generación 2009", "Generación 2010", "Generación 2011", "Generación 2012",
                        "Generación 2013", "Generación 2014", "Generación 2015"]
        semestres = 9
        nodos_finales = ["Egresados", "Titulado", "Deserción"]
        labels = generaciones + [f"Semestre {i+1}" for i in range(semestres)] + nodos_finales
        sources, targets, values, colors = [], [], [], []
    
        colores_generaciones = [
            "255, 99, 71", "60, 179, 113", "30, 144, 255",
            "255, 215, 0", "218, 112, 214", "244, 164, 96", "123, 104, 238"
        ]
        valores_generaciones = [46, 56, 54, 57, 55, 61, 60]
    
        # Nodos iniciales
        for gen, valor in enumerate(valores_generaciones):
            sources.append(gen)
            targets.append(len(generaciones))
            values.append(valor)
            colors.append(f"rgba({colores_generaciones[gen]}, {opacity})")
    
        # Semestres intermedios
        valores_semestres = [
            [46, 56, 48, 57, 55, 61, 54],
            [17, 36, 32, 28, 28, 31, 30],
            [17, 24, 16, 17, 19, 17, 24],
            [12, 15, 14, 17, 23, 20, 20],
            [11, 13, 7, 15, 16, 17, 16],
            [8, 9, 12, 14, 12, 16, 13],
            [5, 10, 10, 11, 14, 14, 13],
            [5, 8, 5, 11, 10, 10, 13]
        ]
        for semestre_index, valores in enumerate(valores_semestres):
            for gen, valor in enumerate(valores):
                sources.append(len(generaciones) + semestre_index)
                targets.append(len(generaciones) + semestre_index + 1)
                values.append(valor)
                colors.append(f"rgba({colores_generaciones[gen]}, {opacity})")
    
        # Nodos finales
        valores_finales = {
            "Egresados": [15, 18, 4, 11, 14, 4, 9],
            "Titulado": [4, 2, 2, 6, 14, 14, 10],
            "Deserción": [31, 39, 48, 32, 6, 38, 4]
        }
        ultimo_semestre = len(generaciones) + semestres - 1
        targets_indices = [labels.index("Egresados"), labels.index("Titulado"), labels.index("Deserción")]
        for gen, color in enumerate(colores_generaciones):
            sources.extend([ultimo_semestre, ultimo_semestre, ultimo_semestre])
            targets.extend(targets_indices)
            values.extend([
                valores_finales["Egresados"][gen],
                valores_finales["Titulado"][gen],
                valores_finales["Deserción"][gen]
            ])
            colors.extend([f"rgba({color}, {opacity})"] * 3)
    
        fig = go.Figure(go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=labels,
                color=[f'rgba(30, 58, 138, {opacity})' for _ in labels]
            ),
            link=dict(
                source=sources,
                target=targets,
                value=values,
                color=colors
            )
        ))
        fig.update_layout(
            title="Diagrama de Sankey: Trayectoria Académica por Generación",
            font=dict(size=14),
            paper_bgcolor="rgba(0, 0, 0, 0)"
        )
        return fig
    
    # Slider y gráfico del primer Sankey
    opacity_1 = st.slider("Ajustar opacidad para el primer Sankey:", 0.2, 1.0, 0.8, 0.1)
    st.plotly_chart(create_dynamic_sankey(opacity_1), use_container_width=True)
    
    # Sankey modificado
    st.subheader("Progreso de los alumnos en tiempo y forma por Semestre (2016-2020)")
    st.subheader("Diagrama de Sankey por Semestre (2016-2020)")
    
    # Función para el segundo Sankey
    def create_dynamic_sankey_2(opacity=0.8):
        generaciones = ["Generación 2016", "Generación 2017", "Generación 2018", "Generación 2019", "Generación 2020"]
        semestres = 8
        nodos_finales = ["Egresados", "Titulado", "Deserción"]
        labels = generaciones + [f"Semestre {i+1}" for i in range(semestres)] + nodos_finales
        sources, targets, values, colors = [], [], [], []
    
        colores_generaciones = [
            "255, 99, 71", "60, 179, 113", "30, 144, 255",
            "255, 215, 0", "218, 112, 214"
        ]
        valores_generaciones = [97, 125, 122, 219, 374]
    
        # Nodos iniciales
        for gen, valor in enumerate(valores_generaciones):
            sources.append(gen)
            targets.append(len(generaciones))
            values.append(valor)
            colors.append(f"rgba({colores_generaciones[gen]}, {opacity})")
    
        # Semestres intermedios
        valores_semestres = [
            [85, 112, 111, 184, 301],
            [63, 97, 93, 116, 120],
            [51, 90, 97, 102, 111],
            [45, 66, 63, 84, 109],
            [41, 53, 74, 80, 98],
            [37, 38, 56, 76, 101],
            [28, 44, 45, 68, 106],
            [26, 35, 48, 44, 0]
        ]
        for semestre_index, valores in enumerate(valores_semestres):
            for gen, valor in enumerate(valores):
                sources.append(len(generaciones) + semestre_index)
                targets.append(len(generaciones) + semestre_index + 1)
                values.append(valor)
                colors.append(f"rgba({colores_generaciones[gen]}, {opacity})")
    
        # Nodos finales
        valores_finales = {
            "Egresados": [13, 19, 23, 22, 0],
            "Titulado": [31, 39, 36, 12, 0],
            "Deserción": [45, 40, 36, 76, 101]
        }
        ultimo_semestre = len(generaciones) + semestres - 1
        targets_indices = [labels.index("Egresados"), labels.index("Titulado"), labels.index("Deserción")]
        for gen, color in enumerate(colores_generaciones):
            sources.extend([ultimo_semestre, ultimo_semestre, ultimo_semestre])
            targets.extend(targets_indices)
            values.extend([
                valores_finales["Egresados"][gen],
                valores_finales["Titulado"][gen],
                valores_finales["Deserción"][gen]
            ])
            colors.extend([f"rgba({color}, {opacity})"] * 3)
    
        fig = go.Figure(go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=labels,
                color=[f'rgba(30, 58, 138, {opacity})' for _ in labels]
            ),
            link=dict(
                source=sources,
                target=targets,
                value=values,
                color=colors
            )
        ))
        fig.update_layout(
            title="Diagrama de Sankey: Trayectoria Académica por Generación (2016-2020)",
            font=dict(size=14),
            paper_bgcolor="rgba(0, 0, 0, 0)"
        )
        return fig
    
    # Slider y gráfico del segundo Sankey
    opacity_2 = st.slider("Ajustar opacidad para el segundo Sankey:", 0.2, 1.0, 0.8, 0.1)
    st.plotly_chart(create_dynamic_sankey_2(opacity_2), use_container_width=True)
    
    
if "SankeyAplicada" in tags: 
    
    # Diagrama de Sankey para generaciones 2009-2015
    st.subheader("Progreso de los alumnos en tiempo y forma por Semestre")
    st.subheader("Diagrama de Sankey por Semestre (2009-2015)")
    
    # Definición de la función para crear el diagrama de Sankey para 2009-2015
    def create_dynamic_sankey_2009_2015(opacity=0.8):
        generaciones = ["Generación 2009", "Generación 2010", "Generación 2011", "Generación 2012",
                        "Generación 2013", "Generación 2014", "Generación 2015"]
        semestres = 9
        nodos_finales = ["Egresados", "Titulado", "Deserción"]
        labels = generaciones + [f"Semestre {i+1}" for i in range(semestres)] + nodos_finales
        
        sources = []
        targets = []
        values = []
        colors = []
        
        colores_generaciones = [
            "255, 99, 71", "60, 179, 113", "30, 144, 255", "255, 215, 0", 
            "218, 112, 214", "244, 164, 96", "123, 104, 238"
        ]
        valores_generaciones = [46, 56, 54, 57, 55, 61, 60]
    
        # Conexión con las generaciones
        for gen, valor in enumerate(valores_generaciones):
            sources.append(gen)
            targets.append(len(generaciones))
            values.append(valor)
            colors.append(f"rgba({colores_generaciones[gen]}, {opacity})")
    
        valores_semestres = [
            [46, 56, 48, 57, 55, 61, 54],
            [17, 36, 32, 28, 28, 31, 30],
            [17, 24, 16, 17, 19, 17, 24],
            [12, 15, 14, 17, 23, 20, 20],
            [11, 13, 7, 15, 16, 17, 16],
            [8, 9, 12, 14, 12, 16, 13],
            [5, 10, 10, 11, 14, 14, 13],
            [5, 8, 5, 11, 10, 10, 13]
        ]
        
        for semestre_index, valores in enumerate(valores_semestres):
            for gen, valor in enumerate(valores):
                sources.append(len(generaciones) + semestre_index)
                targets.append(len(generaciones) + semestre_index + 1)
                values.append(valor)
                colors.append(f"rgba({colores_generaciones[gen]}, {opacity})")
    
        valores_finales = {
            "Egresados": [15, 18, 4, 11, 14, 4, 9],
            "Titulado": [4, 2, 2, 6, 14, 14, 10],
            "Deserción": [31, 39, 48, 32, 6, 38, 4]
        }
        
        ultimo_semestre = len(generaciones) + semestres - 1
        targets_indices = [labels.index("Egresados"), labels.index("Titulado"), labels.index("Deserción")]
    
        for gen, color in enumerate(colores_generaciones):
            sources.extend([ultimo_semestre, ultimo_semestre, ultimo_semestre])
            targets.extend(targets_indices)
            values.extend([
                valores_finales["Egresados"][gen],
                valores_finales["Titulado"][gen],
                valores_finales["Deserción"][gen]
            ])
            colors.extend([f"rgba({color}, {opacity})"] * 3)
    
        fig = go.Figure(go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=labels,
                color=[f'rgba(30, 58, 138, {opacity})' for _ in labels]
            ),
            link=dict(
                source=sources,
                target=targets,
                value=values,
                color=colors
            )
        ))
    
        fig.update_layout(
            title="Diagrama de Sankey: Trayectoria Académica por Generación (2009-2015)",
            font=dict(size=14),
            paper_bgcolor="rgba(0, 0, 0, 0)"
        )
    
        return fig
    
    # Mostrar el slider y el gráfico del Sankey
    opacity_1 = st.slider("Ajustar opacidad (2009-2015):", 0.2, 1.0, 0.8, 0.1)
    st.plotly_chart(create_dynamic_sankey_2009_2015(opacity_1), use_container_width=True)
    
    
    # Diagrama de Sankey para generaciones 2016-2020
    st.subheader("Progreso de los alumnos en tiempo y forma por Semestre")
    st.subheader("Diagrama de Sankey por Semestre (2016-2020)")
    
    # Definición de la función para crear el diagrama de Sankey para 2016-2020
    def create_dynamic_sankey_2016_2020(opacity=0.8):
        generaciones = ["Generación 2016", "Generación 2017", "Generación 2018", "Generación 2019", "Generación 2020"]
        semestres = 8
        nodos_finales = ["Egresados", "Titulado", "Deserción"]
        labels = generaciones + [f"Semestre {i+1}" for i in range(semestres)] + nodos_finales
        
        sources = []
        targets = []
        values = []
        colors = []
        
        colores_generaciones = [
            "255, 99, 71", "60, 179, 113", "30, 144, 255", "255, 215, 0", "218, 112, 214"
        ]
        valores_generaciones = [65, 76, 76, 107, 127]
    
        # Conexión con las generaciones
        for gen, valor in enumerate(valores_generaciones):
            sources.append(gen)
            targets.append(len(generaciones))
            values.append(valor)
            colors.append(f"rgba({colores_generaciones[gen]}, {opacity})")
    
        valores_semestres = [
            [56, 71, 72, 78, 109],
            [41, 52, 54, 48, 41],
            [30, 41, 38, 49, 38],
            [23, 33, 24, 42, 40],
            [21, 26, 27, 41, 43],
            [22, 19, 21, 38, 41],
            [16, 22, 23, 34, 40],
            [15, 26, 29, 30, ""]
        ]
        
        for semestre_index, valores in enumerate(valores_semestres):
            for gen, valor in enumerate(valores):
                sources.append(len(generaciones) + semestre_index)
                targets.append(len(generaciones) + semestre_index + 1)
                values.append(valor)
                colors.append(f"rgba({colores_generaciones[gen]}, {opacity})")
    
        valores_finales = {
            "Egresados": [10, 11, 12, 16, ""],
            "Titulado": [17, 14, 9, 8, ""],
            "Deserción": [36, 28, 36, 47, ""]
        }
        
        ultimo_semestre = len(generaciones) + semestres - 1
        targets_indices = [labels.index("Egresados"), labels.index("Titulado"), labels.index("Deserción")]
    
        for gen, color in enumerate(colores_generaciones):
            sources.extend([ultimo_semestre, ultimo_semestre, ultimo_semestre])
            targets.extend(targets_indices)
            values.extend([
                valores_finales["Egresados"][gen],
                valores_finales["Titulado"][gen],
                valores_finales["Deserción"][gen]
            ])
            colors.extend([f"rgba({color}, {opacity})"] * 3)
    
        fig = go.Figure(go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=labels,
                color=[f'rgba(30, 58, 138, {opacity})' for _ in labels]
            ),
            link=dict(
                source=sources,
                target=targets,
                value=values,
                color=colors
            )
        ))
    
        fig.update_layout(
            title="Diagrama de Sankey: Trayectoria Académica por Generación (2016-2020)",
            font=dict(size=14),
            paper_bgcolor="rgba(0, 0, 0, 0)"
        )
    
        return fig
    
    # Mostrar el slider y el gráfico del Sankey
    opacity_2 = st.slider("Ajustar opacidad (2016-2020):", 0.2, 1.0, 0.8, 0.1)
    st.plotly_chart(create_dynamic_sankey_2016_2020(opacity_2), use_container_width=True)
