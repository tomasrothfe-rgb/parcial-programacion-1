"""
EJERCICIO DE CLASE (Clase XIII) - Estudiantes en archivo binario

Consigna:
  - Clase Estudiante con nombre, edad e id.
  - Crear varias instancias y guardarlas en un archivo binario.
  - Buscar un estudiante por id ingresado por consola (controlar errores si no existe).
  - Buscar un estudiante por nombre ingresado por consola.
  - Menú para que el usuario elija cómo buscar.
  - Modificar el nombre de un estudiante, volver a guardar y verificar el cambio.
"""
import pickle

ARCHIVO = "estudiantes.pkl"


class Estudiante:
    def __init__(self, id, nombre, edad):
        self.id = id
        self.nombre = nombre
        self.edad = edad

    def __str__(self):
        return f"[{self.id}] {self.nombre} ({self.edad} años)"


class EstudianteNoEncontrado(Exception):
    """Excepción propia para cuando no existe el estudiante."""


# ----------------------- Persistencia -----------------------
def guardar_estudiantes(estudiantes):
    with open(ARCHIVO, "wb") as f:
        pickle.dump(estudiantes, f)


def cargar_estudiantes():
    try:
        with open(ARCHIVO, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return []


# ----------------------- Búsquedas -----------------------
def buscar_por_id(estudiantes, id):
    for e in estudiantes:
        if e.id == id:
            return e
    raise EstudianteNoEncontrado(f"No existe un estudiante con id {id}")


def buscar_por_nombre(estudiantes, nombre):
    encontrados = [e for e in estudiantes if e.nombre.lower() == nombre.lower()]
    if not encontrados:
        raise EstudianteNoEncontrado(f"No existe un estudiante llamado '{nombre}'")
    return encontrados


def modificar_nombre(id, nuevo_nombre):
    estudiantes = cargar_estudiantes()            # 1. leer
    est = buscar_por_id(estudiantes, id)          # 2. buscar
    est.nombre = nuevo_nombre                     # 3. modificar
    guardar_estudiantes(estudiantes)              # 4. volver a guardar
    verificado = buscar_por_id(cargar_estudiantes(), id)   # 5. verificar
    print("Cambio guardado:", verificado)


# ----------------------- Menú -----------------------
def pedir_entero(mensaje):
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Ingresá un número válido.")


def menu():
    while True:
        print("\n--- MENÚ ---")
        print("1. Buscar por id")
        print("2. Buscar por nombre")
        print("3. Modificar nombre")
        print("4. Listar todos")
        print("0. Salir")
        opcion = input("Opción: ").strip()
        estudiantes = cargar_estudiantes()
        try:
            if opcion == "1":
                print(buscar_por_id(estudiantes, pedir_entero("Id: ")))
            elif opcion == "2":
                for e in buscar_por_nombre(estudiantes, input("Nombre: ")):
                    print(e)
            elif opcion == "3":
                modificar_nombre(pedir_entero("Id: "), input("Nuevo nombre: "))
            elif opcion == "4":
                for e in estudiantes:
                    print(e)
            elif opcion == "0":
                print("Chau!")
                break
            else:
                print("Opción inválida.")
        except EstudianteNoEncontrado as err:
            print("Error:", err)


if __name__ == "__main__":
    # Datos iniciales
    guardar_estudiantes([
        Estudiante(1, "Ana", 20),
        Estudiante(2, "Juan", 22),
        Estudiante(3, "Lucía", 19),
    ])
    menu()
