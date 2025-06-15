def create_routes(graph):
    """
    Initializes the routes in Managua with their respective weights
    and adds them to the provided graph.
    """
    rutas = [
        ('Estacion_1', 'Estacion_2', 5),
        ('Estacion_1', 'Estacion_3', 10),
        ('Estacion_2', 'Estacion_3', 2),
        ('Estacion_2', 'Estacion_4', 7),
        ('Estacion_3', 'Estacion_4', 3),
        ('Estacion_3', 'Estacion_5', 8),
        ('Estacion_4', 'Estacion_5', 1)
    ]
    
    for origen, destino, peso in rutas:
        graph.add_edge(origen, destino, weight=peso)