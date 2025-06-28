import tkinter as tk
from tkinter import messagebox
import os

class HistorialDestinos:
    def __init__(self, maxlen=5):
        self.maxlen = maxlen
        self.historial = []

    def agregar_destino_si_valido(self, destino, paradas_lista):
        if destino and destino in paradas_lista and (not self.historial or self.historial[-1] != destino):
            if destino in self.historial:
                self.historial.remove(destino)
            self.historial.append(destino)
            if len(self.historial) > self.maxlen:
                self.historial.pop(0)

    def obtener_historial(self):
        return self.historial

    def limpiar_historial(self):
        self.historial.clear()

    def mostrar_ventana_historial(self, parent, set_destino_callback):
        ventana = tk.Toplevel(parent)
        ventana.title("Historial de Destinos")
        ventana.geometry("350x350")
        ventana.resizable(True, True)

        tk.Label(ventana, text="Historial de destinos recientes:", font=("Arial", 12, "bold")).pack(pady=(10, 2))

        listbox = tk.Listbox(ventana, font=("Arial", 12), height=10)
        listbox.pack(padx=20, fill="both", expand=True)
        for destino in reversed(self.obtener_historial()):
            listbox.insert(tk.END, destino)

        def seleccionar():
            seleccion = listbox.curselection()
            if not seleccion:
                messagebox.showwarning("Aviso", "Seleccione un destino del historial.")
                return
            idx = len(self.obtener_historial()) - 1 - seleccion[0]
            destino = self.obtener_historial()[idx]
            set_destino_callback(destino)
            ventana.destroy()
            messagebox.showinfo("Seleccionado", f"Destino '{destino}' seleccionado.")

        btn_seleccionar = tk.Button(
            ventana, text="Seleccionar", bg="#00796b", fg="white", font=("Arial", 11, "bold"),
            command=seleccionar
        )
        btn_seleccionar.pack(pady=8)

        def limpiar():
            if messagebox.askyesno("Limpiar historial", "¿Desea limpiar el historial de destinos?"):
                self.limpiar_historial()
                listbox.delete(0, tk.END)

        btn_limpiar = tk.Button(
            ventana, text="Limpiar historial", bg="#c62828", fg="white", font=("Arial", 10, "bold"),
            command=limpiar
        )
        btn_limpiar.pack(pady=2)