if __name__ == '__main__':
    import context

import genetic
import unittest
from pathlib import Path

from .run_highest_id import runHighestIDSimulation
from .run_first_model import runFirstModelSimulation
from .run_significant_model import runSignificantModelSimulation
from .boson_quick_spot import run_boston_quick_spot

class simulations_fixture(unittest.TestCase):

    def test_generated_ids_unique(self):
        simulation = genetic.Simulation("Test_Battle", [])
        id1 = simulation.generate_id()
        id2 = simulation.generate_id()
        self.assertNotEqual(id1, id2)

    def test_run_highest_id(self):
        runHighestIDSimulation()

    def test_run_first_model(self):
        runFirstModelSimulation()

    def test_run_significant_model(self):
        runSignificantModelSimulation()

if __name__ == '__main__':
    unittest.main()
