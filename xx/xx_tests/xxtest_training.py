if __name__ == '__main__':
    import context

import genetic
import genetic.scorers as scorers

from types import SimpleNamespace

from pandas import read_csv
import numpy as np

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

import unittest
     
# Data tests

class data_fixture(unittest.TestCase):

    def setUp(self):
        filename = 'tests\data\iris.data.csv'
        names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'class']
        self.dataset = read_csv(filename, names=names)
        array = self.dataset.values
        self.x = array[:,0:4]
        self.y = array[:,4]

    def test_training_data_loads(self):

        x = self.x
        y = self.y

        simulation = genetic.Simulation("Test", [genetic.Data(x, y, .2)])
        population1 = genetic.Population(simulation, False)
        self.assertIs(population1.configuration.x, x)
        self.assertIs(population1.configuration.y, y)

    def test_training_data_evaluates(self):

        x = self.x
        y = self.y

        simulation = genetic.Simulation("Test", [genetic.Data(x, y, .2)])
        population1 = genetic.Population(simulation, False)
        population1.evaluate()
        self.assertTrue(hasattr(population1.evaluation, "x_train"))

    def test_training_data_varies(self):
        x = self.x
        y = self.y

        simulation = genetic.Simulation("Test", [genetic.Data(x, y, .2)])
        p1 = genetic.Population(simulation, False)
        p1.evaluate()
        p2 = genetic.Population(simulation, False)
        p2.evaluate()

        self.assertTrue(np.array_equal(p1.evaluation.y_train, p1.evaluation.y_train))
        self.assertFalse(np.array_equal(p1.evaluation.y_train, p2.evaluation.y_train))

    # TODO Replicable
 
class model_fixture(unittest.TestCase):

    def setUp(self):
        filename = 'tests\data\iris.data.csv'
        names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'class']
        self.dataset = read_csv(filename, names=names)
        array = self.dataset.values
        self.x = array[:,0:4]
        self.y = array[:,4]

    def test_model_choice(self):

        models = []
        lr_model = LogisticRegression()
        models.append(('LR', lr_model))
        simulation = genetic.Simulation("Test", [genetic.ModelChoice(models)])
        p1 = genetic.Population(simulation, False)
        p1.evaluate()

        m1 = genetic.Member(p1)
        self.assertEqual(m1.configuration.model_index, 0)
        m1.evaluate()
        self.assertEqual(m1.evaluation.model_name, 'LR')
        self.assertIs(m1.evaluation.model, lr_model)

    def test_evaluate_model_scores(self):

        x = self.x
        y = self.y

        models = []
        lr_model = LogisticRegression(solver = 'liblinear', multi_class = 'ovr')
        models.append(('LR', lr_model))

        simulation = genetic.Simulation("Test", [
            genetic.Data(x, y, .2),
            genetic.ModelChoice(models), 
            genetic.ModelScorer(scorers.accuracy_scorer),
            genetic.ModelScoreFitness(),
            genetic.BattleCompetition(5,5,.2)
        ])
        p1 = genetic.Population(simulation, False)
        p1.evaluate()

        m1 = genetic.Member(p1)
        m1.evaluate()
        self.assertTrue(hasattr(m1.evaluation, 'model_score'))

    def test_score_competition(self):

        x = self.x
        y = self.y

        models = []
        models.append(('LR', LogisticRegression(solver = 'liblinear', multi_class = 'ovr')))
        models.append(('LDA', LinearDiscriminantAnalysis()))
        models.append(('KNN', KNeighborsClassifier()))
        models.append(('CART', DecisionTreeClassifier()))
        models.append(('NB', GaussianNB()))
        models.append(('SVM', SVC()))        

        simulation = genetic.Simulation("Test", [
            genetic.Data(x, y, .3),
            genetic.FixedPopulationSize(20),
            genetic.ModelChoice(models), 
            genetic.ModelScorer(scorers.accuracy_scorer),
            genetic.ModelScoreFitness(),
            genetic.BattleCompetition(5,5,.2)
        ])
        p1 = genetic.Population(simulation, False)
        p1.evaluate()
        p1.battle()
        p1.breed()
        
if __name__ == '__main__':
    unittest.main()
