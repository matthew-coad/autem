# First tuning model

if __name__ == '__main__':
    import context

import tests.quick_knn_tune_simulation as quick_knn_tune

import genetic
import genetic.scorers as scorers
import genetic.learners as learners

from pathlib import Path
from pandas import read_csv

if __name__ == '__main__':
    simulation_name = "quick_knnt"
    simulation = quick_knn_tune.make_knn_tune_simulation(simulation_name, 100, Path("experiments", "boston", "simulations", simulation_name))
    quick_knn_tune.run_knn_tune_simulation(simulation, 50)

