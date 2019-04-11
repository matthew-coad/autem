if __name__ == '__main__':
    import context
import unittest
from tests import datasets

from autem import Simulation
from autem.loaders import Data

import numpy as np

class sources_fixture(unittest.TestCase):

    def test_data_available_in_simulation(self):
        x,y = datasets.load_iris()
        simulation = Simulation("test_sources_fixture", [Data("Test", x, y)])
        simulation.start()
        scorer = simulation.get_scorer()
        loader = simulation.get_loader()


        l_x, l_y = loader.load_training_data(simulation)

        self.assertTrue(np.array_equal(l_x, x))
        self.assertTrue(np.array_equal(l_y, y))

if __name__ == '__main__':
    unittest.main()
