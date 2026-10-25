"""
ARCHIVOS BINARIOS CON PICKLE - Referencia rápida (Clase XIII)

Modos de apertura:
    "rb"  -> lectura binaria            (el archivo DEBE existir)
    "wb"  -> escritura binaria          (si no existe lo crea / si existe LO BORRA)
    "ab"  -> añadir al final            (si no existe lo crea / NO borra)
    "rb+" -> lectura y escritura        (el archivo DEBE existir)

pickle.dump(objeto, archivo) -> SERIALIZAR (guardar)   -> abrir con "wb" o "ab"
pickle.load(archivo)         -> DESERIALIZAR (leer)    -> abrir con "rb"
"""
import os
import pickle

ARCHIVO = "datos_ejemplo.pkl"


# ---------------------------------------------------------------
# 1) Guardar y leer UN objeto (lo más común: guardar una lista entera)
# ---------------------------------------------------------------
def guardar(datos, nombre_archivo=ARCHIVO):
    with open(nombre_archivo, "wb") as f:
        pickle.dump(datos, f)


def cargar(nombre_archivo=ARCHIVO):
    """Devuelve lo guardado o una lista vacía si el archivo no existe."""
    try:
        with open(nombre_archivo, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return []
    except (EOFError, pickle.UnpicklingError):
        print("El archivo está vacío o dañado.")
        return []


# ---------------------------------------------------------------
# 2) Guardar VARIOS objetos sueltos con "ab" y leerlos todos
#    (se leen en el MISMO ORDEN en que se guardaron)
# ---------------------------------------------------------------
def agregar_objeto(objeto, nombre_archivo):
    with open(nombre_archivo, "ab") as f:
        pickle.dump(objeto, f)


def leer_todos(nombre_archivo):
    objetos = []
    try:
        with open(nombre_archivo, "rb") as f:
            while True:
                try:
                    objetos.append(pickle.load(f))
                except EOFError:  # se terminó el archivo
                    break
    except FileNotFoundError:
        pass
    return objetos


if __name__ == "__main__":
    # Se puede guardar cualquier tipo de dato de Python
    datos = {
        "nombres": ["Ana", "Juan"],
        "edades": (20, 22),
        "activo": True,
    }
    guardar(datos)
    print("Leído (un objeto):", cargar())

    # Varios objetos con "ab"
    archivo_log = "log_ejemplo.pkl"
    if os.path.exists(archivo_log):
        os.remove(archivo_log)
    agregar_objeto({"evento": "inicio"}, archivo_log)
    agregar_objeto({"evento": "compra", "monto": 1500}, archivo_log)
    agregar_objeto({"evento": "fin"}, archivo_log)
    print("Leídos (varios objetos):", leer_todos(archivo_log))

    # Limpieza de los archivos de prueba
    os.remove(ARCHIVO)
    os.remove(archivo_log)

    # ⚠ SEGURIDAD: pickle.load() puede ejecutar código arbitrario.
    #   Nunca cargar .pkl de fuentes desconocidas.
    #   Para compartir con otros lenguajes o sistemas -> usar JSON, CSV o SQLite.
