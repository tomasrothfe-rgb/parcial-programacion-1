"""
EJERCICIO INTEGRADOR - Sistema de Biblioteca
Combina TODOS los temas en un solo programa (modelo de consigna tipo parcial):

  [ABSTRACTA]   Material (no se instancia) con métodos abstractos y concretos
  [INTERFAZ]    Prestable: contrato con prestar() / devolver()
  [HERENCIA]    Libro, Revista y Dvd heredan de Material; super().__init__()
  [POLIMORF.]   dias_prestamo() y __str__ distintos en cada clase
  [SOBRECARGA]  __eq__ y __lt__ (operadores), parámetros por defecto
  [AGREGACIÓN]  Biblioteca contiene Socios (existen por su cuenta)
  [COMPOSICIÓN] Biblioteca crea y posee sus Prestamos
  [EXCEPCIONES] Excepciones propias + try/except
  [PICKLE]      Guardar y cargar todo el estado en un archivo binario
  [FUNCIONAL]   Reportes con map / filter / reduce / sorted / lambda
  [EVENTOS]     GestorEventos: se emiten "prestamo", "devolucion", "atraso"
  [MENÚ]        Interfaz de consola

Para usar como base: cambiar Biblioteca/Material por el dominio que pidan
(tienda, clínica, estacionamiento, cine...).
"""
import os
import pickle
from abc import ABC, abstractmethod
from datetime import date, timedelta
from functools import reduce

ARCHIVO = "biblioteca.pkl"


# =====================================================================
# EXCEPCIONES PROPIAS
# =====================================================================
class BibliotecaError(Exception):
    pass


class NoEncontradoError(BibliotecaError):
    pass


class NoDisponibleError(BibliotecaError):
    pass


# =====================================================================
# EVENTOS
# =====================================================================
class GestorEventos:
    def __init__(self):
        self._manejadores = {}

    def suscribir(self, evento, funcion):
        self._manejadores.setdefault(evento, []).append(funcion)

    def emitir(self, evento, *datos):
        for f in self._manejadores.get(evento, []):
            f(*datos)

    # Las funciones (lambdas) no se pueden guardar con pickle -> se excluyen
    def __getstate__(self):
        return {"_manejadores": {}}


# =====================================================================
# INTERFAZ + CLASE ABSTRACTA
# =====================================================================
class Prestable(ABC):
    """'Interfaz': solo métodos abstractos, sin estado."""

    @abstractmethod
    def prestar(self):
        pass

    @abstractmethod
    def devolver(self):
        pass


class Material(Prestable, ABC):
    """Clase abstracta: tiene estado y métodos concretos, pero no se instancia."""
    _ultimo_codigo = 0

    def __init__(self, titulo, anio):
        Material._ultimo_codigo += 1
        self.codigo = Material._ultimo_codigo
        self.titulo = titulo
        self.anio = anio
        self._disponible = True

    @property
    def disponible(self):
        return self._disponible

    @abstractmethod
    def dias_prestamo(self):          # cada hija define el suyo (polimorfismo)
        pass

    def prestar(self):
        if not self._disponible:
            raise NoDisponibleError(f"'{self.titulo}' ya está prestado")
        self._disponible = False

    def devolver(self):
        self._disponible = True

    def __eq__(self, otro):           # sobrecarga de ==
        return isinstance(otro, Material) and self.codigo == otro.codigo

    def __lt__(self, otro):           # sobrecarga de < (permite sorted())
        return self.titulo.lower() < otro.titulo.lower()

    def __str__(self):
        estado = "Disponible" if self._disponible else "Prestado"
        return f"[{self.codigo}] {type(self).__name__}: {self.titulo} ({self.anio}) - {estado}"


# =====================================================================
# HERENCIA
# =====================================================================
class Libro(Material):
    def __init__(self, titulo, anio, autor, paginas):
        super().__init__(titulo, anio)
        self.autor = autor
        self.paginas = paginas

    def dias_prestamo(self):
        return 14

    def __str__(self):
        return super().__str__() + f" | {self.autor}, {self.paginas} págs."


class Revista(Material):
    def __init__(self, titulo, anio, numero):
        super().__init__(titulo, anio)
        self.numero = numero

    def dias_prestamo(self):
        return 7

    def __str__(self):
        return super().__str__() + f" | N° {self.numero}"


