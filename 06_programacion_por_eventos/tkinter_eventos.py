"""
PROGRAMACIÓN POR EVENTOS CON TKINTER (GUI)

- Cada widget (Button, Entry, Label...) genera eventos.
- command=funcion       -> manejador del clic de un botón
- widget.bind("<Evento>", funcion) -> manejador de cualquier evento; recibe 'event'
- ventana.mainloop()    -> EL EVENT LOOP: espera eventos y llama a los manejadores

Eventos comunes en bind:
  "<Button-1>" clic izquierdo   "<Return>" Enter   "<KeyRelease>" soltar tecla
  "<Enter>" mouse entra         "<Leave>" mouse sale   "<Double-Button-1>" doble clic
"""
import tkinter as tk
from tkinter import messagebox


class AppContador:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Eventos con Tkinter")
        self.contador = 0                        # estado

        # --- Widgets ---
        self.lbl_contador = tk.Label(ventana, text="Contador: 0", font=("Arial", 16))
        self.lbl_contador.pack(pady=10)

        frame = tk.Frame(ventana)
        frame.pack()
        tk.Button(frame, text="+1", width=6, command=self.sumar).pack(side="left", padx=5)
        tk.Button(frame, text="-1", width=6, command=self.restar).pack(side="left", padx=5)
        tk.Button(frame, text="Reset", width=6, command=self.reset).pack(side="left", padx=5)

        tk.Label(ventana, text="Escribí tu nombre y apretá Enter:").pack(pady=(15, 0))
        self.entrada = tk.Entry(ventana, width=30)
        self.entrada.pack()
        self.lbl_eco = tk.Label(ventana, text="", fg="gray")
        self.lbl_eco.pack()

        self.lbl_saludo = tk.Label(ventana, text="", font=("Arial", 12, "bold"))
        self.lbl_saludo.pack(pady=5)

        self.lbl_hover = tk.Label(ventana, text="Pasá el mouse por acá", bg="lightgray", width=30)
        self.lbl_hover.pack(pady=10)

        # --- Bindeo de eventos ---
        self.entrada.bind("<Return>", self.saludar)          # tecla Enter
        self.entrada.bind("<KeyRelease>", self.eco)          # cada tecla
        self.lbl_hover.bind("<Enter>", lambda e: self.lbl_hover.config(bg="lightblue"))
        self.lbl_hover.bind("<Leave>", lambda e: self.lbl_hover.config(bg="lightgray"))
        self.lbl_contador.bind("<Double-Button-1>", lambda e: self.reset())
        self.ventana.protocol("WM_DELETE_WINDOW", self.al_cerrar)  # evento del sistema

    # --- Manejadores ---
    def actualizar(self):
        self.lbl_contador.config(text=f"Contador: {self.contador}")

    def sumar(self):
        self.contador += 1
        self.actualizar()

    def restar(self):
        self.contador -= 1
        self.actualizar()

    def reset(self):
        self.contador = 0
        self.actualizar()

    def eco(self, event):
        self.lbl_eco.config(text=f"Última tecla: {event.keysym}")

    def saludar(self, event):
        nombre = self.entrada.get().strip()
        if not nombre:
            messagebox.showwarning("Atención", "Ingresá un nombre")
            return
        self.lbl_saludo.config(text=f"¡Hola, {nombre}!")
        self.entrada.delete(0, tk.END)

    def al_cerrar(self):
        if messagebox.askokcancel("Salir", "¿Cerrar la aplicación?"):
            self.ventana.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("320x320")
    AppContador(root)
    root.mainloop()          # <- event loop
