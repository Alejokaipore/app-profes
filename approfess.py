import pandas as pd  # type: ignore
import numpy as np  # type: ignore
import streamlit as st
from corregir_nombres import corregir_nombre
import requests
from io import BytesIO
import warnings
import matplotlib.pyplot as plt # type: ignore
from datetime import datetime
import pytz
from sqlalchemy import text
import mysql.connector
from db_utils import crear_engine, obtener_notas_planetscale,listado_general_planetscale, planeacion_semanal_planetscale



st.set_page_config(layout="wide")


ingles = ['INGLES LISTENING','INGLES READING','INGLES SPEAKING', 'INGLES WRITING']

def cargar_listado():
    df = listado_general_planetscale()
    df['grado'] = df['grado'].astype(str)
    df['estudiante'] = df['estudiante'].apply(corregir_nombre)
    df = df[df['grado'].isin(['1','2','3','4','5'])]
    return df

@st.cache_data
def cargar_notas():
    df = obtener_notas_planetscale()
    df['grado'] = df['grado'].astype(str)
    df['estudiante'] = df['estudiante'].apply(corregir_nombre)
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
    df = df[~df['asignatura'].isin(ingles)]
    return df

@st.cache_data
def cargar_notas_ingles():
    df = obtener_notas_planetscale()
    df['grado'] = df['grado'].astype(str)
    df['estudiante'] = df['estudiante'].apply(corregir_nombre)
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
    df = df[df['asignatura'].isin(ingles)]
    return df



notas = cargar_notas()
planeacion_primaria = planeacion_semanal_planetscale('primaria')
planeacion_primaria.insert(1, 'ingles', 'x') #Se agrega columna ingles despues de estudiante porque el codigo para generar F1's lee por ubicacion de columna
estudiantes = cargar_listado()
notas_ingles = cargar_notas_ingles()

notas['grado'] = notas['grado'].astype(str)
notas['estudiante'] = notas['estudiante'].apply(corregir_nombre)

asignaturas_1_5= ['BIOLOGIA','QUIMICA','MEDIO AMBIENTE','FISICA',
                  'HISTORIA', 'GEOGRAFIA', 'PARTICIPACION POLITICA','PENSAMIENTO RELIGIOSO',
                  'COMUNICACION Y SISTEMAS SIMBOLICOS','PRODUCCION E INTERPRETACION DE TEXTOS',
                  'INGLES LISTENING','INGLES READING','INGLES SPEAKING', 'INGLES WRITING',
                  'ARITMETICA','ANIMAPLANOS','ESTADISTICA', 'GEOMETRIA', 'DIBUJO TECNICO', 'SISTEMAS']


ciencias_1_5    = ['BIOLOGIA','QUIMICA','MEDIO AMBIENTE','FISICA','ANIMAPLANOS']
sociales_1_5    = ['HISTORIA', 'GEOGRAFIA', 'PARTICIPACION POLITICA','PENSAMIENTO RELIGIOSO','ANIMAPLANOS']
lenguaje_1_5    = ['COMUNICACION Y SISTEMAS SIMBOLICOS','PRODUCCION E INTERPRETACION DE TEXTOS','PENSAMIENTO RELIGIOSO','ANIMAPLANOS']
matematicas_1_5 = ['ARITMETICA','ANIMAPLANOS','ESTADISTICA', 'GEOMETRIA', 'DIBUJO TECNICO', 'SISTEMAS']


col1, col2 = st.columns(2)

