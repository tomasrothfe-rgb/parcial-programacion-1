# Lenguajes interpretados vs compilados (Clase XIV)

Es un tema teórico, sin código, pero puede aparecer como pregunta.

| | Interpretado | Compilado |
|---|---|---|
| **Cómo funciona** | El intérprete traduce y ejecuta el código fuente **en el momento**, línea por línea | El compilador traduce **antes** todo el código a código máquina y genera un ejecutable |
| **Ventajas** | Portabilidad (corre donde haya intérprete). Desarrollo y depuración rápidos | Más rendimiento. Se distribuye sin el código fuente |
| **Desventajas** | Más lento. Hay que distribuir el código fuente y el intérprete (seguridad/privacidad) | El ejecutable depende del SO y de la arquitectura. Compilar puede ser lento |
| **Ejemplos** | Python, JavaScript, PHP | C, C++, Go, Rust |

**Grace Hopper** creó el primer compilador (traducía instrucciones en inglés a lenguaje máquina) e impulsó los lenguajes independientes de la máquina, lo que llevó a **COBOL**.

## Java: un caso híbrido

`.java` → (javac) → **bytecode** `.class` → la **JVM** lo interpreta o lo compila en tiempo de ejecución (JIT).

- **Ventajas:** lenguaje maduro y popular, rendimiento intermedio (la JVM optimiza el bytecode), portable (corre donde haya JVM), ecosistema grande (Spring, Hibernate).
- **Desventajas:** menos rápido que Go o Rust, la JVM agrega complejidad y tarda en arrancar.
- **JDK** (herramientas para desarrollar, incluye el compilador) ⊃ **JRE** (para ejecutar) ⊃ **JVM** (ejecuta el bytecode).

## ¿Y Python?

Python también es, en realidad, híbrido: compila el código a bytecode (`.pyc`, en la carpeta `__pycache__`) y la máquina virtual de Python lo interpreta. Por eso se lo considera "interpretado".
