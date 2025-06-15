# Managua Routes Graph

This project implements a graph representing the routes in Managua, Nicaragua. It utilizes the `networkx` library to manage the graph structure and perform operations such as finding optimal paths between various locations.

## Project Structure

```
managua-routes-graph
├── src
│   ├── __init__.py
│   ├── graph.py         # Contains the ManaguaGraph class for graph operations
│   ├── routes.py        # Defines the routes in Managua and initializes them
│   └── utils.py         # Utility functions for graph operations
├── tests
│   ├── __init__.py
│   └── test_graph.py    # Unit tests for the ManaguaGraph class
├── requirements.txt      # Lists project dependencies
├── .gitignore            # Specifies files to ignore in Git
└── README.md             # Project documentation
```

## Installation

To set up the project, clone the repository and install the required dependencies:

```bash
git clone <repository-url>
cd managua-routes-graph
pip install -r requirements.txt
```

## Usage

1. **Creating the Graph**: Use the `ManaguaGraph` class from `graph.py` to create a graph instance.
2. **Adding Routes**: Utilize the `create_routes` function from `routes.py` to initialize and add routes to the graph.
3. **Finding Optimal Paths**: Call the methods in `ManaguaGraph` to find the shortest paths between locations.

## Example

```python
from src.graph import ManaguaGraph
from src.routes import create_routes

# Create a graph instance
graph = ManaguaGraph()

# Initialize routes
create_routes(graph)

# Find the optimal path
path, cost = graph.find_optimal_path('Location_A', 'Location_B')
print(f"Optimal path: {path} with cost: {cost}")
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.