class Dvd(Material):
    def __init__(self, titulo, anio, duracion_min):
        super().__init__(titulo, anio)
        self.duracion_min = duracion_min

    def dias_prestamo(self):
        return 3

    def __str__(self):
        return super().__str__() + f" | {self.duracion_min} min"


# =====================================================================
# AGREGACIÓN (Socio) y COMPOSICIÓN (Prestamo)
# =====================================================================
class Socio:
    def __init__(self, dni, nombre, max_prestamos=3):    # parámetro por defecto
        self.dni = dni
        self.nombre = nombre
        self.max_prestamos = max_prestamos

    def __str__(self):
        return f"{self.nombre} (DNI {self.dni})"


class Prestamo:
    def __init__(self, socio, material, fecha=None):
        self.socio = socio
        self.material = material
        self.fecha = fecha or date.today()
        self.vencimiento = self.fecha + timedelta(days=material.dias_prestamo())
        self.devuelto = False

    def dias_atraso(self, hoy=None):
        hoy = hoy or date.today()
        return max(0, (hoy - self.vencimiento).days)

    def __str__(self):
        return f"{self.material.titulo} -> {self.socio.nombre} (vence {self.vencimiento})"


class Biblioteca:
    MULTA_POR_DIA = 500

    def __init__(self, nombre):
        self.nombre = nombre
        self.materiales = []
        self.socios = []            # AGREGACIÓN: los socios se crean afuera
        self.prestamos = []         # COMPOSICIÓN: los préstamos se crean adentro
        self.eventos = GestorEventos()

    # ----------------- altas y búsquedas -----------------
    def agregar_material(self, material):
        self.materiales.append(material)

    def agregar_socio(self, socio):
        if any(s.dni == socio.dni for s in self.socios):
            raise BibliotecaError("Ya existe un socio con ese DNI")
        self.socios.append(socio)

    def buscar_material(self, codigo):
        for m in self.materiales:
            if m.codigo == codigo:
                return m
        raise NoEncontradoError(f"No existe material con código {codigo}")

    def buscar_socio(self, dni):
        socio = next((s for s in self.socios if s.dni == dni), None)
        if socio is None:
            raise NoEncontradoError(f"No existe socio con DNI {dni}")
        return socio

    def buscar_por_titulo(self, texto):
        return list(filter(lambda m: texto.lower() in m.titulo.lower(), self.materiales))

    # ----------------- préstamos -----------------
    def prestamos_activos(self, socio=None):
        activos = [p for p in self.prestamos if not p.devuelto]
        return [p for p in activos if p.socio is socio] if socio else activos

    def prestar(self, dni, codigo, fecha=None):
        socio = self.buscar_socio(dni)
        material = self.buscar_material(codigo)
        if len(self.prestamos_activos(socio)) >= socio.max_prestamos:
            raise NoDisponibleError(f"{socio.nombre} alcanzó el máximo de préstamos")
        material.prestar()                                # puede lanzar NoDisponibleError
        prestamo = Prestamo(socio, material, fecha)       # se crea ADENTRO
        self.prestamos.append(prestamo)
        self.eventos.emitir("prestamo", prestamo)
        return prestamo

    def devolver(self, codigo, hoy=None):
        prestamo = next((p for p in self.prestamos_activos() if p.material.codigo == codigo), None)
        if prestamo is None:
            raise NoEncontradoError("Ese material no está prestado")
        prestamo.devuelto = True
        prestamo.material.devolver()
        atraso = prestamo.dias_atraso(hoy)
        multa = atraso * self.MULTA_POR_DIA
        if atraso:
            self.eventos.emitir("atraso", prestamo, atraso, multa)
        self.eventos.emitir("devolucion", prestamo)
        return multa

    # ----------------- reportes (programación funcional) -----------------
    def disponibles(self):
        return sorted(filter(lambda m: m.disponible, self.materiales))

    def titulos_en_mayuscula(self):
        return list(map(lambda m: m.titulo.upper(), self.materiales))

    def cantidad_por_tipo(self):
        return reduce(
            lambda acc, m: {**acc, type(m).__name__: acc.get(type(m).__name__, 0) + 1},
            self.materiales, {},
        )

    def total_paginas(self):
        libros = filter(lambda m: isinstance(m, Libro), self.materiales)
        return reduce(lambda acc, l: acc + l.paginas, libros, 0)

    def vencidos(self, hoy=None):
        return [p for p in self.prestamos_activos() if p.dias_atraso(hoy) > 0]

    # ----------------- persistencia (pickle) -----------------
    def guardar(self, archivo=ARCHIVO):
        with open(archivo, "wb") as f:
            pickle.dump(self, f)

    @staticmethod
    def cargar(archivo=ARCHIVO):
        with open(archivo, "rb") as f:
            biblio = pickle.load(f)
        # restaurar el contador de códigos para no repetir
        Material._ultimo_codigo = max((m.codigo for m in biblio.materiales), default=0)
        return biblio


