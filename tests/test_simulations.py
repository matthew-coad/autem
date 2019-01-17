if __name__ == '__main__':
    import context

import genetic
import unittest
from pathlib import Path

from tests.highest_id_simulation import runHighestIDSimulation
from tests.quick_spot_simulation import run_quick_spot_simulation, make_quick_spot_simulation
from tests.quick_knn_tune_simulation import run_knn_tune_simulation, make_knn_tune_simulation

class simulations_fixture(unittest.TestCase):

    def test_generated_ids_unique(self):
        simulation = genetic.Simulation("Test_Battle", [])
        id1 = simulation.generate_id()
        id2 = simulation.generate_id()
        self.assertNotEqual(id1, id2)

    def test_run_highest_id(self):
        runHighestIDSimulation()

    def test_quick_spot_simulation(self):
        simulation_name = "quick_spot"
        simulation = make_quick_spot_simulation(simulation_name, 10, Path("tests", "simulations", simulation_name))
        run_quick_spot_simulation(simulation, 3)

    def test_knn_tune_simulation(self):
        simulation_name = "quick_knn_tune"
        simulation = make_knn_tune_simulation(simulation_name, 10, Path("tests", "simulations", simulation_name))
        run_knn_tune_simulation(simulation, 3)

if __name__ == '__main__':
    unittest.main()
