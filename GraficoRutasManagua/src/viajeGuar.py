import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

GUARDADOS_PATH = os.path.join(os.path.dirname(__file__), "destinos_guardados.json")

def guardar_destino_personalizado(nombre, origen, destino):
    if not nombre or not origen or not destino:
        raise ValueError("Debe ingresar nombre, origen y destino.")
    guardados = obtener_destinos_guardados()
    guardados[nombre] = {"origen": origen, "destino": destino}
    with open(GUARDADOS_PATH, "w", encoding="utf-8") as f:
        json.dump(guardados, f, ensure_ascii=False, indent=2)

def obtener_destinos_guardados():
    if os.path.exists(GUARDADOS_PATH):
        with open(GUARDADOS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def eliminar_destino_guardado(nombre):
    guardados = obtener_destinos_guardados()
    if nombre in guardados:
        del guardados[nombre]
        with open(GUARDADOS_PATH, "w", encoding="utf-8") as f:
            json.dump(guardados, f, ensure_ascii=False, indent=2)
        return True
    return False

def actualizar_lista_guardados(listbox):
    listbox.delete(0, "end")
    for nombre in obtener_destinos_guardados().keys():
        listbox.insert("end", nombre)

def seleccionar_guardado(listbox):
    seleccion = listbox.curselection()
    if not seleccion:
        return None
    nombre = listbox.get(seleccion[0])
    guardados = obtener_destinos_guardados()
    if nombre in guardados:
        return nombre, guardados[nombre]["origen"], guardados[nombre]["destino"]
    return None

def mostrar_ventana_viajes(parent, paradas_lista, set_origen_destino_callback):
    ventana = tk.Toplevel(parent)
    ventana.title("Viajes Guardados")
    ventana.geometry("400x450")
    ventana.resizable(True, True)

    label_lista = tk.Label(ventana, text="Destinos guardados:", font=("Arial", 12, "bold"))
    label_lista.pack(pady=(10, 2))

    lista_guardados = tk.Listbox(ventana, font=("Arial", 12), height=8)
    lista_guardados.pack(padx=20, fill="x")
    actualizar_lista_guardados(lista_guardados)

    def seleccionar():
        resultado = seleccionar_guardado(lista_guardados)
        if not resultado:
            messagebox.showwarning("Aviso", "Seleccione un guardado para usar.")
            return
        nombre, origen, destino = resultado
        set_origen_destino_callback(origen, destino)
        ventana.destroy()
        messagebox.showinfo("Seleccionado", f"Guardado '{nombre}' seleccionado:\nOrigen: {origen}\nDestino: {destino}")

    btn_seleccionar = tk.Button(
        ventana, text="Seleccionar", bg="#00796b", fg="white", font=("Arial", 11, "bold"),
        command=seleccionar
    )
    btn_seleccionar.pack(pady=(8, 2))

    def eliminar():
        seleccion = lista_guardados.curselection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Seleccione un guardado para eliminar.")
            return
        nombre = lista_guardados.get(seleccion[0])
        if eliminar_destino_guardado(nombre):
            actualizar_lista_guardados(lista_guardados)
            messagebox.showinfo("Eliminado", f"Guardado '{nombre}' eliminado.")

    btn_eliminar = tk.Button(
        ventana, text="Eliminar", bg="#c62828", fg="white", font=("Arial", 11, "bold"),
        command=eliminar
    )
    btn_eliminar.pack(pady=2)

    frame_nuevo = tk.LabelFrame(ventana, text="Crear nuevo guardado", font=("Arial", 11, "bold"))
    frame_nuevo.pack(padx=20, pady=12, fill="x")

    tk.Label(frame_nuevo, text="Nombre:", font=("Arial", 10)).grid(row=0, column=0, sticky="e", pady=2)
    entry_nombre = tk.Entry(frame_nuevo, font=("Arial", 10))
    entry_nombre.grid(row=0, column=1, pady=2, sticky="ew")

    tk.Label(frame_nuevo, text="Origen:", font=("Arial", 10)).grid(row=1, column=0, sticky="e", pady=2)
    combo_origen = ttk.Combobox(frame_nuevo, values=paradas_lista, state="readonly", font=("Arial", 10))
    combo_origen.grid(row=1, column=1, pady=2, sticky="ew")

    tk.Label(frame_nuevo, text="Destino:", font=("Arial", 10)).grid(row=2, column=0, sticky="e", pady=2)
    combo_destino = ttk.Combobox(frame_nuevo, values=paradas_lista, state="readonly", font=("Arial", 10))
    combo_destino.grid(row=2, column=1, pady=2, sticky="ew")

    frame_nuevo.columnconfigure(1, weight=1)

    def guardar_nuevo():
        nombre = entry_nombre.get().strip()
        origen = combo_origen.get().strip()
        destino = combo_destino.get().strip()
        if not nombre or not origen or not destino:
            messagebox.showerror("Error", "Debe ingresar nombre, origen y destino.")
            return
        try:
            guardar_destino_personalizado(nombre, origen, destino)
            actualizar_lista_guardados(lista_guardados)
            messagebox.showinfo("Guardado", "Destino guardado exitosamente.")
            entry_nombre.delete(0, tk.END)
            combo_origen.set("")
            combo_destino.set("")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    btn_guardar = tk.Button(
        frame_nuevo, text="Guardar", bg="#00796b", fg="white", font=("Arial", 10, "bold"),
        command=guardar_nuevo
    )
    btn_guardar.grid(row=3, column=0, columnspan=2, pady=(8, 2))