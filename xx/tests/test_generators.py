if __name__ == '__main__':
    import context


import autem
import autem.simulators as simulators

import unittest

class simulation_generators_fixture(unittest.TestCase):

    def test_generated_ids_unique(self):
        simulation = simulators.Simulation("Test", [])
        id1 = simulation.generate_id()
        id2 = simulation.generate_id()
        self.assertNotEqual(id1, id2)

if __name__ == '__main__':
    unittest.main()
