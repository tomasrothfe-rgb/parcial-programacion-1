"""
PROGRAMACIÓN FUNCIONAL: PRINCIPIOS (Clase XVIII)

Paradigma DECLARATIVO: "qué hacer", no "cómo hacerlo". Evita mutar estado.
  1. Funciones puras        -> sin efectos secundarios; mismo input = mismo output
  2. Inmutabilidad          -> no modificar datos: crear nuevos
  3. Funciones de 1ª clase  -> guardarlas en variables, pasarlas y devolverlas
  4. Composición            -> f(g(x))
  5. Evaluación perezosa    -> se calcula solo cuando se necesita (generadores, map, filter)
"""
from functools import reduce


# 1) FUNCIONES PURAS vs IMPURAS ------------------------------------
def sumar(a, b):              # PURA
    return a + b


total = 0
def acumular(x):              # IMPURA: modifica una variable externa
    global total
    total += x
    return total


def agregar_impuro(lista, x): # IMPURA: modifica la lista recibida
    lista.append(x)
    return lista


def agregar_puro(lista, x):   # PURA: devuelve una lista NUEVA
    return lista + [x]


# 2) INMUTABILIDAD ---------------------------------------------------
punto = (3, 4)                       # tupla: inmutable
config = frozenset({"a", "b"})       # conjunto inmutable

def mover(p, dx, dy):                # no modifica p, crea uno nuevo
    return (p[0] + dx, p[1] + dy)


# 3) FUNCIONES DE PRIMERA CLASE --------------------------------------
def aplicar(funcion, valor):         # recibe una función
    return funcion(valor)


def multiplicador(n):                # devuelve una función (closure)
    def multiplicar(x):
        return x * n                 # "recuerda" n
    return multiplicar


operaciones = {                      # funciones guardadas en un diccionario
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
}


# 4) COMPOSICIÓN -----------------------------------------------------
def componer(*funciones):
    """componer(f, g, h)(x) == f(g(h(x)))"""
    return reduce(lambda f, g: lambda x: f(g(x)), funciones)


# 5) EVALUACIÓN PEREZOSA ---------------------------------------------
def numeros_pares():                 # generador infinito: se calcula de a uno
    n = 0
    while True:
        yield n
        n += 2


if __name__ == "__main__":
    print("Pura:", sumar(2, 3), sumar(2, 3))         # siempre 5
    print("Impura:", acumular(5), acumular(5))       # 5 y luego 10

    original = [1, 2]
    nueva = agregar_puro(original, 3)
    print("Inmutable -> original:", original, "| nueva:", nueva)
    print("Mover punto:", punto, "->", mover(punto, 1, 1))

    print("Aplicar:", aplicar(lambda x: x ** 2, 4))
    doble, triple = multiplicador(2), multiplicador(3)
    print("Closure:", doble(7), triple(7))
    print("Dict de funciones:", operaciones["*"](6, 7))

    sumar1 = lambda x: x + 1
    por2 = lambda x: x * 2
    print("Composición sumar1(por2(5)):", componer(sumar1, por2)(5))

    gen = numeros_pares()
    print("Perezosa (5 pares):", [next(gen) for _ in range(5)])

    # Imperativo vs declarativo
    nums = [1, 2, 3, 4, 5, 6]
    pares_imp = []
    for n in nums:
        if n % 2 == 0:
            pares_imp.append(n)
    pares_dec = list(filter(lambda n: n % 2 == 0, nums))
    print("Imperativo:", pares_imp, "| Declarativo:", pares_dec)
