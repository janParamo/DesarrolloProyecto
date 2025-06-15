def format_route_output(route, cost):
    if route is None:
        return "No route found."
    return f"Optimal route: {' -> '.join(route)} with total cost: {cost}"

def validate_input(station, valid_stations):
    if station not in valid_stations:
        raise ValueError(f"Invalid station: {station}. Valid stations are: {', '.join(valid_stations)}")