import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
from PIL import Image, ImageTk
import os
import json
from viajeGuar import (
    guardar_destino_personalizado,
    obtener_destinos_guardados,
    eliminar_destino_guardado,
    actualizar_lista_guardados,
    seleccionar_guardado,
    mostrar_ventana_viajes
)
from graph import ManaguaGraph
from historial import HistorialDestinos
from mapaRutas import mostrar_mapa_rutas

# Leer rutas desde el archivo Excel
df = pd.read_excel(r"c:\Users\landm\OneDrive\Escritorio\DesarrolloProyecto\GraficoRutasManagua\src\excel\Rutas.xlsx")
rutas_dict = {}
paradas_set = set()
for _, row in df.iterrows():
    ruta = str(row['Ruta']).strip()
    parada = str(row['Parada']).strip()
    if ruta not in rutas_dict:
        rutas_dict[ruta] = []
    rutas_dict[ruta].append(parada)
    paradas_set.add(parada)

paradas_lista = sorted(list(paradas_set))

# Antes de la clase App, crea el grafo y agrega las rutas
managua_graph = ManaguaGraph()
for ruta, paradas in rutas_dict.items():
    for i in range(len(paradas) - 1):
        managua_graph.add_route(paradas[i], paradas[i+1], 2.5)

HISTORIAL_PATH = os.path.join(os.path.dirname(__file__), "historial_destinos.xlsx")

