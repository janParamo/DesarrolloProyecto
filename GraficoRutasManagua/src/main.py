import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt
from graph import ManaguaGraph

# Definir rutas básicas
RUTAS = [
    ("Mercado Oriental", "Rotonda Metrocentro", 5),
    ("Rotonda Metrocentro", "Rotonda Rubén Darío", 3),
    ("Rotonda Rubén Darío", "Universidad Centroamericana", 2),
    ("Universidad Centroamericana", "Rotonda El Güegüense", 4),
    ("Rotonda El Güegüense", "Mercado Roberto Huembes", 6),
    ("Mercado Oriental", "Mercado Roberto Huembes", 7),
    ("Rotonda Metrocentro", "Universidad Centroamericana", 2),
]

# Inicializar grafo
graph = ManaguaGraph()
for origen, destino, costo in RUTAS:
    graph.add_route(origen, destino, costo)

# Interfaz gráfica
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Rutas de Managua")
        self.root.geometry("500x400")
        self.root.configure(bg="#e0f7fa")

        tk.Label(root, text="Rutas Disponibles:", bg="#e0f7fa", font=("Arial", 14, "bold")).pack(pady=10)
        self.rutas_listbox = tk.Listbox(root, font=("Arial", 12), width=50, height=7)
        for idx, (o, d, c) in enumerate(RUTAS):
            self.rutas_listbox.insert(tk.END, f"{idx+1}. {o} ↔ {d} (Costo: {c})")
        self.rutas_listbox.pack(pady=5)

        tk.Label(root, text="Seleccione el número de la ruta de origen y destino:", bg="#e0f7fa").pack(pady=5)
        self.origen_entry = tk.Entry(root, width=5)
        self.origen_entry.pack(side=tk.LEFT, padx=(80,5))
        self.destino_entry = tk.Entry(root, width=5)
        self.destino_entry.pack(side=tk.LEFT)

        tk.Button(root, text="Buscar Ruta Óptima", bg="#00796b", fg="white", command=self.buscar_ruta).pack(pady=10)
        tk.Button(root, text="Ver Grafo de Rutas", bg="#0288d1", fg="white", command=self.mostrar_grafo).pack(pady=5)

    def buscar_ruta(self):
        try:
            idx_origen = int(self.origen_entry.get()) - 1
            idx_destino = int(self.destino_entry.get()) - 1
            origen = RUTAS[idx_origen][0]
            destino = RUTAS[idx_destino][1]
            path, cost = graph.find_optimal_path(origen, destino)
            messagebox.showinfo("Ruta Óptima", f"Ruta: {' → '.join(path)}\nCosto total: {cost}")
        except Exception as e:
            messagebox.showerror("Error", "Seleccione números válidos para origen y destino.")

    def mostrar_grafo(self):
        G = graph.graph
        pos = nx.spring_layout(G, seed=42)
        plt.figure(figsize=(8,6))
        nx.draw_networkx_nodes(G, pos, node_color="#ffb300", node_size=700)
        nx.draw_networkx_edges(G, pos, edge_color="#0288d1", width=2)
        nx.draw_networkx_labels(G, pos, font_size=10, font_color="#37474f")
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color="#d84315")
        plt.title("Grafo de Rutas de Managua", fontsize=16, color="#00796b")
        plt.axis('off')
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()