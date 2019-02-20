if __name__ == '__main__':
    import context

import genetic
import genetic.simulators as simulators
import genetic.scorers as scorers
import genetic.learners.classification as learners
import genetic.loaders as loaders
import genetic.evaluators as evaluators
import genetic.reporters as reporters
import genetic.preprocessors as preprocessors

from tests.datasets import load_iris
from tests.config import simulations_path

def run_preprocessing():

    x,y = load_iris()
    simulation = simulators.Simulation(
        "preprocessing", 
        [
            loaders.Data("iris", x,y),
            scorers.Accuracy(),
            evaluators.Accuracy(),
            evaluators.Survival(),
            evaluators.CrossValidationRater(),
            evaluators.HoldoutValidator(),
            evaluators.ComponentImportance(),
            
            reporters.Path(simulations_path().joinpath("preprocessing")),

            # Imputers
            simulators.Choice("imputer", [
                preprocessors.NoImputer(),
                preprocessors.SimpleImputer(),
                preprocessors.MissingIndicatorImputer(),
            ]),

            # Engineers
            simulators.Choice("engineer", [
                preprocessors.NoEngineering(),
                preprocessors.PolynomialFeatures(),
            ]),

            # Scalers
            simulators.Choice("scaler", [
                preprocessors.NoScaler(),
                preprocessors.MaxAbsScaler(),
                preprocessors.MinMaxScaler(),
                preprocessors.Normalizer(),
                preprocessors.RobustScaler(),
                preprocessors.StandardScaler(),
            ]),

            simulators.Choice("learner", [
                learners.LogisticRegression(), 
                learners.LinearDiscriminantAnalysis(), 
                learners.KNeighborsClassifier(),  
                learners.DecisionTreeClassifier(), 
                learners.GaussianNB(),
            ]),
        ], 
        population_size=20)
    simulation.start()
    simulation.run(100)
    simulation.run(100)
    simulation.finish()
    simulation.report()

    return simulation

if __name__ == '__main__':
    run_preprocessing()

