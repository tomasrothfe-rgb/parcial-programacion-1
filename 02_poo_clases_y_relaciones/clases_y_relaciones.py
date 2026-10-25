"""
POO: CLASES, OBJETOS Y RELACIONES ENTRE CLASES (Clase XV, versión Python)

Clase  -> molde/definición. Objeto -> instancia concreta en memoria.
Cada objeto tiene: ESTADO (atributos), COMPORTAMIENTO (métodos), IDENTIDAD (id()).

Equivalencias Java -> Python:
    constructor Persona(...)   -> __init__(self, ...)
    this                       -> self
    private nombre             -> self.__nombre  (o _nombre por convención)
    getNombre()/setNombre()    -> @property / @nombre.setter
    static                     -> @staticmethod / @classmethod / atributo de clase

RELACIONES:
    ASOCIACIÓN  -> una clase USA a otra; ninguna depende de la otra para existir.
    AGREGACIÓN  -> una clase CONTIENE a otra, pero la parte PUEDE EXISTIR SOLA
                   (la parte se crea AFUERA y se pasa).
    COMPOSICIÓN -> una clase POSEE a otra; si el todo desaparece, las partes también
                   (la parte se crea ADENTRO). Más fuerte que la agregación.
"""


# =============================================================
# 1) CLASE con encapsulamiento, properties, atributo de clase y métodos estáticos
# =============================================================
class Persona:
    cantidad = 0  # atributo de CLASE (compartido por todos los objetos)

    def __init__(self, nombre, edad):
        self.__nombre = nombre     # "privado" (name mangling)
        self.edad = edad           # pasa por el setter -> valida
        Persona.cantidad += 1

    # Getter
    @property
    def nombre(self):
        return self.__nombre

    # Getter + setter con validación
    @property
    def edad(self):
        return self.__edad

    @edad.setter
    def edad(self, valor):
        if valor < 0:
            raise ValueError("La edad no puede ser negativa")
        self.__edad = valor

    def es_mayor(self):
        return self.edad >= 18

    @staticmethod
    def validar_dni(dni):          # no usa self ni la clase
        return str(dni).isdigit() and len(str(dni)) in (7, 8)

    @classmethod
    def desde_texto(cls, texto):   # constructor alternativo: "Ana,20"
        nombre, edad = texto.split(",")
        return cls(nombre, int(edad))

    def __str__(self):             # para print()
        return f"{self.nombre} ({self.edad})"


# =============================================================
# 2) ASOCIACIÓN: Profesor usa Alumno, ninguno depende del otro
# =============================================================
class Alumno:
    def __init__(self, nombre):
        self.nombre = nombre


class Profesor:
    def __init__(self, nombre):
        self.nombre = nombre

    def corregir(self, alumno, nota):     # recibe al alumno solo para usarlo
        return f"{self.nombre} corrigió a {alumno.nombre}: {nota}"


# =============================================================
# 3) AGREGACIÓN: Equipo contiene Jugadores que existen por su cuenta
# =============================================================
class Jugador:
    def __init__(self, nombre):
        self.nombre = nombre


class Equipo:
    def __init__(self, nombre):
        self.nombre = nombre
        self.jugadores = []

    def agregar(self, jugador):           # el jugador viene de AFUERA
        self.jugadores.append(jugador)

    def quitar(self, jugador):
        self.jugadores.remove(jugador)


# =============================================================
# 4) COMPOSICIÓN: Factura posee sus Líneas (no existen sin ella)
# =============================================================
class LineaFactura:
    def __init__(self, producto, cantidad, precio):
        self.producto = producto
        self.cantidad = cantidad
        self.precio = precio

    def subtotal(self):
        return self.cantidad * self.precio


class Factura:
    def __init__(self, numero):
        self.numero = numero
        self.__lineas = []

    def agregar_linea(self, producto, cantidad, precio):
        # La línea se crea ADENTRO: nadie de afuera tiene referencia
        self.__lineas.append(LineaFactura(producto, cantidad, precio))

    def total(self):
        return sum(l.subtotal() for l in self.__lineas)


if __name__ == "__main__":
    p1 = Persona("Ana", 20)
    p2 = Persona.desde_texto("Juan,15")
    print(p1, "| mayor:", p1.es_mayor())
    print(p2, "| mayor:", p2.es_mayor())
    print("Personas creadas:", Persona.cantidad)
    print("DNI válido:", Persona.validar_dni(40123456))
    try:
        p1.edad = -5
    except ValueError as e:
        print("Error:", e)

    print(Profesor("Yackel").corregir(Alumno("Tomás"), 9))

    messi = Jugador("Messi")
    equipo = Equipo("Argentina")
    equipo.agregar(messi)
    del equipo
    print("Agregación: el jugador sigue existiendo ->", messi.nombre)

    f = Factura(1)
    f.agregar_linea("Remera", 2, 5000)
    f.agregar_linea("Pantalón", 1, 12000)
    print("Composición: total factura =", f.total())
