if __name__ == '__main__':
    import context

import genetic
import genetic.simulators as simulators
import genetic.scorers as scorers
import genetic.learners.classification as learners
import genetic.loaders as loaders
import genetic.reporters as reporters
import genetic.contests as contests
import genetic.raters as raters

from tests.datasets import load_iris
from tests.config import simulations_path

def run_tune_simulation():

    x,y = load_iris()
    simulation = simulators.Simulation(
        "tune", 
        [
            loaders.Data("iris", x,y),
            scorers.Accuracy(),

            contests.Accuracy(),
            contests.Survival(),
            raters.CrossValidationRater(),
            raters.HoldoutValidator(),
            reporters.Path(simulations_path().joinpath("tune")),

            learners.LogisticRegression(), 
            learners.LinearDiscriminantAnalysis(), 
            learners.KNeighborsClassifier(),  
            learners.DecisionTreeClassifier(), 
            learners.GaussianNB(), 
            learners.LinearSVC(),

        ], 
        population_size=20)
    simulation.start()
    simulation.run(300)
    simulation.finish()
    simulation.report()

    manager = genetic.ReportManager(simulations_path())
    manager.update_combined_outline_report()
    manager.update_combined_battle_report()

    return simulation

if __name__ == '__main__':
    run_tune_simulation()
