import re
from unidecode import unidecode

def corregir_nombre(nombre):
    # Verificar que el nombre sea una cadena de texto
    if not isinstance(nombre, str):
        raise ValueError("El nombre debe ser una cadena de texto.")

    # Eliminar espacios al inicio y final
    nombre = nombre.strip()

    # Convertir todo a mayúsculas
    nombre = nombre.upper()

    # Eliminar tildes y caracteres especiales
    nombre = unidecode(nombre)

    # Eliminar guiones y otros caracteres no deseados (solo letras y espacios)
    nombre = re.sub(r'[^A-Z\s]', '', nombre)

    # Reemplazar más de un espacio entre las palabras por un solo espacio
    nombre = re.sub(r'\s+', ' ', nombre)

    # Comprobar que las palabras estén separadas solo por un espacio
    if '  ' in nombre:
        raise ValueError("Las palabras solo pueden estar separadas por un espacio.")

    return nombre