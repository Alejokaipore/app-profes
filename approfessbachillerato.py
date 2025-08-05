import pandas as pd  # type: ignore
import numpy as np  # type: ignore
import streamlit as st
from corregir_nombres import corregir_nombre
import datetime
import requests
from io import BytesIO
import warnings
import matplotlib.pyplot as plt # type: ignore

st.set_page_config(layout="wide")

# Enlace de descarga directa 
url_excel = "https://gkinnova-my.sharepoint.com/:x:/g/personal/manuela_gutierrez_gimnasiokaipore_com/ESsbWoRrT2pOq7G6DlLrtAgB7gRvw3J5komJxW7VzbM_vg?download=1"
url_excel_planeacion = 'https://gkinnova-my.sharepoint.com/:x:/g/personal/manuela_gutierrez_gimnasiokaipore_com/EY4Dg1oyrWBIlzQSB6NVjnEB17gVB5324RNAKs4qMRhdSA?e=IXuEc2&download=1'
url_excel_listado = 'https://gkinnova-my.sharepoint.com/:x:/g/personal/manuela_gutierrez_gimnasiokaipore_com/EW47uW_fJFtInsbP1zH_30gBdsFrR5Asr0ouwkvcoqEmXA?download=1'


ingles = ['Inglés - listening','Inglés - speaking','Inglés - writing', 'Inglés - reading', 'Animaplanos']

def cargar_listado():
    response = requests.get(url_excel_listado)
    response.raise_for_status()  # Lanza error si hay HTTP 403/404/500
    df = pd.read_excel(BytesIO(response.content), sheet_name='g')
    df['GRADO'] = df['GRADO'].astype(str)
    df['ESTUDIANTE'] = df['ESTUDIANTE'].apply(corregir_nombre)
    df = df[df['GRADO'].isin(['6','7','8','9','10','11'])]
    return df


def cargar_planeacion():
    response = requests.get(url_excel_planeacion)
    response.raise_for_status()  # Lanza error si hay HTTP 403/404/500
    df = pd.read_excel(BytesIO(response.content), sheet_name='bachillerato')
    return df

@st.cache_data
def cargar_notas():
    response = requests.get(url_excel)
    response.raise_for_status()  # Lanza error si hay HTTP 403/404/500
    df = pd.read_excel(BytesIO(response.content), sheet_name='GK2025')
    df['GRADO'] = df['GRADO'].astype(str)
    df['ESTUDIANTE'] = df['ESTUDIANTE'].apply(corregir_nombre)
    df['FECHA'] = pd.to_datetime(df['FECHA'], errors='coerce')
    df = df[~df['ASIGNATURA'].isin(ingles)]
    return df

notas = cargar_notas()
planeacion_primaria = cargar_planeacion()
estudiantes = cargar_listado()

notas['GRADO'] = notas['GRADO'].astype(str)
notas['ESTUDIANTE'] = notas['ESTUDIANTE'].apply(corregir_nombre)


################################################################################################################
asignaturas_6_7= ['Biología','Química','Medio ambiente','Física',
                  'Historia', 'Geografía', 'Participación política','Filosofía',
                  'Comunicación y sistemas simbólicos','Producción e interpretación de textos',
                  'Aritmética','Estadística', 'Geometría', 'Dibujo técnico', 'Sistemas']

ciencias_6_7  = ['Biología','Química','Medio ambiente','Física']
sociales_6_7  = ['Historia', 'Geografía', 'Participación política','Filosofía']
lenguaje_6_7  = ['Comunicación y sistemas simbólicos','Producción e interpretación de textos']
matemati_6_7  = ['Aritmética','Estadística', 'Geometría', 'Dibujo técnico', 'Sistemas']

######################################################################################################################################

asignaturas_8_9= ['Biología','Química','Medio ambiente','Física',
                  'Historia', 'Geografía', 'Participación política','Filosofía',
                  'Comunicación y sistemas simbólicos','Producción e interpretación de textos',
                  'Álgebra', 'Estadística', 'Geometría', 'Dibujo técnico', 'Sistemas']

ciencias_8_9  = ['Biología','Química','Medio ambiente','Física']
sociales_8_9  = ['Historia', 'Geografía', 'Participación política','Filosofía']
lenguaje_8_9  = ['Comunicación y sistemas simbólicos','Producción e interpretación de textos']
matemati_8_9  = ['Álgebra', 'Estadística', 'Geometría', 'Dibujo técnico', 'Sistemas']

######################################################################################################################################


asignaturas_10=  ['Biología','Química','Medio ambiente','Física',
                  'Ciencias económicas', 'Ciencias políticas','Filosofía',
                  'Comunicación y sistemas simbólicos','Producción e interpretación de textos',
                  'Trigonometría', 'Estadística', 'Matemática financiera', 'Dibujo técnico', 'Sistemas']

ciencias_10  = ['Biología','Química','Medio ambiente','Física']
sociales_10  = ['Ciencias económicas', 'Ciencias políticas','Filosofía']
lenguaje_10  = ['Comunicación y sistemas simbólicos','Producción e interpretación de textos','Metodología']
matemati_10  = ['Trigonometría', 'Estadística', 'Matemática financiera', 'Dibujo técnico', 'Sistemas']

######################################################################################################################################
asignaturas_11=  ['Química','Medio ambiente','Física',
                  'Ciencias económicas', 'Ciencias políticas','Filosofía',
                  'Comunicación y sistemas simbólicos','Producción e interpretación de textos',
                  'Cálculo','Animaplanos', 'Estadística', 'Matemática financiera', 'Dibujo técnico', 'Sistemas']

ciencias_11  = ['Química','Medio ambiente','Física']
sociales_11  = ['Ciencias económicas', 'Ciencias políticas','Filosofía']
lenguaje_11  = ['Comunicación y sistemas simbólicos','Producción e interpretación de textos','Metodología']
matemati_11  = ['Cálculo','Estadística', 'Matemática financiera', 'Dibujo técnico', 'Sistemas']

##################################################################################################################


col1, col2 = st.columns(2)

