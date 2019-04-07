if __name__ == '__main__':
    import context

import autem
import autem.makers as makers
import autem.scorers as scorers
import autem.learners.classification as learners
import autem.loaders as loaders
import autem.evaluators as evaluators
import autem.reporters as reporters
import autem.preprocessors as preprocessors

from tests.datasets import load_iris
from tests.config import simulations_path

def run_preprocessing():

    y,numeric_x = load_iris()
    simulation = autem.Simulation(
        "preprocessing", 
        [
            loaders.Data("iris",y,numeric_x=numeric_x),
            scorers.Accuracy(),

            makers.RandomMaker(),
            
            evaluators.ScoreEvaluator(),
            evaluators.ValidationEvaluator(),
            evaluators.AccuracyContest(),
            evaluators.SurvivalJudge(),
            evaluators.PromotionJudge(),
            evaluators.CrossValidationRater(),
            
            reporters.Path(simulations_path().joinpath("preprocessing")),

            # Scalers
            autem.Choice("scaler", [
                preprocessors.MaxAbsScaler(),
                preprocessors.MinMaxScaler(),
                preprocessors.Normalizer(),
                preprocessors.RobustScaler(),
                preprocessors.StandardScaler(),
            ]),

            autem.Choice("learner", [
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

