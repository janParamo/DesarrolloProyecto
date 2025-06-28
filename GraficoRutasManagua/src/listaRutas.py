def obtener_lista_rutas_y_paradas(rutas_dict):
    """
    Devuelve una lista de tuplas (nombre_ruta, lista_paradas) a partir del diccionario de rutas.
    """
    return [(ruta, paradas) for ruta, paradas in rutas_dict.items()]