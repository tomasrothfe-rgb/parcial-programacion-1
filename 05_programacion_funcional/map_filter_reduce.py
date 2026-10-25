"""
MAP, FILTER, REDUCE, LAMBDA Y COMPRENSIONES (Clases XVIII-XIX)

lambda parametros: expresion        -> función anónima de una línea
map(funcion, iterable)              -> TRANSFORMA cada elemento
filter(funcion, iterable)           -> SE QUEDA con los que devuelven True
reduce(funcion, iterable, inicial)  -> REDUCE todo a un valor  (from functools import reduce)

map y filter devuelven iteradores perezosos -> usar list() para verlos.
Comprensión de listas: [expresion for x in lista if condicion]  (equivale a map + filter)
"""
from functools import reduce

numeros = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
palabras = ["python", "java", "c", "javascript", "go"]
productos = [
    {"nombre": "Remera", "precio": 8000, "stock": 10, "categoria": "ropa"},
    {"nombre": "Zapatilla", "precio": 45000, "stock": 0, "categoria": "calzado"},
    {"nombre": "Pantalón", "precio": 20000, "stock": 5, "categoria": "ropa"},
    {"nombre": "Ojotas", "precio": 6000, "stock": 15, "categoria": "calzado"},
]

# ---------------- MAP ----------------
cuadrados = list(map(lambda x: x ** 2, numeros))
mayusculas = list(map(str.upper, palabras))
largos = list(map(len, palabras))
sumas = list(map(lambda a, b: a + b, [1, 2, 3], [10, 20, 30]))  # varias listas
con_iva = list(map(lambda p: {**p, "precio": p["precio"] * 1.21}, productos))  # dict nuevo

# ---------------- FILTER ----------------
pares = list(filter(lambda x: x % 2 == 0, numeros))
largas = list(filter(lambda p: len(p) > 4, palabras))
con_stock = list(filter(lambda p: p["stock"] > 0, productos))

# ---------------- REDUCE ----------------
suma = reduce(lambda acc, x: acc + x, numeros)              # 55
producto = reduce(lambda acc, x: acc * x, [1, 2, 3, 4, 5])   # 120
maximo = reduce(lambda a, b: a if a > b else b, numeros)     # 10
valor_inventario = reduce(lambda acc, p: acc + p["precio"] * p["stock"], productos, 0)
por_categoria = reduce(
    lambda acc, p: {**acc, p["categoria"]: acc.get(p["categoria"], 0) + 1},
    productos, {},
)

# ---------------- ENCADENADO: filter -> map -> reduce ----------------
# Suma de los cuadrados de los números pares
resultado = reduce(lambda a, b: a + b, map(lambda x: x ** 2, filter(lambda x: x % 2 == 0, numeros)))

# ---------------- COMPRENSIONES (equivalentes) ----------------
cuadrados_pares = [x ** 2 for x in numeros if x % 2 == 0]
nombres_ropa = [p["nombre"] for p in productos if p["categoria"] == "ropa"]
dict_precios = {p["nombre"]: p["precio"] for p in productos}   # comprensión de diccionario
categorias = {p["categoria"] for p in productos}                # comprensión de conjunto

# ---------------- OTRAS FUNCIONES ÚTILES ----------------
ordenados = sorted(productos, key=lambda p: p["precio"])               # ordenar por clave
mas_caro = max(productos, key=lambda p: p["precio"])
hay_sin_stock = any(p["stock"] == 0 for p in productos)
todos_positivos = all(p["precio"] > 0 for p in productos)
total_stock = sum(p["stock"] for p in productos)


if __name__ == "__main__":
    print("map cuadrados:", cuadrados)
    print("map mayúsculas:", mayusculas, "| largos:", largos, "| sumas:", sumas)
    print("map con IVA:", [round(p["precio"]) for p in con_iva])
    print("filter pares:", pares, "| largas:", largas)
    print("filter con stock:", [p["nombre"] for p in con_stock])
    print("reduce suma:", suma, "| producto:", producto, "| máximo:", maximo)
    print("reduce valor inventario:", valor_inventario)
    print("reduce por categoría:", por_categoria)
    print("encadenado (suma cuadrados pares):", resultado)
    print("comprensión:", cuadrados_pares, nombres_ropa)
    print("dict:", dict_precios, "| set:", categorias)
    print("sorted:", [p["nombre"] for p in ordenados], "| max:", mas_caro["nombre"])
    print("any:", hay_sin_stock, "| all:", todos_positivos, "| sum:", total_stock)
