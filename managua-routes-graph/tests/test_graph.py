import unittest
from src.graph import ManaguaGraph

class TestManaguaGraph(unittest.TestCase):

    def setUp(self):
        self.graph = ManaguaGraph()
        self.graph.create_graph()

    def test_add_route(self):
        self.graph.add_route('Estacion_A', 'Estacion_B', 4)
        self.assertIn(('Estacion_A', 'Estacion_B'), self.graph.graph.edges)

    def test_find_optimal_path(self):
        self.graph.add_route('Estacion_A', 'Estacion_B', 4)
        self.graph.add_route('Estacion_B', 'Estacion_C', 1)
        self.graph.add_route('Estacion_A', 'Estacion_C', 2)
        path, cost = self.graph.find_optimal_path('Estacion_A', 'Estacion_C')
        self.assertEqual(path, ['Estacion_A', 'Estacion_C'])
        self.assertEqual(cost, 2)

    def test_no_path(self):
        path, cost = self.graph.find_optimal_path('Estacion_A', 'Estacion_D')
        self.assertIsNone(path)
        self.assertIsNone(cost)

if __name__ == '__main__':
    unittest.main()