# Interfaz gráfica
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Rutas de Managua")
        self.root.geometry("450x850")
        self.root.configure(bg="#e0f7fa")
        self.root.minsize(350, 600)
        self.root.resizable(True, True)

        # --- Estilo para Combobox redondeado ---
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("RoundedCombobox.TCombobox",
                        fieldbackground="#ffffff",
                        background="#ffffff",
                        bordercolor="#00796b",
                        lightcolor="#00796b",
                        darkcolor="#00796b",
                        borderwidth=10,
                        relief="flat",
                        padding=5)

        # PanedWindow vertical para dividir mapa y opciones
        self.paned = tk.PanedWindow(root, orient=tk.VERTICAL, sashwidth=8, sashrelief="raised", bg="#e0f7fa")
        self.paned.pack(fill="both", expand=True)

        # Frame 1: Mapa (arriba)
        self.mapa_frame = tk.Frame(self.paned, bg="#222831")
        self.paned.add(self.mapa_frame, minsize=100)

        # Frame 2: Opciones (abajo)
        self.opciones_frame = tk.Frame(self.paned, bg="#181616")
        self.paned.add(self.opciones_frame, minsize=120)

        # --- Opciones dentro del frame 2 ---
        self.label_origen = tk.Label(self.opciones_frame, text="Seleccione la parada de origen:", bg="#181616", fg="white", font=("Arial", 14))
        self.label_origen.pack(pady=(10, 2), anchor="w")
        self.origen_combo = ttk.Combobox(self.opciones_frame, values=paradas_lista, state="readonly", width=30, font=("Arial", 12), style="RoundedCombobox.TCombobox")
        self.origen_combo.pack(pady=2, padx=10, fill="x") 
        self.origen_combo.set("🔍 ¿Dónde te encuentras el día de hoy?")

        self.label_destino = tk.Label(self.opciones_frame, text="Seleccione la parada de destino:", bg="#181616", fg="white", font=("Arial", 14))
        self.label_destino.pack(pady=(10, 2), anchor="w")
        self.destino_combo = ttk.Combobox(self.opciones_frame, values=paradas_lista, state="readonly", width=30, font=("Arial", 12), style="RoundedCombobox.TCombobox")
        self.destino_combo.pack(pady=2, padx=10, fill="x")
        self.destino_combo.set("🔍 ¿Adonde deseas llegar el día de hoy?")

        self.buscar_btn = tk.Button(self.opciones_frame, text="Buscar Ruta Óptima", bg="#00796b", fg="white", font=("Arial", 12), command=self.buscar_ruta)
        self.buscar_btn.pack(pady=10, anchor="center")

        # --- Lupa y mensaje predeterminado ---
        self.lupa_frame = tk.Frame(self.mapa_frame, bg="#222831")
        self.lupa_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.lupa_label = tk.Label(self.lupa_frame, text="🔍", font=("Arial", 60), bg="#222831", fg="#cccccc")
        self.lupa_label.pack()
        self.lupa_msg = tk.Label(self.lupa_frame, text="Seleccione un destino para ver la ruta", font=("Arial", 16), bg="#222831", fg="#cccccc")
        self.lupa_msg.pack()

        # --- Historial de destinos (persistente) ---
        self.historial = HistorialDestinos(maxlen=5)

        self.historial_label = tk.Label(self.opciones_frame, text="Recientes", bg="#181616", fg="white", font=("Arial", 11))
        self.historial_label.pack(pady=(5, 2), padx=7, anchor="w")
        self.historial_listbox = tk.Listbox(self.opciones_frame, height=6, font=("Arial", 11), bg="#232326", fg="white", selectbackground="#00796b", activestyle="none")
        self.historial_listbox.pack(pady=(0, 8), padx=10, fill="x")
        self.historial_listbox.bind("<<ListboxSelect>>", self.seleccionar_destino_historial)
        self.actualizar_historial()

        # En tu __init__ después de crear el paned y frames:
        self.root.after(100, self.ajustar_sash)
        self.paned.bind("<Configure>", self.ajustar_sash)

        # Evento para ocultar la lupa cuando se selecciona destino (solo una vez aquí)
        self.destino_combo.bind("<<ComboboxSelected>>", self.ocultar_lupa)

        # --- Botón circular con imagen para desplegar panel lateral ---
        img_path = r"c:\Users\landm\OneDrive\Escritorio\DesarrolloProyecto\GraficoRutasManagua\src\Imagenes\Opciones.png"
        if not os.path.exists(img_path):
            print("¡La imagen no existe en la ruta especificada!")

        self.opciones_img = Image.open(img_path).resize((50, 50))
        self.opciones_img_tk = ImageTk.PhotoImage(self.opciones_img)
        self.boton_opciones = tk.Button(
            self.mapa_frame,
            image=self.opciones_img_tk,
            bg="#222831",
            bd=0,
            activebackground="#222831",
            command=self.toggle_panel_lateral,
            highlightthickness=0
        )
        self.boton_opciones.pack(pady=8, padx=8, anchor="nw")

        # --- Frame lateral oculto ---
        self.panel_lateral = tk.Frame(self.root, bg="#232326", width=0, height=850)
        self.panel_lateral.place(x=0, y=0, relheight=1)

        # --- Frame para centrar los botones en el panel lateral ---
        self.botones_panel = tk.Frame(self.panel_lateral, bg="#232326")
        self.botones_panel.place(relx=0.5, rely=0.5, anchor="center")

        self.panel_abierto = False

        # Vincula el evento de clic a toda la ventana
        self.root.bind("<Button-1>", self.cerrar_panel_si_fuera)

        # --- Carga de imágenes para los botones del panel lateral ---
        img_viajes = Image.open(r"c:\Users\landm\OneDrive\Escritorio\DesarrolloProyecto\GraficoRutasManagua\src\Imagenes\Viaje.jpg").resize((28, 28))
        self.img_viajes_tk = ImageTk.PhotoImage(img_viajes)
        img_lista = Image.open(r"c:\Users\landm\OneDrive\Escritorio\DesarrolloProyecto\GraficoRutasManagua\src\Imagenes\Mapaicono.png").resize((28, 28))
        self.img_lista_tk = ImageTk.PhotoImage(img_lista)
        img_mapa = Image.open(r"c:\Users\landm\OneDrive\Escritorio\DesarrolloProyecto\GraficoRutasManagua\src\Imagenes\Lista.jpg").resize((28, 28))
        self.img_mapa_tk = ImageTk.PhotoImage(img_mapa)

        # --- Botones en el panel lateral ---
        frame_viajes = tk.Frame(self.botones_panel, bg="#232326")
        frame_viajes.pack(pady=(10, 10), padx=30, anchor="w")
        tk.Label(frame_viajes, image=self.img_viajes_tk, bg="#232326").pack(side="left")
        self.btn_viajes_guardados = tk.Button(
            frame_viajes,
            text="Viajes Guardados",
            bg="#00796b",
            fg="white",
            font=("Arial", 13, "bold"),
            bd=0,
            activebackground="#009688",
            activeforeground="white",
            width=16,
            command=self.abrir_ventana_viajes
        )
        self.btn_viajes_guardados.pack(side="left")

        frame_lista = tk.Frame(self.botones_panel, bg="#232326")
        frame_lista.pack(pady=(10, 10), padx=30, anchor="w")
        tk.Label(frame_lista, image=self.img_lista_tk, bg="#232326").pack(side="left")
        self.btn_lista_rutas = tk.Button(
            frame_lista,
            text="Lista de Rutas",
            bg="#00796b",
            fg="white",
            font=("Arial", 13, "bold"),
            bd=0,
            activebackground="#009688",
            activeforeground="white",
            width=16,
            command=self.abrir_ventana_lista
        )
        self.btn_lista_rutas.pack(side="left")

        frame_mapa = tk.Frame(self.botones_panel, bg="#232326")
        frame_mapa.pack(pady=(10, 10), padx=30, anchor="w")
        tk.Label(frame_mapa, image=self.img_mapa_tk, bg="#232326").pack(side="left")
        self.btn_mapa_rutas = tk.Button(
            frame_mapa,
            text="Mapa de rutas",
            bg="#00796b",
            fg="white",
            font=("Arial", 13, "bold"),
            bd=0,
            activebackground="#009688",
            activeforeground="white",
            width=16,
            command=self.abrir_ventana_mapa
        )
        self.btn_mapa_rutas.pack(side="left")

        # Métodos para abrir nuevas ventanas
    def abrir_ventana_viajes(self):
        def set_origen_destino(origen, destino):
            self.origen_combo.set(origen)
            self.destino_combo.set(destino)
            self.ocultar_lupa()
        mostrar_ventana_viajes(self.root, paradas_lista, set_origen_destino)

    def abrir_ventana_lista(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Lista de Rutas")
        ventana.geometry("500x400")
        ventana.resizable(True, True)

        frame = tk.Frame(ventana)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Label(frame, text="Ingrese el numero de la ruta:", font=("Arial", 11, "bold")).pack(anchor="w")

        def solo_numeros(char):
            return char.isdigit() or char == ""

        vcmd = (ventana.register(solo_numeros), "%P")
        entry_busqueda = tk.Entry(frame, font=("Arial", 11), validate="key", validatecommand=vcmd)
        entry_busqueda.pack(fill="x", pady=(0, 8))

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")

        lista = tk.Text(frame, font=("Arial", 12), yscrollcommand=scrollbar.set, wrap="word", state="normal")
        lista.pack(fill="both", expand=True)
        scrollbar.config(command=lista.yview)

        def obtener_lista_rutas_y_paradas(rutas_dict):
            """
            Devuelve una lista de tuplas (ruta, [paradas]) a partir del diccionario de rutas.
            """
            return [(ruta, paradas) for ruta, paradas in rutas_dict.items()]

        rutas_y_paradas = obtener_lista_rutas_y_paradas(rutas_dict)

        def mostrar_rutas(filtro=""):
            lista.config(state="normal")
            lista.delete("1.0", "end")
            for ruta, paradas in rutas_y_paradas:
                if filtro and filtro.strip() not in str(ruta):
                    continue
                lista.insert("end", f"Ruta {ruta}:\n")
                for parada in paradas:
                    lista.insert("end", f"   - {parada}\n")
                lista.insert("end", "\n")
            lista.config(state="disabled")

        # Mostrar todas las rutas al abrir la ventana
        mostrar_rutas()

        def on_busqueda(event):
            filtro = entry_busqueda.get().strip()
            mostrar_rutas(filtro)

        entry_busqueda.bind("<KeyRelease>", on_busqueda)

    def abrir_ventana_mapa(self):
        mapa_path = r"C:\Users\landm\OneDrive\Escritorio\DesarrolloProyecto\GraficoRutasManagua\src\Imagenes\mapa.png"
        mostrar_mapa_rutas(self.root, mapa_path)

    def ajustar_sash(self, event=None):
        self.paned.update_idletasks()
        altura_paned = self.paned.winfo_height()
        altura_opciones = int(altura_paned * 0.57)  # 0.57 para que frame2 sea 43%
        self.paned.sash_place(0, 0, altura_opciones)

    def ocultar_lupa(self, event=None):
        destino = self.destino_combo.get().strip()
        if destino and destino != "🔍 Seleccione un destino...":
            self.lupa_frame.place_forget()
        else:
            self.lupa_frame.place(relx=0.5, rely=0.5, anchor="center")

    def buscar_ruta(self):
        origen = self.origen_combo.get().strip()
        destino = self.destino_combo.get().strip()
        if not origen or not destino:
            messagebox.showerror("Error", "Debe seleccionar ambas paradas.")
            return
        self.historial.agregar_destino_si_valido(destino, paradas_lista)
        self.actualizar_historial()

        try:
            recorrido, _ = managua_graph.find_optimal_path(origen, destino)
            rutas_usadas = []
            ruta_cambios = []
            ruta_actual = None

            for i in range(len(recorrido)-1):
                for ruta, paradas in rutas_dict.items():
                    if recorrido[i] in paradas and recorrido[i+1] in paradas:
                        if ruta_actual != ruta:
                            ruta_actual = ruta
                            ruta_cambios.append(f"Ruta {ruta}")
                        ruta_cambios.append(recorrido[i+1])
                        if not rutas_usadas or rutas_usadas[-1] != ruta:
                            rutas_usadas.append(ruta)
                        break

            resultado_ruta = ruta_cambios[0]
            for item in ruta_cambios[1:]:
                resultado_ruta += f" → {item}"

            costo = len(rutas_usadas) * 2.5

            mensaje = f"Ruta óptima encontrada:\n{resultado_ruta}\n"
            mensaje += f"Rutas usadas: {', '.join(rutas_usadas)}\n"
            mensaje += f"Costo total: {costo} córdobas\n"
            messagebox.showinfo("Ruta Óptima", mensaje)
        except Exception as e:
            messagebox.showerror("Sin ruta", f"No se encontró una ruta entre esas paradas.\n{e}")

    def abrir_ventana_historial(self):
        def set_destino(destino):
            self.destino_combo.set(destino)
            self.ocultar_lupa()
        self.historial.mostrar_ventana_historial(self.root, set_destino)

    def toggle_panel_lateral(self):
        if self.panel_abierto:
            self.panel_lateral.config(width=0)
            self.panel_lateral.place_forget()
            self.panel_abierto = False
        else:
            self.panel_lateral.config(width=250)
            self.panel_lateral.place(x=0, y=0, relheight=1)
            self.panel_abierto = True

    def cerrar_panel_si_fuera(self, event):
        # Solo cerrar si el panel está abierto y el clic fue fuera del panel lateral
        if self.panel_abierto:
            x, y = event.x_root, event.y_root
            panel_x1 = self.panel_lateral.winfo_rootx()
            panel_y1 = self.panel_lateral.winfo_rooty()
            panel_x2 = panel_x1 + self.panel_lateral.winfo_width()
            panel_y2 = panel_y1 + self.panel_lateral.winfo_height()
            if not (panel_x1 <= x <= panel_x2 and panel_y1 <= y <= panel_y2):
                self.toggle_panel_lateral()

    def seleccionar_destino_historial(self, event):
        seleccion = self.historial_listbox.curselection()
        if seleccion:
            idx = len(self.historial.obtener_historial()) - 1 - seleccion[0]
            destino = self.historial.obtener_historial()[idx]
            self.destino_combo.set(destino)
            self.ocultar_lupa()

    def actualizar_historial(self):
        self.historial_listbox.delete(0, tk.END)
        for destino in reversed(self.historial.obtener_historial()):
            self.historial_listbox.insert(tk.END, destino)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