# =====================================================================
# CONFIGURACIÓN Y MENÚ
# =====================================================================
def conectar_eventos(biblio):
    biblio.eventos.suscribir("prestamo", lambda p: print(f"  📗 Préstamo registrado: {p}"))
    biblio.eventos.suscribir("devolucion", lambda p: print(f"  📘 Devuelto: {p.material.titulo}"))
    biblio.eventos.suscribir(
        "atraso", lambda p, d, m: print(f"  ⚠ {p.socio.nombre} devolvió con {d} días de atraso. Multa: ${m}")
    )


def datos_iniciales():
    b = Biblioteca("Biblioteca ITEC")
    for m in [
        Libro("Python para todos", 2020, "Muñoz Guerrero", 350),
        Libro("Clean Code", 2008, "Robert C. Martin", 464),
        Revista("Muy Interesante", 2025, 412),
        Dvd("Matrix", 1999, 136),
    ]:
        b.agregar_material(m)
    b.agregar_socio(Socio(40111222, "Tomás"))
    b.agregar_socio(Socio(39888777, "Bruno", max_prestamos=1))
    return b


def pedir_entero(mensaje):
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("  Ingresá un número válido.")


def menu():
    if os.path.exists(ARCHIVO):
        biblio = Biblioteca.cargar()
        print("Datos cargados desde", ARCHIVO)
    else:
        biblio = datos_iniciales()
    conectar_eventos(biblio)

    opciones = {
        "1": "Listar materiales", "2": "Listar disponibles", "3": "Buscar por título",
        "4": "Agregar libro", "5": "Agregar socio", "6": "Prestar", "7": "Devolver",
        "8": "Reportes", "9": "Guardar", "0": "Guardar y salir",
    }
    while True:
        print(f"\n===== {biblio.nombre} =====")
        for k, v in opciones.items():
            print(f"{k}. {v}")
        op = input("Opción: ").strip()
        try:
            if op == "1":
                for m in biblio.materiales:
                    print(" ", m)
            elif op == "2":
                for m in biblio.disponibles():
                    print(" ", m)
            elif op == "3":
                resultados = biblio.buscar_por_titulo(input("Texto: "))
                print(*(f"  {m}" for m in resultados), sep="\n") if resultados else print("  Sin resultados")
            elif op == "4":
                libro = Libro(input("Título: "), pedir_entero("Año: "), input("Autor: "), pedir_entero("Páginas: "))
                biblio.agregar_material(libro)
                print("  Agregado:", libro)
            elif op == "5":
                biblio.agregar_socio(Socio(pedir_entero("DNI: "), input("Nombre: ")))
                print("  Socio agregado")
            elif op == "6":
                biblio.prestar(pedir_entero("DNI del socio: "), pedir_entero("Código del material: "))
            elif op == "7":
                biblio.devolver(pedir_entero("Código del material: "))
            elif op == "8":
                print("  Por tipo:", biblio.cantidad_por_tipo())
                print("  Total páginas:", biblio.total_paginas())
                print("  Títulos:", biblio.titulos_en_mayuscula())
                print("  Préstamos activos:", len(biblio.prestamos_activos()))
            elif op == "9":
                biblio.guardar()
                print("  Guardado")
            elif op == "0":
                biblio.guardar()
                print("  Guardado. ¡Chau!")
                break
            else:
                print("  Opción inválida")
        except BibliotecaError as e:          # captura todas las excepciones propias
            print("  Error:", e)


if __name__ == "__main__":
    menu()
