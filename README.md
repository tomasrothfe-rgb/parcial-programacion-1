# Programación I: ejercicios de referencia para el 2º TP Individual

Material de consulta en **Python** para el parcial de carpeta abierta (ITEC "El Molino", 2026).
Cubre los temas de las **Clases XIII a XX**. Los temas que en clase se vieron en Java están pasados a Python.

## Cómo usarlo

1. Abrí la carpeta en VS Code (`Archivo → Abrir carpeta…`) o hacé doble clic en `parcial.code-workspace`.
2. Instalá la extensión **Python** de Microsoft si no la tenés.
3. Abrí cualquier archivo y apretá **F5** (o el ▶ arriba a la derecha) para ejecutarlo.
   Se ejecuta en la carpeta del archivo, así que los `.pkl` se crean ahí mismo.

No necesita instalar nada: todo usa la librería estándar de Python 3.

## Índice

| Carpeta | Archivo | Qué tiene |
|---|---|---|
| `01_archivos_binarios` | `ejemplo_pickle.py` | Modos `rb`/`wb`/`ab`/`rb+`, `dump`/`load`, leer varios objetos con `EOFError` |
| | `ejercicio_estudiantes.py` | **Ejercicio de clase:** guardar estudiantes, buscar por id o nombre, modificar y verificar, con menú |
| `02_poo_clases_y_relaciones` | `clases_y_relaciones.py` | Constructor, encapsulamiento, `@property`, `@staticmethod`, `@classmethod`, **asociación, agregación y composición** |
| `03_herencia_y_polimorfismo` | `herencia_y_polimorfismo.py` | Herencia en varios niveles, `super()`, sobrescritura, "sobrecarga" en Python, **sobrecarga de operadores**, herencia múltiple |
| `04_abstractas_e_interfaces` | `abstractas_e_interfaces.py` | `ABC` y `@abstractmethod`, interfaces simuladas, implementar varias, **inversión de dependencias** |
| `05_programacion_funcional` | `principios_funcionales.py` | Funciones puras e impuras, inmutabilidad, primera clase, composición, evaluación perezosa |
| | `map_filter_reduce.py` | `map`, `filter`, `reduce`, `lambda`, comprensiones, `sorted`/`max`/`any`/`all` |
| | `ejercicio_ciudades.py` | **Ejercicio de clase (XIX):** ciudades con población > 1000, escaladas ×100 (3 versiones) |
| | `decoradores_closures_functools.py` | Extra de la planificación: closures, decoradores, `partial`, `lru_cache` |
| `06_programacion_por_eventos` | `event_loop_consola.py` | Bus de eventos, **event loop con cola**, propagación |
| | `tkinter_eventos.py` | GUI con botones, `bind`, `<Return>`, `<Enter>`, `mainloop()` |
| `07_integrador` | `sistema_biblioteca.py` | **Todo junto:** abstracta, interfaz, herencia, polimorfismo, agregación, composición, excepciones, pickle, funcional, eventos y menú |
| `teoria` | `interpretados_vs_compilados.md` | Teoría de la Clase XIV (sin código) |

## Equivalencias Java → Python

| Java | Python |
|---|---|
| `class Gato extends Animal` | `class Gato(Animal):` |
| `implements A, B` | heredar de varias clases `ABC`: `class X(A, B):` |
| `abstract class` / `abstract void f();` | `class X(ABC):` + `@abstractmethod` |
| `interface` | clase `ABC` con solo métodos abstractos |
| constructor `Persona(...)` | `def __init__(self, ...):` |
| `this` | `self` |
| `super(x)` / `super.metodo()` | `super().__init__(x)` / `super().metodo()` |
| `@Override` | redefinir el método con el mismo nombre |
| `private` / `protected` | `__atributo` / `_atributo` |
| getters / setters | `@property` / `@x.setter` |
| `static` | `@staticmethod`, `@classmethod` o atributo de clase |
| sobrecarga de métodos | parámetros por defecto o `*args` |
| `toString()` / `equals()` | `__str__` / `__eq__` |
| `instanceof` | `isinstance(obj, Clase)` |
| `ArrayList<T>` / `HashMap<K,V>` | `list` / `dict` |
| `try / catch / throw` | `try / except / raise` |
| `x -> x * 2` (lambda) / `stream().map()` | `lambda x: x * 2` / `map()` |

## Plantilla rápida para arrancar un ejercicio

```python
from abc import ABC, abstractmethod
import pickle
from functools import reduce

class Base(ABC):
    def __init__(self, nombre):
        self.nombre = nombre

    @abstractmethod
    def calcular(self): ...

    def __str__(self):
        return f"{type(self).__name__}: {self.nombre}"

class Hija(Base):
    def __init__(self, nombre, valor):
        super().__init__(nombre)
        self.valor = valor

    def calcular(self):
        return self.valor * 2

if __name__ == "__main__":
    items = [Hija("a", 1), Hija("b", 5)]
    grandes = list(filter(lambda i: i.calcular() > 5, items))
    total = reduce(lambda acc, i: acc + i.calcular(), items, 0)
    with open("datos.pkl", "wb") as f:
        pickle.dump(items, f)
```
