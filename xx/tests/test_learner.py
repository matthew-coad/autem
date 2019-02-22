if __name__ == '__main__':
    import context

import autem.simulators as simulators
import autem.learners.regression as learners
import autem.scorers as scorers
import autem.loaders as loaders

from tests.datasets import load_boston

import unittest

class learner_fixture(unittest.TestCase):

    def test_select_one_learner(self):
        simulation = simulators.Simulation("Test", [ learners.LinearRegression() ], population_size=2)
        simulation.start()
        self.assertEqual(simulation.members[0].configuration.learner.active, "LR")

    def test_learners_random_on_start(self):
        lr = learners.LinearRegression()
        knn = learners.KNeighborsRegressor()
        simulation = simulators.Simulation("Test", [ learners.LinearRegression(), learners.KNeighborsRegressor() ], population_size=50)
        simulation.start()
        n_linear = [m.configuration.learner.active == lr.name for m in simulation.members ].count(True)
        n_knn = [m.configuration.learner.active == knn.name for m in simulation.members ].count(True)
        self.assertGreater(n_linear, 0)
        self.assertGreater(n_knn, 0)

    def test_learner_evaluation_adds_score(self):
        x, y = load_boston()
        lr = learners.LinearRegression()
        simulation = simulators.Simulation("Test", [ 
            loaders.Data(x,y),
            scorers.NegativeRMSE(),
            lr
        ], population_size=50)
        simulation.start()
        member = simulation.members[0]
        evaluation = simulation.evaluate_member(member)
        self.assertTrue(hasattr(evaluation, "test_score"))


if __name__ == '__main__':
    unittest.main()
