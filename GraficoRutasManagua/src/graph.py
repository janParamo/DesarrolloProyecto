import networkx as nx

class ManaguaGraph:
    def __init__(self):
        self.graph = nx.Graph()

    def add_route(self, origen, destino, costo):
        self.graph.add_edge(origen, destino, weight=costo)

    def find_optimal_path(self, origen, destino):
        path = nx.shortest_path(self.graph, origen, destino, weight='weight')
        cost = nx.shortest_path_length(self.graph, origen, destino, weight='weight')
        return path, cost