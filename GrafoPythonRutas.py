import networkx as nx

def crear_grafo():
    # Se crea un grafo ponderado (no dirigido en este caso)
    G = nx.Graph()

    # Agregar nodos (estaciones)
    estaciones = ['Estacion_A', 'Estacion_B', 'Estacion_C', 'Estacion_D']
    G.add_nodes_from(estaciones)

    # Agregar conexiones (rutas) entre estaciones con un atributo "peso"
    # El peso puede representar el tiempo estimado de viaje, distancia o costo.
    rutas = [
        ('Estacion_A', 'Estacion_B', 4),
        ('Estacion_A', 'Estacion_C', 2),
        ('Estacion_B', 'Estacion_C', 1),
        ('Estacion_B', 'Estacion_D', 5),
        ('Estacion_C', 'Estacion_D', 8)
    ]
    for origen, destino, peso in rutas:
        G.add_edge(origen, destino, weight=peso)
    
    return G

def ruta_optima(grafo, origen, destino):
    """
    Calcula la ruta óptima (camino de costo mínimo) entre dos nodos
    usando el algoritmo de Dijkstra.
    """
    try:
        # Utilizando dijkstra_path para obtener la lista de nodos en la ruta óptima
        camino = nx.dijkstra_path(grafo, source=origen, target=destino, weight='weight')
        # Para obtener el coste total de la ruta
        costo_total = nx.dijkstra_path_length(grafo, source=origen, target=destino, weight='weight')
        return camino, costo_total
    except nx.NetworkXNoPath:
        print(f"No existe un camino entre {origen} y {destino}.")
        return None, None

if __name__ == "__main__":
    # Crear grafo con estaciones y rutas
    grafo = crear_grafo()
    
    # Especificar origen y destino para la ruta óptima
    origen = 'Estacion_A'
    destino = 'Estacion_D'
    
    camino, costo = ruta_optima(grafo, origen, destino)
    
    if camino is not None:
        print("La ruta óptima desde", origen, "hasta", destino, "es:")
        print(" -> ".join(camino))
        print("Costo total (tiempo/distancia):", costo) 