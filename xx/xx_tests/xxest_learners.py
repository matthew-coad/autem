if __name__ == '__main__':
    import context

import genetic
import genetic.scorers as scorers
import genetic.learners as learners

from types import SimpleNamespace

from pandas import read_csv
import numpy as np

import unittest

class learner_fixture(unittest.TestCase):

    def setUp(self):
        filename = 'tests\data\iris.data.csv'
        names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'class']
        self.dataset = read_csv(filename, names=names)
        array = self.dataset.values
        self.x = array[:,0:4]
        self.y = array[:,4]

    def test_evaluate_single_learner(self):

        x = self.x
        y = self.y

        simulation = genetic.Simulation("Test", [
            genetic.Data(x, y, .2),
            learners.LogisticRegression()
        ])
        p1 = genetic.Population(simulation, False)
        p1.evaluate()

        m1 = genetic.Member(p1)
        m1.evaluate()
        self.assertTrue(hasattr(m1.evaluation, 'model_name'))
        self.assertIsNotNone(m1.evaluation.model)

    def test_evaluate_learner_choice(self):

        x = self.x
        y = self.y

        simulation = genetic.Simulation("Test", [
            genetic.Data(x, y, .2),
            learners.LogisticRegression(),
            learners.LinearRegression(),
            learners.LearnerChoice()
        ])
        p1 = genetic.Population(simulation, False)
        p1.evaluate()

        m1 = genetic.Member(p1)
        m1.evaluate()
        self.assertTrue(hasattr(m1.evaluation, 'model_name'))
        self.assertIsNotNone(m1.evaluation.model)

        
if __name__ == '__main__':
    unittest.main()
