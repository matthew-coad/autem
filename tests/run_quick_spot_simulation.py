if __name__ == '__main__':
    import context

import genetic
import genetic.simulators as simulators
import genetic.scorers as scorers
import genetic.learners.regression as learners
import genetic.transforms as transforms
import genetic.loaders as loaders
import genetic.reporters as reporters
import genetic.contests as contests

from tests.datasets import load_boston
from tests.config import simulations_path

def run_quick_spot_simulation():

    x,y = load_boston()
    simulation = simulators.Simulation(
        "quick_spot", 
        [
            loaders.Data("boston", x,y),
            scorers.NegativeRMSE(),

            learners.LinearRegression(),
            learners.Lasso(),
            learners.ElasticNet(),
            learners.KNeighborsRegressor(),
            learners.DecisionTreeRegressor(),
            learners.SVR(),

            contests.BestLearner(),
            contests.Survival(),
            reporters.Path(simulations_path())
        ], 
        population_size=20,
        properties={ "experiment": "base" })
    simulation.start()
    simulation.run(500)
    simulation.report()

    manager = genetic.ReportManager(simulations_path())
    manager.update_combined_battle_report()
    manager.update_combined_ranking_report()
    manager.update_combined_outline_report()

    return simulation

if __name__ == '__main__':
    run_quick_spot_simulation()
