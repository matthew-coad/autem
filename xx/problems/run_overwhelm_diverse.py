# First tuning model

if __name__ == '__main__':
    import context

import autem
import autem.scorers as scorers
import autem.learners as learners

from pathlib import Path
from pandas import read_csv

simulation_name = "overwhelm_diverse"
simulation_path = Path("problems", "simulations", simulation_name)
simulation_rounds = 50

# Load dataset
def load_boston():
    filename = 'tests\data\housing.csv'
    names = ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT', 'MEDV']
    dataset = read_csv(filename, delim_whitespace=True, names=names)
    return dataset

def run_overwhelm_diverse_learner():

    df = load_boston()

    array = df.values
    x = array[:,0:13]
    y = array[:,13]
    validation_size = 0.20
    seed = 7

    components = [
        autem.Data(x, y, .3),
        autem.FixedPopulationSize(100),

        # Learners
        learners.LinearRegression(),
        learners.Lasso(),
        learners.ElasticNet(),
        learners.KNeighborsRegressor(),
        learners.DecisionTreeRegressor(),
        learners.SVR(),
        learners.LearnerChoice(),

        # Transforms
        autem.StandardiseTransform(),

        autem.ModelScorer(scorers.neg_mean_squared_error_scorer),
        autem.ModelScoreSignificantFitness(0.1),
        autem.BattleCompetition(5, 5, .5),
        autem.SavePath(simulation_path)
    ]
    simulation = autem.Simulation(simulation_name, components, seed = 1)
    for round in range(simulation_rounds):
        simulation.run()

if __name__ == '__main__':
    run_overwhelm_diverse_learner()