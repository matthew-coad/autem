if __name__ == '__main__':
    import context

import genetic
import genetic.simulators as simulators
import genetic.scorers as scorers
import genetic.learners as learners
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
            loaders.Data(x,y),
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
        population_size=5)
    simulation.start()
    steps = 50
    for step in range(steps):
        simulation.step()
    simulation.report()

    return simulation

if __name__ == '__main__':
    run_quick_spot_simulation()