with col1:

    # Barra de búsqueda con opciones específicas
    area_seleccionada = st.selectbox(
        "Selecciona una opción:",
        ['C', 'S', 'L', 'M', 'E']
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

        # Crear un diccionario clave estudiante y valor grupo
        grupo_map = dict(zip(estudiantes['estudiante'], estudiantes['grupo']))
        grado_map = dict(zip(estudiantes['estudiante'], estudiantes['grado']))

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


        if area_seleccionada == 'M':
            
            for i in range(filasn): #Aca hace un proceso iterativo (realiza la accion tantas veces como estudiantes haya en el listado del area esa semana)
                estudiante_actual = df_nombres.iloc[i, 0] #define el estudiante actual
                grado_actual = df_nombres.iloc[i, 2] #define el el grado actual del estudiante
                notas_estudiante = notas[(notas.iloc[:, 2] == estudiante_actual) & (notas.iloc[:, 3] == grado_actual)] #filtra la base de datos con las nostas unicamente del estudiante y su grado actual
                desempeno_encontrado = False # Bandera booleana para terminar el proceso iterativo una vez se asigne el desempeño 
            
                if df_nombres.iloc[i, 0] in (['LMOD1', 'LMOD2', 'MMOD1', 'MMOD2', 'WMOD1', 'WMOD2', 'JMOD1', 'JMOD2', 'VMOD1']): #omite el proceso a continuacion si el nombre del listado es uno de los modulos
                    desempeno_encontrado = True
                    continue
                    
                bloques = ['A', 'B', 'C', 'D'] #define los bloques que se pueden encontrar en la base de datos
                asignaturas = ['ARITMETICA','ANIMAPLANOS','ESTADISTICA', 'GEOMETRIA', 'DIBUJO TECNICO', 'SISTEMAS'] #define las asignaturas de Matematicas

                for bloque in bloques:
                    notas_bloque_completo = notas_estudiante[notas_estudiante['bloque'] == bloque ]
                    notas_bloque_matematicas = notas_estudiante[ (notas_estudiante['bloque'] == bloque) & (notas_estudiante['asignatura'].isin(asignaturas)) ]
                    if (len(notas_bloque_completo) < 80) and (len(notas_bloque_matematicas) == 30):
                        desempeno_encontrado = True
                        break

                if desempeno_encontrado:
                        continue
                    

                for materia in asignaturas: #hace el proceso de iterar sobre las materias antes definidas para el estudiante actual, para ejemplos de esta descripcion podemos pensar que empieza con aritmetica
                    notas_materia = notas_estudiante[notas_estudiante.iloc[:, 5] == materia] # como ya se habia filtrado las notas del estudiante y su grado actual hace un nuevo filtro con solamente las notas de aritmetica
                    
                    for bloque in bloques: #empieza a iterar sobre los bloques
                        notas_bloque = notas_materia[notas_materia.iloc[:, 6] == bloque] # hace un nuevo filtro a los tres ya aplicados antes, esta vez con el bloque, supongamos que empiza con bloque 'A'
                        desempenos_completos = len(notas_bloque) #cuenta cuantos desempeños tiene el estudiante con todos los filtros ya aplicados

                        #en los cuatro siguientes condicionales (que estan marcados) verifica la cantidad de notas que tiene el estudiante con los filtros aplicas
                        #si tiene un desempeño le asigna el desempeño 2 (marca una X en el segundo vector creado al inicio de este bloque)
                        #si tiene dos desempeños le asigna el desempeño 3 (marca una X en el tercer vector creado al inicio de este bloque)
                        #asi unicamente hasta si tiene cuatro desempeños ya que si tiene cinco sigue iterando y pasa al siguiente bloque, si en los cuatro bloques tiene cero 
                        #o cinco desempeños simplemente esta parte del codigo no hace nada
                        #si por el contrario asigno un desempeño, se activa la bandera booleana y omite el resto del codigo y pasa al siguiente estudiante
                        if desempenos_completos == 1: #1
                            df_bloque.iloc[i] = bloque
                            df_asignatura.iloc[i] = materia
                            df_desempeño2.iloc[i] = 'X'
                            desempeno_encontrado = True
                            break

                        elif desempenos_completos == 2: #2
                            df_bloque.iloc[i] = bloque
                            df_asignatura.iloc[i] = materia
                            df_desempeño3.iloc[i] = 'X'
                            desempeno_encontrado = True
                            break

                        elif desempenos_completos == 3: #3
                            df_bloque.iloc[i] = bloque
                            df_asignatura.iloc[i] = materia
                            df_desempeño4.iloc[i] = 'X'
                            desempeno_encontrado = True
                            break

                        elif desempenos_completos == 4: #4
                            df_bloque.iloc[i] = bloque
                            df_asignatura.iloc[i] = materia
                            df_desempeño5.iloc[i] = 'X'
                            desempeno_encontrado = True
                            break

                    if desempeno_encontrado:
                        break

            # si el codigo llega hasta este punto es porque aun no le ha asignado ningun desempeño al estudiante (no tiene procesos abiertos)
            # es decir que se tiene que buscar desde el bloque A hasta el bloque D, del area de Matematicas donde no tiene completos los desempeños 
            # segun el bloque donde no tiene completos los desempeños se le asigna el primer desempeño (la parte anterior del codigo no lo hace)
            # de la asignatura que no tenga desempeños en dicho bloque
                
                for bloque in bloques: #itera sobre los bloques (Pasobloque)
                    
                    notas_bloque = notas_estudiante[notas_estudiante.iloc[:, 6] == bloque] # al filtro de las nostas del estudiante actual y su grado actual adicional se le aplica el filtro del bloque
                    notas_bloque_filtradas = notas_bloque[notas_bloque.iloc[:, 5].isin(asignaturas)] # al filtro anterior le asigna el filtro unicamente de las asignaturas del area de matematicas
                    longitud_bloque = len(notas_bloque_filtradas) # mira cuantos desempeños hay con todos los filtros aplicados
                    if longitud_bloque == 30 and not desempeno_encontrado: # sin son 30 desempeños, tiene el bloque completo, no ejecuta el resto del codigo y se devuelve para iteral al siguiente bloque (Pasobloque), si no son 30 simplemente sigue el resto del codigo y aqui no hace nada
                        continue 
            
                    if longitud_bloque < 30 and not desempeno_encontrado: # si son menos de 25 desempeños realiza lo que hay dentro de esta aprte del codigo
                        for materia in asignaturas: # itera sobre las asignaturas del area de matematicas
                                if materia not in notas_bloque_filtradas.iloc[:, 5].values: #si el nombre de la materia actual (empieza por aritmetica) no esta en en la base con todos los filtros aplicados entonces le asigna el bloque y la materia sobre la cual le aplico el filtro y sigue con el siguiente estudiante en la lista.
                                    df_bloque.iloc[i] = bloque
                                    df_desempeño1.iloc[i] = 'X'
                                    df_asignatura.iloc[i] = materia
                                    desempeno_encontrado = True
                                    break
                                    
                    if desempeno_encontrado:
                        break

        #Si el area que se ingreso es 'S' ejecutara esta parte del codigo
        if area_seleccionada == 'S':
            
            for i in range(filasn):
                estudiante_actual = df_nombres.iloc[i, 0]
                grado_actual = df_nombres.iloc[i, 2]
                notas_estudiante = notas[(notas.iloc[:, 2] == estudiante_actual) & (notas.iloc[:, 3] == grado_actual)]
                desempeno_encontrado = False
            
                if df_nombres.iloc[i, 0] in (['LMOD1', 'LMOD2', 'MMOD1', 'MMOD2', 'WMOD1', 'WMOD2', 'JMOD1', 'JMOD2', 'VMOD1']):
                    desempeno_encontrado = True
                    continue 
                
                    
                bloques = ['A', 'B', 'C', 'D']
                asignaturas = ['HISTORIA', 'GEOGRAFIA', 'PARTICIPACION POLITICA','PENSAMIENTO RELIGIOSO']

                for bloque in bloques:
                    notas_bloque_completo = notas_estudiante[notas_estudiante['bloque'] == bloque ]
                    notas_bloque_sociales = notas_estudiante[ (notas_estudiante['bloque'] == bloque) & (notas_estudiante['asignatura'].isin(asignaturas)) ]
                    if (len(notas_bloque_completo) < 80) and (len(notas_bloque_sociales) == 20):
                        desempeno_encontrado = True
                        break

                if desempeno_encontrado:
                        continue

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
                                    
                    if desempeno_encontrado:
                        break
                        

        #Si el area que se ingreso es 'L' ejecutara esta parte del codigo
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
                asignaturas = ['COMUNICACION Y SISTEMAS SIMBOLICOS','PRODUCCION E INTERPRETACION DE TEXTOS','PENSAMIENTO RELIGIOSO']


                for bloque in bloques:
                    notas_bloque_completo = notas_estudiante[notas_estudiante['bloque'] == bloque ]
                    notas_bloque_lenguaje = notas_estudiante[ (notas_estudiante['bloque'] == bloque) & (notas_estudiante['asignatura'].isin(asignaturas)) ]
                    if (len(notas_bloque_completo) < 80) and (len(notas_bloque_lenguaje) == 15):
                        desempeno_encontrado = True
                        break

                if desempeno_encontrado:
                        continue

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
                    if longitud_bloque == 15 and not desempeno_encontrado:
                        continue 
            
                    if longitud_bloque < 15 and not desempeno_encontrado:
                        for materia in asignaturas:
                                if materia not in notas_bloque_filtradas.iloc[:, 5].values:
                                    df_bloque.iloc[i] = bloque
                                    df_desempeño1.iloc[i] = 'X'
                                    df_asignatura.iloc[i] = materia
                                    desempeno_encontrado = True
                                    break
                                    
                    if desempeno_encontrado:
                        break
                        
        #Si el area que se ingreso es 'C' ejecutara esta parte del codigo
        if area_seleccionada == 'C':
            
            for i in range(filasn):
                estudiante_actual = df_nombres.iloc[i, 0]
                grado_actual = df_nombres.iloc[i, 2]
                notas_estudiante = notas[(notas.iloc[:, 2] == estudiante_actual) & (notas.iloc[:, 3] == grado_actual)]
                desempeno_encontrado = False
            
                if df_nombres.iloc[i, 0] in (['LMOD1', 'LMOD2', 'MMOD1', 'MMOD2', 'WMOD1', 'WMOD2', 'JMOD1', 'JMOD2', 'VMOD1']):
                    desempeno_encontrado = True
                    continue 
                
                    
                bloques = ['A', 'B', 'C', 'D']
                asignaturas = ['BIOLOGIA','QUIMICA','MEDIO AMBIENTE','FISICA']



                for bloque in bloques:
                    notas_bloque_completo = notas_estudiante[notas_estudiante['bloque'] == bloque ]
                    notas_bloque_ciencias = notas_estudiante[ (notas_estudiante['bloque'] == bloque) & (notas_estudiante['asignatura'].isin(asignaturas)) ]
                    if (len(notas_bloque_completo) < 80) and (len(notas_bloque_ciencias) == 20):
                        desempeno_encontrado = True
                        break

                if desempeno_encontrado:
                        continue

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
                                    
                    if desempeno_encontrado:
                        break

        # En este punto ya esta todo asignado, y unifica todos los vectores creados en el bloque anterior para que quede todo en uno solo
        df_horario = pd.concat([df_nombres, df_bloque, df_asignatura, df_desempeño1, df_desempeño2, df_desempeño3, df_desempeño4, df_desempeño5], ignore_index=True, axis=1)

        #A este punto ya con todo asignado solo hay una cosa que modificar, supongamos que en la lista el estudiante Cristian Moreno Gonzales aparecio tres veces, entonces le asigno
        # las tres veces lo mismo (por ejemplo las tres veces le asigno Aritmetica el segundo desempeño) lo que hace esta parte del codigo es crear la 'escalera'
        # es decir, la primer vez la deja como se le asigno pero la segunda le cambia la X al desempeño siguiente (siguiendo con el ejemplo de Cristian le queda
        # en una escalera sus tareas a realizar, quedandole primero el segundo desempeño, luego el tercero y luego el cuarto)
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
        

        if area_seleccionada == 'M':
            adicionar = ['LIC-M','OLIMPIADAS']
            for excepcion in adicionar:
                # Buscar en qué columnas aparece exactamente el valor de la variable 'excepcion'
                mask = planeacion_primaria.apply(lambda col: col == excepcion)
                columnas_con_valor = mask.any(axis=0)
                #poner en una lista las columnas que tienen el valor de excepcion
                columnas_resultado = columnas_con_valor[columnas_con_valor].index.tolist()
                #para cada columna en la que aprecio la excepcion hacer el filtrado y poner la lista de estudiantes
                for columna in columnas_resultado:
                    if columna == 'l1':
                        lista_del_modulo = planeacion_primaria[planeacion_primaria[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "LMOD1"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'l2':
                        lista_del_modulo = planeacion_primaria[planeacion_primaria[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "LMOD2"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'm1':
                        lista_del_modulo = planeacion_primaria[planeacion_primaria[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "MMOD1"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'm2':
                        lista_del_modulo = planeacion_primaria[planeacion_primaria[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "MMOD2"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'w1':
                        lista_del_modulo = planeacion_primaria[planeacion_primaria[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "WMOD1"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'w2':
                        lista_del_modulo = planeacion_primaria[planeacion_primaria[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "WMOD2"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'j1':
                        lista_del_modulo = planeacion_primaria[planeacion_primaria[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "JMOD1"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'j2':
                        lista_del_modulo = planeacion_primaria[planeacion_primaria[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "JMOD2"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'v1':
                        lista_del_modulo = planeacion_primaria[planeacion_primaria[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "VMOD1"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'v2':
                        lista_del_modulo = planeacion_primaria[planeacion_primaria[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "VMOD2"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)


        if area_seleccionada == 'C':
            adicionar = ['LIC-C']
            for excepcion in adicionar:
                # Buscar en qué columnas aparece exactamente el valor de la variable 'excepcion'
                mask = planeacion_primaria.apply(lambda col: col == excepcion)
                columnas_con_valor = mask.any(axis=0)
                #poner en una lista las columnas que tienen el valor de excepcion
                columnas_resultado = columnas_con_valor[columnas_con_valor].index.tolist()
                #para cada columna en la que aprecio la excepcion hacer el filtrado y poner la lista de estudiantes
                for columna in columnas_resultado:
                    if columna == 'l1':
                        lista_del_modulo = planeacion_primaria[planeacion_primaria[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "LMOD1"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'l2':
                        lista_del_modulo = planeacion_primaria[planeacion_primaria[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "LMOD2"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'm1':
                        lista_del_modulo = planeacion_primaria[planeacion_primaria[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "MMOD1"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'm2':
                        lista_del_modulo = planeacion_primaria[planeacion_primaria[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "MMOD2"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'w1':
                        lista_del_modulo = planeacion_primaria[planeacion_primaria[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "WMOD1"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'w2':
                        lista_del_modulo = planeacion_primaria[planeacion_primaria[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "WMOD2"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'j1':
                        lista_del_modulo = planeacion_primaria[planeacion_primaria[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "JMOD1"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'j2':
                        lista_del_modulo = planeacion_primaria[planeacion_primaria[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "JMOD2"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'v1':
                        lista_del_modulo = planeacion_primaria[planeacion_primaria[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "VMOD1"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'v2':
                        lista_del_modulo = planeacion_primaria[planeacion_primaria[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "VMOD2"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)

        if area_seleccionada == 'S':
            adicionar = ['LIC-S','KAIPOMUN']
            for excepcion in adicionar:
                # Buscar en qué columnas aparece exactamente el valor de la variable 'excepcion'
                mask = planeacion_primaria.apply(lambda col: col == excepcion)
                columnas_con_valor = mask.any(axis=0)
                #poner en una lista las columnas que tienen el valor de excepcion
                columnas_resultado = columnas_con_valor[columnas_con_valor].index.tolist()
                #para cada columna en la que aprecio la excepcion hacer el filtrado y poner la lista de estudiantes
                for columna in columnas_resultado:
                    if columna == 'l1':
                        lista_del_modulo = planeacion_primaria[planeacion_primaria[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "LMOD1"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'l2':
                        lista_del_modulo = planeacion_primaria[planeacion_primaria[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "LMOD2"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'm1':
                        lista_del_modulo = planeacion_primaria[planeacion_primaria[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "MMOD1"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'm2':
                        lista_del_modulo = planeacion_primaria[planeacion_primaria[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "MMOD2"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'w1':
                        lista_del_modulo = planeacion_primaria[planeacion_primaria[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "WMOD1"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'w2':
                        lista_del_modulo = planeacion_primaria[planeacion_primaria[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "WMOD2"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'j1':
                        lista_del_modulo = planeacion_primaria[planeacion_primaria[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "JMOD1"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'j2':
                        lista_del_modulo = planeacion_primaria[planeacion_primaria[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "JMOD2"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'v1':
                        lista_del_modulo = planeacion_primaria[planeacion_primaria[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "VMOD1"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'v2':
                        lista_del_modulo = planeacion_primaria[planeacion_primaria[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "VMOD2"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)

        if area_seleccionada == 'L':
            adicionar = ['LIC-L']
            for excepcion in adicionar:
                # Buscar en qué columnas aparece exactamente el valor de la variable 'excepcion'
                mask = planeacion_primaria.apply(lambda col: col == excepcion)
                columnas_con_valor = mask.any(axis=0)
                #poner en una lista las columnas que tienen el valor de excepcion
                columnas_resultado = columnas_con_valor[columnas_con_valor].index.tolist()
                #para cada columna en la que aprecio la excepcion hacer el filtrado y poner la lista de estudiantes
                for columna in columnas_resultado:
                    if columna == 'l1':
                        lista_del_modulo = planeacion_primaria[planeacion_primaria[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "LMOD1"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'l2':
                        lista_del_modulo = planeacion_primaria[planeacion_primaria[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "LMOD2"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'm1':
                        lista_del_modulo = planeacion_primaria[planeacion_primaria[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "MMOD1"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'm2':
                        lista_del_modulo = planeacion_primaria[planeacion_primaria[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "MMOD2"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'w1':
                        lista_del_modulo = planeacion_primaria[planeacion_primaria[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "WMOD1"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'w2':
                        lista_del_modulo = planeacion_primaria[planeacion_primaria[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "WMOD2"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'j1':
                        lista_del_modulo = planeacion_primaria[planeacion_primaria[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "JMOD1"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'j2':
                        lista_del_modulo = planeacion_primaria[planeacion_primaria[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "JMOD2"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'v1':
                        lista_del_modulo = planeacion_primaria[planeacion_primaria[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "VMOD1"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)
                    if columna == 'v2':
                        lista_del_modulo = planeacion_primaria[planeacion_primaria[f'{columna}']== excepcion]
                        primera_columna = lista_del_modulo.iloc[:, 0].tolist()
                        #buscar donde aparece LMOD1
                        idx = df_horario.index[df_horario.iloc[:, 0] == "VMOD2"][0]
                        parte_1 = df_horario.iloc[:idx+1]
                        parte_2 = df_horario.iloc[idx+1:]
                        #Crear data frame vacio para insertar
                        insertar = pd.DataFrame('', index=range(len(primera_columna)), columns=range(10))
                        insertar[0] = primera_columna 
                        insertar[4] = excepcion
                        df_horario = pd.concat ([parte_1, insertar, parte_2], ignore_index = True)

        

        st.subheader("F1")
        st.write(df_horario)

    # Diccionario de tablas según área
    tablas_por_area = {
        "Sociales": "primaria_s",
        "Matemáticas": "primaria_m",
        "Lenguaje": "primaria_l",
        "Ciencias": "primaria_c",
        "Inglés": "primaria_e"  # si existe
    }

    # Área seleccionada (ya la tienes de tu selectbox inicial)
    area_seleccionad = st.selectbox("Selecciona un área para ver la tabla:", list(tablas_por_area.keys()))

    tabla = tablas_por_area.get(area_seleccionad)

    if tabla:
        try:
            engine = crear_engine()  # Usa la misma función que ya tienes en db_utils.py
            
            with engine.connect() as conn:
                # Usar text() para el query
                query = text(f"SELECT fecha, estudiante, grado, docente,asignatura, bloque, periodo, etapa, calificacion  FROM {tabla} WHERE procesamiento = 'NO' ORDER BY fecha DESC")
                result = conn.execute(query)
                data = result.fetchall()
                cols = result.keys()  # nombres de columnas

            # Mostrar la tabla en Streamlit
            df = pd.DataFrame(data, columns=cols)
            st.write(f"Tabla: {tabla}")
            st.dataframe(df)
            
        except Exception as e:
            st.error(f"Ocurrió un error al cargar la tabla: {e}")
    else:
        st.warning("Área no válida seleccionada")


with col2:
    # Barra de búsqueda con autocompletado
    estudiante_seleccionado = st.selectbox(
        "Selecciona un estudiante:",
        estudiantes['estudiante'].unique()
    )

    # Definir el orden personalizado para etapa
    orden_etapas = {"D1": 1, "D2": 2, "D3": 3, "D4": 4, "D5": 5}
    # Nombres de las columnas
    columnas_personalizadas = [f"A{i}" for i in range(1,6)] + [f"B{i}" for i in range(1,6)] + [f"C{i}" for i in range(1,6)] + [f"D{i}" for i in range(1,6)]

    # Procesar solo si hay selección
    if estudiante_seleccionado and area_seleccionada in ['C','S','L','M','E']:

        # Filtrar la base principal por el estudiante seleccionado
        if area_seleccionada == 'E':
            grado_por_defecto = estudiantes.loc[estudiantes['estudiante'] == estudiante_seleccionado, 'grado'].values[0]
            grado = st.text_input("Grado", value=str(grado_por_defecto))

        else:
            grado = estudiantes.loc[estudiantes['estudiante'] == estudiante_seleccionado, 'grado'].values[0] 
            grado = str(grado)


        #aqui se crea el f5 de acuerdo al area

        if grado in ['1','2','3','4','5'] and area_seleccionada == 'C':
            F5_2 = pd.DataFrame(np.full((len(ciencias_1_5), 20), "", dtype=str), index=ciencias_1_5, columns= columnas_personalizadas)
            for asignatura,_ in F5_2.iterrows():
                notas_asi = notas[ (notas['estudiante'] == estudiante_seleccionado) & (notas['grado'] == grado) & (notas['asignatura'] == asignatura) ]
                notas_asi['ETAPA_ORD'] = notas_asi['etapa'].map(orden_etapas)
                notas_asi = notas_asi.sort_values(by=['bloque', 'ETAPA_ORD'])
                notas_asi = notas_asi.drop(columns='ETAPA_ORD')
                lista_calificaciones = notas_asi['calificacion'].tolist()
                F5_2.iloc[F5_2.index.get_loc(asignatura), :len(lista_calificaciones)] = lista_calificaciones

        if grado in ['1','2','3','4','5'] and area_seleccionada == 'S':
            F5_2 = pd.DataFrame(np.full((len(sociales_1_5), 20), "", dtype=str), index=sociales_1_5, columns= columnas_personalizadas)
            for asignatura,_ in F5_2.iterrows():
                notas_asi = notas[ (notas['estudiante'] == estudiante_seleccionado) & (notas['grado'] == grado) & (notas['asignatura'] == asignatura) ]
                notas_asi['ETAPA_ORD'] = notas_asi['etapa'].map(orden_etapas)
                notas_asi = notas_asi.sort_values(by=['bloque', 'ETAPA_ORD'])
                notas_asi = notas_asi.drop(columns='ETAPA_ORD')
                lista_calificaciones = notas_asi['calificacion'].tolist()
                F5_2.iloc[F5_2.index.get_loc(asignatura), :len(lista_calificaciones)] = lista_calificaciones

        if grado in ['1','2','3','4','5'] and area_seleccionada == 'L':
            F5_2 = pd.DataFrame(np.full((len(lenguaje_1_5), 20), "", dtype=str), index=lenguaje_1_5, columns= columnas_personalizadas)
            for asignatura,_ in F5_2.iterrows():
                notas_asi = notas[ (notas['estudiante'] == estudiante_seleccionado) & (notas['grado'] == grado) & (notas['asignatura'] == asignatura) ]
                notas_asi['ETAPA_ORD'] = notas_asi['etapa'].map(orden_etapas)
                notas_asi = notas_asi.sort_values(by=['bloque', 'ETAPA_ORD'])
                notas_asi = notas_asi.drop(columns='ETAPA_ORD')
                lista_calificaciones = notas_asi['calificacion'].tolist()
                F5_2.iloc[F5_2.index.get_loc(asignatura), :len(lista_calificaciones)] = lista_calificaciones

        if grado in ['1','2','3','4','5'] and area_seleccionada == 'M':
            F5_2 = pd.DataFrame(np.full((len(matematicas_1_5), 20), "", dtype=str), index=matematicas_1_5, columns= columnas_personalizadas)
            for asignatura,_ in F5_2.iterrows():
                notas_asi = notas[ (notas['estudiante'] == estudiante_seleccionado) & (notas['grado'] == grado) & (notas['asignatura'] == asignatura) ]
                notas_asi['ETAPA_ORD'] = notas_asi['etapa'].map(orden_etapas)
                notas_asi = notas_asi.sort_values(by=['bloque', 'ETAPA_ORD'])
                notas_asi = notas_asi.drop(columns='ETAPA_ORD')
                lista_calificaciones = notas_asi['calificacion'].tolist()
                F5_2.iloc[F5_2.index.get_loc(asignatura), :len(lista_calificaciones)] = lista_calificaciones
        
        if area_seleccionada == 'E':
            F5_2 = pd.DataFrame(np.full((len(ingles), 20), "", dtype=str), index=ingles, columns= columnas_personalizadas)
            for asignatura,_ in F5_2.iterrows():
                notas_asi = notas_ingles[ (notas_ingles['estudiante'] == estudiante_seleccionado) & (notas_ingles['grado'] == grado) & (notas_ingles['asignatura'] == asignatura) ]
                notas_asi['ETAPA_ORD'] = notas_asi['etapa'].map(orden_etapas)
                notas_asi = notas_asi.sort_values(by=['bloque', 'ETAPA_ORD'])
                notas_asi = notas_asi.drop(columns='ETAPA_ORD')
                lista_calificaciones = notas_asi['calificacion'].tolist()
                F5_2.iloc[F5_2.index.get_loc(asignatura), :len(lista_calificaciones)] = lista_calificaciones

    st.subheader("Notas")
    st.write(F5_2)

############################################## FORMULARIO PARA INGRESAR NOTAS ##############################################

    # Lista de areas
    materias = ["Matemáticas", "Lenguaje", "Inglés", "Ciencias", "Sociales"]

    # Selectbox para materia
    materia_seleccionada = st.selectbox("Selecciona una materia:", materias)

######################################################## CAMBIAR CADA PERIODO ##############################################
    # Selectbox para periodo
    periodo_seleccionado = '4'

    # Fijar zona horaria
    bogota = pytz.timezone("America/Bogota")
    fecha_actual = datetime.now(bogota).date()  # solo día, mes, año

    st.write(f"Fecha del registro: {fecha_actual}")
    st.write(f"Periodo actual: {periodo_seleccionado}")


   # --- Formulario ---
    with st.form("formulario_estudiante"):
        # Diccionario {estudiante: grado}
        estudiantes_dict = dict(zip(estudiantes["estudiante"], estudiantes["grado"]))

        if materia_seleccionada != 'Inglés':
            # Grado automático según estudiante
            grado = estudiantes_dict[estudiante_seleccionado]
            st.write(f"Grado del estudiante: {grado}")

            # "area" debe venir de la selección previa (fuera del formulario)
            if materia_seleccionada == "Ciencias":
                asignatura = st.selectbox("Asignatura", ciencias_1_5)
            elif materia_seleccionada == "Sociales":
                asignatura = st.selectbox("Asignatura", sociales_1_5)
            elif materia_seleccionada == "Lenguaje":
                asignatura = st.selectbox("Asignatura", lenguaje_1_5)
            elif materia_seleccionada == "Matemáticas":
                asignatura = st.selectbox("Asignatura", matematicas_1_5)
            elif materia_seleccionada == "Inglés":
                asignatura = st.selectbox("Asignatura", ingles)
            else:
                asignatura = None  # En caso de que no se haya escogido área

            # --- Otros campos ---
            bloque = st.selectbox("Bloque", ["A", "B", "C", "D"])
            etapa = st.selectbox("Etapa", ["D1", "D2", "D3", "D4", "D5"])
            calificacion = st.number_input("Calificación", min_value=3.6, max_value=5.0, step=0.1)


            # Docente y tabla según área
            area_info = {
                "Sociales": ("ANA MORA", "primaria_s"),
                "Matemáticas": ("GINA", "primaria_m"),
                "Lenguaje": ("CAMILA", "primaria_l"),
                "Ciencias": ("LEONARDO", "primaria_c"),
                "Inglés": ("JUAN ANDRÉS", "primaria_e")
            }

            docente, tabla = area_info.get(materia_seleccionada, ("Desconocido", None))
            st.write(f"Docente : {docente}")

            # --- Botón de submit ---
            submitted = st.form_submit_button("Guardar")

            if submitted:
                if asignatura is None or tabla is None:
                    st.warning("Selecciona un área válida primero")
                else:
                    try:
                        engine = crear_engine()
                        
                        with engine.connect() as conn:
                            query = text(f"""
                                INSERT INTO {tabla} (fecha, estudiante, grado, docente, asignatura, bloque, periodo, etapa, calificacion)
                                VALUES (:fecha, :estudiante, :grado, :docente, :asignatura, :bloque, :periodo, :etapa, :calificacion)
                            """)
                            
                            # Ejecutar con parámetros nombrados (más seguro y legible)
                            conn.execute(query, {
                                'fecha': fecha_actual,
                                'estudiante': estudiante_seleccionado,
                                'grado': grado,
                                'docente': docente,
                                'asignatura': asignatura,
                                'bloque': bloque,
                                'periodo': periodo_seleccionado,
                                'etapa': etapa,
                                'calificacion': calificacion
                            })
                            
                            # Hacer commit de la transacción
                            conn.commit()
                        
                        st.success(f"Registro guardado correctamente en {tabla} ✅")
                        
                    except Exception as e:
                        st.error(f"Ocurrió un error: {e}")

        else:
            
            
            grado = estudiantes_dict[estudiante_seleccionado]
            st.write(f"Grado del estudiante: {grado}")

            grado_distinto = st.text_input("Ingresar un grado distinto")

            # "area" debe venir de la selección previa (fuera del formulario)
            if materia_seleccionada == "Ciencias":
                asignatura = st.selectbox("Asignatura", ciencias_1_5)
            elif materia_seleccionada == "Sociales":
                asignatura = st.selectbox("Asignatura", sociales_1_5)
            elif materia_seleccionada == "Lenguaje":
                asignatura = st.selectbox("Asignatura", lenguaje_1_5)
            elif materia_seleccionada == "Matemáticas":
                asignatura = st.selectbox("Asignatura", matematicas_1_5)
            elif materia_seleccionada == "Inglés":
                asignatura = st.selectbox("Asignatura", ingles)
            else:
                asignatura = None  # En caso de que no se haya escogido área

            # --- Otros campos ---
            bloque = st.selectbox("Bloque", ["A", "B", "C", "D"])
            etapa = st.selectbox("Etapa", ["D1", "D2", "D3", "D4", "D5"])
            calificacion = st.number_input("Calificación", min_value=3.6, max_value=5.0, step=0.1)


            # Docente y tabla según área
            area_info = {
                "Sociales": ("ANA MORA", "primaria_s"),
                "Matemáticas": ("GINA", "primaria_m"),
                "Lenguaje": ("CAMILA", "primaria_l"),
                "Ciencias": ("LEONARDO", "primaria_c"),
                "Inglés": ("JUAN ANDRÉS", "primaria_e")
            }

            docente, tabla = area_info.get(materia_seleccionada, ("Desconocido", None))
            st.write(f"Docente : {docente}")

            # --- Botón de submit ---
            submitted = st.form_submit_button("Guardar")

            if submitted:
                if asignatura is None or tabla is None:
                    st.warning("Selecciona un área válida primero")
                else:
                    try:
                        engine = crear_engine()
                        
                        with engine.connect() as conn:
                            query = text(f"""
                                INSERT INTO {tabla} (fecha, estudiante, grado, docente, asignatura, bloque, periodo, etapa, calificacion)
                                VALUES (:fecha, :estudiante, :grado, :docente, :asignatura, :bloque, :periodo, :etapa, :calificacion)
                            """)
                            
                            # Ejecutar con parámetros nombrados (más seguro y legible)
                            conn.execute(query, {
                                'fecha': fecha_actual,
                                'estudiante': estudiante_seleccionado,
                                'grado': grado_distinto,
                                'docente': docente,
                                'asignatura': asignatura,
                                'bloque': bloque,
                                'periodo': periodo_seleccionado,
                                'etapa': etapa,
                                'calificacion': calificacion
                            })
                            
                            # Hacer commit de la transacción
                            conn.commit()
                        
                        st.success(f"Registro guardado correctamente en {tabla} ✅")
                        
                    except Exception as e:
                        st.error(f"Ocurrió un error: {e}")

            

