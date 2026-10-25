"""
PROGRAMACIÓN CONDUCIDA POR EVENTOS (Clase XX) - sin interfaz gráfica

El flujo lo determinan los EVENTOS; el programa REACCIONA a ellos.
  EVENTO          -> suceso detectable (de usuario, del sistema o personalizado)
  MANEJADOR       -> función que se ejecuta en respuesta a un evento (event handler)
  EVENT LOOP      -> ciclo que: 1) espera un evento  2) lo encola
                     3) procesa el siguiente ejecutando su manejador  4) repite
  PROPAGACIÓN     -> el evento pasa por elementos anidados (padre/hijo)

Este archivo implementa:
  1. Un "bus" de eventos (suscribir/emitir), patrón Observador.
  2. Un event loop con cola, con variables de estado (vidas de un juego).
  3. Propagación de un evento por una jerarquía de elementos.
"""
from collections import deque


# =============================================================
# 1) BUS DE EVENTOS: varios manejadores por evento
# =============================================================
class GestorEventos:
    def __init__(self):
        self.manejadores = {}            # {"nombre_evento": [funcion1, funcion2]}

    def suscribir(self, evento, manejador):
        self.manejadores.setdefault(evento, []).append(manejador)

    def desuscribir(self, evento, manejador):
        self.manejadores.get(evento, []).remove(manejador)

    def emitir(self, evento, *datos):
        for manejador in self.manejadores.get(evento, []):
            manejador(*datos)


# =============================================================
# 2) EVENT LOOP con cola y estado
# =============================================================
class Juego:
    def __init__(self):
        self.vidas = 3                   # variables de estado
        self.puntos = 0
        self.cola = deque()              # cola de eventos
        self.manejadores = {
            "golpe": self.on_golpe,
            "moneda": self.on_moneda,
            "vida_extra": self.on_vida_extra,
        }

    # ----- manejadores -----
    def on_golpe(self):
        self.vidas -= 1
        print(f"  ¡Golpe! Vidas: {self.vidas}")

    def on_moneda(self, valor=10):
        self.puntos += valor
        print(f"  Moneda +{valor}. Puntos: {self.puntos}")

    def on_vida_extra(self):
        self.vidas += 1
        print(f"  Vida extra. Vidas: {self.vidas}")

    # ----- loop -----
    def encolar(self, evento, *datos):
        self.cola.append((evento, datos))

    def ejecutar(self):
        while self.vidas > 0 and self.cola:          # mientras la condición sea verdadera
            evento, datos = self.cola.popleft()      # toma el siguiente evento
            manejador = self.manejadores.get(evento)
            if manejador:
                manejador(*datos)                    # ejecuta su manejador
            else:
                print(f"  Evento desconocido: {evento}")
        print("GAME OVER" if self.vidas <= 0 else "Fin de los eventos")


# =============================================================
# 3) PROPAGACIÓN de eventos (burbujeo hijo -> padre)
# =============================================================
class Elemento:
    def __init__(self, nombre, padre=None):
        self.nombre = nombre
        self.padre = padre

    def click(self, detener_en=None):
        elemento = self
        while elemento:                              # sube por la jerarquía
            print(f"  click recibido por: {elemento.nombre}")
            if elemento.nombre == detener_en:        # "stopPropagation"
                print("  propagación detenida")
                break
            elemento = elemento.padre


if __name__ == "__main__":
    print("1) Bus de eventos")
    gestor = GestorEventos()
    gestor.suscribir("compra", lambda prod, monto: print(f"  Log: se vendió {prod}"))
    gestor.suscribir("compra", lambda prod, monto: print(f"  Caja: +${monto}"))
    gestor.suscribir("stock_bajo", lambda prod: print(f"  ALERTA: queda poco {prod}"))
    gestor.emitir("compra", "Remera", 8000)
    gestor.emitir("stock_bajo", "Remera")

    print("\n2) Event loop")
    juego = Juego()
    for ev in ["moneda", "golpe", "vida_extra", "golpe", "salto", "golpe", "golpe", "moneda"]:
        juego.encolar(ev)
    juego.ejecutar()

    print("\n3) Propagación")
    ventana = Elemento("ventana")
    formulario = Elemento("formulario", ventana)
    boton = Elemento("botón", formulario)
    boton.click()
    boton.click(detener_en="formulario")
