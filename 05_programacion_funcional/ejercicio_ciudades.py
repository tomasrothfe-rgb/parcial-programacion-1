"""
EJERCICIO DE CLASE (Clase XIX) - Ciudades

Dada una clase Ciudad con 2 atributos: nombre y población.
  1. Declarar diferentes ciudades como ejemplo.
  2. Aplicando programación funcional:
     a. Quedarnos con las ciudades cuya población es mayor a 1000.
     b. Escalar la población de cada ciudad filtrada multiplicándola por 100.
     c. Imprimir las ciudades filtradas con su población escalada.
"""
from functools import reduce


class Ciudad:
    def __init__(self, nombre, poblacion):
        self.nombre = nombre
        self.poblacion = poblacion

    def __str__(self):
        return f"{self.nombre}: {self.poblacion:,} habitantes"


# 1. Ciudades de ejemplo
ciudades = [
    Ciudad("Esperanza", 5000),
    Ciudad("Pujato Norte", 800),
    Ciudad("Humboldt", 1500),
    Ciudad("Cavour", 600),
    Ciudad("Rafaela", 3000),
]

# ---------------------------------------------------------------
# VERSIÓN 1: filter + map (paso a paso)
# ---------------------------------------------------------------
# a. filter: población > 1000
filtradas = filter(lambda c: c.poblacion > 1000, ciudades)

# b. map: escalar ×100 creando OBJETOS NUEVOS (inmutabilidad: no tocamos los originales)
escaladas = list(map(lambda c: Ciudad(c.nombre, c.poblacion * 100), filtradas))


# ---------------------------------------------------------------
# VERSIÓN 2: con funciones puras con nombre (más legible) + composición
# ---------------------------------------------------------------
def es_grande(ciudad, minimo=1000):
    return ciudad.poblacion > minimo


def escalar(ciudad, factor=100):
    return Ciudad(ciudad.nombre, ciudad.poblacion * factor)


def procesar(lista):
    return list(map(escalar, filter(es_grande, lista)))


# ---------------------------------------------------------------
# VERSIÓN 3: comprensión de listas (una línea)
# ---------------------------------------------------------------
escaladas_v3 = [Ciudad(c.nombre, c.poblacion * 100) for c in ciudades if c.poblacion > 1000]


if __name__ == "__main__":
    # c. Imprimir
    print("Versión 1 (filter + map):")
    list(map(print, escaladas))          # imprimir de forma "funcional"

    print("\nVersión 2 (funciones con nombre):")
    for c in procesar(ciudades):
        print(c)

    print("\nVersión 3 (comprensión):")
    for c in escaladas_v3:
        print(c)

    # Extras típicos con reduce
    total = reduce(lambda acc, c: acc + c.poblacion, escaladas, 0)
    mayor = reduce(lambda a, b: a if a.poblacion > b.poblacion else b, escaladas)
    print(f"\nPoblación total escalada: {total:,}")
    print("Ciudad más poblada:", mayor)
    print("Originales sin modificar:", [c.poblacion for c in ciudades])
