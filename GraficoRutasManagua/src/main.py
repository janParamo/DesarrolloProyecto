import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import networkx as nx
from graph import ManaguaGraph  # Asegúrate de que este import sea correcto

# Leer rutas desde el archivo Excel
df = pd.read_excel(r"c:\Users\landm\OneDrive\Escritorio\DesarrolloProyecto\GraficoRutasManagua\src\Rutas.xlsx")
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

# Interfaz gráfica
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Rutas de Managua")
        self.root.geometry("1200x750")  # Aumenta el tamaño de la ventana

        self.root.configure(bg="#e0f7fa")

        # Frame principal para organizar mapa y lista de rutas
        main_frame = tk.Frame(root, bg="#e0f7fa")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Frame izquierdo para la lista de rutas
        left_frame = tk.Frame(main_frame, bg="#e0f7fa")
        left_frame.pack(side="left", fill="y", padx=(0, 1))  # Espacio horizontal mínimo

        # Lista de solo nombres de rutas, sin paradas
        self.rutas_listbox = tk.Listbox(
            left_frame,
            font=("Arial", 12),
            width=20,
            height=22,
            bg="#e0f7fa",
            highlightthickness=0,
            borderwidth=0,
            relief="flat"
        )
        for ruta in rutas_dict.keys():
            self.rutas_listbox.insert(tk.END, f"Ruta {ruta}")
        self.rutas_listbox.pack(pady=0, fill="y", expand=True)

        # Frame derecho para el mapa y controles
        right_frame = tk.Frame(main_frame, bg="#e0f7fa")
        right_frame.pack(side="left", fill="both", expand=True)

        # Cargar y mostrar la imagen del mapa (500x375 * 1.25 = 625x468)
        try:
            imagen = Image.open(r"c:\Users\landm\OneDrive\Escritorio\DesarrolloProyecto\GraficoRutasManagua\src\mapa.png")
            imagen = imagen.resize((625, 468), Image.Resampling.LANCZOS)
            self.imagen_tk = ImageTk.PhotoImage(imagen)
            tk.Label(right_frame, image=self.imagen_tk, bg="#e0f7fa").pack(pady=10)
        except Exception as e:
            tk.Label(right_frame, text=f"No se pudo cargar el mapa: {e}", bg="#e0f7fa", fg="red").pack(pady=10)

        # Controles debajo del mapa (Origen y Destino en la misma fila)
        controls_frame = tk.Frame(right_frame, bg="#e0f7fa")
        controls_frame.pack(pady=10)

        # Origen
        tk.Label(controls_frame, text="Seleccione la parada de origen:", bg="#e0f7fa").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.origen_combo = ttk.Combobox(controls_frame, values=paradas_lista, state="readonly", width=25)
        self.origen_combo.grid(row=1, column=0, padx=5, pady=2)

        # Destino
        tk.Label(controls_frame, text="Seleccione la parada de destino:", bg="#e0f7fa").grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.destino_combo = ttk.Combobox(controls_frame, values=paradas_lista, state="readonly", width=25)
        self.destino_combo.grid(row=1, column=1, padx=5, pady=2)

        # Botón debajo de ambos combos
        tk.Button(right_frame, text="Buscar Ruta Óptima", bg="#00796b", fg="white", command=self.buscar_ruta).pack(pady=10)

    def buscar_ruta(self):
        origen = self.origen_combo.get().strip()
        destino = self.destino_combo.get().strip()
        if not origen or not destino:
            messagebox.showerror("Error", "Debe seleccionar ambas paradas.")
            return

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

            # Construir el string de la ruta óptima con cambios de ruta
            resultado_ruta = ruta_cambios[0]
            for item in ruta_cambios[1:]:
                resultado_ruta += f" → {item}"

            costo = len(rutas_usadas) * 2.5
            mensaje = f"Ruta óptima encontrada:\n{resultado_ruta}\n"
            mensaje += f"Rutas usadas: {', '.join(rutas_usadas)}\n"
            mensaje += f"Costo total: {costo} córdobas"
            messagebox.showinfo("Ruta Óptima", mensaje)
            self.mostrar_ruta_en_mapa(recorrido)
        except Exception as e:
            messagebox.showerror("Sin ruta", f"No se encontró una ruta entre esas paradas.\n{e}")

    def mostrar_ruta_en_mapa(self, recorrido):
        # Cargar el mapa base
        mapa_path = r"c:\Users\landm\OneDrive\Escritorio\DesarrolloProyecto\GraficoRutasManagua\src\mapa.png"
        img = Image.open(mapa_path)
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.imshow(img)
        ax.axis('off')

       # Posiciones de las paradas (debes adaptar esto a tus coordenadas reales)
        posiciones = {
            "Mercado Oriental": (120, 340),
            "Rotonda Cristo Rey": (200, 310),
            "UCA": (350, 400),
            "El Zumen": (250, 500),
            "Hospital Lenín Fonseca": (400, 520),
            # ...agrega todas tus paradas aquí
        }

        # Dibuja nodos y líneas
        for i, parada in enumerate(recorrido):
            color = 'red' if i == 0 or i == len(recorrido)-1 else 'green'
            ax.plot(*posiciones[parada], 'o', color=color, markersize=12)
            ax.text(*posiciones[parada], parada, fontsize=9, color='black', ha='center', va='bottom')
            if i > 0:
                prev = recorrido[i-1]
                ax.plot([posiciones[prev][0], posiciones[parada][0]], [posiciones[prev][1], posiciones[parada][1]], color='blue', linewidth=2)

        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

