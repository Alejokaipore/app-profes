# db_utils.py
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text  # Agregar text aquí

def crear_engine():
    # Obtener los secretos dentro de la función
    host = st.secrets["mysql"]["host"]
    port = st.secrets["mysql"]["port"]
    user = st.secrets["mysql"]["user"]
    password = st.secrets["mysql"]["password"]
    database = st.secrets["mysql"]["database"]
    
    # Configuración SSL para PlanetScale
    try:
        ssl_args = {"ssl": {"verify_ssl_cert": True}}
        
        connection_string = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
        
        return create_engine(
            connection_string,
            connect_args=ssl_args
        )
    except Exception as e:
        st.error(f"Error con SSL básico: {e}")
        # Opción 2: Sin SSL args específicos (fallback)
        return create_engine(
            f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
        )

def obtener_notas_planetscale():
    try:
        query1 = text("""
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
            LIMIT 70000
        """)
        
        query2 = text("""
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
            LIMIT 100000 OFFSET 70000
        """)
        
        # Usar la función crear_engine() que ya tienes
        engine = crear_engine()
        with engine.connect() as conn:
            df1 = pd.read_sql(query1, conn)
            df2 = pd.read_sql(query2, conn)
        
        df = pd.concat([df1, df2], ignore_index=True)
        return df
        
    except Exception as e:
        st.error(f"Error en obtener_notas_planetscale: {e}")
        return pd.DataFrame()

def listado_general_planetscale():
    try:
        query = text("SELECT estudiante, grupo, grado, dg, correo, meta FROM estudiantes")
        
        # Usar la función crear_engine() que ya tienes
        engine = crear_engine()
        with engine.connect() as conn:
            df = pd.read_sql(query, conn)
        return df
        
    except Exception as e:
        st.error(f"Error en listado_general_planetscale: {e}")
        return pd.DataFrame()