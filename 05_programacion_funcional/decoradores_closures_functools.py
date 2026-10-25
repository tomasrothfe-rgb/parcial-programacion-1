"""
EXTRA: CLOSURES, DECORADORES Y FUNCTOOLS
(Están en la planificación de la Unidad 3 aunque no aparecen en las diapositivas.)

CLOSURE:    función interna que "recuerda" variables de la función que la creó.
DECORADOR:  función que recibe una función y devuelve otra que la "envuelve"
            para agregarle comportamiento. Se aplica con @decorador.
functools:  partial (fija argumentos), reduce, lru_cache (memoriza resultados), wraps.
"""
import time
from functools import partial, lru_cache, wraps


# ---------------- CLOSURE ----------------
def crear_contador():
    cuenta = 0

    def incrementar():
        nonlocal cuenta          # para modificar la variable de afuera
        cuenta += 1
        return cuenta

    return incrementar


# ---------------- DECORADORES ----------------
def registrar(funcion):
    @wraps(funcion)              # conserva el nombre y la doc de la función original
    def envoltura(*args, **kwargs):
        print(f"-> Llamando a {funcion.__name__}{args}")
        resultado = funcion(*args, **kwargs)
        print(f"<- {funcion.__name__} devolvió {resultado}")
        return resultado
    return envoltura


def medir_tiempo(funcion):
    @wraps(funcion)
    def envoltura(*args, **kwargs):
        inicio = time.perf_counter()
        resultado = funcion(*args, **kwargs)
        print(f"{funcion.__name__} tardó {time.perf_counter() - inicio:.6f} s")
        return resultado
    return envoltura


def repetir(veces):              # decorador CON parámetros (3 niveles)
    def decorador(funcion):
        @wraps(funcion)
        def envoltura(*args, **kwargs):
            return [funcion(*args, **kwargs) for _ in range(veces)]
        return envoltura
    return decorador


def validar_positivos(funcion):
    @wraps(funcion)
    def envoltura(*args):
        if any(a < 0 for a in args):
            raise ValueError("Solo se aceptan números positivos")
        return funcion(*args)
    return envoltura


@registrar
def sumar(a, b):
    return a + b


@repetir(3)
def saludar(nombre):
    return f"Hola {nombre}"


@validar_positivos
def raiz(x):
    return x ** 0.5


# ---------------- FUNCTOOLS ----------------
def potencia(base, exponente):
    return base ** exponente


cuadrado = partial(potencia, exponente=2)   # partial: fija un argumento
cubo = partial(potencia, exponente=3)


@lru_cache(maxsize=None)                    # memoriza resultados ya calculados
def fibonacci(n):
    return n if n < 2 else fibonacci(n - 1) + fibonacci(n - 2)


@medir_tiempo
def fib_rapido(n):
    return fibonacci(n)


if __name__ == "__main__":
    contador = crear_contador()
    print("Closure:", contador(), contador(), contador())

    sumar(3, 4)
    print(saludar("Tomás"))
    print("Raíz:", raiz(16))
    try:
        raiz(-4)
    except ValueError as e:
        print("Error:", e)

    print("partial:", cuadrado(5), cubo(2))
    print("lru_cache fibonacci(80):", fib_rapido(80))
    print(fibonacci.cache_info())
