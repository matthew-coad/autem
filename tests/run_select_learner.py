if __name__ == '__main__':
    import context

import autem
import autem.scorers as scorers
import autem.learners.classification as learners
import autem.loaders as loaders
import autem.evaluators as evaluators
import autem.reporters as reporters

from tests.datasets import load_iris
from tests.config import simulations_path

def run_select_learner():

    x,y = load_iris()
    simulation = autem.Simulation(
        "select_learner", 
        [
            loaders.Data("iris", x,y),
            scorers.Accuracy(),

            evaluators.Accuracy(),
            evaluators.Survival(),
            evaluators.CrossValidationRater(),
            evaluators.HoldoutValidator(),
            evaluators.PreferImportantChoices(),
            
            reporters.Path(simulations_path().joinpath("select_learner")),

            autem.Choice("learner", [
                learners.LogisticRegression(), 
                learners.LinearDiscriminantAnalysis(), 
                learners.KNeighborsClassifier(),  
                learners.DecisionTreeClassifier(), 
                learners.GaussianNB(), 
                learners.LinearSVC()
            ])
        ], 
        population_size=20)
    simulation.start()
    simulation.run(100)
    simulation.run(100)
    simulation.finish()
    simulation.report()

    #manager = autem.ReportManager(simulations_path())
    #manager.update_combined_outline_report()
    #manager.update_combined_battle_report()

    return simulation

if __name__ == '__main__':
    run_select_learner()
