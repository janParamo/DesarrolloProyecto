class ManaguaGraph:
    def __init__(self):
        self.graph = self.crear_grafo()

    def crear_grafo(self):
        import networkx as nx
        G = nx.Graph()
        return G

    def agregar_ruta(self, origen, destino, peso):
        self.graph.add_edge(origen, destino, weight=peso)

    def ruta_optima(self, origen, destino):
        import networkx as nx
        try:
            camino = nx.dijkstra_path(self.graph, source=origen, target=destino, weight='weight')
            costo_total = nx.dijkstra_path_length(self.graph, source=origen, target=destino, weight='weight')
            return camino, costo_total
        except nx.NetworkXNoPath:
            print(f"No existe un camino entre {origen} y {destino}.")
            return None, None

    def mostrar_grafo(self):
        return self.graph.edges(data=True)