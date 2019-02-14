if __name__ == '__main__':
    import context
import unittest
from tests import datasets

from genetic.simulators import Simulation
from genetic.loaders import Data

import numpy as np

class sources_fixture(unittest.TestCase):

    def test_data_available_in_simulation(self):
        x,y = datasets.load_iris()
        simulation = Simulation("test_sources_fixture", [Data(x, y)])
        simulation.start()
        loader = simulation.resources.loader

        l_x, l_y = loader.load_divided(simulation)

        self.assertTrue(np.array_equal(l_x, x))
        self.assertTrue(np.array_equal(l_y, y))
