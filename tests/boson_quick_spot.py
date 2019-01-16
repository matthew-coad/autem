# Boston quick spot check simulation

# Simulation that does a very quick regression spot check on the Boston Housing model

# Demonstrates:
# Regression
# Spot check on a slightly more complex problem than Iris

if __name__ == '__main__':
    import context

import genetic
import genetic.scorers as scorers
import genetic.learners as learners

from pathlib import Path
from pandas import read_csv

simulation_name = "boston_quick_spot"
simulation_path = Path("tests", "simulations", simulation_name)
simulation_rounds = 50

# Load dataset
def load_boston():
    filename = 'tests\data\housing.csv'
    names = ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT', 'MEDV']
    dataset = read_csv(filename, delim_whitespace=True, names=names)
    return dataset

def run_boston_quick_spot():

    df = load_boston()

    array = df.values
    x = array[:,0:13]
    y = array[:,13]
    validation_size = 0.20
    seed = 7

    components = [
        genetic.Data(x, y, .3),
        genetic.FixedPopulationSize(100),

        # Learners
        learners.LinearRegression(),
        learners.Lasso(),
        learners.ElasticNet(),
        learners.KNeighborsRegressor(),
        learners.DecisionTreeRegressor(),
        learners.SVR(),
        learners.LearnerChoice(),

        # Transforms
        genetic.StandardiseTransform(),

        genetic.ModelScorer(scorers.neg_mean_squared_error_scorer),
        genetic.ModelScoreSignificantFitness(0.1),
        genetic.BattleCompetition(5, 5, .5),
        genetic.SavePath(simulation_path)
    ]
    simulation = genetic.Simulation(simulation_name, components, seed = 1)
    for round in range(simulation_rounds):
        simulation.run()

if __name__ == '__main__':
    run_boston_quick_spot()
