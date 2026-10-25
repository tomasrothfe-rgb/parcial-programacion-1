"""
CLASES ABSTRACTAS E INTERFACES (Clase XVII, versión Python)

Python no tiene la palabra "interface". Se usa el módulo abc:
    from abc import ABC, abstractmethod

CLASE ABSTRACTA: no se puede instanciar. Mezcla métodos abstractos (sin cuerpo)
                 y concretos (con cuerpo). Puede tener atributos y constructor.
INTERFAZ:        "contrato". Se simula con una clase ABC que tiene SOLO métodos
                 abstractos y sin atributos. Una clase puede "implementar" varias.

| Interfaz                           | Clase abstracta                         |
|------------------------------------|-----------------------------------------|
| Solo métodos abstractos            | Abstractos + concretos                  |
| Sin estado (sin atributos)         | Puede tener atributos                   |
| Sin constructor                    | Puede tener constructor (super())       |
| Se pueden implementar VARIAS       | En Java se extiende SOLO UNA            |
| Contratos, desacoplar, varias      | Compartir código y estado entre hijas   |
|   fuentes de comportamiento        |                                         |

REGLA: si una hija no implementa TODOS los métodos abstractos, no se puede instanciar
       (TypeError).
"""
from abc import ABC, abstractmethod
import math


# =============================================================
# 1) CLASE ABSTRACTA con estado, constructor y métodos concretos
# =============================================================
class Figura(ABC):
    def __init__(self, nombre):
        self.nombre = nombre                 # estado compartido

    @abstractmethod
    def area(self):                          # abstracto: lo define cada hija
        pass

    @abstractmethod
    def perimetro(self):
        pass

    def describir(self):                     # concreto: se hereda tal cual
        return f"{self.nombre}: área={self.area():.2f}, perímetro={self.perimetro():.2f}"


class Circulo(Figura):
    def __init__(self, radio):
        super().__init__("Círculo")
        self.radio = radio

    def area(self):
        return math.pi * self.radio ** 2

    def perimetro(self):
        return 2 * math.pi * self.radio


class Rectangulo(Figura):
    def __init__(self, base, altura):
        super().__init__("Rectángulo")
        self.base, self.altura = base, altura

    def area(self):
        return self.base * self.altura

    def perimetro(self):
        return 2 * (self.base + self.altura)


# =============================================================
# 2) "INTERFACES": solo métodos abstractos, sin estado
# =============================================================
class Pagable(ABC):
    @abstractmethod
    def calcular_pago(self):
        pass


class Imprimible(ABC):
    @abstractmethod
    def imprimir(self):
        pass


# Clase abstracta + varias interfaces (como extends + implements en Java)
class Empleado(ABC):
    def __init__(self, nombre, sueldo_base):
        self.nombre = nombre
        self.sueldo_base = sueldo_base

    @abstractmethod
    def bono(self):
        pass


class EmpleadoTiempoCompleto(Empleado, Pagable, Imprimible):
    def bono(self):
        return self.sueldo_base * 0.10

    def calcular_pago(self):
        return self.sueldo_base + self.bono()

    def imprimir(self):
        return f"[TC] {self.nombre}: ${self.calcular_pago():,.0f}"


class Freelancer(Pagable, Imprimible):      # no es Empleado, pero cumple los contratos
    def __init__(self, nombre, horas, valor_hora):
        self.nombre, self.horas, self.valor_hora = nombre, horas, valor_hora

    def calcular_pago(self):
        return self.horas * self.valor_hora

    def imprimir(self):
        return f"[FL] {self.nombre}: ${self.calcular_pago():,.0f}"


# =============================================================
# 3) INVERSIÓN DE DEPENDENCIAS: depender de la abstracción, no de la clase concreta
# =============================================================
class Notificador(ABC):
    @abstractmethod
    def enviar(self, mensaje):
        pass


class NotificadorEmail(Notificador):
    def enviar(self, mensaje):
        return f"Email: {mensaje}"


class NotificadorSMS(Notificador):
    def enviar(self, mensaje):
        return f"SMS: {mensaje}"


class SistemaPedidos:
    def __init__(self, notificador: Notificador):   # recibe CUALQUIER Notificador
        self.notificador = notificador

    def confirmar(self, pedido):
        return self.notificador.enviar(f"Pedido {pedido} confirmado")


if __name__ == "__main__":
    for fig in [Circulo(2), Rectangulo(3, 4)]:
        print(fig.describir())

    try:
        Figura("x")                          # no se puede instanciar
    except TypeError as e:
        print("Error esperado:", e)

    # Polimorfismo a través de la "interfaz": no importa la clase, solo el contrato
    pagables = [EmpleadoTiempoCompleto("Ana", 500000), Freelancer("Juan", 40, 8000)]
    for p in pagables:
        print(p.imprimir())
    print("Total a pagar:", sum(p.calcular_pago() for p in pagables))

    print(SistemaPedidos(NotificadorEmail()).confirmar(101))
    print(SistemaPedidos(NotificadorSMS()).confirmar(102))
