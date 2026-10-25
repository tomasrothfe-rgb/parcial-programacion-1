"""
HERENCIA Y POLIMORFISMO (Clase XVI, versión Python)

HERENCIA: una clase hija obtiene atributos y métodos de la clase padre.
          Relación "ES UN". Reutiliza código y permite especializar.
    Java: class Gato extends Animal      Python: class Gato(Animal)
    super(nombre)      -> super().__init__(nombre)   (llama al constructor del padre)
    super.metodo()     -> super().metodo()           (llama al método del padre para EXTENDERLO)
    @Override          -> en Python solo se redefine el método con el mismo nombre

    Java: herencia SIMPLE. Python: permite herencia MÚLTIPLE (class C(A, B)).

POLIMORFISMO ("muchas formas"): misma llamada, distinto comportamiento según el tipo real.
    - SOBRESCRITURA (overriding, en ejecución): mismo método y misma firma en la hija,
      con otra implementación.
    - SOBRECARGA (overloading, en compilación): mismo nombre y distinta firma.
      Python NO tiene sobrecarga real (la última definición pisa a la anterior).
      Se simula con parámetros por defecto, *args, o chequeando tipos.
"""


# =============================================================
# 1) HERENCIA en varios niveles: SerVivo -> Animal -> Gato / Perro
# =============================================================
class SerVivo:
    def respirar(self):
        return "Respira"


class Animal(SerVivo):
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad

    def moverse(self):
        return f"{self.nombre} se mueve"

    def hacer_sonido(self):
        return "..."

    def __str__(self):
        return f"{type(self).__name__} {self.nombre} ({self.edad} años)"


class Gato(Animal):
    def __init__(self, nombre, edad, color):
        super().__init__(nombre, edad)       # constructor del padre
        self.color = color                   # atributo propio

    def hacer_sonido(self):                  # SOBRESCRITURA (override)
        return "Miau"

    def moverse(self):                       # EXTIENDE el método del padre
        return super().moverse() + " sigilosamente"


class Perro(Animal):
    def hacer_sonido(self):
        return "Guau"

    def buscar_pelota(self):                 # método propio de Perro
        return f"{self.nombre} busca la pelota"


# =============================================================
# 2) POLIMORFISMO: misma llamada, comportamiento según el tipo real
# =============================================================
def presentar_animales(animales):
    for a in animales:
        print(f"{a} dice {a.hacer_sonido()} | {a.moverse()} | {a.respirar()}")
        if isinstance(a, Perro):            # "casting"/chequeo de tipo
            print("   ", a.buscar_pelota())


# =============================================================
# 3) "SOBRECARGA" en Python (simulada)
# =============================================================
class Calculadora:
    # a) Con parámetros por defecto
    def sumar(self, a, b, c=0):
        return a + b + c

    # b) Con *args (cantidad variable de argumentos)
    def sumar_todos(self, *numeros):
        return sum(numeros)

    # c) Según el tipo del argumento
    def area(self, *args):
        if len(args) == 1:                   # cuadrado
            return args[0] ** 2
        if len(args) == 2:                   # rectángulo
            return args[0] * args[1]
        raise TypeError("area() recibe 1 o 2 argumentos")


# =============================================================
# 4) SOBRECARGA DE OPERADORES (métodos mágicos)
# =============================================================
class Vector:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __add__(self, otro):        # v1 + v2
        return Vector(self.x + otro.x, self.y + otro.y)

    def __mul__(self, escalar):     # v * 3
        return Vector(self.x * escalar, self.y * escalar)

    def __eq__(self, otro):         # v1 == v2
        return self.x == otro.x and self.y == otro.y

    def __lt__(self, otro):         # v1 < v2 (compara módulo) -> permite sorted()
        return (self.x**2 + self.y**2) < (otro.x**2 + otro.y**2)

    def __str__(self):              # print(v)
        return f"Vector({self.x}, {self.y})"

    __repr__ = __str__              # para que se vea bien dentro de listas


# =============================================================
# 5) HERENCIA MÚLTIPLE (en Java se resuelve con interfaces)
# =============================================================
class Nadador:
    def nadar(self):
        return "Nada"


class Volador:
    def volar(self):
        return "Vuela"


class Pato(Animal, Nadador, Volador):
    def hacer_sonido(self):
        return "Cuac"


if __name__ == "__main__":
    animales = [Gato("Michi", 3, "negro"), Perro("Firulais", 5), Pato("Donald", 2)]
    presentar_animales(animales)

    pato = animales[2]
    print(pato.nadar(), "y", pato.volar())
    print("Orden de búsqueda de métodos (MRO):", [c.__name__ for c in Pato.__mro__])
    print("¿Gato es un Animal?", isinstance(animales[0], Animal))
    print("¿Gato hereda de SerVivo?", issubclass(Gato, SerVivo))

    calc = Calculadora()
    print(calc.sumar(1, 2), calc.sumar(1, 2, 3), calc.sumar_todos(1, 2, 3, 4))
    print("Área cuadrado:", calc.area(4), "| rectángulo:", calc.area(3, 5))

    v1, v2 = Vector(1, 2), Vector(3, 4)
    print(v1 + v2, v1 * 3, v1 == Vector(1, 2), sorted([v2, v1]))