with col1:

    # Barra de búsqueda con opciones específicas
    area_seleccionada = st.selectbox(
        "Selecciona una opción:",
        ['C1','C2', 'S1','S2', 'L', 'M1','M2']
    )


    # Procesar solo si hay selección
    if area_seleccionada:


        #Lista de modulos
        LMOD1l = ["LMOD1"] + planeacion_primaria[planeacion_primaria.iloc[:, 2] == area_seleccionada].iloc[:, 0].tolist()
        LMOD2l = ["LMOD2"] + planeacion_primaria[planeacion_primaria.iloc[:, 7] == area_seleccionada].iloc[:, 0].tolist()
        MMOD1l = ["MMOD1"] + planeacion_primaria[planeacion_primaria.iloc[:, 3] == area_seleccionada].iloc[:, 0].tolist()
        MMOD2l = ["MMOD2"] + planeacion_primaria[planeacion_primaria.iloc[:, 8] == area_seleccionada].iloc[:, 0].tolist()
        WMOD1l = ["WMOD1"] + planeacion_primaria[planeacion_primaria.iloc[:, 4] == area_seleccionada].iloc[:, 0].tolist()
        WMOD2l = ["WMOD2"] + planeacion_primaria[planeacion_primaria.iloc[:, 9] == area_seleccionada].iloc[:, 0].tolist()
        JMOD1l = ["JMOD1"] + planeacion_primaria[planeacion_primaria.iloc[:, 5] == area_seleccionada].iloc[:, 0].tolist()
        JMOD2l = ["JMOD2"] + planeacion_primaria[planeacion_primaria.iloc[:, 10] == area_seleccionada].iloc[:, 0].tolist()
        VMOD1l = ["VMOD1"] + planeacion_primaria[planeacion_primaria.iloc[:, 6] == area_seleccionada].iloc[:, 0].tolist()
        VMOD2l = ["VMOD2"] + planeacion_primaria[planeacion_primaria.iloc[:, 11] == area_seleccionada].iloc[:, 0].tolist()
        
        LMOD1 = pd.DataFrame(LMOD1l)
        LMOD2 = pd.DataFrame(LMOD2l)
        MMOD1 = pd.DataFrame(MMOD1l)
        MMOD2 = pd.DataFrame(MMOD2l)
        WMOD1 = pd.DataFrame(WMOD1l)
        WMOD2 = pd.DataFrame(WMOD2l)
        JMOD1 = pd.DataFrame(JMOD1l)
        JMOD2 = pd.DataFrame(JMOD2l)
        VMOD1 = pd.DataFrame(VMOD1l)
        VMOD2 = pd.DataFrame(VMOD2l)
        
        df_nombres = pd.concat([LMOD1, LMOD2, MMOD1, MMOD2, WMOD1, WMOD2, JMOD1, JMOD2, VMOD1, VMOD2], ignore_index=True)

        # Crear un diccionario clave ESTUDIANTE y valor GRUPO
        grupo_map = dict(zip(estudiantes['ESTUDIANTE'], estudiantes['GRUPO']))
        grado_map = dict(zip(estudiantes['ESTUDIANTE'], estudiantes['GRADO']))

        # Asignar grupo y grado correspondiente a cada estudiante de df_nombres
        df_nombres['1'] = df_nombres.iloc[:, 0].map(grupo_map)
        df_nombres['2'] = df_nombres.iloc[:, 0].map(grado_map)

        filasn, _ = df_nombres.shape

        #Crea siete vectores vacios tan grandes como la lista generada dos bloques anteriores, en el primero ira el bloque en el que esta el estudiante
        #en el segundo la Asignatura que debe ver y los cinco restantes corresponden respectivamente a si se marca el primero al primer desempeño
        #el segundo al segundo desempeño y asi sucesivamente hasta el quinto el quinto desempeño 

        df_bloque = pd.DataFrame([""] * filasn)
        df_asignatura = pd.DataFrame([""] * filasn)
        df_desempeño1 = pd.DataFrame([""] * filasn)
        df_desempeño2 = pd.DataFrame([""] * filasn)
        df_desempeño3 = pd.DataFrame([""] * filasn)
        df_desempeño4 = pd.DataFrame([""] * filasn)
        df_desempeño5 = pd.DataFrame([""] * filasn)


        if (area_seleccionada == 'M1') or (area_seleccionada =='M2'):
            for i in range(filasn):
                estudiante_actual = df_nombres.iloc[i, 0]
                grado_actual = df_nombres.iloc[i, 2]
                notas_estudiante = notas[(notas.iloc[:, 2] == estudiante_actual) & (notas.iloc[:, 3] == grado_actual)]
                desempeno_encontrado = False
            
                if df_nombres.iloc[i, 0] in (['LMOD1', 'LMOD2', 'MMOD1', 'MMOD2', 'WMOD1', 'WMOD2', 'JMOD1', 'JMOD2', 'VMOD1']):
                    desempeno_encontrado = True
                    continue 
                
                materias_especificas_6_7 = ['Aritmética', 'Geometría', 'Estadística', 'Dibujo técnico', 'Sistemas']
                materias_especificas_8_9 = ['Álgebra', 'Geometría', 'Estadística', 'Dibujo técnico', 'Sistemas']
                materias_especificas_10 =  ['Trigonometría', 'Matemática financiera', 'Estadística', 'Dibujo técnico', 'Sistemas']
                materias_especificas_11 =  ['Cálculo', 'Matemática financiera', 'Estadística', 'Dibujo técnico', 'Sistemas']
                    
                bloques = ['A', 'B', 'C', 'D']
                asignaturas = ['Aritmética', 'Geometría','Matemática financiera', 'Álgebra', 'Estadística', 'Dibujo técnico', 'Sistemas','Trigonometría','Cálculo']


                for materia in asignaturas:
                    notas_materia = notas_estudiante[notas_estudiante.iloc[:, 5] == materia]
                    
                    for bloque in bloques:
                        notas_bloque = notas_materia[notas_materia.iloc[:, 6] == bloque]
                        desempenos_completos = len(notas_bloque)

                        if desempenos_completos == 1:
                            df_bloque.iloc[i] = bloque
                            df_asignatura.iloc[i] = materia
                            df_desempeño2.iloc[i] = 'X'
                            desempeno_encontrado = True
                            break

                        elif desempenos_completos == 2:
                            df_bloque.iloc[i] = bloque
                            df_asignatura.iloc[i] = materia
                            df_desempeño3.iloc[i] = 'X'
                            desempeno_encontrado = True
                            break

                        elif desempenos_completos == 3:
                            df_bloque.iloc[i] = bloque
                            df_asignatura.iloc[i] = materia
                            df_desempeño4.iloc[i] = 'X'
                            desempeno_encontrado = True
                            break

                        elif desempenos_completos == 4: 
                            df_bloque.iloc[i] = bloque
                            df_asignatura.iloc[i] = materia
                            df_desempeño5.iloc[i] = 'X'
                            desempeno_encontrado = True
                            break

                    if desempeno_encontrado:
                        break
                    
                for bloque in bloques:
                    notas_bloque = notas_estudiante[notas_estudiante.iloc[:, 6] == bloque]
                    if grado_actual in ['6','7']:
                        notas_bloque_filtradas = notas_bloque[notas_bloque.iloc[:, 5].isin(materias_especificas_6_7)]
                        longitud_bloque = len(notas_bloque_filtradas)
                        if longitud_bloque == 25 and not desempeno_encontrado:
                            continue 
                        if longitud_bloque < 25 and not desempeno_encontrado:
                            for materia in materias_especificas_6_7:
                                if materia not in notas_bloque_filtradas.iloc[:, 5].values:
                                    df_bloque.iloc[i] = bloque
                                    df_desempeño1.iloc[i] = 'X'
                                    df_asignatura.iloc[i] = materia
                                    desempeno_encontrado = True
                                    break
                                    
                    if grado_actual in ['8','9']:
                        notas_bloque_filtradas = notas_bloque[notas_bloque.iloc[:, 5].isin(materias_especificas_8_9)]
                        longitud_bloque = len(notas_bloque_filtradas)
                        if longitud_bloque == 25 and not desempeno_encontrado:
                            continue 
            
                        if longitud_bloque < 25 and not desempeno_encontrado:
                            for materia in materias_especificas_8_9:
                                if materia not in notas_bloque_filtradas.iloc[:, 5].values:
                                    df_bloque.iloc[i] = bloque
                                    df_desempeño1.iloc[i] = 'X'
                                    df_asignatura.iloc[i] = materia
                                    desempeno_encontrado = True
                                    break
                                    
                    if grado_actual == '10':
                        notas_bloque_filtradas = notas_bloque[notas_bloque.iloc[:, 5].isin(materias_especificas_10)]
                        longitud_bloque = len(notas_bloque_filtradas)
                        if longitud_bloque == 25 and not desempeno_encontrado:
                            continue 
            
                        if longitud_bloque < 25 and not desempeno_encontrado:
                            for materia in materias_especificas_10:
                                if materia not in notas_bloque_filtradas.iloc[:, 5].values:
                                    df_bloque.iloc[i] = bloque
                                    df_desempeño1.iloc[i] = 'X'
                                    df_asignatura.iloc[i] = materia
                                    desempeno_encontrado = True
                                    break
                                    
                    if grado_actual == '11':
                        notas_bloque_filtradas = notas_bloque[notas_bloque.iloc[:, 5].isin(materias_especificas_11)]
                        longitud_bloque = len(notas_bloque_filtradas)
                        if longitud_bloque == 25 and not desempeno_encontrado:
                            continue 
            
                        if longitud_bloque < 25 and not desempeno_encontrado:
                            for materia in materias_especificas_11:
                                if materia not in notas_bloque_filtradas.iloc[:, 5].values:
                                    df_bloque.iloc[i] = bloque
                                    df_desempeño1.iloc[i] = 'X'
                                    df_asignatura.iloc[i] = materia
                                    desempeno_encontrado = True
                                    break
                                    
                    if desempeno_encontrado:
                        break

        if  (area_seleccionada == 'C1') or (area_seleccionada =='C2'):
            
            for i in range(filasn):
                
                estudiante_actual = df_nombres.iloc[i, 0]
                grado_actual = df_nombres.iloc[i, 2]
                notas_estudiante = notas[(notas.iloc[:, 2] == estudiante_actual) & (notas.iloc[:, 3] == grado_actual)]
                desempeno_encontrado = False
            
                if df_nombres.iloc[i, 0] in (['LMOD1', 'LMOD2', 'MMOD1', 'MMOD2', 'WMOD1', 'WMOD2', 'JMOD1', 'JMOD2', 'VMOD1']):
                    desempeno_encontrado = True
                    continue 
                
                    
                bloques = ['A', 'B', 'C', 'D']
                asignaturas = ['Biología', 'Química', 'Medio ambiente', 'Física']
                asignaturas_11 = ['Química', 'Medio ambiente', 'Física']

                for materia in asignaturas:
                    notas_materia = notas_estudiante[notas_estudiante.iloc[:, 5] == materia]
                    
                    for bloque in bloques:
                        notas_bloque = notas_materia[notas_materia.iloc[:, 6] == bloque]
                        desempenos_completos = len(notas_bloque)

                        if desempenos_completos == 1:
                            df_bloque.iloc[i] = bloque
                            df_asignatura.iloc[i] = materia
                            df_desempeño2.iloc[i] = 'X'
                            desempeno_encontrado = True
                            break

                        elif desempenos_completos == 2:
                            df_bloque.iloc[i] = bloque
                            df_asignatura.iloc[i] = materia
                            df_desempeño3.iloc[i] = 'X'
                            desempeno_encontrado = True
                            break

                        elif desempenos_completos == 3:
                            df_bloque.iloc[i] = bloque
                            df_asignatura.iloc[i] = materia
                            df_desempeño4.iloc[i] = 'X'
                            desempeno_encontrado = True
                            break

                        elif desempenos_completos == 4: 
                            df_bloque.iloc[i] = bloque
                            df_asignatura.iloc[i] = materia
                            df_desempeño5.iloc[i] = 'X'
                            desempeno_encontrado = True
                            break

                    if desempeno_encontrado:
                        break
                    
                for bloque in bloques:
                    
                    notas_bloque = notas_estudiante[notas_estudiante.iloc[:, 6] == bloque]
                    
                    if grado_actual in ['6','7','8','9','10']:
                        notas_bloque_filtradas = notas_bloque[notas_bloque.iloc[:, 5].isin(asignaturas)]
                        longitud_bloque = len(notas_bloque_filtradas)
                        if longitud_bloque == 20 and not desempeno_encontrado:
                            continue 
            
                        if longitud_bloque < 20 and not desempeno_encontrado:
                            for materia in asignaturas:
                                if materia not in notas_bloque_filtradas.iloc[:, 5].values:
                                    df_bloque.iloc[i] = bloque
                                    df_desempeño1.iloc[i] = 'X'
                                    df_asignatura.iloc[i] = materia
                                    desempeno_encontrado = True
                                    break
                                    
                    if grado_actual == '11':
                        notas_bloque_filtradas = notas_bloque[notas_bloque.iloc[:, 5].isin(asignaturas_11)]
                        longitud_bloque = len(notas_bloque_filtradas)
                        if longitud_bloque == 15 and not desempeno_encontrado:
                            continue 
            
                        if longitud_bloque < 15 and not desempeno_encontrado:
                            for materia in asignaturas_11:
                                if materia not in notas_bloque_filtradas.iloc[:, 5].values:
                                    df_bloque.iloc[i] = bloque
                                    df_desempeño1.iloc[i] = 'X'
                                    df_asignatura.iloc[i] = materia
                                    desempeno_encontrado = True
                                    break
                                    
                    if desempeno_encontrado:
                        break
                    

        if area_seleccionada == 'S1':
            
            for i in range(filasn):
                estudiante_actual = df_nombres.iloc[i, 0]
                grado_actual = df_nombres.iloc[i, 2]
                notas_estudiante = notas[(notas.iloc[:, 2] == estudiante_actual) & (notas.iloc[:, 3] == grado_actual)]
                desempeno_encontrado = False
            
                if df_nombres.iloc[i, 0] in (['LMOD1', 'LMOD2', 'MMOD1', 'MMOD2', 'WMOD1', 'WMOD2', 'JMOD1', 'JMOD2', 'VMOD1']):
                    desempeno_encontrado = True
                    continue 
                
                materias_especificas_6_7_8_9 = ['Historia', 'Geografía', 'Participación política', 'Filosofía']
                materias_especificas_10_11 = ['Ciencias económicas', 'Ciencias políticas', 'Filosofía']
            
                        
                bloques = ['A', 'B', 'C', 'D']
                asignaturas = ['Historia', 'Geografía', 'Ciencias económicas', 'Participación política','Ciencias políticas','Filosofía']

                for materia in asignaturas:
                    notas_materia = notas_estudiante[notas_estudiante.iloc[:, 5] == materia]
                    
                    for bloque in bloques:
                        notas_bloque = notas_materia[notas_materia.iloc[:, 6] == bloque]
                        desempenos_completos = len(notas_bloque)

                        if desempenos_completos == 1:
                            df_bloque.iloc[i] = bloque
                            df_asignatura.iloc[i] = materia
                            df_desempeño2.iloc[i] = 'X'
                            desempeno_encontrado = True
                            break

                        elif desempenos_completos == 2:
                            df_bloque.iloc[i] = bloque
                            df_asignatura.iloc[i] = materia
                            df_desempeño3.iloc[i] = 'X'
                            desempeno_encontrado = True
                            break

                        elif desempenos_completos == 3:
                            df_bloque.iloc[i] = bloque
                            df_asignatura.iloc[i] = materia
                            df_desempeño4.iloc[i] = 'X'
                            desempeno_encontrado = True
                            break

                        elif desempenos_completos == 4: 
                            df_bloque.iloc[i] = bloque
                            df_asignatura.iloc[i] = materia
                            df_desempeño5.iloc[i] = 'X'
                            desempeno_encontrado = True
                            break

                    if desempeno_encontrado:
                        break
                    
                for bloque in bloques:
                    notas_bloque = notas_estudiante[notas_estudiante.iloc[:, 6] == bloque]
                    
                    
                    if grado_actual in ['6','7','8','9']:
                        notas_bloque_filtradas = notas_bloque[notas_bloque.iloc[:, 5].isin(materias_especificas_6_7_8_9)]
                        longitud_bloque = len(notas_bloque_filtradas)
                        if longitud_bloque == 20 and not desempeno_encontrado:
                            continue 
            
                        if longitud_bloque < 20 and not desempeno_encontrado:
                            for materia in materias_especificas_6_7_8_9:
                                if materia not in notas_bloque_filtradas.iloc[:, 5].values:
                                    df_bloque.iloc[i] = bloque
                                    df_desempeño1.iloc[i] = 'X'
                                    df_asignatura.iloc[i] = materia
                                    desempeno_encontrado = True
                                    break
                                    
                    if grado_actual in ['10','11']:
                        notas_bloque_filtradas = notas_bloque[notas_bloque.iloc[:, 5].isin(materias_especificas_10_11)]
                        longitud_bloque = len(notas_bloque_filtradas)
                        if longitud_bloque == 15 and not desempeno_encontrado:
                            continue 
            
                        if longitud_bloque < 15 and not desempeno_encontrado:
                            for materia in materias_especificas_10_11:
                                if materia not in notas_bloque_filtradas.iloc[:, 5].values:
                                    df_bloque.iloc[i] = bloque
                                    df_desempeño1.iloc[i] = 'X'
                                    df_asignatura.iloc[i] = materia
                                    desempeno_encontrado = True
                                    break
                                    
                    if desempeno_encontrado:
                        break


        if area_seleccionada == 'S2':
            
            for i in range(filasn):
                estudiante_actual = df_nombres.iloc[i, 0]
                grado_actual = df_nombres.iloc[i, 2]
                notas_estudiante = notas[(notas.iloc[:, 2] == estudiante_actual) & (notas.iloc[:, 3] == grado_actual)]
                desempeno_encontrado = False
            
                if df_nombres.iloc[i, 0] in (['LMOD1', 'LMOD2', 'MMOD1', 'MMOD2', 'WMOD1', 'WMOD2', 'JMOD1', 'JMOD2', 'VMOD1']):
                    desempeno_encontrado = True
                    continue 
                
                materias_especificas_6_7_8_9 = ['Historia', 'Geografía', 'Participación política', 'Filosofía']
                materias_especificas_10_11 = ['Ciencias económicas', 'Ciencias políticas', 'Filosofía']
            
                        
                bloques = ['A', 'B', 'C', 'D']
                asignaturas = ['Historia', 'Geografía', 'Ciencias económicas', 'Participación política','Ciencias políticas','Filosofía']

                for materia in asignaturas:
                    notas_materia = notas_estudiante[notas_estudiante.iloc[:, 5] == materia]
                    
                    for bloque in bloques:
                        notas_bloque = notas_materia[notas_materia.iloc[:, 6] == bloque]
                        desempenos_completos = len(notas_bloque)

                        if desempenos_completos == 1:
                            df_bloque.iloc[i] = bloque
                            df_asignatura.iloc[i] = materia
                            df_desempeño2.iloc[i] = 'X'
                            desempeno_encontrado = True
                            break

                        elif desempenos_completos == 2:
                            df_bloque.iloc[i] = bloque
                            df_asignatura.iloc[i] = materia
                            df_desempeño3.iloc[i] = 'X'
                            desempeno_encontrado = True
                            break

                        elif desempenos_completos == 3:
                            df_bloque.iloc[i] = bloque
                            df_asignatura.iloc[i] = materia
                            df_desempeño4.iloc[i] = 'X'
                            desempeno_encontrado = True
                            break

                        elif desempenos_completos == 4: 
                            df_bloque.iloc[i] = bloque
                            df_asignatura.iloc[i] = materia
                            df_desempeño5.iloc[i] = 'X'
                            desempeno_encontrado = True
                            break

                    if desempeno_encontrado:
                        break
                    
                for bloque in bloques:
                    notas_bloque = notas_estudiante[notas_estudiante.iloc[:, 6] == bloque]
                    
                    
                    if grado_actual in ['6','7','8','9']:
                        notas_bloque_filtradas = notas_bloque[notas_bloque.iloc[:, 5].isin(materias_especificas_6_7_8_9)]
                        longitud_bloque = len(notas_bloque_filtradas)
                        if longitud_bloque == 20 and not desempeno_encontrado:
                            continue 
            
                        if longitud_bloque < 20 and not desempeno_encontrado:
                            for materia in materias_especificas_6_7_8_9:
                                if materia not in notas_bloque_filtradas.iloc[:, 5].values:
                                    df_bloque.iloc[i] = bloque
                                    df_desempeño1.iloc[i] = 'X'
                                    df_asignatura.iloc[i] = materia
                                    desempeno_encontrado = True
                                    break
                                    
                    if grado_actual in ['10','11']:
                        notas_bloque_filtradas = notas_bloque[notas_bloque.iloc[:, 5].isin(materias_especificas_10_11)]
                        longitud_bloque = len(notas_bloque_filtradas)
                        if longitud_bloque == 20 and not desempeno_encontrado:
                            continue 
            
                        if longitud_bloque < 20 and not desempeno_encontrado:
                            for materia in materias_especificas_10_11:
                                if materia not in notas_bloque_filtradas.iloc[:, 5].values:
                                    df_bloque.iloc[i] = bloque
                                    df_desempeño1.iloc[i] = 'X'
                                    df_asignatura.iloc[i] = materia
                                    desempeno_encontrado = True
                                    break
                                    
                    if desempeno_encontrado:
                        break


        if area_seleccionada == 'L':
            
            for i in range(filasn):
                estudiante_actual = df_nombres.iloc[i, 0]
                grado_actual = df_nombres.iloc[i, 2]
                notas_estudiante = notas[(notas.iloc[:, 2] == estudiante_actual) & (notas.iloc[:, 3] == grado_actual)]
                desempeno_encontrado = False
            
                if df_nombres.iloc[i, 0] in (['LMOD1', 'LMOD2', 'MMOD1', 'MMOD2', 'WMOD1', 'WMOD2', 'JMOD1', 'JMOD2', 'VMOD1']):
                    desempeno_encontrado = True
                    continue 
                
                    
                bloques = ['A', 'B', 'C', 'D']
                asignaturas = ['Comunicación y sistemas simbólicos', 'Producción e interpretación de textos','Metodología']

                for materia in asignaturas:
                    notas_materia = notas_estudiante[notas_estudiante.iloc[:, 5] == materia]
                    
                    for bloque in bloques:
                        notas_bloque = notas_materia[notas_materia.iloc[:, 6] == bloque]
                        desempenos_completos = len(notas_bloque)

                        if desempenos_completos == 1:
                            df_bloque.iloc[i] = bloque
                            df_asignatura.iloc[i] = materia
                            df_desempeño2.iloc[i] = 'X'
                            desempeno_encontrado = True
                            break

                        elif desempenos_completos == 2:
                            df_bloque.iloc[i] = bloque
                            df_asignatura.iloc[i] = materia
                            df_desempeño3.iloc[i] = 'X'
                            desempeno_encontrado = True
                            break

                        elif desempenos_completos == 3:
                            df_bloque.iloc[i] = bloque
                            df_asignatura.iloc[i] = materia
                            df_desempeño4.iloc[i] = 'X'
                            desempeno_encontrado = True
                            break

                        elif desempenos_completos == 4: 
                            df_bloque.iloc[i] = bloque
                            df_asignatura.iloc[i] = materia
                            df_desempeño5.iloc[i] = 'X'
                            desempeno_encontrado = True
                            break

                    if desempeno_encontrado:
                        break
                    
                for bloque in bloques:
                    
                    notas_bloque = notas_estudiante[notas_estudiante.iloc[:, 6] == bloque]
                    notas_bloque_filtradas = notas_bloque[notas_bloque.iloc[:, 5].isin(asignaturas)]
                    longitud_bloque = len(notas_bloque_filtradas)
                    if longitud_bloque == 10 and not desempeno_encontrado:
                        continue 
            
                    if longitud_bloque < 10 and not desempeno_encontrado:
                        for materia in asignaturas:
                                if materia not in notas_bloque_filtradas.iloc[:, 5].values:
                                    df_bloque.iloc[i] = bloque
                                    df_desempeño1.iloc[i] = 'X'
                                    df_asignatura.iloc[i] = materia
                                    desempeno_encontrado = True
                                    break
                                    
                    if desempeno_encontrado:
                        break
        
        df_horario = pd.concat([df_nombres, df_bloque, df_asignatura, df_desempeño1, df_desempeño2, df_desempeño3, df_desempeño4, df_desempeño5], ignore_index=True, axis=1)

        for i in range(len(df_horario)):
            for k in range(i + 1, len(df_horario)):
                if df_horario.iloc[i, 0] == df_horario.iloc[k, 0]:
                    if 'X' in df_horario.iloc[i].values:
                        b = df_horario.iloc[i].eq('X').idxmax()
                        if b + 1 < len(df_horario.columns):
                            df_horario.iloc[k, b + 1] = 'X'
                            for col in range(5, b + 1):
                                df_horario.iloc[k, col] = np.nan
                    break

        st.subheader("F1")
        st.write(df_horario)

