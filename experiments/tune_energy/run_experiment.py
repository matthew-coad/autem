# First tuning model

if __name__ == '__main__':
    import context

import genetic
import genetic.scorers as scorers
import genetic.learners as learners

from pathlib import Path
from pandas import read_csv

# Load dataset
def load_boston():
    filename = 'experiments\data\housing.csv'
    names = ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT', 'MEDV']
    dataset = read_csv(filename, delim_whitespace=True, names=names)
    return dataset

def run_tune_battle_experiment(experiment, hp, energy, survivor_ratio):

    simulation_name = "tune hd= %d en=%d sr=%f" % (hp, energy, survivor_ratio)
    simulation_rounds = 50
    simulation_path = Path("experiments", experiment, "simulations", simulation_name)

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
        genetic.BattleCompetition(hp, energy, survivor_ratio),
        genetic.SavePath(simulation_path)
    ]
    simulation = genetic.Simulation(simulation_name, components, seed = 1)
    for round in range(simulation_rounds):
        simulation.run()

if __name__ == '__main__':
    run_tune_battle_experiment("tune_energy", 5, 5, 0.5)
    run_tune_battle_experiment("tune_energy", 5, 10, 0.5)
    run_tune_battle_experiment("tune_energy", 5, 15, 0.5)
    run_tune_battle_experiment("tune_energy", 5, 20, 0.5)
    run_tune_battle_experiment("tune_energy", 5, 30, 0.5)
