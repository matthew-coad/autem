# First tuning model

if __name__ == '__main__':
    import context

import genetic
import genetic.scorers as scorers
import genetic.learners as learners
import genetic.transforms as transforms

from pathlib import Path
from pandas import read_csv

simulation_name = "knn_tune"
simulation_path = Path("tests", "simulations", simulation_name)
simulation_rounds = 50

# Load dataset
def load_boston():
    filename = 'tests\data\housing.csv'
    names = ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT', 'MEDV']
    dataset = read_csv(filename, delim_whitespace=True, names=names)
    return dataset

def make_knn_tune_simulation(simulation_name, simulation_path = None):

    df = load_boston()

    array = df.values
    x = array[:,0:13]
    y = array[:,13]
    validation_size = 0.20
    seed = 7

    components = [
        genetic.Data(x, y, .3),
        genetic.FixedPopulationSize(10),

        # Learners
        learners.KNeighborsRegressor(),

        # Transforms
        transforms.StandardiseTransform(),

        # Compete
        genetic.ModelScorer(scorers.neg_mean_squared_error_scorer),
        genetic.ModelScoreSignificantFitness(0.1),
        genetic.BattleCompetition(5, 5, .5),
    ]
    if not simulation_path is None:
        components.append(genetic.SavePath(simulation_path))
    simulation = genetic.Simulation(simulation_name, components, seed = 1)
    return simulation

def run_knn_tune_simulation(simulation, simulation_rounds):
    for round in range(simulation_rounds):
        simulation.run()

if __name__ == '__main__':
    simulation_name = "quick_knn_tune"
    simulation = make_knn_tune_simulation(simulation_name, Path("tests", "simulations", simulation_name))
    run_knn_tune_simulation(simulation, 3)

