if __name__ == '__main__':
    import context

import genetic
import genetic.scorers as scorers

from pathlib import Path
from pandas import read_csv

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

def runFirstModelSimulation():

    filename = 'tests\data\iris.data.csv'
    names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'class']
    dataset = read_csv(filename, names=names)
    array = dataset.values
    x = array[:,0:4]
    y = array[:,4]

    models = []
    models.append(('LR', LogisticRegression(solver = 'liblinear', multi_class = 'ovr')))
    models.append(('LDA', LinearDiscriminantAnalysis()))
    models.append(('KNN', KNeighborsClassifier()))
    models.append(('CART', DecisionTreeClassifier()))
    models.append(('NB', GaussianNB()))
    models.append(('SVM', SVC()))

    path = Path("tests", "simulations", "first_model")

    components = [
        genetic.Data(x, y, .3),
        genetic.FixedPopulationSize(20),
        genetic.ModelChoice(models), 
        genetic.ModelScorer(scorers.accuracy_scorer),
        genetic.ModelScoreFitness(),
        genetic.BattleCompetition(5, 5, .5),
        genetic.SavePath(path)
    ]
    simulation = genetic.Simulation("First_Model", components)
    simulation.run()
    simulation.run()

if __name__ == '__main__':
    runFirstModelSimulation()

