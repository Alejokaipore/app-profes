# db_utils.py
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import tempfile

host=st.secrets["mysql"]["host"],
port=st.secrets["mysql"]["port"],
user=st.secrets["mysql"]["user"],
password=st.secrets["mysql"]["password"],
database=st.secrets["mysql"]["database"]
ssl_ca = st.secrets["mysql"]["ssl_ca"]

def crear_engine():
    # Crear un archivo temporal con el contenido del certificado
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pem") as tmp:
        tmp.write(ssl_ca.encode("utf-8"))
        ca_path = tmp.name

    # Crear engine usando la ruta del archivo temporal
    return create_engine(
        f"mysql+pymysql://{user}:{password}@{host}/{database}",
        connect_args={
            "ssl": {
                "ca": ca_path
            }
        }
    )

def obtener_notas_planetscale():
   
    query1 = """
        SELECT 
            n.fecha,
            n.anio,
            e.estudiante,
            n.grado,
            n.docente,
            a.asignatura,
            n.bloque,
            n.periodo,
            n.semana,
            n.etapa,
            n.calificacion
        FROM notas n
        JOIN estudiantes e ON e.codigo = n.codigo_estudiante
        JOIN asignaturas a ON a.codigo = n.codigo_asignatura
        LIMIT 700
        """
    query2 = """
        SELECT 
            n.fecha,
            n.anio,
            e.estudiante,
            n.grado,
            n.docente,
            a.asignatura,
            n.bloque,
            n.periodo,
            n.semana,
            n.etapa,
            n.calificacion
        FROM notas n
        JOIN estudiantes e ON e.codigo = n.codigo_estudiante
        JOIN asignaturas a ON a.codigo = n.codigo_asignatura
        LIMIT 100000 OFFSET 700
        """
    
    engine = create_engine(
        f"mysql+pymysql://{user}:{password}@{host}/{database}"
    )
    with engine.connect() as conn:
        df1 = pd.read_sql(query1, conn)
        df2 = pd.read_sql(query2, conn)
    df = pd.concat([df1, df2], ignore_index=True)
    return df

def listado_general_planetscale():
    query = "SELECT estudiante, grupo, grado, dg, correo, meta FROM estudiantes"
    engine = create_engine(
        f"mysql+pymysql://{user}:{password}@{host}/{database}"
    )
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    return df