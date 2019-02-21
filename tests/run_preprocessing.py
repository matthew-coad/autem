if __name__ == '__main__':
    import context

import genetic
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
    simulation = genetic.Simulation(
        "preprocessing", 
        [
            loaders.Data("iris", x,y),
            scorers.Accuracy(),
            evaluators.Accuracy(),
            evaluators.Survival(),
            evaluators.CrossValidationRater(),
            evaluators.HoldoutValidator(),
            evaluators.PreferImportantChoices(),
            
            reporters.Path(simulations_path().joinpath("preprocessing")),

            # Imputers
            genetic.Choice("imputer", [
                preprocessors.SimpleImputer(),
                preprocessors.MissingIndicatorImputer(),
            ], preprocessors.NoImputer()),

            # Engineers
            genetic.Choice("engineer", [
                preprocessors.PolynomialFeatures(),
            ], preprocessors.NoEngineering()),

            # Scalers
            genetic.Choice("scaler", [
                preprocessors.MaxAbsScaler(),
                preprocessors.MinMaxScaler(),
                preprocessors.Normalizer(),
                preprocessors.RobustScaler(),
                preprocessors.StandardScaler(),
            ], preprocessors.NoScaler()),

            genetic.Choice("learner", [
                learners.LogisticRegression(), 
                learners.LinearDiscriminantAnalysis(), 
                learners.KNeighborsClassifier(),  
                learners.DecisionTreeClassifier(), 
                learners.GaussianNB(),
            ]),
        ], 
        population_size=20)
    simulation.start()
    simulation.run(500)
    simulation.run(500)
    simulation.run(500)
    simulation.run(500)
    simulation.finish()
    simulation.report()

    return simulation

if __name__ == '__main__':
    run_preprocessing()