with col2:
    # Barra de búsqueda con autocompletado
    estudiante_seleccionado = st.selectbox(
        "Selecciona un estudiante:",
        estudiantes['ESTUDIANTE'].unique()
    )

    # Definir el orden personalizado para ETAPA
    orden_etapas = {"D1": 1, "D2": 2, "D3": 3, "D4": 4, "D5": 5}
    # Nombres de las columnas
    columnas_personalizadas = [f"A{i}" for i in range(1,6)] + [f"B{i}" for i in range(1,6)] + [f"C{i}" for i in range(1,6)] + [f"D{i}" for i in range(1,6)]

    # Procesar solo si hay selección
    if estudiante_seleccionado and area_seleccionada in ['C1','C2','S1','S2','L','M1','M2']:

        # Filtrar la base principal por el estudiante seleccionado
        grado = estudiantes.loc[estudiantes['ESTUDIANTE'] == estudiante_seleccionado, 'GRADO'].values[0]
        grado = str(grado)

        #aqui se crea el f5 de acuerdo al area si el grado es sexto o septimo

        if grado in ['6', '7'] and area_seleccionada in ['C1', 'C2']:
            F5_2 = pd.DataFrame(np.full((len(ciencias_6_7), 20), "", dtype=str), index=ciencias_6_7, columns= columnas_personalizadas)
            largo = {}
            for asignatura,_ in F5_2.iterrows():
                notas_asi = notas[ (notas['ESTUDIANTE'] == estudiante_seleccionado) & (notas['GRADO'] == grado) & (notas['ASIGNATURA'] == asignatura) ]
                notas_asi['ETAPA_ORD'] = notas_asi['ETAPA'].map(orden_etapas)
                notas_asi = notas_asi.sort_values(by=['BLOQUE', 'ETAPA_ORD'])
                notas_asi = notas_asi.drop(columns='ETAPA_ORD')
                lista_calificaciones = notas_asi['CALIFICACIÓN'].tolist()
                F5_2.iloc[F5_2.index.get_loc(asignatura), :len(lista_calificaciones)] = lista_calificaciones
            notas_año = notas[ (notas['ESTUDIANTE'] == estudiante_seleccionado) & (notas['GRADO'] == grado)]

        if grado in ['6', '7'] and area_seleccionada in ['C1', 'C2']:
            F5_2 = pd.DataFrame(np.full((len(sociales_6_7), 20), "", dtype=str), index=sociales_6_7, columns= columnas_personalizadas)
            largo = {}
            for asignatura,_ in F5_2.iterrows():
                notas_asi = notas[ (notas['ESTUDIANTE'] == estudiante_seleccionado) & (notas['GRADO'] == grado) & (notas['ASIGNATURA'] == asignatura) ]
                notas_asi['ETAPA_ORD'] = notas_asi['ETAPA'].map(orden_etapas)
                notas_asi = notas_asi.sort_values(by=['BLOQUE', 'ETAPA_ORD'])
                notas_asi = notas_asi.drop(columns='ETAPA_ORD')
                lista_calificaciones = notas_asi['CALIFICACIÓN'].tolist()
                F5_2.iloc[F5_2.index.get_loc(asignatura), :len(lista_calificaciones)] = lista_calificaciones
            notas_año = notas[ (notas['ESTUDIANTE'] == estudiante_seleccionado) & (notas['GRADO'] == grado)]

        if grado in ['6','7'] and area_seleccionada == 'L':
            F5_2 = pd.DataFrame(np.full((len(lenguaje_6_7), 20), "", dtype=str), index=lenguaje_6_7, columns= columnas_personalizadas)
            largo = {}
            for asignatura,_ in F5_2.iterrows():
                notas_asi = notas[ (notas['ESTUDIANTE'] == estudiante_seleccionado) & (notas['GRADO'] == grado) & (notas['ASIGNATURA'] == asignatura) ]
                notas_asi['ETAPA_ORD'] = notas_asi['ETAPA'].map(orden_etapas)
                notas_asi = notas_asi.sort_values(by=['BLOQUE', 'ETAPA_ORD'])
                notas_asi = notas_asi.drop(columns='ETAPA_ORD')
                lista_calificaciones = notas_asi['CALIFICACIÓN'].tolist()
                F5_2.iloc[F5_2.index.get_loc(asignatura), :len(lista_calificaciones)] = lista_calificaciones
            notas_año = notas[ (notas['ESTUDIANTE'] == estudiante_seleccionado) & (notas['GRADO'] == grado)]

        if grado in ['6', '7'] and area_seleccionada in ['M1', 'M2']:
            F5_2 = pd.DataFrame(np.full((len(matemati_6_7), 20), "", dtype=str), index=matemati_6_7, columns= columnas_personalizadas)
            largo = {}
            for asignatura,_ in F5_2.iterrows():
                notas_asi = notas[ (notas['ESTUDIANTE'] == estudiante_seleccionado) & (notas['GRADO'] == grado) & (notas['ASIGNATURA'] == asignatura) ]
                notas_asi['ETAPA_ORD'] = notas_asi['ETAPA'].map(orden_etapas)
                notas_asi = notas_asi.sort_values(by=['BLOQUE', 'ETAPA_ORD'])
                notas_asi = notas_asi.drop(columns='ETAPA_ORD')
                lista_calificaciones = notas_asi['CALIFICACIÓN'].tolist()
                F5_2.iloc[F5_2.index.get_loc(asignatura), :len(lista_calificaciones)] = lista_calificaciones
            notas_año = notas[ (notas['ESTUDIANTE'] == estudiante_seleccionado) & (notas['GRADO'] == grado)]


        ########################################## AQUI SE CREA EL F5 SI EL GRADO ES OCTAVO O NOVENO

        if grado in ['8', '9'] and area_seleccionada in ['C1', 'C2']:
            F5_2 = pd.DataFrame(np.full((len(ciencias_8_9), 20), "", dtype=str), index=ciencias_8_9, columns= columnas_personalizadas)
            largo = {}
            for asignatura,_ in F5_2.iterrows():
                notas_asi = notas[ (notas['ESTUDIANTE'] == estudiante_seleccionado) & (notas['GRADO'] == grado) & (notas['ASIGNATURA'] == asignatura) ]
                notas_asi['ETAPA_ORD'] = notas_asi['ETAPA'].map(orden_etapas)
                notas_asi = notas_asi.sort_values(by=['BLOQUE', 'ETAPA_ORD'])
                notas_asi = notas_asi.drop(columns='ETAPA_ORD')
                lista_calificaciones = notas_asi['CALIFICACIÓN'].tolist()
                F5_2.iloc[F5_2.index.get_loc(asignatura), :len(lista_calificaciones)] = lista_calificaciones
            notas_año = notas[ (notas['ESTUDIANTE'] == estudiante_seleccionado) & (notas['GRADO'] == grado)]

        if grado in ['8', '9'] and area_seleccionada in ['C1', 'C2']:
            F5_2 = pd.DataFrame(np.full((len(sociales_8_9), 20), "", dtype=str), index=sociales_8_9, columns= columnas_personalizadas)
            largo = {}
            for asignatura,_ in F5_2.iterrows():
                notas_asi = notas[ (notas['ESTUDIANTE'] == estudiante_seleccionado) & (notas['GRADO'] == grado) & (notas['ASIGNATURA'] == asignatura) ]
                notas_asi['ETAPA_ORD'] = notas_asi['ETAPA'].map(orden_etapas)
                notas_asi = notas_asi.sort_values(by=['BLOQUE', 'ETAPA_ORD'])
                notas_asi = notas_asi.drop(columns='ETAPA_ORD')
                lista_calificaciones = notas_asi['CALIFICACIÓN'].tolist()
                F5_2.iloc[F5_2.index.get_loc(asignatura), :len(lista_calificaciones)] = lista_calificaciones
            notas_año = notas[ (notas['ESTUDIANTE'] == estudiante_seleccionado) & (notas['GRADO'] == grado)]

        if grado in ['8','9'] and area_seleccionada == 'L':
            F5_2 = pd.DataFrame(np.full((len(lenguaje_8_9), 20), "", dtype=str), index=lenguaje_8_9, columns= columnas_personalizadas)
            largo = {}
            for asignatura,_ in F5_2.iterrows():
                notas_asi = notas[ (notas['ESTUDIANTE'] == estudiante_seleccionado) & (notas['GRADO'] == grado) & (notas['ASIGNATURA'] == asignatura) ]
                notas_asi['ETAPA_ORD'] = notas_asi['ETAPA'].map(orden_etapas)
                notas_asi = notas_asi.sort_values(by=['BLOQUE', 'ETAPA_ORD'])
                notas_asi = notas_asi.drop(columns='ETAPA_ORD')
                lista_calificaciones = notas_asi['CALIFICACIÓN'].tolist()
                F5_2.iloc[F5_2.index.get_loc(asignatura), :len(lista_calificaciones)] = lista_calificaciones
            notas_año = notas[ (notas['ESTUDIANTE'] == estudiante_seleccionado) & (notas['GRADO'] == grado)]

        if grado in ['8', '9'] and area_seleccionada in ['M1', 'M2']:
            F5_2 = pd.DataFrame(np.full((len(matemati_8_9), 20), "", dtype=str), index=matemati_8_9, columns= columnas_personalizadas)
            largo = {}
            for asignatura,_ in F5_2.iterrows():
                notas_asi = notas[ (notas['ESTUDIANTE'] == estudiante_seleccionado) & (notas['GRADO'] == grado) & (notas['ASIGNATURA'] == asignatura) ]
                notas_asi['ETAPA_ORD'] = notas_asi['ETAPA'].map(orden_etapas)
                notas_asi = notas_asi.sort_values(by=['BLOQUE', 'ETAPA_ORD'])
                notas_asi = notas_asi.drop(columns='ETAPA_ORD')
                lista_calificaciones = notas_asi['CALIFICACIÓN'].tolist()
                F5_2.iloc[F5_2.index.get_loc(asignatura), :len(lista_calificaciones)] = lista_calificaciones
            notas_año = notas[ (notas['ESTUDIANTE'] == estudiante_seleccionado) & (notas['GRADO'] == grado)]


        ######################## AQUI SE CREA EL F5 SI EL GRADO ES DECIMO

        if grado in ['10'] and area_seleccionada in ['C1', 'C2']:
            F5_2 = pd.DataFrame(np.full((len(ciencias_10), 20), "", dtype=str), index=ciencias_10, columns= columnas_personalizadas)
            largo = {}
            for asignatura,_ in F5_2.iterrows():
                notas_asi = notas[ (notas['ESTUDIANTE'] == estudiante_seleccionado) & (notas['GRADO'] == grado) & (notas['ASIGNATURA'] == asignatura) ]
                notas_asi['ETAPA_ORD'] = notas_asi['ETAPA'].map(orden_etapas)
                notas_asi = notas_asi.sort_values(by=['BLOQUE', 'ETAPA_ORD'])
                notas_asi = notas_asi.drop(columns='ETAPA_ORD')
                lista_calificaciones = notas_asi['CALIFICACIÓN'].tolist()
                F5_2.iloc[F5_2.index.get_loc(asignatura), :len(lista_calificaciones)] = lista_calificaciones
            notas_año = notas[ (notas['ESTUDIANTE'] == estudiante_seleccionado) & (notas['GRADO'] == grado)]

        if grado in ['10'] and area_seleccionada in ['C1', 'C2']:
            F5_2 = pd.DataFrame(np.full((len(sociales_10), 20), "", dtype=str), index=sociales_10, columns= columnas_personalizadas)
            largo = {}
            for asignatura,_ in F5_2.iterrows():
                notas_asi = notas[ (notas['ESTUDIANTE'] == estudiante_seleccionado) & (notas['GRADO'] == grado) & (notas['ASIGNATURA'] == asignatura) ]
                notas_asi['ETAPA_ORD'] = notas_asi['ETAPA'].map(orden_etapas)
                notas_asi = notas_asi.sort_values(by=['BLOQUE', 'ETAPA_ORD'])
                notas_asi = notas_asi.drop(columns='ETAPA_ORD')
                lista_calificaciones = notas_asi['CALIFICACIÓN'].tolist()
                F5_2.iloc[F5_2.index.get_loc(asignatura), :len(lista_calificaciones)] = lista_calificaciones
            notas_año = notas[ (notas['ESTUDIANTE'] == estudiante_seleccionado) & (notas['GRADO'] == grado)]

        if grado in ['10'] and area_seleccionada == 'L':
            F5_2 = pd.DataFrame(np.full((len(lenguaje_10), 20), "", dtype=str), index=lenguaje_10, columns= columnas_personalizadas)
            largo = {}
            for asignatura,_ in F5_2.iterrows():
                notas_asi = notas[ (notas['ESTUDIANTE'] == estudiante_seleccionado) & (notas['GRADO'] == grado) & (notas['ASIGNATURA'] == asignatura) ]
                notas_asi['ETAPA_ORD'] = notas_asi['ETAPA'].map(orden_etapas)
                notas_asi = notas_asi.sort_values(by=['BLOQUE', 'ETAPA_ORD'])
                notas_asi = notas_asi.drop(columns='ETAPA_ORD')
                lista_calificaciones = notas_asi['CALIFICACIÓN'].tolist()
                F5_2.iloc[F5_2.index.get_loc(asignatura), :len(lista_calificaciones)] = lista_calificaciones
            notas_año = notas[ (notas['ESTUDIANTE'] == estudiante_seleccionado) & (notas['GRADO'] == grado)]

        if grado in ['10'] and area_seleccionada in ['M1', 'M2']:
            F5_2 = pd.DataFrame(np.full((len(matemati_10), 20), "", dtype=str), index=matemati_10, columns= columnas_personalizadas)
            largo = {}
            for asignatura,_ in F5_2.iterrows():
                notas_asi = notas[ (notas['ESTUDIANTE'] == estudiante_seleccionado) & (notas['GRADO'] == grado) & (notas['ASIGNATURA'] == asignatura) ]
                notas_asi['ETAPA_ORD'] = notas_asi['ETAPA'].map(orden_etapas)
                notas_asi = notas_asi.sort_values(by=['BLOQUE', 'ETAPA_ORD'])
                notas_asi = notas_asi.drop(columns='ETAPA_ORD')
                lista_calificaciones = notas_asi['CALIFICACIÓN'].tolist()
                F5_2.iloc[F5_2.index.get_loc(asignatura), :len(lista_calificaciones)] = lista_calificaciones
            notas_año = notas[ (notas['ESTUDIANTE'] == estudiante_seleccionado) & (notas['GRADO'] == grado)]


        ######################################## AQUI SE CREA EL F5 SI EL GRADO ES 11

        if grado in ['11'] and area_seleccionada in ['C1', 'C2']:
            F5_2 = pd.DataFrame(np.full((len(ciencias_11), 20), "", dtype=str), index=ciencias_11, columns= columnas_personalizadas)
            largo = {}
            for asignatura,_ in F5_2.iterrows():
                notas_asi = notas[ (notas['ESTUDIANTE'] == estudiante_seleccionado) & (notas['GRADO'] == grado) & (notas['ASIGNATURA'] == asignatura) ]
                notas_asi['ETAPA_ORD'] = notas_asi['ETAPA'].map(orden_etapas)
                notas_asi = notas_asi.sort_values(by=['BLOQUE', 'ETAPA_ORD'])
                notas_asi = notas_asi.drop(columns='ETAPA_ORD')
                lista_calificaciones = notas_asi['CALIFICACIÓN'].tolist()
                F5_2.iloc[F5_2.index.get_loc(asignatura), :len(lista_calificaciones)] = lista_calificaciones
            notas_año = notas[ (notas['ESTUDIANTE'] == estudiante_seleccionado) & (notas['GRADO'] == grado)]

        if grado in ['11'] and area_seleccionada in ['S1', 'S2']:
            F5_2 = pd.DataFrame(np.full((len(sociales_11), 20), "", dtype=str), index=sociales_11, columns= columnas_personalizadas)
            largo = {}
            for asignatura,_ in F5_2.iterrows():
                notas_asi = notas[ (notas['ESTUDIANTE'] == estudiante_seleccionado) & (notas['GRADO'] == grado) & (notas['ASIGNATURA'] == asignatura) ]
                notas_asi['ETAPA_ORD'] = notas_asi['ETAPA'].map(orden_etapas)
                notas_asi = notas_asi.sort_values(by=['BLOQUE', 'ETAPA_ORD'])
                notas_asi = notas_asi.drop(columns='ETAPA_ORD')
                lista_calificaciones = notas_asi['CALIFICACIÓN'].tolist()
                F5_2.iloc[F5_2.index.get_loc(asignatura), :len(lista_calificaciones)] = lista_calificaciones
            notas_año = notas[ (notas['ESTUDIANTE'] == estudiante_seleccionado) & (notas['GRADO'] == grado)]

        if grado in ['11'] and area_seleccionada == 'L':
            F5_2 = pd.DataFrame(np.full((len(lenguaje_11), 20), "", dtype=str), index=lenguaje_11, columns= columnas_personalizadas)
            largo = {}
            for asignatura,_ in F5_2.iterrows():
                notas_asi = notas[ (notas['ESTUDIANTE'] == estudiante_seleccionado) & (notas['GRADO'] == grado) & (notas['ASIGNATURA'] == asignatura) ]
                notas_asi['ETAPA_ORD'] = notas_asi['ETAPA'].map(orden_etapas)
                notas_asi = notas_asi.sort_values(by=['BLOQUE', 'ETAPA_ORD'])
                notas_asi = notas_asi.drop(columns='ETAPA_ORD')
                lista_calificaciones = notas_asi['CALIFICACIÓN'].tolist()
                F5_2.iloc[F5_2.index.get_loc(asignatura), :len(lista_calificaciones)] = lista_calificaciones
            notas_año = notas[ (notas['ESTUDIANTE'] == estudiante_seleccionado) & (notas['GRADO'] == grado)]

        if grado in ['11'] and area_seleccionada in ['M1', 'M2']:
            F5_2 = pd.DataFrame(np.full((len(matemati_11), 20), "", dtype=str), index=matemati_11, columns= columnas_personalizadas)
            largo = {}
            for asignatura,_ in F5_2.iterrows():
                notas_asi = notas[ (notas['ESTUDIANTE'] == estudiante_seleccionado) & (notas['GRADO'] == grado) & (notas['ASIGNATURA'] == asignatura) ]
                notas_asi['ETAPA_ORD'] = notas_asi['ETAPA'].map(orden_etapas)
                notas_asi = notas_asi.sort_values(by=['BLOQUE', 'ETAPA_ORD'])
                notas_asi = notas_asi.drop(columns='ETAPA_ORD')
                lista_calificaciones = notas_asi['CALIFICACIÓN'].tolist()
                F5_2.iloc[F5_2.index.get_loc(asignatura), :len(lista_calificaciones)] = lista_calificaciones
            notas_año = notas[ (notas['ESTUDIANTE'] == estudiante_seleccionado) & (notas['GRADO'] == grado)]

    st.subheader("Notas")
    st.write(F5_2)

